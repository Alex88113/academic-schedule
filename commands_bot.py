from datetime import datetime

def print_date_today(date=datetime.now()) -> str:
    return f"Date today {date.strftime("%Y-%m-%d")}"

print(print_date_today())