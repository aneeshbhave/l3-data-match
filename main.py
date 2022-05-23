from pytterns import *

def main():
    mat = FMatcher(
        keep_special=True,
        keep_unique=True
        )

    mat.f_add_pat("./Data/TRUTH.TXT", pad=' ')
    #mat.f_add_pat("./Data/TRUTH.TXT")
    print(mat.patterns)
    mat.dir_match_pat("./Data/TextBlobs3000/", format_func)

def format_func(pattern_found, i, j, e, f):
    print(f"{f}\t{pattern_found}\t{i}\t{j}\t{e}")

if __name__ == "__main__":
    main()
