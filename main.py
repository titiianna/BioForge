import argparse
from pathlib import Path

from exceptions import BioForgeError
from filters import LengthFilter, WeightFilter
from logger import setup_logging
from models import DataDirLoad
from parsers import read_fasta
from pipeline import Pipeline
from report import write_report

DATA_DIR = Path.cwd() / "data"

def get_args():
    parser = argparse.ArgumentParser(description="BioForge")
    parser.add_argument("--input", required=True, help="FASTA file path")
    parser.add_argument("--out", required=True, help="output directory")
    parser.add_argument("--min-length", required=True, type=int, help="minimum length")
    parser.add_argument("--min-weight", required=True, type=float, help="minimum weight")
    return parser.parse_args()

def get_organism(description):
    for part in description.split():
        if part.startswith("organism="):
            return part[len("organism="):]
    return None

def prepare_for_report(record, orfs):
    organism = get_organism(record.description)
    if organism is None:
        record.sequence_id = record.id
    else:
        record.sequence_id = record.id + " (organism=" + organism + ")"

    for orf in orfs:
        orf.is_complete = orf.complete_incomplete

def main():
    args = get_args()
    log = setup_logging(args.out)
    log.info("Run started: input=%s", args.input)

    try:
        codon_table = DataDirLoad.load_codon_table(DATA_DIR / "codon_table.txt")
        amino_weights = DataDirLoad.load_amino_weights(DATA_DIR / "amino_weights.txt")
    except (BioForgeError, ValueError) as e:
        log.error("Data file error: %s", e)
        return 1

    try:
        records = read_fasta(args.input, log)
    except BioForgeError as e:
        log.error("FASTA error: %s", e)
        return 1

    seen_ids = []
    for record in records:
        if record.id in seen_ids:
            log.warning("Duplicate ID: %s", record.id)
        seen_ids.append(record.id)

    filters = [
        LengthFilter(args.min_length),
        WeightFilter(args.min_weight, amino_weights),
    ]
    pipeline = Pipeline(codon_table, filters)

    results = []
    for record in records:
        try:
            orfs = pipeline.process(record.sequence)
        except BioForgeError as e:
            log.error("Record %s skipped: %s", record.id, e)
            continue
        log.info("Record %s: %d ORF(s) kept", record.id, len(orfs))
        prepare_for_report(record, orfs)
        results.append((record, orfs))

    # write report
    report_path = Path(args.out) / "report.txt"
    write_report(results, report_path)
    log.info("Run finished: report written to %s", report_path)
    return 0

if __name__ == "__main__":
    main()