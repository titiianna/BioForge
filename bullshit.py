 
class ProteinWeight:
    def load_amino_weights(self):
        amino_weights = {}

        with open("data/amino_weights.txt", "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line == "" or line.startswith("#"):
                    continue

                clear_line = line.split()
                amino = clear_line[0]
                weight = float(clear_line[1])

                amino_weights[amino] = weight

        return amino_weights

    def calculate_weight(self, protein):
        amino_weights = self.load_amino_weights()
        final_protein_weight = 0

        for amino in protein:
            final_protein_weight += amino_weights[amino]

        return final_protein_weight
