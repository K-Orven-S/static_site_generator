import os
import shutil

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
            os.mkdir(dest_path)
            copy_directory_recursive(src_path, dest_path)


def copy_static_to_public(static_dir: str = "static", public_dir: str = "public") -> None:
    if not os.path.exists(static_dir):
        raise FileNotFoundError(f"Source directory does not exist: {static_dir}")

    if os.path.exists(public_dir):
        print(f"Deleting existing directory: {public_dir}")
        shutil.rmtree(public_dir)

    print(f"Creating directory: {public_dir}")
    os.mkdir(public_dir)

    copy_directory_recursive(static_dir, public_dir)


def main():
    copy_static_to_public("static", "public")
    generate_pages_recursive("content", "template.html", "public")


if __name__ == "__main__":
    main()