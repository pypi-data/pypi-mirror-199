# example.py

from functools import partial
from typing import Optional

from pyselector import Menu
from pyselector.key_manager import Keybind

items = [
    {"name": "item0", "date": "2022-02-10", "category": "A"},
    {"name": "item1", "date": "2022-03-20", "category": "A"},
    {"name": "item2", "date": "2022-03-19", "category": "B"},
    {"name": "item3", "date": "2022-03-18", "category": "A"},
    {"name": "item4", "date": "2022-03-21", "category": "C"},
    {"name": "item5", "date": "2022-03-20", "category": "B"},
]


def sort_by_key(key: str, items: list[dict[str, str]]) -> list[dict[str, str]]:
    return sorted(items, key=lambda x: x[key])


def parse_selection(menu: Menu, keycode: int, **kwargs) -> Optional[Keybind]:
    for key in menu.keybind.list_registered:
        if key.code == keycode:
            return key
    return None


def main() -> int:
    Menu.logging_debug(True)
    menu = Menu.rofi()

    menu.keybind.add(
        key="alt-r",
        description="sort by date",
        callback=lambda: "date",
    )
    menu.keybind.add(
        key="alt-t",
        description="sort by category",
        callback=lambda: "category",
    )
    menu.keybind.add(
        key="alt-n",
        description="sort by name",
        callback=lambda: "name",
    )

    prompt = partial(menu.prompt, prompt="Example>", width="40%", height="40%")

    item, keycode = prompt(items=items)

    keybind = parse_selection(menu, keycode, item=item)
    sorted_items = sort_by_key(keybind.callback(), items=items)

    selected, keycode = prompt(items=sorted_items)

    print("Selected:::", selected)
    return 0


if __name__ == "__main__":
    main()
