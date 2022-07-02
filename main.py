#!/usr/bin/python

from pytterns import FMatcher
import getopt, sys

def main():
    dict_path, match_path, output_file = "", "", ""         #Strings with no value
    pad_str = ' '                                           #Strings with proprietary default value

    keep_special, training, is_raw = False, False, False    #Booleans
    
    argv = sys.argv[1:]

    try:
        opts, args = getopt.getopt(argv, "d:m:o:p:str")
    except getopt.GetoptError as err:
        print(err)

    #Parse options and assign to variables
    for opt, arg in opts:
        if opt in ["-d"]:
            dict_path = arg
        elif opt in ["-m"]:
            match_path = arg
        elif opt in ["-o"]:
            output_file = arg
        elif opt in ["-p"]:
            pad_str = arg
        elif opt in ["-s"]:
            keep_special = True
        elif opt in ["-t"]:
            training = True
        elif opt in ["-r"]:
            is_raw = True

    #!DEBUG PRINT
    print("DEBUG PRINT", dict_path, match_path, output_file, pad_str, keep_special, training, is_raw, "", sep=f"\n{'-' * 15}\n")

    mat = FMatcher(keep_special=keep_special)

    #Set STDOUT
    if output_file:
        sys.stdout = open(output_file, "w")

    #Fetching patterns
    mat.smart_add_pat(dict_path, pad_str)
    if training:
        for p in sorted(mat.patterns):
            print(p)
        sys.exit(0)
    
    #Matching patterns
    mat.smart_match_pat(match_path, format_func)

    
    sys.stdout.close()


def format_func(pattern_found, i, j, e, f):
    print(f"{f}\t{pattern_found}\t{i}\t{j}\t{e}")

def resolve_path(path :str):
    ...

if __name__ == "__main__":
    main()
