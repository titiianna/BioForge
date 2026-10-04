class ORF:
    def __init__(self, annotation_id, protein, strand, frame, start_position, complete_incomplete):
        self.annotation_id = annotation_id
        self.protein = protein
        self.strand = strand
        self.frame = frame
        self.start_position = start_position
        self.complete_incomplete = complete_incomplete