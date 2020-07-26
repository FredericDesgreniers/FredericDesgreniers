import calendar
from datetime import date, datetime


def generate_calendar(year: int, month: int, day: int):
    cal = calendar.Calendar(6)
    calendar_format = "<b>CALENDAR</b>\n\n_____________________________\n\n<b>" + calendar.month_name[month] + "</b> - <b>" + str(year) \
                      + "</b>\n\n<b> SU  MO  TU  WE  TH  FR  SA</b>\n\n"

    current_week = 0
    for row in cal.itermonthdates(year, month):
        day_of_week = (row.weekday() + 1) % 7
        if day_of_week == 0:
            current_week += 1
            if current_week > 1:
                calendar_format += "\n\n"
        is_today = row.month == month and row.day == day
        if is_today:
            calendar_format += "<b>["
        else:
            calendar_format += " "
        if row.day < 10:
            calendar_format += " "
        calendar_format += str(row.day)
        if is_today:
            calendar_format += "]</b>"
        else:
            calendar_format += " "
    return calendar_format


def generate_bar(c: str = '‾', max: int = 61, step: int = 10):
    bar = ""
    current = 0
    until_step = 0
    while current < max:
        if until_step == 0:
            bar += str(current)
            if current < 10:
                bar += c
            current += 1
            until_step = step - 1
        else:
            bar += c
        until_step -= 1
        current += 1
    return bar


def generate_progress_bar(progress: int, max: int = 61, step: int = 10, top_bar: bool = True, bottom_bar: bool = True):
    progress_bar = ""
    if top_bar:
        progress_bar += "/" + generate_bar(max=max, step=step) + "\\ \n\n"
    progress_bar += "|"
    for _ in range(progress-1):
        progress_bar += 'O'
    progress_bar += " <b>" + str(progress) + "</b>"
    for _ in range(max - progress):
        progress_bar += ' '
    progress_bar += "|\n\n"
    if bottom_bar:
        progress_bar += "\\" + generate_bar(c="_", max=max, step=step) + "/\n\n"
    return progress_bar

def hlen(s: str) -> int:
    return len(s.replace("<b>", "").replace("</b>", ""))

def join_blocks(left: str, right: str, delimiter="  |  "):
    left_width = max([hlen(x) for x in left.split("\n\n")])
    left_lines = left.split('\n\n')
    right_lines = right.split('\n\n')

    block = ""
    for i, line in enumerate(left_lines):
        while hlen(line) < left_width:
            line += " "
        block += line
        if len(right_lines) > i:
            block += delimiter + right_lines[i] + "\n\n"
        else:
            block += "\n\n"
    if len(left_lines) < len(right_lines):
        padding = ''
        for _ in range(left_width):
            padding += ' '
        for i, line in enumerate(right_lines):
            if i >= len(left_lines):
                block += padding + delimiter + line + "\n\n"

    return block


def wrap_in_ticks(content: str):
    new_content = ""
    for line in content.split("\n\n"):
        new_content += '``' + line + '``\n\n'
    return '<pre>\n\n' + content + '\n\n</pre>'


if __name__ == '__main__':
    today = date.today()
    generated_calendar = generate_calendar(today.year, today.month, today.day)
    print(generated_calendar)

    content = "**Frederic Desgreniers**\n\n" + wrap_in_ticks(join_blocks(generated_calendar,
                                                                         "<b>CLOCK</b> (UTC)\n\n_______________________________\n\n"
                                                                         + generate_progress_bar(datetime.now().hour,
                                                                                                 max=25, step=6,
                                                                                                 bottom_bar=False)
                                                                         + generate_progress_bar(datetime.now().minute,
                                                                                                 top_bar=False)
                                                                         )
                                                             )
    print(content)

    f = open("README.md", "w", encoding="utf-8")
    f.write(content)
    f.close()
