#کد مربوط به بخش وزن پروتئین ها 
from exceptions import DataFileError   

class Protein_weight:

    def __init__(self, amino_weights):
        self.amino_weights = amino_weights


    def file_analysis(self , amino_weights):

        with open("data/amino_weights.txt" , "r" , encoding="utf-8") as file:
        
            amino_weights = {}

            for line in file:
                line = line.strip()
        
                if line == "" or line.startswith("#"):
                    continue
                clear_line = line.split()
                aminos = clear_line[0]
                weight = float(clear_line[1])
                amino_weights[aminos] = weight

            
                if amino_weights =={}:
                    raise DataFileError("amino_weights.txt not found")

        return amino_weights

    def weight_calculate(self , protein):

        final_protein_weight = 18.015
      
        for amino in protein:
            final_protein_weight += self.amino_weights[amino]

        return final_protein_weight


