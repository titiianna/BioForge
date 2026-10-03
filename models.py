from exceptions import DataFileError
from pathlib import Path

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