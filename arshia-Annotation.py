class Annotation:

    def __init__(self ,counter = 1 , annotation_id =None ):
        self.counter= counter 
        self.annotation_id= self.set_annotation_id (annotation_id)

    def set_annotation_id (self,annotation_id ):
        if annotation_id is not None:
            return annotation_id
        return []

    def get_annotation_id(self):
        annotation_id= f"BFG_{self.counter:03d}"
        self.counter+=1
        self.annotation_id.append(annotation_id)
        return annotation_id

    def get_all_annotation_id(self , final_orfs):
        for orf in final_orfs:
            annotation_id= self.get_annotation_id()
            orf.annotation_id = annotation_id