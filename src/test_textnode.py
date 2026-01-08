import unittest
from textnode import TextNode, TextType
from delimiter import *
from extract import extract_markdown_images
from converter import *

class TestTextToTextNodes(unittest.TestCase):
    def test_plain_text(self):
        text = "Just plain text."
        self.assertEqual(
            text_to_textnodes(text),
            [TextNode("Just plain text.", TextType.TEXT)],
        )

    def test_bold_only(self):
        text = "This is **bold** text"
        self.assertEqual(
            text_to_textnodes(text),
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_italic_only_underscore(self):
        text = "This is _italic_ text"
        self.assertEqual(
            text_to_textnodes(text),
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_code_only(self):
        text = "This is `code` here"
        self.assertEqual(
            text_to_textnodes(text),
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" here", TextType.TEXT),
            ],
        )

    def test_single_image(self):
        text = "Hello ![cat](cat.png) world"
        self.assertEqual(
            text_to_textnodes(text),
            [
                TextNode("Hello ", TextType.TEXT),
                TextNode("cat", TextType.IMAGES, "cat.png"),
                TextNode(" world", TextType.TEXT),
            ],
        )

    def test_single_link(self):
        text = "Go to [boot](https://www.boot.dev) now"
        self.assertEqual(
            text_to_textnodes(text),
            [
                TextNode("Go to ", TextType.TEXT),
                TextNode("boot", TextType.LINKS, "https://www.boot.dev"),
                TextNode(" now", TextType.TEXT),
            ],
        )

    def test_image_not_treated_as_link(self):
        text = "An image ![cat](cat.png) and a [site](x)"
        self.assertEqual(
            text_to_textnodes(text),
            [
                TextNode("An image ", TextType.TEXT),
                TextNode("cat", TextType.IMAGES, "cat.png"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("site", TextType.LINKS, "x"),
            ],
        )

    def test_all_features_mixed(self):
        text = (
            "This is **text** with an _italic_ word and a `code block` "
            "and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) "
            "and a [link](https://boot.dev)"
        )
        self.assertEqual(
            text_to_textnodes(text),
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGES, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINKS, "https://boot.dev"),
            ],
        )

    def test_adjacent_links(self):
        text = "[a](x)[b](y)"
        self.assertEqual(
            text_to_textnodes(text),
            [
                TextNode("a", TextType.LINKS, "x"),
                TextNode("b", TextType.LINKS, "y"),
            ],
        )

    def test_adjacent_images(self):
        text = "![a](x)![b](y)"
        self.assertEqual(
            text_to_textnodes(text),
            [
                TextNode("a", TextType.IMAGES, "x"),
                TextNode("b", TextType.IMAGES, "y"),
            ],
        )


if __name__ == "__main__":
    unittest.main()





if __name__ == "__main__":
    unittest.main()