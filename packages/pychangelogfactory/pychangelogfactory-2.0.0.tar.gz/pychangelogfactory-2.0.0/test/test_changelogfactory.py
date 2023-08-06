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
        hdlr = pychangelogfactory.ChangeLogFactory()
        hdlr.ProcessFullChangelog(inputstr)
        changelog = hdlr.RenderFullChangelog()
        for test in teststrs:
            self.assertIn(test, changelog)

    def test_simplegeneration_ignored2(self):
        raw = "break: testbreak break" + "\n" + "#doc: testdoc doc" + "\n" + "#style: teststyle beautify" + "\n" + "//test: testtest check"

        hdlr = pychangelogfactory.ChangeLogFactory(raw)
        changelog = hdlr.RenderFullChangelog()

        self.assertIn("testbreak", changelog)
        self.assertNotIn("testdoc", changelog)
        self.assertNotIn("teststyle", changelog)
        self.assertNotIn("testtest", changelog)

    def test_simplegeneration_ignored(self):
        raw = "break: testbreak" + "\n" + "#doc: testdoc" + "\n" + "#style: teststyle" + "\n" + "//test: testtest"

        hdlr = pychangelogfactory.ChangeLogFactory(raw)
        changelog = hdlr.RenderFullChangelog()
        self.assertIn("testbreak", changelog)
        self.assertNotIn("testdoc", changelog)
        self.assertNotIn("teststyle", changelog)
        self.assertNotIn("testtest", changelog)

    def test_simplegeneration_order(self):
        raw = "break: testbreak" + "\n" + "doc: testdoc" + "\n" + "style: teststyle" + "\n" + "test: testtest"
        hdlr = pychangelogfactory.ChangeLogFactory(raw)
        changelog = hdlr.RenderFullChangelog().splitlines()
        self.assertIn("testbreak", changelog[1])
        self.assertIn("teststyle", changelog[3])
        self.assertIn("testdoc", changelog[5])
        self.assertIn("testtest", changelog[7])

    def test_simplegeneration_multiple(self):
        raw = "break: testbreak" + "\n" + "doc: testdoc" + "\n" + "style: teststyle"
        self.simplegeneration(raw, ["testbreak", "testdoc", "teststyle"])

    def test_simplegeneration_breaking(self):
        self.simplegeneration("break: teststring", ["teststring"])
        self.simplegeneration("test break dummy1 dummy2", ["test break"])

    def test_simplegeneration_features(self):
        self.simplegeneration("feat: teststring", ["teststring"])
        self.simplegeneration("test feat dummy1 dummy2", ["test feat"])
        self.simplegeneration("test new dummy1 dummy2", ["test new"])
        self.simplegeneration("test create dummy1 dummy2", ["test create"])
        self.simplegeneration("test add dummy1 dummy2", ["test add"])

    def test_simplegeneration_fix(self):
        self.simplegeneration("fix: teststring", ["teststring"])
        self.simplegeneration("test fix dummy1 dummy2", ["test fix"])
        self.simplegeneration("test issue dummy1 dummy2", ["test issue"])
        self.simplegeneration("test problem dummy1 dummy2", ["test problem"])

    def test_simplegeneration_security(self):
        self.simplegeneration("security: teststring", ["teststring"])
        self.simplegeneration("test safe dummy1 dummy2", ["test safe"])
        self.simplegeneration("test leak dummy1 dummy2", ["test leak"])

    def test_simplegeneration_chore(self):
        self.simplegeneration("chore: teststring", ["teststring"])
        self.simplegeneration("chore refactor dummy1 dummy2", ["chore refactor"])
        self.simplegeneration("chore build dummy1 dummy2", ["chore build"])
        self.simplegeneration("chore better dummy1 dummy2", ["chore better"])
        self.simplegeneration("chore improve dummy1 dummy2", ["chore improve"])

    def test_simplegeneration_perf(self):
        self.simplegeneration("perf: teststring", ["teststring"])
        self.simplegeneration("test fast dummy1 dummy2", ["test fast"])

    def test_simplegeneration_wip(self):
        self.simplegeneration("wip: teststring", ["teststring"])
        self.simplegeneration("test temp dummy1 dummy2", ["test temp"])

    def test_simplegeneration_docs(self):
        self.simplegeneration("doc: teststring", ["teststring"])
        self.simplegeneration("test doc dummy1 dummy2", ["test doc"])

    def test_simplegeneration_style(self):
        self.simplegeneration("style: teststring", ["teststring"])
        self.simplegeneration("test beautify dummy1 dummy2", ["test beautify"])

    def test_simplegeneration_refactor(self):
        self.simplegeneration("refactor: teststring", ["teststring"])

    def test_simplegeneration_ci(self):
        self.simplegeneration("ci: teststring", ["teststring"])
        self.simplegeneration("test jenkins dummy1 dummy2", ["test jenkins"])
        self.simplegeneration("test git dummy1 dummy2", ["test git"])

    def test_simplegeneration_test(self):
        self.simplegeneration("test: teststring", ["teststring"])
        self.simplegeneration("test unittest dummy1 dummy2", ["test unittest"])
        self.simplegeneration("test check dummy1 dummy2", ["test check"])

    def test_simplegeneration_build(self):
        self.simplegeneration("build: teststring", ["teststring"])
        self.simplegeneration("test compile dummy1 dummy2", ["test compile"])
        self.simplegeneration("test version dummy1 dummy2", ["test version"])

    def test_simplegeneration_revert(self):
        self.simplegeneration("revert: teststring", ["~~teststring~~"])

    # fmt: off
    raw_changelog = (
        "feat: add a nice feature to the project\n"
        "style: reindent the full Foo class\n"
        "security: fix a security issue on the Foo2 component\n"
        "security: fix another security problem on the Foo2 component\n"
        "improve core performances by reducing complexity\n"
        "some random changes in the text content\n"
    )
    expected_formated = (
        "#### Features      :sparkles: :\n"
        "> add a nice feature to the project\n"
        "#### Security :shield: :\n"
        "> fix a security issue on the Foo2 component\n"
        "> fix another security problem on the Foo2 component\n"
        "#### Performance Enhancements :rocket: :\n"
        "> improve core performances by reducing complexity\n"
        "#### Style :art: :\n"
        "> reindent the full Foo class\n"
        "#### Others :question: :\n"
        "> some random changes in the text content\n"
    )
    # fmt: on

    def test_sample(self):
        hdlr = pychangelogfactory.ChangeLogFactory(self.raw_changelog)
        changelog = hdlr.RenderFullChangelog(include_unknown=True)
        self.assertEqual(changelog, self.expected_formated)

    def test_sample_aio(self):
        changelog = pychangelogfactory.ChangeLogFactory(self.raw_changelog).RenderFullChangelog(include_unknown=True)
        print(changelog)
        self.assertEqual(changelog, self.expected_formated)

    def test_sample_exploded(self):
        hdlr = pychangelogfactory.ChangeLogFactory()
        hdlr.ProcessFullChangelog(self.raw_changelog)
        changelog = hdlr.RenderFullChangelog(include_unknown=True)
        self.assertEqual(changelog, self.expected_formated)


class Testtest_module_othercontext(unittest.TestCase):
    def test_custom(self):

        from src.pychangelogfactory import ChangeLogFormater, ChangeLogFormaterRecordType, ChangeLogFactory

        @ChangeLogFormaterRecordType
        class ChangeLogFormater_TEST(ChangeLogFormater):
            """My formater"""

            prefix: str = "mytag"
            title: str = "My Title :"
            keywords: list[str] = ["foo", "42"]
            priority: int = 10

        # fmt: off
        raw_changelog = ("mytag: add a nice feature to the project\n" 
                         "foo modification in my file\n" 
                         "need 42 coffee\n"
                        )
        expected_formated = (
        "#### My Title :\n"
        "> add a nice feature to the project\n"
        "> foo modification in my file\n"
        "> need 42 coffee\n"
        )
        # fmt: on

        hdlr = ChangeLogFactory(raw_changelog)
        changelog = hdlr.RenderFullChangelog(include_unknown=True)
        self.assertEqual(changelog, expected_formated)
