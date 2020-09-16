import unittest
import ocr

class TestOcr(unittest.TestCase):

    def test_get_extension(self):
        unix_path: str = "example/unix/path/1.txt"
        self.assertEqual(ocr.get_filename(unix_path), "1")

        unix_path_noext: str = "another/unix/path/no_extension"
        self.assertEqual(ocr.get_filename(unix_path_noext), "no_extension")

        windows_path: str = "example\\windows\\path.extension" # backslashes are escaped because python likes it that way
        self.assertEqual(ocr.get_filename(windows_path), "path")

        windows_path_noext: str = "example\\windows\\path\\no_extension"
        self.assertEqual(ocr.get_filename(windows_path_noext), "no_extension")


if __name__ == "__main__":
    unittest.main()