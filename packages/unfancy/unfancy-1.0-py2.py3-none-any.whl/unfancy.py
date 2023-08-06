#!/usr/bin/env python3
# Translate fancy text to regular text
# SPDX-FileCopyrightText: 2023 Ngô Ngọc Đức Huy <huyngo@disroot.org>
#
# SPDX-License-Identifier: MPL-2.0

import argparse
from typing import Dict, Optional, Tuple

__version__ = "1.0"


def create_alphabet_map(
    a: str, tag: str, upper: bool = True
) -> Dict[str, Tuple[str, str]]:
    """Take the first letter and create a map from fancy to regular alphabet.

    >>> alphabet_map = create_alphabet_map("𝐚", "mathematical bold", False)
    >>> alphabet_map["𝐚"]
    ('a', 'mathematical bold')
    >>> alphabet_map["𝐳"]
    ('z', 'mathematical bold')
    >>> alphabet_map = create_alphabet_map("𝐀", "mathematical bold")
    >>> alphabet_map["𝐀"]
    ('A', 'mathematical bold')
    >>> alphabet_map["𝐙"]
    ('Z', 'mathematical bold')
    >>> len(alphabet_map)
    26
    """
    standard_a = "a"
    if upper:
        standard_a = "A"
    return {chr(ord(a) + i): (chr(ord(standard_a) + i), tag)
            for i in range(26)}


def create_numeric_map(
    start: int, end: int, char: str, tag: str
) ->  Dict[str, Tuple[str, str]]:
    """Create map from fancy numeric characters to regular ones.

    Both ``start`` and ``end`` are inclusive.

    >>> numeric_map = create_numeric_map(1, 20, "①", "circled")
    >>> len(numeric_map)
    20
    >>> numeric_map["⑫"]
    ('12', 'circled')
    """
    return {chr(ord(char) + num - start): (str(num), tag) for num in range(start, end + 1)}


def create_multi_alphabet_map() -> Dict[str, Tuple[str, str]]:
    """Create all alphabet maps.  Supported alphabets are:

    * `Mathematical alphanumeric symbols <https://en.wikipedia.org/wiki/Mathematical_Alphanumeric_Symbols>`_
    * `Enclosed Alphanumerics <https://en.wikipedia.org/wiki/Enclosed_Alphanumerics>`_
    * `Enclosed Alphanumeric Supplement <https://en.wikipedia.org/wiki/Enclosed_Alphanumeric_Supplement>`_
    """
    character_map = dict()
    # Mathematical alphanumeric symbols
    character_map.update(create_alphabet_map("𝐀", "mathematical bold"))
    character_map.update(create_alphabet_map("𝐚", "mathematical bold", False))
    character_map.update(create_alphabet_map("𝐴", "mathematical italic"))
    character_map.update(create_alphabet_map("𝑎", "mathematical italic", False))
    character_map.update(create_alphabet_map("𝑨", "mathematical bold italic"))
    character_map.update(create_alphabet_map("𝒂", "mathematical bold italic", False))
    character_map.update(create_alphabet_map("𝖠", "mathematical san-serif"))
    character_map.update(create_alphabet_map("𝖺", "mathematical san-serif", False))
    character_map.update(create_alphabet_map("𝗔", "mathematical san-serif bold"))
    character_map.update(create_alphabet_map("𝗮", "mathematical san-serif bold", False))
    character_map.update(create_alphabet_map("𝘈", "mathematical san-serif italic"))
    character_map.update(create_alphabet_map("𝘢", "mathematical san-serif italic", False))
    character_map.update(create_alphabet_map("𝘼", "mathematical san-serif bold italic"))
    character_map.update(create_alphabet_map("𝙖", "mathematical san-serif bold italic", False))
    character_map.update(create_alphabet_map("𝒜", "mathematical script"))
    character_map.update(create_alphabet_map("𝒶", "mathematical script", False))
    character_map.update(create_alphabet_map("𝓐", "mathematical script bold"))
    character_map.update(create_alphabet_map("𝓪", "mathematical script bold", False))
    character_map.update(create_alphabet_map("𝔄", "mathematical fraktur"))
    character_map.update(create_alphabet_map("𝔞", "mathematical fraktur", False))
    character_map.update(create_alphabet_map("𝕬", "mathematical fraktur bold"))
    character_map.update(create_alphabet_map("𝖆", "mathematical fraktur bold", False))
    character_map.update(create_alphabet_map("𝙰", "mathematical monospace"))
    character_map.update(create_alphabet_map("𝚊", "mathematical monospace", False))
    character_map.update(create_alphabet_map("𝔸", "mathematical double-struck"))
    character_map.update(create_alphabet_map("𝕒", "mathematical double-struck", False))
    character_map.update(create_numeric_map(0, 9, "𝟎", "bold"))
    character_map.update(create_numeric_map(0, 9, "𝟘", "double-struck"))
    character_map.update(create_numeric_map(0, 9, "𝟢", "sans-serif"))
    character_map.update(create_numeric_map(0, 9, "𝟬", "sans-serif bold"))
    character_map.update(create_numeric_map(0, 9, "𝟶", "monospace"))
    # Enclosed alphanumerics
    character_map.update(create_numeric_map(0, 0, "⓪", "circled"))
    character_map.update(create_numeric_map(1, 20, "①", "circled"))
    character_map.update(create_numeric_map(1, 20, "⑴", "parenthesized"))
    character_map.update(create_numeric_map(1, 20, "⒈", "full stop"))
    character_map.update(create_alphabet_map("⒜", "parenthesized", False))
    character_map.update(create_alphabet_map("Ⓐ", "circled"))
    character_map.update(create_alphabet_map("ⓐ", "circled", False))
    character_map.update(create_numeric_map(0, 0, "⓿", "negative circled"))
    character_map.update(create_numeric_map(11, 20, "⓫", "negative circled"))
    character_map.update(create_numeric_map(1, 10, "⓵", "double circled"))
    # Enclosed alphanumeric supplement
    character_map.update(create_numeric_map(0, 0, "🄀", "full stop"))
    character_map.update(create_numeric_map(0, 9, "🄁", "comma"))
    character_map.update(create_numeric_map(0, 0, "🄋", "dingbat circled sans-serif"))
    character_map.update(create_numeric_map(0, 0, "🄌", "dingbat negative circled sans-serif"))
    character_map.update(create_numeric_map(0, 0, "🄍", "circled"))  # "with slash" is not informative here
    character_map.update(create_alphabet_map("🄐", "parenthesized"))
    character_map.update(create_alphabet_map("🄰", "squared"))
    character_map.update(create_alphabet_map("🅐", "negative circled"))
    character_map.update(create_alphabet_map("🅰", "negative squared"))

    return character_map


