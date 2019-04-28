#!/usr/bin/env python3
# -*-*- encoding: utf-8 -*-*-
# Created: Wed, 18 Jun 2014 21:52:03 +0200

"""
Script para renomear arquivos recursivamente, trocando espaços por underscores
e caracteres unicode por equivalentes em ascii.

./renamer -amp "_and_": Troca '&' por '_and_';
./renamer -ru: Troca unicode por ascii;
./renamer -rs: Troca espaços por underscores;
./renamer -rp: Troca pontuação por underscore;
./renamer -tt: Iniciais em maiúsculas;
./renamer -dr: Imprime comandos `mv`.
"""

import argparse
import sys
import os
import itertools
from unidecode import unidecode


__author__ = "Julio Batista Silva"
__copyright__ = "Copyright (c) 2014-2015, Julio Batista Silva"
__license__ = "GPL v3"
__version__ = "1.1"
__email__ = "julio@juliobs.com"


def main(args):
    for root, dirs, files in os.walk('./', topdown=False):
        for path in itertools.chain(files, dirs):

            name = path

            if args.ru:
                name = unidecode(name)

            # Tabela usada pelo str.translate()
            table = {ord('/'): '_'}

            if args.amp:
                dic = {ord('&'): args.amp}
                table.update(dic)

            if args.rs:
                ws = ' \t\n\r\x0b\x0c'
                dic = str.maketrans(ws, '_' * len(ws))
                table.update(dic)

            # TODO: Remove dots, but keep the last one for the extension
            # Missing: '&' | ',' | '.' | '/' | '-'
            if args.rp:
                p = '!"#$%\'()*+:;<=>?@[\\]^`{|}~'
                dic = str.maketrans(p, '_' * len(p))
                table.update(dic)

            name = name.translate(table)

            # Remove _-_, --, .. and __
            replaces = (("_-_", "-"), ("__", "_"), ("--", "-"), ("..", "."),
                        ("._", "_"), ("-_", "-"), ("_-", "-"), (",_", ","))
            for r in replaces:
                while r[0] in name:
                    name = name.replace(*r)

            # Remove undesired first and last character
            nome, ext = os.path.splitext(name)
            if nome[0] in ".-_":
                name = f"{nome[1:]}{ext}"
            if nome[-1] in ".-_":
                name = f"{nome[:-1]}{ext}"

            # Capitalize
            if args.tt:
                nome, ext = os.path.splitext(name)
                name = f"{nome[:-1].title()}{ext}"

            old = os.path.join(root, path)
            new = os.path.join(root, name)
            if not os.path.exists(new):
                if args.dr:
                    print(f'mv "{old}" "{new}"')
                else:
                    if args.verbosity == 1:
                        print(f'"{old}"')
                    elif args.verbosity > 1:
                        print(f'mv "{old}" "{new}"')
                    os.rename(old, new)
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Renomeia arquivos recursivamente')
    parser.add_argument('-ru', '--replace_unicode', dest="ru",
                        action='store_true',
                        help="Troca unicode por ascii")
    parser.add_argument('-rs', '--remove_space', dest="rs",
                        action='store_true',
                        help="Troca espaço por underscore")
    parser.add_argument('-rp', '--remove_puctuation', dest="rp",
                        action='store_true',
                        help="Troca pontuação por underscore")
    parser.add_argument('-amp', '--remove_ampersand', dest="amp",
                        metavar='\"STRING\"',
                        help=("Troca '&' por alguma string. "
                              "Eg.: -amp '_and_'."))
    parser.add_argument('-tt', '--to_title', dest="tt",
                        action='store_true',
                        help="Inicia cada palavra com maiúscula")
    parser.add_argument('-dr', '--dry_run', dest="dr",
                        action='store_true',
                        help=("Imprime os comandos que seriam executados sem "
                              "renomear nada"))
    parser.add_argument("-v", "--verbosity", action="count", default=0,
                        help="Increase output verbosity")
    parser.add_argument('--version', action='version',
                        version='%(prog)s v' + __version__)
    args = parser.parse_args()

    sys.exit(main(args))
