# pyChaChaDummyProject (c) by chacha
#
# pyChaChaDummyProject is licensed under a
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International Unported License.
#
# You should have received a copy of the license along with this
# work.  If not, see <https://creativecommons.org/licenses/by-nc-sa/4.0/>.

from __future__ import annotations
from typing import TYPE_CHECKING

from pathlib import Path

from mypy import api

from .helper_base import helper_withresults_base


class types_check(helper_withresults_base):
    JUnitReportName = "junit.xml"

    @classmethod
    def do_job(cls):
        print("checking code typing ...")
        result = api.run(
            [  # project path
                "-m",
                "src." + str(cls.pyproject["project"]["name"]),
                # analysis configuration
                "--ignore-missing-imports",
                "--strict-equality",
                # reports generation
                "--cobertura-xml-report",
                str(cls.get_result_dir()),
                "--html-report",
                str(cls.get_result_dir()),
                "--linecount-report",
                str(cls.get_result_dir()),
                "--linecoverage-report",
                str(cls.get_result_dir()),
                "--lineprecision-report",
                str(cls.get_result_dir()),
                "--txt-report",
                str(cls.get_result_dir()),
                "--xml-report",
                str(cls.get_result_dir()),
                "--junit-xml",
                str(cls.get_result_dir()) + "/" + cls.JUnitReportName,
            ]
        )

        if result[0]:
            print("\nType checking report:\n")
            print(result[0])  # stdout

        if result[1]:
            print("\nError report:\n")
            print(result[1])  # stderr

        print("\nExit status:", result[2])
        print("Done")
