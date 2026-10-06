from exceptions import FastaFormatError
from models import DNASequence
from exceptions import InvalidSequenceError

class FastaRecord:

    def __init__(self, record_id, description, sequence):
        self.id = record_id
        self.description = description
        self.sequence = DNASequence(sequence)

def _add_record(records, record_id, description, sequence, logger):
    if sequence == "":
        raise FastaFormatError(f"empty header: {record_id}")
    try:
        records.append(FastaRecord(record_id, description, sequence))
    except InvalidSequenceError as e:
        logger.error(f"error in {record_id}: {e}")

def read_fasta(file_name,logger):

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
                        _add_record(records, current_id, current_description, current_sequence, logger)
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

                _add_record(records, current_id, current_description, current_sequence, logger)

    except FileNotFoundError:

        raise FastaFormatError("FASTA file not found")

    if len(records) == 0:
        raise FastaFormatError("FASTA file is empty")

    return records