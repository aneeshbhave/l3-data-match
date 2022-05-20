from patterns import *

def main():
    #patterns = find_pat_file("./TRUTH.TXT", pad = ' ', keep_special=True, unique=True)
    patterns = [get_pat("9146196969")]
    match_pat_file("./numbers.txt", patterns, format_func, True)

def format_func(found_pattern :str, start_idx, end_idx, file_path, found_data):
    print(f"{found_pattern} found from {start_idx} to {end_idx + 1} in {file_path}\nText : {found_data}")

if __name__ == "__main__":
    main()