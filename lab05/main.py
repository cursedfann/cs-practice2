
from pathlib import Path
import sys

from logstats import count_levels, top_errors, format_report


def iter_log_lines(path):
    """Читает файл построчно."""
    with open(path, "r", encoding="utf-8") as log:
        yield from log


def main():
    filename = sys.stdin.readline().strip()

    if not filename:
        raise SystemExit("Не указано имя файла")

    path = Path(filename)

    counts = count_levels(iter_log_lines(path))
    errors = top_errors(iter_log_lines(path), 3)

    total = sum(counts.values())

    print(total)
    print(counts["ERROR"])
    print(counts["BROKEN"])

    report = format_report(counts, errors)

    report_path = Path(__file__).resolve().parent / "report.txt"
    report_path.write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
