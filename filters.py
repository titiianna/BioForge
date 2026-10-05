from exceptions import BioForgeError

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

    