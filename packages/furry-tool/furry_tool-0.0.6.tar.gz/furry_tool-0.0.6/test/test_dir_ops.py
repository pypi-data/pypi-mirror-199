import unittest

from furry_tool.io.dir_ops import get_dir_files_by_asb_filename


class Test_dir_ops(unittest.TestCase):
    def test_get_dir_files_by_asb_filename(self):
        path = r'./Kart/'
        dir_files_names = get_dir_files_by_asb_filename(path)


unittest.main()
