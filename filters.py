from exceptions import BioForgeError
from weight import Protein_weight

class Filter :

    def filter(self , orf):
        pass


class LengthFilter(Filter):

    def __init__(self , min_length):
        self.min_length = min_length

    def filter(self, orf):
        length = len(orf.protein)

        if length < self.min_length:
            return False

        return True

class WeightFilter(Filter):
    def __init__(self, protein_weight, min_weight=None, max_weight=None):
        self.protein_weight = protein_weight
        self.min_weight = min_weight
        self.max_weight = max_weight

    def filter(self, orf):
        weight = self.protein_weight.calculate_weight(orf.protein)

        if self.min_weight is not None and weight < self.min_weight:
            return False

        if self.max_weight is not None and weight > self.max_weight:
            return False

        return True




    