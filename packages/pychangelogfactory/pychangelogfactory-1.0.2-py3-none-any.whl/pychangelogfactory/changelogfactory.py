#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pychangelogfactory (c) by chacha
#
# pychangelogfactory  is licensed under a
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International Unported License.
#
# You should have received a copy of the license along with this
# work.  If not, see <https://creativecommons.org/licenses/by-nc-sa/4.0/>.

"""A simple changelog formater that consume merged commit message and produce nice pre-formated changelogs.

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
    ChangeLogFormater.ar_Klass.append(Klass)
    return Klass


class ChangeLogFormater(ABC):
    """The main changelog class that define nearly everythings.

    This was supposed to be a very shorty script this is why it is all-in-one...
    /// warning
    Factory and base-objects are mixed in the same class.
    ///
    """

    ar_Klass: list[ChangeLogFormater] = []
    ar_LinesResult: list[ChangeLogFormater] = []
    prefix: str = "^\s+"
    title: str = "Others :"
    checkCommentPattern: str = r"^[ \t]*(?:\/\/|#)"
    keywords: list[str] = []
    priority: int = 0

    def __init__(self, scope: str | None, ChangelogString: str):
        """Main ChangeLogFormater class constructor

        This class contain both formater and factory.

        /// warning
        this class does not aim to be instantiated by user.
        ///
        Args:
            scope: scope of the formater (tag)
            ChangelogString: formater rendered title
        """
        self._scope = scope
        self._ChangelogString = ChangelogString.strip()

    def RenderLine(self):
        """Get a rendered line
        Returns:
            the rendered line
        """
        return self._ChangelogString.strip()

    @classmethod
    def RenderLines(cls) -> str:
        """Render all lines
        Returns:
            the rendered lines
        """
        changelog_category: str = ""
        lines = cls.GetLines()
        if len(lines) > 0:
            changelog_category = f"#### {cls.title}\n"
            for line in lines:
                changelog_category = changelog_category + f"> {line.RenderLine()}"
                if (scope := line.GetScope()) != "":
                    changelog_category = changelog_category + f"\t*[{scope}]*"
                changelog_category = changelog_category + "\n"
        return changelog_category

    def GetScope(self) -> str:
        """Return the current scope (category)
        Returns:
            the current scope
        """
        return self._scope if self._scope is not None else ""

    @classmethod
    def Clear(cls) -> None:
        """Clear internal memory"""
        ChangeLogFormater.ar_LinesResult = []

    @classmethod
    def CheckLine(cls, content: str) -> re.Match:
        """Check if a line is in the current scope (lazy identification)
        only formal tags are parsed by this function
        eg: <change_type>(<change_target>): <change_message>
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
        """Check if a line is in the current scope (deeper in-word identification)
        any word in the message can be used to categorize this message.
        this function test only for the current category.
        Args:
            content: line to parse
        Returns:
            True if a keyword has matched
        """
        keyword_list = cls.keywords
        for _keyword in keyword_list:
            if (_keyword != "") and re.search(_keyword, content):
                return True
        return False

    @classmethod
    def FactoryProcessLineMain(cls, RawChangelogLine: str) -> ChangeLogFormater:
        """Process a line and look for identified ones
        this function will try to apply every available formater for the 1st search round: formal search
        order of search is set according to formater's configuration
        Args:
            RawChangelogLine: line to parse
        Returns:
            a corresponding ChangeLogFormater_XXX() object, or a ChangeLogFormater_others()
        """
        for Klass in sorted(ChangeLogFormater.ar_Klass, key=lambda x: x.priority):
            content = Klass.CheckLine(RawChangelogLine)
            if content is not None:
                return Klass(content.group(1), content.group(2))
        return ChangeLogFormater_others(None, RawChangelogLine)

    @classmethod
    def FactoryProcessLineSecond(cls, RawChangelogLine: str) -> ChangeLogFormater:
        """Process a line and look for non-identified ones
        this function will try to apply every available formater for the 2ns search round: any keyword
        order of search is set according to formater's configuration
        Args:
            RawChangelogLine: line to parse
        Returns:
            a corresponding ChangeLogFormater_XXX() object, or a ChangeLogFormater_others()
        """
        for Klass in sorted(ChangeLogFormater.ar_Klass, key=lambda x: x.priority, reverse=True):
            if Klass.CheckLine_keywords(RawChangelogLine):
                return Klass(None, RawChangelogLine)

        return ChangeLogFormater_others(None, RawChangelogLine)

    @classmethod
    def FactoryProcessFullChangelog(cls, RawChangelogMessage: str) -> list[ChangeLogFormater]:
        """Process all input lines
        This function handle the main 2-round changes search algo.
        Tt takes care of search-order and automatically skip any non-relevants message line.
        A non relevant line can be a commented one, or a to short one.
        Available comment patterns are: // and #
        A relevant commit line must contain:
        - at least 2 words for formal
        - at least 3 words for keywords
        Args:
            RawChangelogMessage: The full raw changelog (merged commit-history)
        Returns:
            a list of ChangeLogFormater_XXX() object
        """
        LinesResult = []
        Lines2ndRound = []

        for line in RawChangelogMessage.split("\n"):
            lineWordsCount = len(line.split())
            if (lineWordsCount > 1) and (not re.match(cls.checkCommentPattern, line)):
                res = cls.FactoryProcessLineMain(line)
                if type(res) is not ChangeLogFormater_others:
                    LinesResult.append(res)
                elif lineWordsCount > 2:
                    Lines2ndRound.append(line)

        for line in Lines2ndRound:
            LinesResult.append(cls.FactoryProcessLineSecond(line))

        ChangeLogFormater.ar_LinesResult = LinesResult
        return ChangeLogFormater.ar_LinesResult

    @classmethod
    def GetLinesOfType(cls, Klass: type) -> list[ChangeLogFormater]:
        """Retrieve all lines of specified formater type
        Args:
            Klass: type of formater to get
        Returns:
            a list of ChangeLogFormater_XXX() object
        """
        return [_ for _ in ChangeLogFormater.ar_LinesResult if isinstance(_, Klass)]

    @classmethod
    def GetLines(cls) -> list[ChangeLogFormater]:
        """Retrieve all lines for the current formater
        Returns:
            a list of ChangeLogFormater_XXX() object
        """
        return ChangeLogFormater.GetLinesOfType(cls)

    @classmethod
    def RenderFullChangelog(cls, include_unknown: bool = False) -> str:
        """Render the main changelog
        Args:
            include_unknown: includes unknown lines in an Unknown category
        Returns:
            the final formated changelog
        """
        full_changelog = ""
        for Klass in sorted(ChangeLogFormater.ar_Klass, key=lambda x: x.priority, reverse=True):
            if (include_unknown is False) and (Klass == ChangeLogFormater_others):
                continue
            full_changelog = full_changelog + Klass.RenderLines()
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
                    ":rotating_light: Breaking changes :rotating_light::",
                ),
    "feat":     (   20, ["feat", "new", "create", "add"],
                    "Features      :sparkles::"
                ),
    "fix":      (   0, ["fix","issue", "problem"],
                    "Fixes :wrench::"
                ),
    "security": (   20, ["safe", "leak"],
                    "Security :shield::"
                ),
    "chore":    (   20, ["task", "refactor", "build", "better", "improve"],
                    "Chore :building_construction::",
                ),
    "perf":     (   0,  ["fast", ],
                    "Performance Enhancements :rocket::",
                ),
    "wip":      (   0,  ["temp", ],
                    "Work in progress changes :construction::",
                ), 
    "docs":     (   0,  [ "doc", ], 
                    "Documentations :book::",
                ),
    "style":    (   5,  ["beautify", ],
                    "Style :art::", 
                ),
    "refactor": (   0,  [],
                    "Refactorings :recycle::"
                ),
    "ci":       (   0,  ["jenkins", "git"], 
                    "Continuous Integration :cyclone::"
                ),
    "test":     (   -5, ["unittest", "check", r"^(?:\s)*test(?:\s)*$"], 
                    "Testings :vertical_traffic_light::"
                ),
    "build":    (   0,  ["compile", "version"], 
                    "Builds :package:"
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
    ChangeLogFormater.ar_Klass.append(_tmp)


@ChangeLogFormaterRecordType
class ChangeLogFormater_revert(ChangeLogFormater):
    """Revert scope formater"""

    prefix: str = "revert"
    title: str = "Reverts :back::"
    keywords: list[str] = ["fallback"]
    priority: int = 0

    def RenderLine(self) -> str:
        """an overloaded RenderLine implementation that adds surrounding '~~'
        Returns:
            the rendered pattern
        """
        return "~~" + super().RenderLine() + "~~"


@ChangeLogFormaterRecordType
class ChangeLogFormater_others(ChangeLogFormater):
    """Others / unknown scope formater"""

    prefix: str = "other"
    title: str = "Others :question::"
    keywords: list[str] = [""]
    priority: int = -20
