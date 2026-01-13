from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block):
    lines = block.split("\n")
    if block.startswith("```\n") and block.endswith("\n```"):
        return BlockType.CODE

    if block.startswith("#"):
        i = 0
        while i < len(block) and block[i] == "#":
            i += 1

        if 1 <= i <= 6 and i < len(block) and block[i] == " ":
            return BlockType.HEADING
    
    if all(line.startswith("> ") for line in lines):
        return BlockType.QUOTE

    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    expected = 1
    is_ordered = True

    for line in lines:
        prefix = f"{expected}. "
        if not line.startswith(prefix):
            is_ordered = False
            break

        expected += 1

    if is_ordered:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
            

