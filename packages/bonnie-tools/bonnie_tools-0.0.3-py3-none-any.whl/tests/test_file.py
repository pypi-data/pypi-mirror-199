# coding: utf-8

from unittest import TestCase
from bonnie.utils.file import add_suffix_to_filename


class TestMsg(TestCase):
    def test_add_suffix_to_simple_filename(self):
        src_file = 'test.txt'
        suffix = '_new'
        result = add_suffix_to_filename(src_file, suffix)
        expected_result = 'test_new.txt'
        self.assertEqual(result, expected_result)

    def test_add_suffix_to_filename_with_multiple_dots(self):
        src_file = 'test.file.txt'
        suffix = '_new'
        result = add_suffix_to_filename(src_file, suffix)
        expected_result = 'test.file_new.txt'
        self.assertEqual(result, expected_result)

    def test_add_suffix_to_hidden_filename(self):
        src_file = '.test.txt'
        suffix = '_new'
        result = add_suffix_to_filename(src_file, suffix)
        expected_result = '.test_new.txt'
        self.assertEqual(result, expected_result)

    def test_add_suffix_to_filename_with_space(self):
        src_file = 'test file.txt'
        suffix = '_new'
        result = add_suffix_to_filename(src_file, suffix)
        expected_result = 'test file_new.txt'
        self.assertEqual(result, expected_result)

    def test_add_suffix_to_unicode_filename(self):
        src_file = '你好.txt'
        suffix = '_new'
        result = add_suffix_to_filename(src_file, suffix)
        expected_result = '你好_new.txt'
        self.assertEqual(result, expected_result)

    def test_add_suffix_to_filename_with_special_characters(self):
        src_file = 'test#$.txt'
        suffix = '_new'
        result = add_suffix_to_filename(src_file, suffix)
        expected_result = 'test#$_new.txt'
        self.assertEqual(result, expected_result)

    def test_add_suffix_to_filename_with_long_extension(self):
        src_file = 'test.very.long.extension.txt'
        suffix = '_new'
        result = add_suffix_to_filename(src_file, suffix)
        expected_result = 'test.very.long.extension_new.txt'
        self.assertEqual(result, expected_result) 
    
    def test_add_suffix_to_windows_file_name(self):
        # Test adding suffix to Windows file path
        src_file = 'C:\\Users\\test\\abc.xlsx'
        suffix = '_1'
        expected_result = 'C:\\Users\\test\\abc_1.xlsx'
        self.assertEqual(add_suffix_to_filename(src_file, suffix), expected_result)
        
    def test_add_suffix_to_mac_file_name(self):
        # Test adding suffix to Mac file path
        src_file = '/Users/test/abc.xlsx'
        suffix = '_1'
        expected_result = '/Users/test/abc_1.xlsx'
        self.assertEqual(add_suffix_to_filename(src_file, suffix), expected_result)
        
    def test_add_suffix_to_linux_file_name(self):
        # Test adding suffix to Linux file path
        src_file = '/home/test/abc.xlsx'
        suffix = '_1'
        expected_result = '/home/test/abc_1.xlsx'
        self.assertEqual(add_suffix_to_filename(src_file, suffix), expected_result)
