#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pychangelogfactory (c) by chacha
#
# pychangelogfactory  is licensed under a
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International Unported License.
#
# You should have received a copy of the license along with this
# work.  If not, see <https://creativecommons.org/licenses/by-nc-sa/4.0/>.

"""A simple changelog formater that consume merged message and produce nice pre-formated changelogs.

"""

from __future__ import annotations

from re import Match, search, compile as _compile, match
from abc import ABC
from copy import deepcopy

from typing import TYPE_CHECKING

from typing import Generic, TypeVar, cast

if TYPE_CHECKING:
    from typing import Optional, ClassVar, Type, Dict, List

T_ChangelogFormater = TypeVar("T_ChangelogFormater", bound="ChangelogFormater")


class _ChangelogFormatersCtx(Generic[T_ChangelogFormater]):
    """Storage class that manage Formaters"""

    def __init__(self) -> None:
        """Storage class init method"""
        self._savedFormaterList: set[Type[T_ChangelogFormater]] = set()

    def add(self, record: Type[T_ChangelogFormater]) -> None:
        """Add a Formater to the storage class
        Args:
            record: the Formater class to be added
        """
        self._savedFormaterList.add(record)

    def remove(self, record: Type[T_ChangelogFormater]) -> None:
        """Remove a Formater from the storage class
        Args:
            record: the Formater class to be removed
        """
        self._savedFormaterList.remove(record)

    def reset(self) -> None:
        """Reset the storage class"""
        self._savedFormaterList = set()

    def get(self) -> set[Type[T_ChangelogFormater]]:
        """Get the storage data set
        Returns:
            The internal storage class (set)
        """
        return self._savedFormaterList

    def __copy__(self) -> _ChangelogFormatersCtx[T_ChangelogFormater]:
        """Copy the class"""
        cls = self.__class__
        result = cls.__new__(cls)
        result._savedFormaterList = self._savedFormaterList
        return result

    def __deepcopy__(self, memo: Dict[int, object]) -> _ChangelogFormatersCtx[T_ChangelogFormater]:
        """Deep-Copy the class
        Args:
            memo: __deepcopy__ interface impl"""
        result = self.__copy__()
        memo[id(self)] = result
        result._savedFormaterList = self._savedFormaterList.copy()
        return result


def ChangelogFormaterRecordType(Klass: Type[T_ChangelogFormater]) -> Type[T_ChangelogFormater]:
    """Decorator function that registers formater implementation in factory
    Args:
        Klass: class to register in the factory
    Returns:
        untouched class"""
    ChangelogFactory.RegisterBaseFormater(Klass)
    return Klass


def _ChangelogFormaterRecordType(Klass: Type[T_ChangelogFormater]) -> Type[T_ChangelogFormater]:
    """Internal decorator function that registers formater implementation in factory
    Args:
        Klass: class to register in the factory
    Returns:
        untouched class"""
    cast(ChangelogFactory[ChangelogFormater], ChangelogFactory).ar_SavedFormaterKlass.add(Klass)
    return ChangelogFormaterRecordType(Klass)


class ChangelogFormater(ABC):
    """ChangelogFormater class

    This class is the formater base class.

    This class is for:

    - classifying message: CheckLine() and CheckLine_keywords()
    - storing lines: Clear() and PushLine()
    - returning the formated output: Render() and RenderLines()


    /// warning
    this class does not aim to be instantiated by user.
    ///
    """

    prefix: ClassVar[Optional[str]] = None
    title: ClassVar[Optional[str]] = None
    keywords: ClassVar[Optional[list[str]]] = None
    priority: ClassVar[int] = 0
    _lines: List[None | str] = []

    def __init__(self) -> None:
        """ChangelogFormater class constructor"""
        self._lines: List[None | str] = []

    def Clear(self) -> None:
        """Clear the formater content"""
        self._lines = []

    def PushLine(self, ChangelogString: str) -> None:
        """Push a new line in the formater

        Args:
            ChangelogString: the new line to insert
        """
        self._lines.append(ChangelogString.strip())

    def Render(self) -> str:
        """Render all lines + title
        Returns:
            the rendered lines
        """
        changelog_category = ""
        if len(self._lines) > 0:
            changelog_category = f"#### {self.title}\n"
            changelog_category = changelog_category + self.RenderLines()
        return changelog_category

    def RenderLines(self) -> str:
        """Render only lines
        Returns:
            the rendered lines
        """
        full_lines = ""
        for line in self._lines:
            full_lines = full_lines + f"> {line}" + "\n"
        return full_lines

    @classmethod
    def CheckLine(cls, content: str) -> None | Match[str]:
        """Check if a line match the current formater (lazy identification)

        /// warning
        Only formal tags are parsed by this function
         eg: `<change_type>(<change_target>): <change_message>`
        ///

        Args:
            content: line to parse
        Returns:
            match object
        """
        regex = _compile(rf"^(?:-\s+)?(?:{cls.prefix})(?:\((.*)\))?(?::)(?:\s*)([^\s].+)")
        _match = regex.match(content)
        return _match

    @classmethod
    def CheckLine_keywords(cls, content: str) -> bool:
        """Check if a line match the current formater (deeper in-content identification)

        Any word in the message can be used to categorize this message.

        Args:
            content: line to parse
        Returns:
            True if a keyword has matched, False otherwise
        """
        keyword_list = cls.keywords
        if keyword_list:
            for _keyword in keyword_list:
                if _keyword and search(_keyword, content):
                    return True
        return False


