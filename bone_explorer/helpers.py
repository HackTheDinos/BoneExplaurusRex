# -*- coding: utf-8 -*-
"""
    bone_explorer.helpers
    ~~~~~~~~~~~~~~~~~~~~~~~~

    .doc parser for bone_explorer
"""

import subprocess


def doc_to_tokens(filename):
    """takes a .doc filename and returns the list of lines in the file"""
    unprocessed_text = subprocess.check_output(['antiword', filename])
    tokens = [
        word
        for line in unprocessed_text.split('\n')
        for word in line.split(' ')
        if line and word
    ]
    return tokens


def bigramify(tokens):
    """turns a list of tokens into bigrams"""
    return zip(tokens, tokens[1:])
