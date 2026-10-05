def write_report(results, report_path):
    lines = []
    lines.append("Report")
    lines.append("===================")
    for record, orfs in results:
        lines.append(f"Record: {record.sequence_id}")
        if not orfs:
            lines.append("  (no ORFs passed the filters)")
            continue
        lines.append(f"{'ID'} {'Strand'} {'Frame'} {'Start'} {'Status'} Protein")
        for orf in orfs:
            if orf.is_complete: 
                status = "Complete" 
            else:
                status = "InComplete" 
            lines.append(f"{orf.annotation_id} {orf.strand} {orf.frame} {orf.start_position} {status} {orf.protein}")
        lines.append("")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
