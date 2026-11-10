"""Tests for claude_code_rtl.py. Run with: python -m unittest"""

import contextlib
import io
import os
import shutil
import subprocess
import tempfile
import unittest

import claude_code_rtl as rtl

LEGACY_START, LEGACY_END = rtl.CSS_MARKERS[1]
LEGACY_BLOCK = "\n" + LEGACY_START + "\n.old { direction: rtl; }\n" + LEGACY_END + "\n"
ORIGINAL = "body{color:red}\r\n.a{b:c}\n"


def quietly(fn, *args):
    with contextlib.redirect_stdout(io.StringIO()):
        return fn(*args)


class InjectRemoveTests(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.path = os.path.join(self.dir, "index.css")
        self.bak = self.path + ".bak"

    def tearDown(self):
        shutil.rmtree(self.dir)

    def write(self, content, path=None):
        rtl._write(path or self.path, content)

    def read(self, path=None):
        return rtl._read(path or self.path)

    def inject(self):
        return quietly(rtl._inject, self.path, rtl.RTL_CSS_RULES, rtl.CSS_MARKERS, "CSS:", "t")

    def remove(self):
        return quietly(rtl._remove, self.path, rtl.CSS_MARKERS, "CSS:", "t")

    def state(self):
        return rtl._install_state(self.path, rtl.RTL_CSS_RULES, rtl.CSS_MARKERS)

    def test_apply_then_remove_restores_original_exactly(self):
        self.write(ORIGINAL)
        self.assertTrue(self.inject())
        self.assertEqual(self.read(self.bak), ORIGINAL)
        self.assertEqual(self.state(), "installed")
        self.assertTrue(self.remove())
        self.assertEqual(self.read(), ORIGINAL)
        self.assertFalse(os.path.exists(self.bak))

    def test_remove_without_backup_strips_block(self):
        for original in (ORIGINAL, "no newline", "two\n\n"):
            self.write(original)
            self.inject()
            os.remove(self.bak)
            self.assertTrue(self.remove())
            self.assertEqual(self.read(), original)

    def test_second_apply_changes_nothing(self):
        self.write(ORIGINAL)
        self.inject()
        once = self.read()
        self.assertTrue(self.inject())
        self.assertEqual(self.read(), once)

    def test_legacy_install_is_detected_and_upgraded(self):
        self.write(ORIGINAL + LEGACY_BLOCK)
        self.assertTrue(rtl.is_rtl_installed(self.path))
        self.assertEqual(self.state(), "outdated")

        self.assertTrue(self.inject())
        content = self.read()
        self.assertNotIn(LEGACY_START, content)
        self.assertEqual(content.count(rtl.RTL_START_MARKER), 1)
        self.assertEqual(self.state(), "installed")
        # The backup made during the upgrade holds no patch.
        self.assertNotIn(LEGACY_START, self.read(self.bak))

        self.assertTrue(self.remove())
        self.assertNotIn(LEGACY_START, self.read())
        self.assertNotIn(rtl.RTL_START_MARKER, self.read())

    def test_patched_backup_is_replaced_and_not_restored(self):
        # State an earlier version could leave: both the file and its backup
        # hold the legacy block, plus a duplicate current block.
        self.write(ORIGINAL + LEGACY_BLOCK, self.bak)
        self.write(ORIGINAL + LEGACY_BLOCK + "\n" + rtl.RTL_CSS_RULES)
        self.assertTrue(self.inject())
        self.assertNotIn(LEGACY_START, self.read(self.bak))
        self.assertTrue(self.remove())
        self.assertNotIn(LEGACY_START, self.read())
        self.assertNotIn(rtl.RTL_START_MARKER, self.read())

    def test_remove_skips_patched_backup(self):
        self.write(ORIGINAL + LEGACY_BLOCK, self.bak)
        self.write(ORIGINAL + LEGACY_BLOCK)
        self.assertTrue(self.remove())
        self.assertNotIn(LEGACY_START, self.read())
        self.assertFalse(os.path.exists(self.bak))

    def test_damaged_block_is_left_alone(self):
        damaged = ORIGINAL + "\n" + rtl.RTL_START_MARKER + "\n.x{}\n"
        self.write(damaged)
        self.assertFalse(self.inject())
        self.assertEqual(self.read(), damaged)
        self.assertFalse(self.remove())
        self.assertEqual(self.read(), damaged)

    def test_not_installed(self):
        self.write(ORIGINAL)
        self.assertEqual(self.state(), "missing")
        self.assertTrue(self.remove())
        self.assertEqual(self.read(), ORIGINAL)


class JsBlockTests(unittest.TestCase):
    def test_markers_wrap_block(self):
        block = rtl.RTL_JS_CODE.strip()
        self.assertTrue(block.startswith(rtl.JS_START_MARKER))
        self.assertTrue(block.endswith(rtl.JS_END_MARKER))
        css = rtl.RTL_CSS_RULES.strip()
        self.assertTrue(css.startswith(rtl.RTL_START_MARKER))
        self.assertTrue(css.endswith(rtl.RTL_END_MARKER))

    @unittest.skipUnless(shutil.which("node"), "node not installed")
    def test_js_block_parses(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "block.js")
            rtl._write(path, rtl.RTL_JS_CODE)
            result = subprocess.run(["node", "--check", path], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
