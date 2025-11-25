
def save_fact_check_to_file(fact_check_report: str, filename: str) -> dict:
    """Saves the fact check report to a file."""
    with open(filename, "w") as f:
        f.write(fact_check_report)
    return {"status": "success"}
