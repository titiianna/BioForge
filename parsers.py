from exceptions import FastaFormatError
from dna_sequence import DNASequence


class FastaRecord:

    def __init__(self, record_id, description, sequence):
        self.id = record_id
        self.description = description
        self.sequence = DNASequence(sequence)


def read_fasta(file_name):

    records = []

    current_id = None
    current_description = ""
    current_sequence = ""

    try:

        with open(file_name, "r", encoding="utf-8") as file:

            for line in file:

                line = line.strip()

                if line == "":
                    continue

                if line.startswith(">"):

                    if current_id is not None:

                        if current_sequence == "":
                            raise FastaFormatError(
                                "Header has no sequence: " + current_id
                            )

                        record = FastaRecord(
                            current_id,
                            current_description,
                            current_sequence
                        )

                        records.append(record)

                    header = line[1:].strip()

                    if header == "":
                        raise FastaFormatError("Empty header")

                    parts = header.split(" ", 1)

                    current_id = parts[0]

                    if len(parts) > 1:
                        current_description = parts[1]
                    else:
                        current_description = ""

                    current_sequence = ""

                else:

                    if current_id is None:
                        raise FastaFormatError(
                            "Sequence found before first header"
                        )

                    current_sequence += line

            if current_id is not None:

                if current_sequence == "":
                    raise FastaFormatError(
                        "Header has no sequence: " + current_id
                    )

                record = FastaRecord(
                    current_id,
                    current_description,
                    current_sequence
                )

                records.append(record)

    except FileNotFoundError:

        raise FastaFormatError("FASTA file not found")

    if len(records) == 0:
        raise FastaFormatError("FASTA file is empty")

    return records