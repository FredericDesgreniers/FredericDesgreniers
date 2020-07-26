import calendar
from datetime import date


def generate_calendar(year, month, day):
    cal = calendar.Calendar(6)
    content = "``" + calendar.month_name[month] + " - " + str(year) + "``\n\n``"

    current_week = 0
    for row in cal.itermonthdates(year, month):
        day_of_week = (row.weekday() + 1) % 7
        if day_of_week == 0:
            current_week += 1
            if current_week > 1:
                content += "``\n\n``"
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
    return content + '``'


if __name__ == '__main__':
    today = date.today()
    generated_calendar = generate_calendar(today.year, today.month, today.day)
    print(generated_calendar)

    f = open("README.md", "w", encoding="utf-8")
    f.write(generated_calendar)
    f.close()
