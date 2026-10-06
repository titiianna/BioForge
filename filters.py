class BaseFilter:
    def filter(self, orf):
        return True

class LengthFilter(BaseFilter):
    def __init__(self, min_length):
        self.min_length = min_length

    def filter(self, orf):
        return len(orf.protein) >= self.min_length

class WeightFilter(BaseFilter):
    def __init__(self, min_weight, amino_weights):
        self.min_weight = min_weight
        self.amino_weights = amino_weights

    def calculate_weight(self, protein):
        if not protein:
            return 0.0
        # Formula based on file note: sum(residue_weights) + 18.015
        weight = 0
        for amino_a in protein:
            if amino_a in self.amino_weights:
                weight+=self.amino_weights[amino_a]
        weight += 18.015

        return weight

    def filter(self, orf):
        w = self.calculate_weight(orf.protein)
        return w >= self.min_weight