class ChangelogFactory(Generic[T_ChangelogFormater]):
    """The main changelog class"""

    ar_SavedFormaterKlass: ClassVar[_ChangelogFormatersCtx[ChangelogFormater]] = _ChangelogFormatersCtx[ChangelogFormater]()
    ar_FormaterKlass: _ChangelogFormatersCtx[T_ChangelogFormater] = _ChangelogFormatersCtx[T_ChangelogFormater]()

    ar_Formater: Dict[str, T_ChangelogFormater] = {}
    checkCommentPattern: str = r"^[ \t]*(?:\/\/|#)"

    def __init__(self, ChangelogString: Optional[str] = None) -> None:
        """Main ChangelogFormater class constructor

        Args:
            ChangelogString: optional input string to be processed
        """
        self.ar_Formater: Dict[str, T_ChangelogFormater] = {}
        self.ar_FormaterKlass = deepcopy(type(self).ar_FormaterKlass)

        for FormaterKlass in self.ar_FormaterKlass.get():
            self.ar_Formater[FormaterKlass.__name__] = FormaterKlass()

        # missing mypy coverage here because of internal bad isinstance() handling
        # could be fixed using 'type(ChangelogString) is str' but then quality check will bad
        # so let quality advise
        if isinstance(ChangelogString, str):
            self.ProcessFullChangelog(ChangelogString)

    def ResetFormaterList(self) -> ChangelogFactory[T_ChangelogFormater]:
        """Reset the formater class list to original (Instance wise)
        Returns:
            self for convenience
        """
        self.ar_FormaterKlass: T_ChangelogFormater = deepcopy(
            cast(_ChangelogFormatersCtx[T_ChangelogFormater], ChangelogFactory.ar_SavedFormaterKlass)
        )
        self.ar_Formater = {}
        for FormaterKlass in self.ar_FormaterKlass.get():
            self.ar_Formater[FormaterKlass.__name__] = FormaterKlass()
        return self

    @classmethod
    def RegisterBaseFormater(cls, FormaterKlass: Type[T_ChangelogFormater]) -> None:
        """Register a new formater in the current instance

        Args:
            FormaterKlass: class of the formater to be added
        """
        cls.ar_FormaterKlass.add(FormaterKlass)

    @classmethod
    def ResetBaseFormaterList(cls) -> None:
        """Reset the formater class list to original (BaseClass wise)"""
        cls.ar_FormaterKlass = deepcopy(cls.ar_SavedFormaterKlass)

    def RegisterFormater(self, FormaterKlass: Type[T_ChangelogFormater]) -> ChangelogFactory[T_ChangelogFormater]:
        """Register a new formater in the current instance

        Args:
            FormaterKlass: class of the formater to be added
        Returns:
            self for convenience
        """
        self.ar_FormaterKlass.add(FormaterKlass)
        self.ar_Formater[FormaterKlass.__name__] = FormaterKlass()
        return self

    def unRegisterFormater(self, FormaterKlass: Type[T_ChangelogFormater]) -> ChangelogFactory[T_ChangelogFormater]:
        """unRegister a new formater in the current instance

        Args:
            FormaterKlass: class of the formater to be dropped
        Returns:
            self for convenience
        """
        self.ar_FormaterKlass.remove(FormaterKlass)
        del self.ar_Formater[FormaterKlass.__name__]
        return self

    def Clear(self) -> ChangelogFactory[T_ChangelogFormater]:
        """Clear internal memory
        Returns:
            self for convenience
        """
        for formater in self.ar_Formater.values():
            formater.Clear()
        return self

    def _ProcessLineMain(self, RawChangelogLine: str) -> bool:
        """Process a line and look for identified ones

        This function will try to apply every available formater for the 1st search round: formal search
        If a matching formater is found, line is inserted.

        Args:
            RawChangelogLine: line to process
        Returns:
            True if successfully matched, False otherwise
        """
        for formater in sorted(self.ar_Formater.values(), key=lambda x: x.priority):
            content: Optional[Match[str]] = formater.CheckLine(RawChangelogLine)
            # missing mypy coverage here because of internal bad isinstance() handling AND Match type
            if isinstance(content, Match) and (len(content.groups()) == 2):
                res: str = content.group(2)
                formater.PushLine(res)
                return True

        return False

    def _ProcessLineSecond(self, RawChangelogLine: str) -> bool:
        """Process a line and look for non-identified ones

        This function will try to apply every available formater for the 2ns search round: any keyword
        If a matching formater is found, line is inserted.

        Args:
            RawChangelogLine: line to process
        Returns:
            True if successfully matched, False otherwise
        """
        for formater in sorted(self.ar_Formater.values(), key=lambda x: x.priority, reverse=True):
            if formater.CheckLine_keywords(RawChangelogLine):
                formater.PushLine(RawChangelogLine)
                return True

        self.ar_Formater[ChangelogFormater_others.__name__].PushLine(RawChangelogLine)
        return False

    def ProcessFullChangelog(self, RawChangelogMessage: str) -> ChangelogFactory[T_ChangelogFormater]:
        """Process all input lines

        This function handles the main 2-round changes search algo.
        It takes care of search-order and automatically skip any non-relevants message line.
        A non relevant line can be a commented one, or a to short one.

        Available comment patterns are:  `// and #`

        A relevant commit line must contain:

        - at least 2 words for formal
        - at least 3 words for keywords

        Args:
            RawChangelogMessage: The full raw changelog to be processed
        Returns:
            self for convenience
        """

        Lines2ndRound = []

        for line in RawChangelogMessage.split("\n"):
            lineWordsCount = len(line.split())
            if (lineWordsCount > 1) and (not match(self.checkCommentPattern, line)):
                if self._ProcessLineMain(line) is True:
                    continue
                if lineWordsCount > 2:
                    Lines2ndRound.append(line)

        for line in Lines2ndRound:
            self._ProcessLineSecond(line)

        return self

    def RenderFullChangelog(self, include_unknown: bool = False) -> str:
        """Render the main changelog
        Args:
            include_unknown: includes unknown lines in an Unknown category
        Returns:
            the final formated changelog
        """
        full_changelog = ""
        for formater in sorted(self.ar_Formater.values(), key=lambda x: x.priority, reverse=True):
            # missing mypy coverage here because of internal bad isinstance() handling
            if (include_unknown is False) and (isinstance(formater, ChangelogFormater_others)):
                continue
            full_changelog = full_changelog + formater.Render()

        return full_changelog


