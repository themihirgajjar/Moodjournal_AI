from datetime import date
from datetime import timedelta
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import csv
import os
import random
import sys


def main():
    # Writing mode: get journal entry, do a sentiment analysis, add to csv with date of entry
    if len(sys.argv) == 1 or len(sys.argv) == 2 and sys.argv[1] == "prompt":
        text = prompt()
        sentiment = sentimental(text)
        day = date.today()
        write_in_journal(day, text, sentiment)

    # Analysis mode: analyse sentiments of journal entries
    elif len(sys.argv) >= 2 and sys.argv[1] == "analyse":
        try:
            analyse = []
            # Analysis of all journal entries
            if len(sys.argv) == 2:
                with open("journal.csv") as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        analyse.append(row["sentiment"])
            # Analysis with optional arguments: week, month, year
            elif len(sys.argv) == 3:
                if sys.argv[2] == "week":
                    daterange = get_daterange(7)

                elif sys.argv[2] == "month":
                    daterange = get_daterange(30)

                elif sys.argv[2] == "year":
                    daterange = get_daterange(365)

                with open("journal.csv") as file:
                        reader = csv.DictReader(file)
                        for row in reader:
                            if row["date"] in daterange:
                                analyse.append(row["sentiment"])

            print_analysis(analyse)
            print(daterange)

        except FileNotFoundError:
            sys.exit("No journal entries found to analyse, get started today")

    else:
        sys.exit("Optional arguments: prompt, analyse (week/ month/ year)")


# Writing mode functions

# prompt():
# prompts user for journal entry
# reprompts until user input is at least 15, non-blank characters long
# optional cla 'prompt' randomly generates questions for user and allows to change question
def prompt():
    while True:
        if len(sys.argv) == 1:
            t = input("How was your day?: ").strip()
        elif len(sys.argv) == 2 and sys.argv[1] == "prompt":
            t = input(f"{generate_prompt()} [enter to reprompt]: ").strip()
        if len(t) >= 15:
            return t


# generate_prompt():
# randomly generates journal prompts from a list
def generate_prompt():
    questions = [
        "Share one thing that you are grateful for",
        "What was the highlight of your day?",
        "Plan how would you want to spend your next day off",
        "What has been draining your energy these days?",
        "What would you rather be doing right now?",
        "What is something you can do to feel better right now?",
        "What did you do today that takes you closer to your long term goals?",
        "Where is your favorite place to visit, and why?",
        "How often do you experience joy, wonder, and appreciation in your life? How can you add more of this?",
        "Write about something awesome coming up shortly",
    ]
    i = random.randint(0, 9)
    for question in questions:
        return questions[i]


# sentimental(s):
# uses vaderSentiment library to perform sentiment analysis on user input
# returns sentiment of user input
def sentimental(s):
    analyzer = SentimentIntensityAnalyzer()
    vs = analyzer.polarity_scores(s)

    if vs["compound"] >= 0.05:
        return "Positive"
    elif vs["compound"] <= -0.05:
        return "Negative"
    else:
        return "Neutral"


# write_in_journal(a, b, c):
# takes date, text and sentiment as argument
# appends to csv in appropriate format
# if being used for the first time, adds header row
def write_in_journal(a, b, c):
    path = os.path.isfile(os.path.abspath("journal.csv"))

    with open("journal.csv", "a") as file:
        writer = csv.DictWriter(file, fieldnames=["date", "text", "sentiment"])
        if not path:
            writer.writeheader()
        writer.writerow({"date": a, "text": b, "sentiment": c})


# Analysis mode functions

# get_daterange(n):
# when analysing with optional cla, generates a list of dates from last week/month/year
def get_daterange(n):
    daterange = []
    start_date = date.today() - timedelta(days=n)
    end_date = date.today()
    while start_date <= end_date:
        daterange.append(start_date.strftime("%Y-%m-%d"))
        start_date += timedelta(days=1)
    return daterange


# print_analysis(a):
# prints analysis of sentiments of journal entries
def print_analysis(a):
    count = {}
    count["pos"] = 0
    count["neg"] = 0
    count["neut"] = 0
    for senti in a:
        if senti == "Positive":
            print("🟩", end="")
            count["pos"] += 1
        elif senti == "Negative":
            print("🟥", end="")
            count["neg"] += 1
        else:
            print("🟨", end="")
            count["neut"] += 1
    print()
    print(f"😃: {count['pos']}")
    print(f"🙁: {count['neg']}")
    print(f"😐: {count['neut']}")


if __name__ == "__main__":
    main()
