from patterns import *

def main():
    #patterns = find_pat_file("./TRUTH.TXT", pad = ' ', keep_special=True, unique=True)
    patterns = find_pat_file("./Data/TRUTH.TXT", pad=' ', keep_special=True, unique=True)
    # match_pat_file("./pool", patterns, format_func, True)
    match_pat_dir("./Data/TextBlobs700/", patterns, format_func, True)

def format_func(found_pattern :str, start_idx, end_idx, file_path, found_data):
    print(f"{found_pattern} found from {start_idx} to {end_idx + 1} in {file_path}\nText : {found_data}")

if __name__ == "__main__":
    main()