def translate_text(
    fancy_text: str, alphabet_map: Optional[Dict[str, Tuple[str, str]]] = None
) -> Tuple[str, str]:
    """Translate fancy text to regular text, with a tag.

    >>> fancy_text = "𝐓𝐡𝐞 𝐪𝐮𝐢𝐜𝐤 𝐛𝐫𝐨𝐰𝐧 𝐟𝐨𝐱 𝐣𝐮𝐦𝐩𝐬 𝐨𝐯𝐞𝐫 𝐭𝐡𝐞 𝐥𝐚𝐳𝐲 𝐝𝐨𝐠"
    >>> unfancy_text, label = translate_text(fancy_text)
    >>> unfancy_text
    'The quick brown fox jumps over the lazy dog'
    >>> label
    'mathematical bold'

    Similarly styled alphanumeric characters are considered the same
    even when they're not continuous on unicode block.

    >>> fancy_text = "Ⓘ ⓗⓐⓥⓔ ①⓪② ⓐⓟⓟⓛⓔⓢ"
    >>> unfancy_text, label = translate_text(fancy_text)
    >>> unfancy_text
    'I have 102 apples'
    >>> label
    'circled'

    If two or more alphabets are used, the label will be 'mixed'

    >>> fancy_text = "𝐓𝐡𝐞 𝖖𝖚𝖎𝖈𝖐 𝖇𝖗𝖔𝖜𝖓 𝖋𝖔𝖝 𝐣𝐮𝐦𝐩𝐬 𝐨𝐯𝐞𝐫 𝐭𝐡𝐞 𝐥𝐚𝐳𝐲 𝐝𝐨𝐠"
    >>> unfancy_text, label = translate_text(fancy_text)
    >>> unfancy_text
    'The quick brown fox jumps over the lazy dog'
    >>> label
    'mixed'
    """
    if alphabet_map is None:
        alphabet_map = create_multi_alphabet_map()
    translator = str.maketrans({k: v[0] for k, v in alphabet_map.items()})
    character_sets = set(map(lambda c: alphabet_map[c][1] if c in alphabet_map else None, fancy_text))
    if None in character_sets:
        character_sets.remove(None)

    label = "mixed"
    if len(character_sets) == 1:
        label = list(character_sets)[0]
    return fancy_text.translate(translator), label


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Translate fancy to regular text.")
    parser.add_argument("--test", type=bool, help="Run doctest")
    parser.add_argument("--verbose", type=bool, help="Run verbose mode (for tests)")
    args = parser.parse_args()
    if args.test:
        import doctest
        failure, total = doctest.testmod(verbose=args.verbose)
        print(f"{total - failure}/{total} tests passed")
    else:
        alphabet_map = create_multi_alphabet_map()
        print("Press Ctrl+C or Ctrl+D to exit")
        try:
            while True:
                fancy_text = input()
                unfancy_text, label = translate_text(fancy_text, alphabet_map)
                print("Fancy type:", label)
                print(unfancy_text)
        except (EOFError, KeyboardInterrupt):
            print("Bye")
