========================================
parselib - HTML parser for web scraping
========================================

.. code-block:: python

    from parselib import Parser

    html = """
        <div class="class1 class2"><div>ABC<div>XYZ</div></div></div>
    """ * 5
    parser = Parser(html)
    divs = parser.find_all("div", {"class": "class1"})
    div = divs[0].find("div")
    div.text     # ABC
    div.all_text # ABC XYZ
