from .finder import _find_all, _find


class HTMLElement():
    def __init__(self,
                 tagname: str,
                 attrs: dict = {},
                 text: str = "",
                 all_text: str = "",
                 closed: bool = False,
                 descendants: list = [],
                 _children: list = [],
                 parent=None,
                 previous_sibling=None,
                 next_sibling=None
                 ):
        self.tagname = tagname
        self.attrs = attrs
        self.text = text
        self.all_text = all_text
        self.closed = closed
        self.descendants = descendants
        self._children = _children
        self.parent = parent
        self.previous_sibling = previous_sibling
        self.next_sibling = next_sibling

    def __repr__(self) -> str:
        return f"{self.tagname.upper()} attrs={self.attrs} text={self.text}"

    def find_all(self, *args) -> list:
        return _find_all(self.descendants, *args)

    def find(self, *args):
        return _find(self.descendants, *args)

    @property
    def children(self) -> list:
        self._children.reverse()
        return self._children
