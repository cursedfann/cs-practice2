
LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR")


def parse_event(line: str) -> dict:
    """Разбирает строку журнала."""
    parts = line.strip().split(maxsplit=2)

    if len(parts) != 3:
        raise ValueError("Некорректная строка")

    time, level, message = parts

    if level not in LEVELS or not message:
        raise ValueError("Некорректная строка")

    return {
        "time": time,
        "level": level,
        "message": message
    }



def count_levels(lines: list[str]) -> dict:
    """Считает количество записей по уровням."""
    counts = {}

    for line in lines:
        try:
            event = parse_event(line)
        except (ValueError, TypeError):
            counts["BROKEN"] = counts.get("BROKEN", 0) + 1
        else:
            level = event["level"]
            counts[level] = counts.get(level, 0) + 1

    return counts



def top_errors(lines: list[str], n: int) -> list:
    """Возвращает n самых частых сообщений ERROR."""
    errors = {}

    for line in lines:
        try:
            event = parse_event(line)
        except (ValueError, TypeError):
            continue

        if event["level"] == "ERROR":
            message = event["message"]
            errors[message] = errors.get(message, 0) + 1

    result = sorted(
        errors.items(),
        key=lambda item: (-item[1], item[0])
    )

    return [[message, count] for message, count in result[:max(0, n)]]




def format_report(counts: dict, errors: list) -> str:
    """Формирует текстовый отчёт."""
    lines = ["Отчёт по журналу", ""]

    for level, count in counts.items():
        lines.append(f"{level}: {count}")

    lines.extend(["", "Частые ошибки:"])

    for message, count in errors:
        lines.append(f"- {message} — {count}")

    return "\n".join(lines) + "\n"


