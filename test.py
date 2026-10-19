import csv
from datetime import datetime
with open("stock.csv",encoding="utf-8") as f:
    reader=csv.DictReader(f)
    for line in reader:
        date=datetime.strptime(line["記録日"],"%Y-%m-%d %H:%M:%S.%f").date()
        today_date=datetime.today().date()
        if date==today_date:
            return False
        else:
            print(date,date==today_date)
            pass