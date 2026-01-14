from textnode import TextNode, TextType
from htmlnode import LeafNode, HTMLNode, ParentNode
from delimiter import *
from blocks import *

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
        return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})

    if text_node.text_type is TextType.IMAGES:
        return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
    
    raise ValueError(f"Unsupported TextType: {text_node.text_type}")

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

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes
 
def markdown_to_html_node(markdown: str):
    blocks = markdown_to_blocks(markdown)

    block_nodes = []
    for block in blocks:
        btype = block_to_block_type(block)

        if btype == BlockType.HEADING:
            level = 0
            while level < len(block) and block[level] == "#":
                level += 1
            text = block[level:].lstrip()
            block_nodes.append(
                ParentNode(tag=f"h{level}", children=text_to_children(text))
            )

        elif btype == BlockType.PARAGRAPH:
            block_nodes.append(
                ParentNode(tag="p", children=text_to_children(block))
            )

        elif btype == BlockType.QUOTE:
            quote_lines = []
            for line in block.split("\n"):
                stripped = line.strip()
                if stripped.startswith(">"):
                    stripped = stripped[1:].lstrip()  # remove ">" then one+ spaces
                quote_lines.append(stripped)

            quote_text = "\n".join(quote_lines).strip()

            block_nodes.append(
                ParentNode("blockquote", children=text_to_children(quote_text))
            )


        elif btype == BlockType.UNORDERED_LIST:
            # each line like: "- item" or "* item"
            items = []
            for line in block.split("\n"):
                text = line[2:].strip()  # remove "- " or "* "
                items.append(ParentNode(tag="li", children=text_to_children(text)))
            block_nodes.append(ParentNode(tag="ul", children=items))

        elif btype == BlockType.ORDERED_LIST:
            # each line like: "1. item"
            items = []
            for line in block.split("\n"):
                # split only on the first "."
                _, rest = line.split(".", 1)
                text = rest.strip()
                items.append(ParentNode(tag="li", children=text_to_children(text)))
            block_nodes.append(ParentNode(tag="ol", children=items))

        elif btype == BlockType.CODE:
            # strip the surrounding triple backticks; DO NOT parse inline markdown
            lines = block.split("\n")
            # remove first and last line if they are ``` fences
            if lines and lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].endswith("```"):
                lines = lines[:-1]
            code_text = "\n".join(lines)

            code_leaf = text_node_to_html_node(TextNode(code_text, TextType.TEXT))
            code_node = ParentNode(tag="code", children=[code_leaf])
            block_nodes.append(ParentNode(tag="pre", children=[code_node]))

        else:
            # fallback: treat as paragraph
            block_nodes.append(
                ParentNode(tag="p", children=text_to_children(block))
            )

    return ParentNode(tag="div", children=block_nodes)

        
