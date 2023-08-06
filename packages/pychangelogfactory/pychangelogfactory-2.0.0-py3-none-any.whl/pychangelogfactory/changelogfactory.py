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

import re
from abc import ABC


def ChangeLogFormaterRecordType(Klass: type) -> type:
    """Decorator helper function to register interface implementation in factory
    Args:
        Klass: class to register in the factory
    Returns:
        untouched class"""
    ChangeLogFactory.ar_FormaterKlass.add(Klass)
    return Klass


class ChangeLogFormater(ABC):

    prefix: str = "^\s+"
    title: str = "Others :"
    keywords: list[str] = []
    priority: int = 0

    _lines: list[str] = []

    def __init__(self):
        """ChangeLogFormater class constructor

        This class is the base formater class.

        This class is for:

        - classifying message: CheckLine() and CheckLine_keywords()
        - storing lines: Clear() and PushLine()
        - returning the formated output: Render() and RenderLines()


        /// warning
        this class does not aim to be instantiated by user.
        ///

        """
        self._lines: list[str] = []

    def Clear(self) -> None:
        """Clear the formater content"""
        self._lines: list[str] = []

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
    def CheckLine(cls, content: str) -> re.Match:
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
        regex = re.compile(r"^(?:-\s+)?(?:{0})(?:\((.*)\))?(?::)(?:\s*)([^\s].+)".format(cls.prefix))
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
        for _keyword in keyword_list:
            if (_keyword != "") and re.search(_keyword, content):
                return True
        return False


class ChangeLogFactory:
    """The main changelog class"""

    ar_FormaterKlass: set[type[ChangeLogFormater]] = set()
    ar_Formater: dict[ChangeLogFormater] = dict()
    checkCommentPattern: str = r"^[ \t]*(?:\/\/|#)"

    def __init__(self, ChangelogString: None | str = None):
        """Main ChangeLogFormater class constructor

        Args:
            ChangelogString: optionnal input string to start with
        """
        for FormaterKlass in ChangeLogFactory.ar_FormaterKlass:
            self.ar_Formater[FormaterKlass.__name__] = FormaterKlass()

        if isinstance(ChangelogString, str):
            self.ProcessFullChangelog(ChangelogString)

    def RegisterFormater(self, FormaterKlass: ChangeLogFormater) -> None:
        """Register a new formater

        Args:
            FormaterKlass: class of the formater to be added
        Returns:
            self class for convenience
        """
        self.ar_FormaterKlass.add(FormaterKlass)
        self.ar_Formater[FormaterKlass.__name__] = FormaterKlass()
        return self

    def unRegisterFormater(self, FormaterKlass: ChangeLogFormater) -> None:
        """Register a new formater

        Args:
            FormaterKlass: class of the formater to be removed
        Returns:
            self class for convenience
        """
        self.ar_FormaterKlass.remove(FormaterKlass)
        del self.ar_Formater[FormaterKlass.__name__]
        return self

    def Clear(self) -> ChangeLogFactory:
        """Clear internal memory
        Returns:
            self class for convenience
        """
        for formater in self.ar_Formater.values():
            formater.Clear()
        return self

    def _ProcessLineMain(self, RawChangelogLine: str) -> bool:
        """Process a line and look for identified ones

        This function will try to apply every available formater for the 1st search round: formal search
        If a matching formater is found, line is inserted.

        Args:
            RawChangelogLine: line to parse
        Returns:
            True if successfully matched, False otherwise
        """
        for formater in sorted(self.ar_Formater.values(), key=lambda x: x.priority):
            content = formater.CheckLine(RawChangelogLine)
            if content is not None:
                formater.PushLine(content.group(2))
                return True

        return False

    def _ProcessLineSecond(self, RawChangelogLine: str) -> bool:
        """Process a line and look for non-identified ones

        This function will try to apply every available formater for the 2ns search round: any keyword
        If a matching formater is found, line is inserted.

        Args:
            RawChangelogLine: line to parse
        Returns:
            True if successfully matched, False otherwise
        """
        for formater in sorted(self.ar_Formater.values(), key=lambda x: x.priority, reverse=True):
            if formater.CheckLine_keywords(RawChangelogLine):
                formater.PushLine(RawChangelogLine)
                return True

        self.ar_Formater[ChangeLogFormater_others.__name__].PushLine(RawChangelogLine)
        return False

    def ProcessFullChangelog(self, RawChangelogMessage: str) -> ChangeLogFactory:
        """Process all input lines

        This function handles the main 2-round changes search algo.
        It takes care of search-order and automatically skip any non-relevants message line.
        A non relevant line can be a commented one, or a to short one.
        Available comment patterns are: // and #
        A relevant commit line must contain:
        - at least 2 words for formal
        - at least 3 words for keywords

        Args:
            RawChangelogMessage: The full raw changelog (merged commit-history)
        Returns:
            self class for convenience
        """

        Lines2ndRound = []

        for line in RawChangelogMessage.split("\n"):
            lineWordsCount = len(line.split())
            if (lineWordsCount > 1) and (not re.match(self.checkCommentPattern, line)):
                if self._ProcessLineMain(line) is True:
                    continue
                elif lineWordsCount > 2:
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
            if (include_unknown is False) and (isinstance(formater, ChangeLogFormater_others)):
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
    _name = f"ChangeLogFormater_{RecordType}"
    _tmp = globals()[_name] = type(
        _name,
        (ChangeLogFormater,),
        {
            "prefix": RecordType,
            "title": Config[2],
            "keywords": Config[1],
            "priority": Config[0],
        },
    )
    ChangeLogFactory.ar_FormaterKlass.add(_tmp)


@ChangeLogFormaterRecordType
class ChangeLogFormater_revert(ChangeLogFormater):
    """Revert scope formater"""

    prefix: str = "revert"
    title: str = "Reverts :back: :"
    keywords: list[str] = ["revert", "fallback"]
    priority: int = 0

    def RenderLines(self) -> str:
        """Render all lines
        Returns:
            the rendered lines
        """
        full_lines = ""
        for line in self._lines:
            full_lines = full_lines + f"> ~~{line}~~" + "\n"
        return full_lines


@ChangeLogFormaterRecordType
class ChangeLogFormater_others(ChangeLogFormater):
    """Others / unknown scope formater"""

    prefix: str = "other"
    title: str = "Others :question: :"
    keywords: list[str] = [""]
    priority: int = -20
