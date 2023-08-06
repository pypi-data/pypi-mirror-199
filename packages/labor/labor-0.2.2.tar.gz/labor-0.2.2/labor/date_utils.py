import calendar

months = {
    "Jan": 1,
    "Fev": 2,
    "Mar": 3,
    "Abr": 4,
    "Mai": 5,
    "Jun": 6,
    "Jul": 7,
    "Ago": 8,
    "Set": 9,
    "Out": 10,
    "Nov": 11,
    "Dez": 12,
}

def get_last_day_of_month(month_number, year): 
    _, last_day = calendar.monthrange(int(year), int(month_number))
    return last_day