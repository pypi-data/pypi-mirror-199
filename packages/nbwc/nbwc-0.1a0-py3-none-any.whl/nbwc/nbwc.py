#!/usr/bin/env python

import io
from tokenize import generate_tokens, COMMENT
from argparse import ArgumentParser, RawDescriptionHelpFormatter

from nltk.tokenize import RegexpTokenizer
import jupytext


def get_comments(code):
    code_io = io.StringIO(code)
    comments = []
    for toktype, tok, start, end, line in generate_tokens(code_io.readline):
        # we can also use token.tok_name[toktype] instead of 'COMMENT'
        # from the token module 
        if toktype == COMMENT:
            comments.append(tok)
    return '\n'.join(comments)


def wc_nb(fname, types=('markdown',)):
    nb = jupytext.read(fname)
    tokenizer = RegexpTokenizer(r'\w+')
    word_counts = 0
    for cell in nb['cells']:
        if cell['cell_type'] not in types:
            continue
        source = cell['source']
        if cell['cell_type'] == 'code':
            source = get_comments(source)
        tokens = tokenizer.tokenize(source)
        word_counts += len(tokens)
    return word_counts


def get_parser():
    parser = ArgumentParser(description=__doc__,  # Usage from docstring
                            formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument('nb_fname',
                        help='Notebook filename')
    parser.add_argument('--code', action='store_true',
                        help='Count words in code comments')
    parser.add_argument('--raw', action='store_true',
                        help='Count words in raw cells')
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()
    types = ['markdown']
    if args.code:
        types.append('code')
    if args.raw:
        types.append('raw')
    print(f'Wordcount for {args.nb_fname}:', wc_nb(args.nb_fname, types))


if __name__ == '__main__':
    main()
