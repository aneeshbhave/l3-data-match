#!/usr/bin/python
from pytterns import FMatcher
from datetime import datetime
import getopt, json, sys, os

#*---------------------- TODO Table ----------------------*#
#TODO:> Improve error handling
#TODO:> Add Verbose output mode
#TODO:> Write a better README.md
#*-------------------------------------------------------*#

SETTINGS_FILE = "./settings.json"

# def profiler():
#     import cProfile, pstats

#     with cProfile.Profile() as pr:
#         main()

#     stats = pstats.Stats(pr)
#     stats.sort_stats(pstats.SortKey.TIME)
#     stats.dump_stats(filename="profiling.prof")

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

    #!DEBUG PRINT
    #eprint("DEBUG PRINT", dict_path, match_path, output_file, pad_str, keep_special, training, is_raw, "", sep=f"\n{'-' * 15}\n")

    mat = FMatcher(keep_special=keep_special)

    #Set STDOUT
    if output_file:
        sys.stdout = open(output_file, "w")

    #Fetching patterns
    handle_path(dict_path)
    if is_raw:
        fetch_preproc_data(mat, dict_path)
    else:
        mat.smart_add_pat(dict_path, pad_str)

    if training:
        write_preproc_data(mat.patterns, dict_path, keep_special)
        sys.exit(0)
    
    #Matching patterns
    handle_path(match_path)
    mat.smart_match_pat(match_path, format_func)
    
    sys.stdout.close()

def eprint(data :any):
    sys.stderr.write(f"{data}\n") 

#callback function for matcher
def format_func(pattern_found, i, j, e, f):
    print(f"{f}\t{pattern_found}\t{i}\t{j}\t{e}")

#Checks if path is valid, or option is provided
def handle_path(fpath :str):
    if os.path.exists(fpath):
        return
    elif not fpath:
        eprint("Please execute the program with appropriate flags")
        sys.exit(-1)
    else:
        eprint(f"File does not exist at \"{fpath}\"")
        sys.exit(-1)

#Fetch and add preprocessed data to mat from path
def fetch_preproc_data(mat :FMatcher, path :str):
    with open(path) as f:
        data = json.load(f)
        eprint(
        f"""\
        Preprocessed patterns generated from {data["from_file"]}
        Trained on {data["train_time"]}
        Special characters are {"preserved" if data["keep_special"] else "not preserved"}\n\
        """)
        patterns = data["patterns"]
        for p in patterns:
            mat.patterns.add(p)

#Write preprocessed data to STDOUT
def write_preproc_data(data :set, fpath :str, keep_special :bool):
    json_data = {
        "from_file"    : os.path.abspath(fpath),
        "train_time"   : str(datetime.now()),
        "keep_special" : keep_special,
        "patterns"     : list(sorted(data)),
    }
    print(json.dumps(json_data, indent = 4))


if __name__ == "__main__":
    main()
    # profiler()
