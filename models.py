from exceptions import InvalidSequenceError
from exceptions import DataFileError
from pathlib import Path

class DNASequence:

    def __init__(self, sequence):
        self.sequence = sequence.upper().strip()
        self.validate()

    def validate(self):
        if self.sequence == "":
            raise InvalidSequenceError(f"Empty sequence: {self.sequence_id}")
        for letter in self.sequence:
            if letter not in "ACGT":
                raise InvalidSequenceError(
                    f"Invalid DNA sequence: {self.sequence}"
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

class DataDirLoad:
    @staticmethod
    def load_codon_table(ct_path):
        ct_full_path = Path.cwd() / ct_path 
        if not ct_full_path.is_file():
            raise DataFileError(f"wrong codon_table directory: {ct_full_path} ")
        codon_table = {}
        with open(ct_full_path, "r", encoding="utf-8") as ct:
            for line_num, line in enumerate(ct, 1):
                line = line.strip()
                if line=="" or line.startswith("#"):
                    continue
                parts = line.split()
                if len(parts) != 2:
                    raise DataFileError(f"error linr {line_num}: {line}")
                codon_table[parts[0].upper()] = parts[1].upper()
        return codon_table

    @staticmethod
    def load_amino_weights(aw_path):
        aw_full_path = Path.cwd() / aw_path 
        if not aw_full_path.is_file():
            raise DataFileError(f"wrong amino_weights directory: {aw_full_path} ")
        amino_weights = {}
        with open(aw_full_path, "r", encoding="utf-8") as aw:
            for line_num, line in enumerate(aw, 1):
                line = line.strip()
                if line=="" or line.startswith("#"):
                    continue
                parts = line.split()
                if len(parts) != 2:
                    raise DataFileError(f"error line {line_num}: {line}")
                amino_weights[parts[0].upper()] = float(parts[1])
        return amino_weights

class ORF:
    def __init__(self, annotation_id, protein, strand, frame, start_position, complete_incomplete):
        self.annotation_id = annotation_id
        self.protein = protein
        self.strand = strand
        self.frame = frame
        self.start_position = start_position
        self.complete_incomplete = complete_incomplete