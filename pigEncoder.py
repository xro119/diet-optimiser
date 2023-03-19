import re


class PigLatinEncoder:

    def __init__(self):
        """
        Inits basic vars
        """
        self.allowed_chars = r'[^a-z-A-Z\s]'
        self.vowel_ending = "ay"
        self.consonants_ending = "way"
        self.vowels = "aeiouAEIOU"
        self.consonants = "bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXZ"

    def stripp_phrase(self, phrase):
        """
        Strips any non word characters and checks if input is string.
        """
        if type(phrase) == str:
            stripped_phrase = re.sub(self.allowed_chars, '', phrase)
            return stripped_phrase
        else:
            return False

    def encode_word(self, word):
        """
        Encodes a single word to Pig Latin.
        """

        if word[0] in self.vowels or word[0] == 'Y':
            return word.capitalize() + self.vowel_ending
        else:
            consonants = ""
            for i in range(len(word)):
                if word[i] not in self.vowels:
                    consonants += word[i]
                else:
                    break
            return word[len(consonants):].capitalize() + consonants.lower() + self.consonants_ending

    def decode_word(self, word):
        """
        Gives 2 variants of decoded text from Pig Latin
        """

        if word[-len(self.consonants_ending):] == self.consonants_ending:
            word = word[-1 - len(self.consonants_ending)::-1]
            chars = ''
            decoded_word_length = len(word)
            for i in range(decoded_word_length):
                if word[i] in self.consonants:
                    chars = word[i] + chars
                else:
                    break
            return (chars + word[:len(chars) - 1:-1], word[0] + word[:0:-1])
        elif word.endswith(self.vowel_ending):
            word = word[:-len(self.vowel_ending)]
            return (word, word)

    def decode_phrase(self, phrase):
        """
        Gives 2 variants of decoded text from Pig Latin
        """
        final_phrase = ""
        final_phrase_v2 = ""
        stripped_phrase = self.stripp_phrase(phrase)
        if not stripped_phrase:
            return "Not a string! please retry using a string as input!"
        for word in stripped_phrase.split():
            final_phrase += self.decode_word(word)[0].lower() + " "
            final_phrase_v2 += self.decode_word(word)[1].lower() + " "
        return f"{final_phrase} \n{final_phrase_v2}"

    def encode_phrase(self, phrase):
        """
        Encodes a phrase into Pig Latin.
        """
        final_phrase = ""
        stripped_phrase = self.stripp_phrase(phrase)
        if not stripped_phrase:
            return "Not a string! please retry using a string as input!"
        for word in stripped_phrase.split():
            final_phrase += self.encode_word(word) + " "
        return final_phrase[:-1]


if __name__ == "__main__":
    pass
    # ph = PigLatinEncoder()
    # print(ph.encode_phrase("Th1is is, a p123HHra!@#@se with chara2cters of any kind even ygrec"))
    # print(ph.encode_phrase("We are sorry but the page you are looking for was not found.."))
    # print(ph.decode_phrase(
    #     "Ewway Areay Orrysway Utbway Ethway Agepway Ouyway Areay Ookinglway Orfway Aswway Otnway Oundfway"))
