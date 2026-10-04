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

    def translate(self, rna_sequence):
        protein = []
        sequence_len = len(rna_sequence)

        while index + 3 <= sequence_len:
            codon = rna_sequence[index : index + 3].upper()

            if codon in STOP_CODON:
                break

            amino_acid = self.translator_codon(codon)
            protein.append(amino_acid)

            index += 3

        return "".join(protein) 