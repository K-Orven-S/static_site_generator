from textnode import TextNode, TextType
from htmlnode import LeafNode
from delimiter import *

def text_node_to_html_node(text_node):

    if text_node.text_type is TextType.TEXT:
        return LeafNode(tag=None, value=text_node.text)
    
    if text_node.text_type is TextType.BOLD:
        return LeafNode(tag="b", value=text_node.text)
    
    if text_node.text_type is TextType.ITALIC:
        return LeafNode(tag="i", value=text_node.text)
    
    if text_node.text_type is TextType.CODE:
        return LeafNode(tag="code", value=text_node.text)

    if text_node.text_type is TextType.LINKS:
        return LeafNode(tag="a", value=text_node.text, props={"href": "https://www.google.com"})

    if text_node.text_type is TextType.IMAGES:
        return LeafNode(tag="img", value="", props={"src": "https://example.com/img.png", "alt": "Alt text"})

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]

    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC) 
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)


    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    cleaned_blocks = []
    for block in blocks:
        stripped = block.strip()
        if len(stripped) == 0:
            continue
        cleaned_blocks.append(stripped)
    
    return cleaned_blocks
 
