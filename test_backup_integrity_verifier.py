import sys, os, json, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unittest
from main import create_manifest, verify


class TestBackupVerifier(unittest.TestCase):
    def _tree(self):
        tmp = tempfile.TemporaryDirectory()
        with open(os.path.join(tmp.name, "a.txt"), "w") as f:
            f.write("hello")
        with open(os.path.join(tmp.name, "b.txt"), "w") as f:
            f.write("world")
        return tmp

    def test_clean_verify(self):
        tmp = self._tree()
        with tmp:
            self.assertTrue(verify(tmp.name, create_manifest(tmp.name))["ok"])

    def test_changed_detected(self):
        tmp = self._tree()
        with tmp:
            manifest = create_manifest(tmp.name)
            with open(os.path.join(tmp.name, "a.txt"), "w") as f:
                f.write("CHANGED")
            self.assertEqual(verify(tmp.name, manifest)["changed"], ["a.txt"])

    def test_missing_and_new_detected(self):
        tmp = self._tree()
        with tmp:
            manifest = create_manifest(tmp.name)
            os.remove(os.path.join(tmp.name, "b.txt"))
            with open(os.path.join(tmp.name, "c.txt"), "w") as f:
                f.write("new")
            result = verify(tmp.name, manifest)
            self.assertEqual(result["missing"], ["b.txt"])
            self.assertEqual(result["new"], ["c.txt"])


if __name__ == "__main__":
    unittest.main()