# to avoid writing class, they are initialized with the following structure:
# creating category classes: '<NAME>':       (    priority, ['<prefix1>',...],
#                                                '<header>'
#                                            )
#
#    =>  priority is both for ordering categories in final changelog
#        and parsing commit to extract messages
#
for RecordType, Config in {
    # fmt: off
    "break":    (   20, ["break"],
                    ":rotating_light: Breaking changes :rotating_light: :",
                ),
    "feat":     (   25, ["feat", "new", "create", "add"],
                    "Features      :sparkles: :"
                ),
    "fix":      (   0,  ["fix","issue", "problem"],
                    "Fixes :wrench: :"
                ),
    "security": (   20, ["safe", "leak"],
                    "Security :shield: :"
                ),
    "chore":    (   10, ["task", "refactor", "build", "better", "improve"],
                    "Chore :building_construction: :",
                ),
    "perf":     (   15, ["fast","perf" ],
                    "Performance Enhancements :rocket: :",
                ),
    "wip":      (   0,  ["temp", ],
                    "Work in progress changes :construction: :",
                ),
    "doc":     (   0,  [ "doc", "manual"],
                    "Documentations :book: :",
                ),
    "style":    (   5,  ["beautify", ],
                    "Style :art: :",
                ),
    "refactor": (   0,  [],
                    "Refactorings :recycle: :"
                ),
    "ci":       (   0,  ["jenkins", "git"],
                    "Continuous Integration :cyclone: :"
                ),
    "test":     (   -5, ["unittest", "check", "testing"],
                    "Testings :vertical_traffic_light: :"
                ),
    "build":    (   0,  ["compile", "version"],
                    "Builds :package: :"
                ),
    # fmt: on
}.items():
    # then we instantiate all of them
    _name = f"ChangelogFormater_{RecordType}"

    # can not change globals definition so mypy will keep complaining
    _tmp = type(
        _name,
        (ChangelogFormater,),
        {
            "prefix": RecordType,
            "title": Config[2],
            "keywords": Config[1],
            "priority": Config[0],
        },
    )
    globals()[_name] = _tmp
    cast(ChangelogFactory[ChangelogFormater], ChangelogFactory).RegisterBaseFormater(_tmp)
    cast(ChangelogFactory[ChangelogFormater], ChangelogFactory).ar_SavedFormaterKlass.add(_tmp)


@_ChangelogFormaterRecordType
class ChangelogFormater_revert(ChangelogFormater):
    """Revert scope formater"""

    prefix: ClassVar[Optional[str]] = "revert"
    title: ClassVar[Optional[str]] = "Reverts :back: :"
    keywords: ClassVar[Optional[List[str]]] = ["revert", "fallback"]
    priority: ClassVar[int] = 0

    def RenderLines(self) -> str:
        """Render all lines
        Returns:
            the rendered lines
        """
        full_lines = ""
        for line in self._lines:
            full_lines = full_lines + f"> ~~{line}~~" + "\n"
        return full_lines


@_ChangelogFormaterRecordType
class ChangelogFormater_others(ChangelogFormater):
    """Others / unknown scope formater"""

    prefix: ClassVar[Optional[str]] = "other"
    title: ClassVar[Optional[str]] = "Others :question: :"
    keywords: ClassVar[Optional[List[str]]] = [""]
    priority: ClassVar[int] = -20
