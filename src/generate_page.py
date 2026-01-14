import os
from pathlib import Path

from converter import *
from htmlnode import *


def extract_title(markdown: str) -> str:
    """
    Return the text of the first H1 header in the markdown.

    H1 header is a line that starts with exactly one '# ' (single hash + space).
    Example: "# Hello" -> "Hello"

    Raises:
        Exception: if no H1 header is found.
    """
    for line in markdown.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):  # single # and a space
            return stripped[2:].strip()

    raise Exception("No H1 header found in markdown")


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(
        f"Generating page from {from_path} to {dest_path} using {template_path}"
    )

    # read markdown
    with open(from_path, "r", encoding="utf-8") as f:
        markdown = f.read()

    # read template
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    # convert markdown -> html
    html_node = markdown_to_html_node(markdown)
    content_html = html_node.to_html()

    # title
    title = extract_title(markdown)

    # replace placeholders
    full_html = template.replace("{{ Title }}", title).replace("{{ Content }}", content_html)

    # ensure dest directory exists
    dest_dir = os.path.dirname(dest_path)
    if dest_dir != "":
        os.makedirs(dest_dir, exist_ok=True)

    # write output
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(full_html)

def generate_pages_recursive(
    dir_path_content: str,
    template_path: str,
    dest_dir_path: str,
    content_root: str | None = None,
) -> None:
    """
    Recursively crawl dir_path_content and generate an HTML page for every .md file.
    Output goes into dest_dir_path with the same directory structure as content_root.

    Example:
      content/blog/tom.md -> public/blog/tom.html
    """
    if content_root is None:
        content_root = dir_path_content

    for entry in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, entry)

        # recurse into subdirectories
        if os.path.isdir(from_path):
            generate_pages_recursive(from_path, template_path, dest_dir_path, content_root)
            continue

        # only markdown files
        if not entry.endswith(".md"):
            continue

        # relative path from content root (stable even in recursion)
        rel_md_path = os.path.relpath(from_path, content_root)

        # change .md -> .html
        rel_html_path = os.path.splitext(rel_md_path)[0] + ".html"

        dest_path = os.path.join(dest_dir_path, rel_html_path)

        generate_page(from_path, template_path, dest_path)

