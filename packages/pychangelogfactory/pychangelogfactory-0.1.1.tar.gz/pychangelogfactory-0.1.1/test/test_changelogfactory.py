# pychangelogfactory (c) by chacha
#
# pychangelogfactory  is licensed under a
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International Unported License.
#
# You should have received a copy of the license along with this
# work.  If not, see <https://creativecommons.org/licenses/by-nc-sa/4.0/>.

import unittest

from src import pychangelogfactory


class Testtest_module(unittest.TestCase):
    def simplegeneration(self, inputstr, teststrs: list[str]):
        pychangelogfactory.ChangeLogFormater.FactoryProcessFullChangelog(inputstr)
        changelog = pychangelogfactory.ChangeLogFormater.RenderFullChangelog()
        for test in teststrs:
            self.assertIn(test, changelog)

    def test_simplegeneration_order(self):
        raw = "break: testbreak" + "\n" + "docs: testdoc" + "\n" + "style: teststyle" + "\n" + "test: testtest"
        pychangelogfactory.ChangeLogFormater.FactoryProcessFullChangelog(raw)
        changelog = pychangelogfactory.ChangeLogFormater.RenderFullChangelog().splitlines()
        self.assertIn("testbreak", changelog[1])
        self.assertIn("testtest", changelog[3])
        self.assertIn("teststyle", changelog[5])
        self.assertIn("testdoc", changelog[7])

    def test_simplegeneration_multiple(self):
        raw = "break: testbreak" + "\n" + "docs: testdoc" + "\n" + "style: teststyle"

        self.simplegeneration(raw, ["testbreak", "testdoc", "teststyle"])

    def test_simplegeneration_breaking(self):
        self.simplegeneration("break: teststring", ["teststring"])
        self.simplegeneration("test break", ["test break"])

    def test_simplegeneration_features(self):
        self.simplegeneration("feat: teststring", ["teststring"])
        self.simplegeneration("test feat", ["test feat"])
        self.simplegeneration("test new", ["test new"])
        self.simplegeneration("test create", ["test create"])
        self.simplegeneration("test add", ["test add"])

    def test_simplegeneration_fix(self):
        self.simplegeneration("fix: teststring", ["teststring"])
        self.simplegeneration("test fix", ["test fix"])
        self.simplegeneration("test issue", ["test issue"])
        self.simplegeneration("test problem", ["test problem"])

    def test_simplegeneration_security(self):
        self.simplegeneration("security: teststring", ["teststring"])
        self.simplegeneration("test safe", ["test safe"])
        self.simplegeneration("test leak", ["test leak"])

    def test_simplegeneration_task(self):
        self.simplegeneration("task: teststring", ["teststring"])
        self.simplegeneration("test refactor", ["test refactor"])
        self.simplegeneration("test build", ["test build"])
        self.simplegeneration("test better", ["test better"])
        self.simplegeneration("test improve", ["test improve"])

    def test_simplegeneration_perf(self):
        self.simplegeneration("perf: teststring", ["teststring"])
        self.simplegeneration("test fast", ["test fast"])

    def test_simplegeneration_wip(self):
        self.simplegeneration("wip: teststring", ["teststring"])
        self.simplegeneration("test temp", ["test temp"])

    def test_simplegeneration_docs(self):
        self.simplegeneration("docs: teststring", ["teststring"])
        self.simplegeneration("test doc", ["test doc"])

    def test_simplegeneration_style(self):
        self.simplegeneration("style: teststring", ["teststring"])
        self.simplegeneration("test beautify", ["test beautify"])

    def test_simplegeneration_refactor(self):
        self.simplegeneration("refactor: teststring", ["teststring"])

    def test_simplegeneration_ci(self):
        self.simplegeneration("ci: teststring", ["teststring"])
        self.simplegeneration("test jenkins", ["test jenkins"])
        self.simplegeneration("test git", ["test git"])

    def test_simplegeneration_test(self):
        self.simplegeneration("test: teststring", ["teststring"])
        self.simplegeneration("test unittest", ["test unittest"])
        self.simplegeneration("test check", ["test check"])

    def test_simplegeneration_build(self):
        self.simplegeneration("build: teststring", ["teststring"])
        self.simplegeneration("test compile", ["test compile"])
        self.simplegeneration("test version", ["test version"])

    def test_simplegeneration_revert(self):
        self.simplegeneration("revert: teststring", ["~~teststring~~"])
