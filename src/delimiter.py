from textnode import *
from extract import extract_markdown_images, extract_markdown_links
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []
    for old_node in old_nodes:
        if old_node.text_type is not TextType.TEXT:
            result.append(old_node)
            continue
        if delimiter not in old_node.text:
            raise ValueError("delimiter not found")
        d = re.escape(delimiter)
        text_list = re.split(fr"({d}(?:(?!{d}).)*{d})", old_node.text)
    
        for text in text_list:
            if text.startswith(delimiter) and text.endswith(delimiter):
                new_node = TextNode(text[len(delimiter):(len(delimiter) * -1)], text_type)
                result.append(new_node)
            else:
                new_node = TextNode(text, TextType.TEXT)
                result.append(new_node)
    return result

def split_nodes_link(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        text = old_node.text
        links = extract_markdown_links(text)

        if not links:
            new_nodes.append(old_node)
            continue

        for anchor, url in links:
            markdown = f"[{anchor}]({url})"
            parts = text.split(markdown, 1)
            before = parts[0]
            if len(parts) != 2:
                raise Exception("Sorry, an error occurred")
            after = parts[1]

            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))
        
            new_nodes.append(TextNode(anchor, TextType.LINKS, url))

            text = after
        
        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        text = old_node.text
        images = extract_markdown_images(text)

        if not images:
            new_nodes.append(old_node)
            continue

        for alt, url in images:
            markdown = f"![{alt}]({url})"
            parts = text.split(markdown, 1)
            before = parts[0]

            if len(parts) != 2:
                raise Exception("Sorry, an error occurred")
            after = parts[1]

            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))
        
            new_nodes.append(TextNode(alt, TextType.IMAGES, url))

            text = after
        
        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes
        

   
            
        