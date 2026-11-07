
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
    """Считает количество строк каждого уровня."""
    counts = {level: 0 for level in LEVELS}
    counts["BROKEN"] = 0

    for line in lines:
        try:
            event = parse_event(line)
        except (ValueError, TypeError):
            counts["BROKEN"] += 1
        else:
            counts[event["level"]] += 1

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
    """Формирует текст отчёта."""
    order = ("BROKEN", "DEBUG", "ERROR", "INFO", "WARNING")

    lines = ["Отчёт по журналу", ""]

    for level in order:
        lines.append(f"{level}: {counts.get(level, 0)}")

    lines.extend(["", "Частые ошибки:"])

    for message, count in errors:
        lines.append(f"- {message} — {count}")

    return "\n".join(lines) + "\n"
