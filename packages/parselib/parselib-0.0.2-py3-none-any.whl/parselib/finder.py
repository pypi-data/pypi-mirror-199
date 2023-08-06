def _find_all(elements: list, tag: str, attrs: dict = {}, exclude_attrs: dict = {}) -> list:
    results = []
    for el in elements:
        if el.tagname != tag:
            continue
        if exclude_attrs and _should_exclude(el.attrs, exclude_attrs):
            continue
        if not attrs:
            results.append(el)
            continue
        if _should_include(el.attrs, attrs):
            results.append(el)
    return results


def _find(elements: list, tag: str, attrs: dict = {}, exclude_attrs: dict = {}):
    for el in elements:
        if el.tagname != tag:
            continue
        if exclude_attrs and _should_exclude(el.attrs, exclude_attrs):
            continue
        if not attrs:
            return el
        if _should_include(el.attrs, attrs):
            return el
    return None


def _should_exclude(dict: dict, attrs: dict):
    dict_classes = dict.get("class").split(" ")
    attrs_classes = attrs.get("class").split(" ")
    for cls in attrs_classes:
        if cls in dict_classes:
            return True
    dict.pop("class")
    attrs.pop("class")
    for k, v in attrs.items():
        if dict.get(k) and dict.get(k) == v:
            return True
    return False


def _should_include(dict: dict, attrs: dict):
    dict_classes = dict.get("class").split(" ")
    attrs_classes = attrs.get("class").split(" ")
    for cls in attrs_classes:
        if cls not in dict_classes:
            return False
    dict.pop("class")
    attrs.pop("class")
    for k, v in attrs.items():
        if not dict.get(k) or dict.get(k) != v:
            return False
    return True
