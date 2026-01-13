import unittest
from textnode import TextNode, TextType
from delimiter import *
from extract import extract_markdown_images
from converter import *
from blocks import *

class TestBlockToBlockType(unittest.TestCase):
    # -------- CODE --------
    def test_code_block_basic(self):
        block = "```\nprint('hi')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_block_with_hashes_not_heading(self):
        block = "```\n# not a heading inside code\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_block_with_list_markers_not_list(self):
        block = "```\n- not a list inside code\n1. not ordered inside code\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    # -------- HEADING --------
    def test_heading_level_1(self):
        block = "# Title"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_level_6(self):
        block = "###### Title"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_reject_too_many_hashes(self):
        block = "####### Too many"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading_reject_no_space(self):
        block = "###NoSpace"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading_reject_only_hashes(self):
        block = "###"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # -------- QUOTE --------
    def test_quote_single_line(self):
        block = "> hello"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_multi_line(self):
        block = "> hello\n> there\n> friend"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_reject_if_one_line_missing_prefix(self):
        block = "> good\nbad"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # -------- UNORDERED LIST --------
    def test_unordered_list_single_line(self):
        block = "- one"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_multi_line(self):
        block = "- one\n- two\n- three"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_reject_if_one_line_missing_prefix(self):
        block = "- one\ntwo"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # -------- ORDERED LIST --------
    def test_ordered_list_single_line(self):
        block = "1. one"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_multi_line(self):
        block = "1. one\n2. two\n3. three"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_reject_if_starts_not_one(self):
        block = "2. two\n3. three"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_reject_if_not_incrementing(self):
        block = "1. one\n3. three"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_reject_if_missing_space_after_dot(self):
        block = "1.one\n2. two"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_reject_if_one_line_wrong_prefix(self):
        block = "1. one\n2. two\n- three"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # -------- PARAGRAPH DEFAULT --------
    def test_paragraph_basic(self):
        block = "This is just a normal paragraph."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraph_multi_line_text(self):
        block = "This is a paragraph\nthat spans multiple lines"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()