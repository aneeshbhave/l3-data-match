from pytterns import Matcher

class EmailMatcher(Matcher):
    START = 0
    DSTART = 1
    END = 2

    def __init__(self, keep_unique, keep_special):
        state = 0
        super().__init__(keep_special=keep_special, keep_unique=keep_unique)
    
    def find_email_in(self, data :str):
        state = 0
        startidx = 0
        pat_data = self.__to_pat__(data)
        emails = [[], [], []]

        for i,c in enumerate(pat_data):
            if state == 0: #? Start
                if c == self.SPACE:
                    state += 1
                    continue
            elif state == 1: #? Post Whitespace
                if c == self.ALPHABET:
                    state += 1
                    startidx = i
                    continue
                else:
                    state = 0
                    continue
            elif state == 2: #? Post Alphabet
                if c == '@':
                    state += 1
                    continue
                if c == self.SPACE:
                    state -= 1
                    continue
            elif state == 3: #? Post @
                if c == self.ALPHABET:
                    state += 1
                    emails[self.DSTART].append(i)
                    continue
                else:
                    state = 0
                    continue
            elif state == 4: #? Post Alphabet past @
                if c == '.':
                    state += 1
                    continue
                elif c == self.SPACE:
                    state = 0
                    continue
            elif state == 5: #? Post .
                if c == self.ALPHABET:
                    state += 1
                    continue
                else:
                    state = 0
                    continue
            elif state == 6: #? Post Alphabet
                print(emails)
                if c == self.SPACE:
                    state += 1
                    emails[self.START].append(startidx)
                    emails[self.END].append(i)

                if c == self.NUMERICAL:
                    state = 0
                    continue

if __name__ == "__main__":
    mat = EmailMatcher(keep_special=True, keep_unique=True)
    data = "Aneesh's email is aneesh1701@gmail.com "
    print(data[29:])
    mat.find_email_in(data)
