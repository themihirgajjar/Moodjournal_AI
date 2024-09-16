from datetime import date
from datetime import timedelta
import csv
import random

def main():
    dates = []

    start_date = date.today() - timedelta(days=450)
    end_date = date.today()
    while start_date <= end_date:
        dates.append(start_date.strftime("%Y-%m-%d"))
        start_date += timedelta(days=1)

    sents = ["Positive", "Negative", "Neutral"]
    with open("filler.csv", "w") as file:
        # date,text,sentiment
        # random_date,"xyz",random_sentiment
        writer = csv.DictWriter(file, fieldnames=["date", "text", "sentiment"])
        writer.writeheader()
        for d in dates:
            r = random.randint(0,2)
            writer.writerow({"date": d, "text": "xyz", "sentiment": sents[r]})



if __name__ == "__main__":
    main()

