# -*- coding: utf-8 -*-
"""
    bone_explorer.helpers
    ~~~~~~~~~~~~~~~~~~~~~~~~

    .doc parser for bone_explorer
"""

import subprocess


def doc_to_lines(filename):
    """takes a .doc filename and returns the list of lines in the file"""
    unprocessed_text = subprocess.check_output(['antiword', filename])
    lines = [line.strip() for line in unprocessed_text.split('\n') if line]
    return lines
