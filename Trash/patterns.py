from os.path import exists
from glob import glob
import ahocorasick

ALPHABET, NUMERICAL, SPECIAL, SPACE = 'A', 'N', 'S', 'W'

#? File name, pattern name(AAASSWWWN), decoded pattern (actual value), BYTE Index

def find_pat_file(inp_path :str, pad :str = '', keep_special :bool = False, unique :bool = False,) -> list:
    if not exists(inp_path):
        return []

    patterns = []
    with open(inp_path, 'r') as inp_file:
        lines = inp_file.read().splitlines()
        for line in lines:
            patterns.append(get_pat(line, pad, keep_special))
    patterns = list(set(patterns)) if unique else patterns

    return patterns

def match_pat_dir(dir_path :str, patterns :list, format_func, keep_special = False) -> None:
    if not exists(dir_path):
        return

    paths = glob(dir_path + "/*")
    for path in paths:
        if exists(path):
            match_pat_file(path, patterns, format_func, keep_special)

def match_pat_file(inp_path :str, patterns :list, format_func, keep_special = False) -> None:
    if not exists(inp_path):
        return

    with open(inp_path) as file:
        data = file.read()
        pat_data = get_pat(data, keep_special=keep_special)

        aho = ahocorasick.Automaton()

        for idx, val in enumerate(patterns):
            aho.add_word(val, (idx, val))

        aho.make_automaton()

        for j, (idx, val) in aho.iter(pat_data):
            i = j  - len(val) + 1
            format_func(patterns[idx], i, j, inp_path, data[i:j+1])

def get_pat(inp :str, pad :str = '', keep_special = False) -> str:
    inp = pad + inp + pad
    pat = ""
    for c in inp:
        if c.isalpha():
            pat += ALPHABET
            continue
        elif c.isnumeric():
            pat += NUMERICAL
            continue
        elif c == ' ':
            pat += SPACE
            continue
        else:
            pat += c if keep_special else SPECIAL
            continue
    return pat 