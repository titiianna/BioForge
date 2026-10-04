from models import ORF
from exceptions import DataFileError

START_CODON = "AUG"
STOP_SYMBOL = "*"

class Pipeline:
    def __init__(self, codon_table, filters):
        self.codon_table = codon_table
        self.filters = filters
        self.counter = 1

    def _translate_codon(self, codon):
        try:
            return self.codon_table[codon]
        except KeyError:
            raise DataFileError(f"Codon {codon}: is not in codon dara.")

    def find_orfs(self, dna_obj, strand_name):
        if strand_name == "Forward":
            rna = dna_obj.dna_to_rna()
        else:
            rna = dna_obj.reverse_complement().replace("T", "U")

        found_orfs = []
        rna_len = len(rna)

        for frame in [0,1,2]:
            i = frame
            while i + 3 <= rna_len:
                if rna[i:i + 3] != START_CODON:
                    i += 3
                    continue

                protein = []
                is_complete = False
                j = i
                while j + 3 <= rna_len:
                    aa = self._translate_codon(rna[j:j + 3])
                    if aa == STOP_SYMBOL:
                        is_complete = True
                        break
                    protein.append(aa)
                    j += 3

                if strand_name == "Forward":
                    start_pos = i + 1
                else:
                    start_pos = rna_len - i
                protein = "".join(protein)
                found_orfs.append(
                    ORF(None, protein, strand_name, frame, start_pos, is_complete)
                )

                if not is_complete:
                    break
                i = j + 3

        return found_orfs

    def _passes_filters(self, orf):
        pass_all = True
        for f in self.filters:
            if f.filter(orf) == False:
                pass_all = False
                break
        return pass_all

    def process(self, dna_obj):
        all_orfs = self.find_orfs(dna_obj, "Forward") + self.find_orfs(dna_obj, "Reverse")
        final_orfs = []
        for orf in all_orfs:
            if self._passes_filters(orf):
                final_orfs.append(orf)
        for orf in final_orfs:
            orf.annotation_id = f"BFG_{self.counter:03d}"
            self.counter += 1

        return final_orfs