from exceptions import InvalidSequenceError


class DNASequence:

    def __init__(self, sequence):
        self.sequence = sequence.upper()
        self.validate()

    def validate(self):
        for letter in self.sequence:
            if letter not in "ACGT":
                raise InvalidSequenceError(
                    "Invalid DNA sequence: " + self.sequence
                )

    def complement(self):
        result = ""

        for letter in self.sequence:
            if letter == "A":
                result += "T"
            elif letter == "T":
                result += "A"
            elif letter == "C":
                result += "G"
            elif letter == "G":
                result += "C"

        return result

    def reverse_complement(self):
        return self.complement()[::-1]

    def to_rna(self):
        result = ""

        for letter in self.sequence:
            if letter == "T":
                result += "U"
            else:
                result += letter

        return result

    def gc_content(self):
        if len(self.sequence) == 0:
            return 0

        gc_count = 0

        for letter in self.sequence:
            if letter == "G" or letter == "C":
                gc_count += 1

        return (gc_count / len(self.sequence)) * 100