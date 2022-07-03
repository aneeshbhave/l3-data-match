#!/usr/bin/python

from pytterns import FMatcher
import getopt, sys, json

SETTINGS_FILE = "./settings.json"

def main():
    dict_path, match_path, output_file = "", "", ""         #Strings with no value

    training, is_raw = False, False                         #Booleans

    #JSON Setting Variables
    pad_str = ' '
    keep_special = False 
    
    argv = sys.argv[1:]

    try:
        opts, args = getopt.getopt(argv, "d:m:o:tr")
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
    
    #Parse settings from SETTINGS_FILE
    settings = None 
    with open(SETTINGS_FILE) as f:
        settings = json.load(f)
        pad_str = settings["pad_str"]
        keep_special = settings["keep_special"]
    print(settings)

    #!DEBUG PRINT
    print("DEBUG PRINT", dict_path, match_path, output_file, pad_str, keep_special, training, is_raw, "", sep=f"\n{'-' * 15}\n")

    mat = FMatcher(keep_special=keep_special)

    #Set STDOUT
    if output_file:
        sys.stdout = open(output_file, "w")

    #Fetching patterns
    if is_raw:
        lines = mat.__f_get_data__(dict_path, True) #Read data from file as list
        for line in lines:
            mat.patterns.add(line)
    else:
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


if __name__ == "__main__":
    main()
