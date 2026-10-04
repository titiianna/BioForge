from exceptions import DataFileError

START_CODON = "AUG"
STOP_CODON = ["UAA", "UAG", "UGA"]


class Traslator:
    def __init__(self, codon_table):
        pass