#!/usr/bin/env python3
# -*-*- encoding: utf-8 -*-*-
# Created: Wed, 18 Jun 2014 21:52:03 +0200

"""
Script para renomear arquivos recursivamente, trocando espaços por underscores
e caracteres unicode por equivalentes em ascii.
"""
__author__ = "Julio Batista Silva"
__copyright__ = ""
__license__ = "GPL v3"
__version__ = "1.0"

import argparse
import sys
import os
import itertools
from unidecode import unidecode


def main(rs, rp):
    for root, dirs, files in os.walk('./', topdown=False):
        for path in itertools.chain(files, dirs):

            dict = str.maketrans("/", "_")
            if rs:
                dict[ord(' ')] = ord('_')
            if rp:
                dict[ord('[')] = dict[ord(']')] = dict[ord(':')] = dict[ord('?')] = dict[ord('!')] = dict[ord('"')] = ord('_')
            name = unidecode(path).translate(dict)

            old = os.path.join(root, path)
            new = os.path.join(root, name)
            if not os.path.exists(new):
                os.rename(old, new)
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Renomeia arquivos recursivamente')
    parser.add_argument('-rs', '--remove_space', dest="rs",
                        action='store_true',
                        help='Troca espaço por underscore.')
    parser.add_argument('-rp', '--remove_puctuation', dest="rp",
                        action='store_true',
                        help='Troca pontuação por underscore.')
    args = parser.parse_args()

    sys.exit(main(args.rs))
