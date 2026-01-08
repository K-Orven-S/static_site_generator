import unittest
from textnode import TextNode, TextType
from delimiter import *
from extract import extract_markdown_images


class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_images_none(self):
        text = "Just plain text, no images here."
        self.assertEqual(extract_markdown_images(text), [])

    def test_extract_images_single(self):
        text = "Hello ![cat](cat.png) world"
        self.assertEqual(extract_markdown_images(text), [("cat", "cat.png")])

    def test_extract_images_multiple(self):
        text = (
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) "
            "and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertEqual(
            extract_markdown_images(text),
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
        )

    def test_extract_images_allows_empty_alt(self):
        text = "Look ![](a.png)"
        self.assertEqual(extract_markdown_images(text), [("", "a.png")])


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_links_none(self):
        text = "Just plain text, no links here."
        self.assertEqual(extract_markdown_links(text), [])

    def test_extract_links_single(self):
        text = "Hello [boot](https://www.boot.dev) world"
        self.assertEqual(extract_markdown_links(text), [("boot", "https://www.boot.dev")])

    def test_extract_links_multiple(self):
        text = (
            "This is text with a link [to boot dev](https://www.boot.dev) "
            "and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertEqual(
            extract_markdown_links(text),
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
        )

    def test_extract_links_does_not_match_images(self):
        text = "Image: ![cat](cat.png) then link: [site](https://example.com)"
        self.assertEqual(extract_markdown_links(text), [("site", "https://example.com")])


class TestSplitNodesLink(unittest.TestCase):
    def test_split_link_no_links_returns_original(self):
        node = TextNode("No links here", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [node])

    def test_split_link_single(self):
        node = TextNode("Hello [boot](https://www.boot.dev) world", TextType.TEXT)
        new_nodes = split_nodes_link([node])

        expected = [
            TextNode("Hello ", TextType.TEXT),
            TextNode("boot", TextType.LINKS, "https://www.boot.dev"),
            TextNode(" world", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_link_multiple(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])

        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINKS, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINKS, "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_link_at_start(self):
        node = TextNode("[boot](https://www.boot.dev) is cool", TextType.TEXT)
        new_nodes = split_nodes_link([node])

        expected = [
            TextNode("boot", TextType.LINKS, "https://www.boot.dev"),
            TextNode(" is cool", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_link_at_end(self):
        node = TextNode("Go to [boot](https://www.boot.dev)", TextType.TEXT)
        new_nodes = split_nodes_link([node])

        expected = [
            TextNode("Go to ", TextType.TEXT),
            TextNode("boot", TextType.LINKS, "https://www.boot.dev"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_link_adjacent_links(self):
        node = TextNode(
            "[a](x)[b](y)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])

        expected = [
            TextNode("a", TextType.LINKS, "x"),
            TextNode("b", TextType.LINKS, "y"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_link_leaves_non_text_nodes_unchanged(self):
        old_nodes = [
            TextNode("prefix ", TextType.TEXT),
            TextNode("already bold", TextType.BOLD),
            TextNode("[boot](https://www.boot.dev)", TextType.TEXT),
        ]
        new_nodes = split_nodes_link(old_nodes)

        expected = [
            TextNode("prefix ", TextType.TEXT),
            TextNode("already bold", TextType.BOLD),
            TextNode("boot", TextType.LINKS, "https://www.boot.dev"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_link_does_not_split_images(self):
        node = TextNode("An image ![cat](cat.png) and a [site](x)", TextType.TEXT)
        new_nodes = split_nodes_link([node])

        expected = [
            TextNode("An image ![cat](cat.png) and a ", TextType.TEXT),
            TextNode("site", TextType.LINKS, "x"),
        ]
        self.assertEqual(new_nodes, expected)


class TestSplitNodesImage(unittest.TestCase):
    def test_split_image_no_images_returns_original(self):
        node = TextNode("No images here", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, [node])

    def test_split_image_single(self):
        node = TextNode("Hello ![cat](cat.png) world", TextType.TEXT)
        new_nodes = split_nodes_image([node])

        expected = [
            TextNode("Hello ", TextType.TEXT),
            TextNode("cat", TextType.IMAGES, "cat.png"),
            TextNode(" world", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_image_multiple(self):
        node = TextNode(
            "A ![one](1.png) and ![two](2.png) done",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])

        expected = [
            TextNode("A ", TextType.TEXT),
            TextNode("one", TextType.IMAGES, "1.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("two", TextType.IMAGES, "2.png"),
            TextNode(" done", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_image_at_start(self):
        node = TextNode("![cat](cat.png) is here", TextType.TEXT)
        new_nodes = split_nodes_image([node])

        expected = [
            TextNode("cat", TextType.IMAGES, "cat.png"),
            TextNode(" is here", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_image_at_end(self):
        node = TextNode("Look ![cat](cat.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])

        expected = [
            TextNode("Look ", TextType.TEXT),
            TextNode("cat", TextType.IMAGES, "cat.png"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_image_adjacent_images(self):
        node = TextNode("![a](x)![b](y)", TextType.TEXT)
        new_nodes = split_nodes_image([node])

        expected = [
            TextNode("a", TextType.IMAGES, "x"),
            TextNode("b", TextType.IMAGES, "y"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_image_leaves_non_text_nodes_unchanged(self):
        old_nodes = [
            TextNode("prefix ", TextType.TEXT),
            TextNode("already code", TextType.CODE),
            TextNode("![cat](cat.png)", TextType.TEXT),
        ]
        new_nodes = split_nodes_image(old_nodes)

        expected = [
            TextNode("prefix ", TextType.TEXT),
            TextNode("already code", TextType.CODE),
            TextNode("cat", TextType.IMAGES, "cat.png"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_image_does_not_split_links(self):
        node = TextNode("A link [site](x) and ![cat](cat.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])

        expected = [
            TextNode("A link [site](x) and ", TextType.TEXT),
            TextNode("cat", TextType.IMAGES, "cat.png"),
        ]
        self.assertEqual(new_nodes, expected)


if __name__ == "__main__":
    unittest.main()