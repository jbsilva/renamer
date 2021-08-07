#!/usr/bin/env python3
# -*-*- encoding: utf-8 -*-*-
# Created: Wed, 18 Jun 2014 21:52:03 +0200

"""
    Convert unicode to ascii and replace undesired characters.

     ./clean_text.py -a -s '_' -p '_' -amp '_e_' text.txt > clean_text.txt
"""

import argparse
import sys
from unidecode import unidecode


__author__ = "Julio Batista Silva"
__copyright__ = "Copyright (c) 2014-2021, Julio Batista Silva"
__license__ = "GPL v3"
__version__ = "1.0"
__email__ = "julio@juliobs.com"


def clean_text(text, ascii=True, ampersand="&", spaces="_", punctuation="_"):
    # translation table
    table = {}

    if ascii:
        text = unidecode(text)

    if ampersand != "&":
        dic = {ord("&"): ampersand}
        table.update(dic)

    if len(spaces) > 0:
        ws = " \t"
        dic = str.maketrans(ws, spaces * len(ws))
        table.update(dic)

    # Not replaced: '&' | ',' | '.' | '-'
    if len(punctuation) > 0:
        p = "/!\"#$%'()*+:;<=>?@[\\]^`{|}~"
        dic = str.maketrans(p, punctuation * len(p))
        table.update(dic)

    text = text.translate(table)

    # Remove _-_, --, .. and __
    replaces = (
        ("_-_", "-"),
        ("__", "_"),
        ("--", "-"),
        ("..", "."),
        ("._", "_"),
        ("-_", "-"),
        ("_-", "-"),
        (",_", ","),
        ("_.", "."),
    )
    for r in replaces:
        while r[0] in text:
            text = text.replace(*r)

    # Remove undesired first and last character
    while text[0] in ".-_":
        text = text[1:]
    while text[-1] in ".-_":
        text = text[:-1]

    return text


def main(args):
    with args.infile as infile:
        print(
            clean_text(
                infile.read(),
                ascii=args.to_ascii,
                ampersand=args.ampersand_replacement,
                spaces=args.space_replacement,
                punctuation=args.punctuation_replacement,
            )
        )

    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cleans text")
    parser.add_argument(
        "infile", nargs="?", type=argparse.FileType("r"), default=sys.stdin
    )
    parser.add_argument(
        "-a",
        "--to_ascii",
        action="store_true",
        help="Replace unicode with ascii",
    )
    parser.add_argument(
        "-s",
        "--space_replacement",
        default="",
        help="Replace spaces and tabs",
    )
    parser.add_argument(
        "-p",
        "--punctuation_replacement",
        default="",
        help="Character to replace punctuation",
    )
    parser.add_argument(
        "-amp",
        "--ampersand_replacement",
        default="&",
        metavar='"STRING"',
        help=("Replace '&' with string"),
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s v{__version__}"
    )
    args = parser.parse_args()

    sys.exit(main(args))
