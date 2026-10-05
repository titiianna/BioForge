from exceptions import BioForgeError
from weight import Protein_weight

class Filter :

    def aplly(self , protein):
        pass


class LengthFilter(Filter):

    def __init__(self , min_length , max_length=0):
        self.min_length = min_length
        self.max_length = max_length

    def apply(self, proteins):
        result = []
        for protein in proteins:
            length = len(protein.protein)

            if length < self.min_length:
                continue

            if self.max_length is not None and length > self.max_length:
                continue

            result.append(protein)

        return result


class WeightFilter(Filter):
    def __init__(self, protein_weight, min_weight=None, max_weight=None):
        self.protein_weight = protein_weight
        self.min_weight = min_weight
        self.max_weight = max_weight
        pass

    def apply(self, proteins):
        result = []
        for protein in proteins:
            weight = self.protein_weight.calculate_weight(protein.protein)

            if self.min_weight is not None and weight < self.min_weight:
                continue
            if self.max_weight is not None and weight > self.max_weight:
                continue

            result.append(protein)

        return result



    