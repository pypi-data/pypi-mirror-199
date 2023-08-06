========================================
parselib - HTML parser for web scraping
========================================

.. code-block:: python

    from parselib import Parser

    html = """
        <div class="one two">
            some text
            <div>
                more text
            </div>
        </div>
    """
    parser = Parser(html)
    div = parser.find("*", {"class": "two"})
    div.text     # some text
    div.all_text # some text more text

----

find(tag, attrs={}, exclude_attrs={})
    return first matching element

find_all(tag, attrs={}, exclude_attrs={})
    return all matching elements

element.text
    text of the element

element.all_text
    text of the element and its descendants

element.children
    list of direct descendants

element.descendants
    list of all descendants

element.next_sibling

element.previous_sibling

element.parent

element.tagname

element.attrs
