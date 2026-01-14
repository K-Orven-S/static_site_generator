import os
from pathlib import Path

from converter import *
from htmlnode import *


def extract_title(markdown: str) -> str:
    for line in markdown.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
    raise Exception("No H1 header found in markdown")


def generate_page(from_path: str, template_path: str, dest_path: str, basepath: str = "/") -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r", encoding="utf-8") as f:
        markdown = f.read()

    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    html_node = markdown_to_html_node(markdown)
    content_html = html_node.to_html()
    title = extract_title(markdown)

    full_html = template.replace("{{ Title }}", title).replace("{{ Content }}", content_html)

    full_html = full_html.replace('href="/', f'href="{basepath}')
    full_html = full_html.replace('src="/', f'src="{basepath}')

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(full_html)


def generate_pages_recursive(
    dir_path_content: str,
    template_path: str,
    dest_dir_path: str,
    basepath: str = "/",
    content_root: str | None = None,
) -> None:
    if content_root is None:
        content_root = dir_path_content

    for entry in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, entry)

        if os.path.isdir(from_path):
            generate_pages_recursive(from_path, template_path, dest_dir_path, basepath, content_root)
            continue

        if not entry.endswith(".md"):
            continue

        rel_md_path = os.path.relpath(from_path, content_root)      # e.g. contact.md
        rel_no_ext = os.path.splitext(rel_md_path)[0]              # e.g. contact

        if rel_no_ext.endswith("index"):
            # content/index.md -> docs/index.html
            dest_path = os.path.join(dest_dir_path, rel_no_ext + ".html")
            generate_page(from_path, template_path, dest_path, basepath)
        else:
            # 1) content/contact.md -> docs/contact/index.html
            dest_index = os.path.join(dest_dir_path, rel_no_ext, "index.html")
            generate_page(from_path, template_path, dest_index, basepath)

            # 2) ALSO write a no-extension file so /contact works
            dest_no_ext = os.path.join(dest_dir_path, rel_no_ext)
            generate_page(from_path, template_path, dest_no_ext, basepath)

