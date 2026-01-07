from enum import Enum


_MISSING = object()

class LeafTag(Enum):
    TEXT = None
    BOLD = "b"
    ITALIC = "i"
    CODE = "code"
    LINK = "a"
    IMAGE = "img"
    PARAGRAPH = "p"

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("not implemented")

    def props_to_html(self):
        if self.props == None:
            return ""

        parts = []
        for key, value in self.props.items():
            parts.append(f'{key}="{value}"')
        text = " ".join(parts)
        return text

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)

        if tag is _MISSING:
            raise TypeError("tag is required (can be None)")

        self.tag = tag
        self.value = value
        self.props = props

    def to_html(self):

        if self.value is None:
            raise ValueError("Node has no value")

        if self.tag is None:
            return self.value
        
        if self.tag == "a":
            attrs = ""
            if self.props:
                parts = [f'{k}="{v}"' for k, v in self.props.items()]
                attrs = " " + " ".join(parts)
            
            return f'<{self.tag}{attrs}>{self.value}</{self.tag}>'
        
        if self.tag == "img":
            attrs = ""
            parts = []

            for k, v in self.props.items():
                parts.append(f'{k}="{v}"')
            
            attrs = " " + " ".join(parts) if parts else ""

            return f'<{self.tag}{attrs}>'

        else:
            return f"<{self.tag}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, value, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)

        self.tag = tag
        self.children = children
        self.props = props

    def to_html(self):

        if self.tag is None:
            raise ValueError("Node has no tag")

        if self.children is None:
            raise ValueError("Node has no children")

        opening_tag = f"<{self.tag}>"
        closing_tag = f"</{self.tag}>"

        for child in children:
            opening_tag += child.to_html()
        
        return opening_tag + closing_tag
        
            

        