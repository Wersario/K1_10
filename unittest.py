import unittest
import os
from emulator import ShellEmulator

class TestShellEmulator(unittest.TestCase):

    def setUp(self):
        self.shell = ShellEmulator("test_config.xml")
        self.shell.fs_root = "/tmp/test_fs"
        os.makedirs(self.shell.fs_root, exist_ok=True)
        open(os.path.join(self.shell.fs_root, "testfile.txt"), 'w').close()

    def tearDown(self):
        shutil.rmtree(self.shell.fs_root)

    def test_ls(self):
        self.shell.current_directory = "/"
        self.shell.ls()
        self.assertIn("testfile.txt", os.listdir(self.shell.fs_root))

    def test_cd(self):
        self.shell.cd(["testfile.txt"])
        self.assertEqual(self.shell.current_directory, "/testfile.txt")

    def test_whoami(self):
        self.assertEqual(self.shell.username, "test_user")

if __name__ == '__main__':
    unittest.main()
