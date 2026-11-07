
from pathlib import Path
import sys

from logstats import count_levels, top_errors, format_report


def iter_log_lines(path):
    """Читает файл построчно."""
    with open(path, "r", encoding="utf-8") as log:
        yield from log


def main():
    folder = Path(__file__).resolve().parent

    # Можно передать имя файла аргументом при запуске.
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = sys.stdin.readline().strip()

    if not filename:
        raise SystemExit("Не указано имя файла")

    path = Path(filename)

    if not path.is_absolute() and not path.exists():
        path = folder / path

    if not path.is_file():
        raise FileNotFoundError(f"Файл не найден: {filename}")

    print(f"Обрабатываю файл: {path.name}", file=sys.stderr)

    counts = count_levels(iter_log_lines(path))
    errors = top_errors(iter_log_lines(path), 3)

    total = sum(counts.values())

    # Выводим три требуемых числа.
    print(total)
    print(counts["ERROR"])
    print(counts["BROKEN"])

    report = format_report(counts, errors)

    report_path = folder / "report.txt"
    report_path.write_text(report, encoding="utf-8")

    print("Отчёт сохранён в report.txt", file=sys.stderr)


if __name__ == "__main__":
    main()
