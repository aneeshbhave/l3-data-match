import ahocorasick
from os import listdir
from os.path import isdir, isfile, join

#TODO Add Comments
#TODO Add DocStrings

class Matcher:
    patterns :list
    keep_special :bool
    keep_unique :bool

    ALPHABET = 'A'
    NUMERICAL = 'N'
    SPACE = 'W'
    SPECIAL = 'S'

    def __init__(self, *, keep_special :bool, keep_unique :bool):
        self.patterns = []
        self.keep_special = keep_special
        self.keep_unique = keep_unique

    def __repr__(self):
        return str(self.patterns)

    def add_pat(self, inp :str, pad :str = '') -> None:
        self.patterns.append(self.__to_pat__(pad + inp + pad))

    def match_pat(self, haystack :str, callback_func, file_name) -> None:
        if not len(self.patterns):
            return

        if not callable(callback_func):
            raise TypeError("callback_func must be a callable function.")

        pat_haystack = self.__to_pat__(haystack)
        aho = ahocorasick.Automaton()

        for idx, val in enumerate(self.patterns):
            aho.add_word(val, (idx, val))
        
        aho.make_automaton()

        for j, (idx, val) in aho.iter(pat_haystack):
            j += 1
            i = j - len(val)
            callback_func(self.patterns[idx], i, j, haystack[i:j], {file_name})

    def __to_pat__(self, inp :str) -> str:
        pat = ""
        for c in inp:
            if c.isalpha():
                pat += self.ALPHABET
                continue
            elif c.isnumeric():
                pat += self.NUMERICAL
                continue
            elif c == ' ':
                pat += self.SPACE
                continue
            else:
                pat += c if self.keep_special else self.SPECIAL
                continue
        return pat
    
    def __rm_duplicates__(self):
        self.patterns = list(set(self.patterns))


class FMatcher(Matcher):
    def __init__(self, *, keep_special :bool, keep_unique :bool):
        super().__init__(
            keep_special=keep_special,
            keep_unique=keep_unique
            )
    
    def f_add_pat(self, f_path :str, pad :str = '') -> None:
        """Hello world"""
        lines = self.__f_get_data__(f_path, True)
        for line in lines:
            self.add_pat(line, pad)

        if self.keep_unique:
            self.__rm_duplicates__()
    
    def dir_add_pat(self, dir_path :str, pad :str = '') -> None:
        files = self.__dir_ls__(dir_path)

        for file in files:
            self.f_add_pat(file, pad)
    
    def f_match_pat(self, f_path :str, callback_func) -> None:
        data = self.__f_get_data__(f_path, False)

        self.match_pat(data, callback_func, f_path)
    
    def dir_match_pat(self, dir_path :str, callback_func) -> None:
        files = self.__dir_ls__(dir_path)
        
        for file in files:
            self.f_match_pat(file, callback_func)

    def __f_get_data__(self, f_path :str, split :bool) -> list or str:
        if not isfile(f_path):
            raise OSError(f"Could not open file at \'{f_path}\'.")
        with open(f_path) as file:
            return file.read().splitlines() if split else file.read()
    
    def __dir_ls__(self, dir_path :str) -> list:
        if not isdir(dir_path):
            raise OSError(f"\'{dir_path}\' is not a valid directory.")
        return [join(dir_path, f) for f in listdir(dir_path) if isfile(join(dir_path, f))]

if __name__ == "__main__":
    print("This is a module, import it in your own script and run it!")
    exit(-1)