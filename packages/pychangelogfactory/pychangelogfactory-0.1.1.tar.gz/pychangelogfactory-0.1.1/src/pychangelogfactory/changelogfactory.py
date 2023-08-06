#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pychangelogfactory (c) by chacha
#
# pychangelogfactory  is licensed under a
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International Unported License.
#
# You should have received a copy of the license along with this
# work.  If not, see <https://creativecommons.org/licenses/by-nc-sa/4.0/>.

""" A simple changelog formater that consume merged commit message and produce nice pre-formated changelogs

"""

from __future__ import annotations

import re
from abc import ABC


def ChangeLogFormaterRecordType(Klass: type) -> type:
    """decorator helper function to register interface implementation"""
    ChangeLogFormater.ar_Klass.append(Klass)
    return Klass


class ChangeLogFormater(ABC):
    """the main changelog class that define nearly everythings.
    This was supposed to be a very shorty script this is why it is all-in-one...
    Factory and base-object are mixed.
    """

    ar_Klass: list[ChangeLogFormater] = []
    ar_LinesResult: list[ChangeLogFormater] = []
    prefix: str = ""
    title: str = "Others :"
    keywords: list[str] = []
    priority: int = 0

    def __init__(self, scope: str | None, ChangelogString: str):
        self._scope = scope
        self._ChangelogString = ChangelogString.strip()

    def RenderLine(self):
        """return a rendered line"""
        return self._ChangelogString.strip()

    @classmethod
    def RenderLines(cls) -> str:
        """render all lines"""
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
        """return the current scope (category)"""
        return self._scope if self._scope is not None else ""

    @classmethod
    def Clear(cls) -> None:
        """clear internal memory"""
        ChangeLogFormater.ar_LinesResult = []

    @classmethod
    def CheckLine(cls, content: str) -> bool:
        """check if a line is in the current scope (lazy identification)"""
        regex = re.compile(r"^(?:-\s+)?(?:{0})(?:\((.*)\))?(?::)(?:\s*)([^\s].+)".format(cls.prefix))
        _match = regex.match(content)
        return _match

    @classmethod
    def CheckLine_keywords(cls, content: str) -> bool:
        """check if a line is in the current scope (deeper in-word identification)"""
        keyword_list = cls.keywords
        for _keyword in keyword_list:
            if (_keyword != "") and re.search(_keyword, content):
                return True
        return False

    @classmethod
    def FactoryProcessLineMain(cls, RawChangelogLine: str) -> ChangeLogFormater:
        """Process a line and look for identified ones"""
        for Klass in sorted(ChangeLogFormater.ar_Klass, key=lambda x: x.priority):
            content = Klass.CheckLine(RawChangelogLine)
            if content is not None:
                return Klass(content.group(1), content.group(2))
        return ChangeLogFormater_others(None, RawChangelogLine)

    @classmethod
    def FactoryProcessLineSecond(cls, RawChangelogLine: str) -> ChangeLogFormater:
        """Process a line and look for non-identified ones"""
        for Klass in sorted(ChangeLogFormater.ar_Klass, key=lambda x: x.priority, reverse=True):
            if Klass.CheckLine_keywords(RawChangelogLine):
                return Klass(None, RawChangelogLine)

        return ChangeLogFormater_others(None, RawChangelogLine)

    @classmethod
    def FactoryProcessFullChangelog(cls, RawChangelogMessage: str) -> list[ChangeLogFormater]:
        """Process all input lines"""
        LinesResult = []
        Lines2ndRound = []

        for line in RawChangelogMessage.split("\n"):
            if line.strip() != "":
                res = cls.FactoryProcessLineMain(line)
                if res is not ChangeLogFormater_others:
                    LinesResult.append(res)
                else:
                    Lines2ndRound.append(line)

        for line in Lines2ndRound:
            LinesResult.append(cls.FactoryProcessLineSecond(line))

        ChangeLogFormater.ar_LinesResult = LinesResult
        return ChangeLogFormater.ar_LinesResult

    @classmethod
    def GetLinesOfType(cls, Klass: type) -> list[ChangeLogFormater]:
        """retrieve all lines of specified type"""
        return [_ for _ in ChangeLogFormater.ar_LinesResult if isinstance(_, Klass)]

    @classmethod
    def GetLines(cls) -> list[ChangeLogFormater]:
        """retrieve all lines for the current formater"""
        return ChangeLogFormater.GetLinesOfType(cls)

    @classmethod
    def RenderFullChangelog(cls) -> str:
        """render the main changelog"""
        full_changelog = ""
        for Klass in sorted(ChangeLogFormater.ar_Klass, key=lambda x: x.priority, reverse=True):
            full_changelog = full_changelog + Klass.RenderLines()
        return full_changelog


# to avoid writing class, they are initialized with the following structure:
# creating category classes: '<NAME>':       (priority, ['<prefix1>',...],                        '<header>')
for RecordType, Config in {
    "break": (
        20,
        [],
        ":rotating_light: Breaking changes :rotating_light::",
    ),
    "feat": (20, ["feat", "new", "create", "add"], "Features      :sparkles::"),
    "fix": (10, ["issue", "problem"], "Fixes :wrench::"),
    "security": (20, ["safe", "leak"], "Security :shield::"),
    "chore": (
        20,
        ["task", "refactor", "build", "better", "improve"],
        "Chore :building_construction::",
    ),
    "perf": (
        0,
        [
            "fast",
        ],
        "Performance Enhancements :rocket::",
    ),
    "wip": (
        0,
        [
            "temp",
        ],
        "Work in progress changes :construction::",
    ),
    "docs": (
        0,
        [
            "doc",
        ],
        "Documentations :book::",
    ),
    "style": (
        5,
        [
            "beautify",
        ],
        "Style :art::",
    ),
    "refactor": (0, [], "Refactorings :recycle::"),
    "ci": (0, ["jenkins", "git"], "Continuous Integration :cyclone::"),
    "test": (15, ["unittest", "check", r"^(?:\s)*test(?:\s)*$"], "Testings :vertical_traffic_light::"),
    "build": (0, ["compile", "version"], "Builds :package:"),
}.items():
    # then we instantiate all of them
    name = f"ChangeLogFormater_{RecordType}"
    tmp = globals()[name] = type(
        name,
        (ChangeLogFormater,),
        {
            "prefix": RecordType,
            "title": Config[2],
            "keywords": Config[1],
            "priority": Config[0],
        },
    )
    ChangeLogFormater.ar_Klass.append(tmp)


@ChangeLogFormaterRecordType
class ChangeLogFormater_revert(ChangeLogFormater):
    """revert scope formater"""

    prefix: str = "revert"
    title: str = "Reverts :back::"
    keywords: list[str] = ["fallback"]
    priority: int = 0

    def RenderLine(self) -> str:
        return "~~" + super().RenderLine() + "~~"


@ChangeLogFormaterRecordType
class ChangeLogFormater_others(ChangeLogFormater):
    """others / unknown scope formater"""

    prefix: str = "other"
    title: str = "Others :question::"
    keywords: list[str] = [""]
    priority: int = -20
