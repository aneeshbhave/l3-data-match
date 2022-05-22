import ahocorasick
from os.path import exists

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

    def add_pat(self, inp :str, pad :str ='') -> None:
        self.patterns.append(self.__to_pat__(pad + inp + pad))

    def match_pat(self, haystack :str, callback_func :str) -> None:
        if not len(self.patterns):
            return

        if callable(callback_func):
            raise TypeError("Hello")

        pat_haystack = self.__to_pat__(haystack)

        aho = ahocorasick.Automaton()

        for idx, val in enumerate(self.patterns):
            aho.add_word(val, (idx, val))
        
        aho.make_automaton()

        for j, (idx, val) in aho.iter(pat_haystack):
            i = j - len(val) + 1
            callback_func(self.patterns[idx], i, j, haystack[i:j+1])

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

class FMatcher(Matcher):
    def __init__(self, *, keep_special :bool, keep_unique :bool):
        super().__init__(
            keep_special=keep_special,
            keep_unique=keep_unique
            )
    
    def f_add_patts(self, inp_path :str, pad :str = '') -> None:
        if not exists(inp_path):
            raise #TODO

        with open(inp_path) as file:
            lines = file.read().splitlines()
            for line in lines:
                self.add_pat(line, pad)
            
        self.patterns = list(set(self.patterns)) if self.keep_unique else self.patterns
    
    def f_match_pat(self, ):
        ...

if __name__ == "__main__":
    print("This is a module, import it in your own script and run it!")
    mat = Matcher(
        keep_special=True,
        keep_unique=True
    )
    mat.add_pat("Aneesh")
    mat.add_pat("aneesh1701")
    print(mat)