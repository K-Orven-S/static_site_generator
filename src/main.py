import os
import shutil
import sys

from generate_page import *


def copy_directory_recursive(src_dir: str, dest_dir: str) -> None:
    for entry in os.listdir(src_dir):
        src_path = os.path.join(src_dir, entry)
        dest_path = os.path.join(dest_dir, entry)

        if os.path.isfile(src_path):
            print(f"Copying file: {src_path} -> {dest_path}")
            shutil.copy(src_path, dest_path)
        else:
            print(f"Creating directory: {dest_path}")
            os.makedirs(dest_path, exist_ok=True)
            copy_directory_recursive(src_path, dest_path)


def copy_static_to_dest(static_dir: str, dest_dir: str) -> None:
    if not os.path.exists(static_dir):
        raise FileNotFoundError(f"Source directory does not exist: {static_dir}")

    if os.path.exists(dest_dir):
        print(f"Deleting existing directory: {dest_dir}")
        shutil.rmtree(dest_dir)

    print(f"Creating directory: {dest_dir}")
    os.makedirs(dest_dir, exist_ok=True)

    copy_directory_recursive(static_dir, dest_dir)


def main():
    # basepath from CLI: default "/"
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    # normalize basepath to always start and end with "/"
    if not basepath.startswith("/"):
        basepath = "/" + basepath
    if not basepath.endswith("/"):
        basepath = basepath + "/"

    output_dir = "docs"

    copy_static_to_dest("static", output_dir)

    generate_pages_recursive(
        dir_path_content="content",
        template_path="template.html",
        dest_dir_path=output_dir,
        basepath=basepath,
    )


if __name__ == "__main__":
    main()