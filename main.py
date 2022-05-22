from pytterns import *

def main():
    mat = FMatcher(keep_special=True,
    keep_unique=True)
    
    mat.f_add_pat("./Data/TRUTH.TXT", ' ')
    mat.dir_match_pat("./Data/TextBlobs700/", format_func)

def format_func(*args):
    #print(f"{found_pattern} found from {start_idx} to {end_idx + 1} in {file_path}\nText : {found_data}")
    print(*args)

if __name__ == "__main__":
    main()
