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


def generate_time_bar(minutes: int):
    content = "\n\n/0‾‾‾‾‾‾‾‾‾10‾‾‾‾‾‾‾‾20‾‾‾‾‾‾‾‾30‾‾‾‾‾‾‾‾40‾‾‾‾‾‾‾‾50‾‾‾‾‾‾‾60‾\\\n\n"
    content += "| "
    for _ in range(int(minutes)):
        content += 'O'
    content += "\n\n"
    content += "\\0_________10________20________30________40________50_______60_/"
    return content


def join_blocks(left: str, right: str, delimiter = " | "):
    left_width = max([len(x) for x in left.split("\n\n")])
    left_lines = left.split('\n\n')
    right_lines = right.split('\n\n')

    content = ""
    for i, line in enumerate(left_lines):
        content += line.ljust(left_width)
        if len(right_lines) > i:
            content += delimiter + right_lines[i] + "\n\n"
        else:
            content += "\n\n"
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

    content = wrap_in_ticks(join_blocks(generated_calendar, generate_time_bar(datetime.now().minute)))
    print(content)

    f = open("README.md", "w", encoding="utf-8")
    f.write(content)
    f.close()
