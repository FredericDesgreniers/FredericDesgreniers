import calendar
from datetime import date, datetime


def generate_calendar(year: int, month: int, day: int):
    cal = calendar.Calendar(6)
    content = calendar.month_name[month] + " - " + str(year) + "\n\n"

    current_week = 0
    for row in cal.itermonthdates(year, month):
        day_of_week = (row.weekday() + 1) % 7
        if day_of_week == 0:
            current_week += 1
            if current_week > 1:
                content += "\n\n"
        is_today = row.month == month and row.day == day
        if is_today:
            content += "["
        else:
            content += " "
        if row.day < 10:
            content += " "
        content += str(row.day)
        if is_today:
            content += "]"
        else:
            content += " "
    return content


def generate_bar(c: str = '‾', max: int = 61, step: int = 10):
    bar = ""
    current = 0
    until_step = 0
    while current < max:
        if until_step == 0:
            bar += str(current)
            current += 1
            until_step = step - 1
        else:
            bar += c
        until_step -= 1
        current += 1
    return bar


def generate_progress_bar(progress: int, max: int = 61, step: int = 10):
    content = "/" + generate_bar(max=max, step=step) + "\\ \n\n"
    content += "|"
    for _ in range(progress):
        content += 'O'
    for _ in range(max-progress):
        content += ' '
    content += " |\n\n"
    content += "\\" + generate_bar(c="_", max=max, step=step) + "/\n\n"
    return content


def join_blocks(left: str, right: str, delimiter=" | "):
    left_width = max([len(x) for x in left.split("\n\n")])
    left_lines = left.split('\n\n')
    right_lines = right.split('\n\n')

    content = ""
    for i, line in enumerate(left_lines):
        while len(line) < left_width:
            line += " "
        content += line
        if len(right_lines) > i:
            content += delimiter + right_lines[i] + "\n\n"
        else:
            content += "\n\n"
    if len(left_lines) < len(right_lines):
        padding = ''
        for _ in range(left_width):
            padding += ' '
        for i, line in enumerate(right_lines):
            if i >= len(left_lines):
                content += padding + delimiter + line + "\n\n"

    return content


def wrap_in_ticks(content: str):
    new_content = ""
    for line in content.split("\n\n"):
        new_content += '``' + line + '``\n\n'
    return new_content


if __name__ == '__main__':
    today = date.today()
    generated_calendar = generate_calendar(today.year, today.month, today.day)
    print(generated_calendar)

    content = wrap_in_ticks(join_blocks(generated_calendar,
                                        "hour\n\n" + generate_progress_bar(datetime.now().hour, max=25, step=6)
                                        +"\n\nminute\n\n" + generate_progress_bar(datetime.now().minute)
                                        )
                            )
    print(content)

    f = open("README.md", "w", encoding="utf-8")
    f.write(content)
    f.close()
