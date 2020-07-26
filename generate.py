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


def renderBook(title: str, link: str, description) -> str:
    return f"<b><a href=\"{link}\">{title}</a></b>:\n\n    <i>" + description + "</i>\n\n"


def book_list():
    return "------------------------------------------------------\n\n<b>Book List</b> (Some of my favorite books read in the last 2-3 years)\n\n" + \
        renderBook("The Spy And The Traitor", "https://www.goodreads.com/book/show/37542581-the-spy-and-the-traitor", "Story of Oleg Gordievsky, a real soviet era spy turned double agent for MI6.") + \
        renderBook("Manufacturing Consent", "https://www.goodreads.com/book/show/12617.Manufacturing_Consent", "Classic Chomskey novel relating the politics and media. Regardless of ones opinion, it presents a lot of useful context and example relating to how media will shape the view of political events.") + \
        renderBook("The Elegant Universe", "https://www.goodreads.com/book/show/8049273-the-elegant-universe", "Brian Greene tries his hand at explaining string theory to the layman and he succeeds. Much of the material is up for debate, however it offers a lot of interesting knowledge relating to both the universe and the mathematics behind multi-demensional universes.") + \
        renderBook("The Little Typer", "https://www.goodreads.com/book/show/39736150-the-little-typer", "Great introduction to dependent types in an easy to follow book. Also great demonstration of the power of the Racket programming language") + \
        renderBook("Thinking Fast and Slow", "https://www.goodreads.com/book/show/11468377-thinking-fast-and-slow", "Deep dive into how we think and the different systems surrounding thinking.") + \
        renderBook("The Code Book", "https://www.goodreads.com/book/show/17994.The_Code_Book", "Cool history of the evolution of criptography through the ages and how different types of codes work and are broken. The part on the enigma machine is especially interesting.") + \
        renderBook("The Ride Of A Lifetime", "https://www.goodreads.com/book/show/44525305-the-ride-of-a-lifetime", "Autobiography from former Disney CEO Robert Iger. Through written before his retirement, it offers an insight into how to rise in complex organization using strong relationships and motivation.") + \
        renderBook("Flash Boys", "https://www.goodreads.com/book/show/24724602-flash-boys", "Story of how high frequency trading started and evolved along with the consequences of it.") + \
        renderBook("Compilers - Principles, Techniques & Tools", "https://www.goodreads.com/book/show/703102.Compilers", "Interesting read. Great as a reference when working on compilers. Even when not in the business of implementing compilers, offers a lot of details on generally useful algorithms (especially relating to parsing techniques).") + \
        renderBook("Understanding Exposure", "https://www.goodreads.com/book/show/142239.Understanding_Exposure", "Must read for anyone interested in photography. Covers a wide range of techniques about how to shoot just about anything.")

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
                                                                         ) +
                                                                        book_list()
                                                             )
    print(content)

    f = open("README.md", "w", encoding="utf-8")
    f.write(content)
    f.close()
