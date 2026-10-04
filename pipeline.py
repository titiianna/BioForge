from exceptions import DataFileError

START_CODON = "AUG"
STOP_CODON = ["UAA", "UAG", "UGA"]


class Traslator:
    def __init__(self, codon_table):
        self.codon_table = codon_table

    def translator_codon(self, codon):
        codon_upper = codon.upper()
        if codon_upper in self.codon_table:
            return self.codon_table[codon_upper]
        else:
            raise DataFileError(f"codon {codon} : it is not in codon data.")