 # Moodjournal_AI
    #### Video Demo:  <https://youtu.be/g_VTELWvWHQ>
    #### Description:
    Moodjournal_AI is a journaling tool that takes journal entries, evaluates their sentiment and saves the entries in a csv file. The program can also help visualise the sentiments of previous journal entries which can further be filtered by week, month or year.

    #### Structure:
    ...

    #### Writing Mode in main():

    main():
    if len(sys.argv) == 1 or len(sys.argv) == 2 and sys.argv[1] == "prompt":
        text = prompt()
        sentiment = sentimental(text)
        day = date.today()
        write_in_journal(day, text, sentiment)

    The first part of the program is writing mode accessed by: python moodjournal_ai.py. This mode takes a user input by prompting the user "How was your day?". The program checks whether the length of the command line arguments is 1 and uses a function called prompt() to get user response.

    def prompt():
    while True:
        if len(sys.argv) == 1:
            t = input("How was your day?: ").strip()
        elif len(sys.argv) == 2 and sys.argv[1] == "prompt":
            t = input(f"{generate_prompt()} [enter to reprompt]: ").strip()
        if len(t) >= 15:
            return t

    The prompt() function does not take any arguments. It asks the user for an input and checks whether the user has given a journal entry that is at least 15 (non-blank) characters long. If not, the function reprompts the user until they provide appropriate response. The function then returns the user input.

    In the main() function, the response from prompt() is stored in a variable called text. Which then passes the user entry to a function called sentimental() to perform sentiment analysis on the user input using the vaderSentiment library.

    def sentimental(s):
    analyzer = SentimentIntensityAnalyzer()
    vs = analyzer.polarity_scores(s)

    if vs["compound"] >= 0.05:
        return "Positive"
    elif vs["compound"] <= -0.05:
        return "Negative"
    else:
        return "Neutral"


    The function analyses a str user inpyt and returns a value between -1 and 1. According to the documentation of the vaderSentiment library, simple interpretation of the value is as follows:
    If the value is >= 0.05, the sentiment of the text is likely to be positive.
    If the value is <= -0.05, the sentiment of the text is likely to be negative.
    Otherwise, the sentiment of the text is likely to be neutral.
    The function interprets the outcome accordingly and returns a string, classifying the sentiment as positive. negative or neutral.

    From datetime module, the program uses the date.today() function to get the date of user input. The collection of text, sentiment analysis and the date of entry is then stored in a csv file using the write_in_journal(a, b, c) function.

    def write_in_journal(a, b, c):
    path = os.path.isfile(os.path.abspath("journal.csv"))

    with open("journal.csv", "a") as file:
        writer = csv.DictWriter(file, fieldnames=["date", "text", "sentiment"])
        if not path:
            writer.writeheader()
        writer.writerow({"date": a, "text": b, "sentiment": c})

    The function takes the text, sentiment of the text and the date of entry as arguments, and creates/appends to a file called "journal.csv". By using path from the os module, the function determines whether the "journal.csv" file exists in the directory. If not, the program assumes the user entry as being the first one. It then creates the csv, adds a header row and appends to the file the date, journal entry and sentiment of the entry. In case the file already exists, the function simply appends another row to the file.

    Within the writing mode, there is another functionality. If the commandline argument is as follows: python moodjournal_ai.py prompt.

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

    In case the user needs a randomly generated prompt that asks different questions than the default "How was your day?", the generate_prompt() function returns a randomly generated question from a list called questions. Everytime the user gives an empty entry, the function returns a different question. Although the function does not store or evaluate whether the user has replied the the question being asked, it provides the user with some inspiration to journal when the user does not know what to write. Since the program is supposed to be a daily mood journal, the accuracy of whether the journal entry is the answer to the question being prompted is not relevant. Hence, there is no function that stores the question.

    #### Analysis Mode in Main():

    The journal allows users to analyse the sentiments of their journal entries using the following command: python moodjournal_ai.py analyse. It opens the journal.csv file and creates a list of the sentiments of each entries from the file. Optionally, the user can also ask to see just the analysis of past week, month or year. In which case, the program calls a function called get_daterange().

    def get_daterange(n):
    daterange = []
    start_date = date.today() - timedelta(days=n)
    end_date = date.today()
    while start_date <= end_date:
        daterange.append(start_date.strftime("%Y-%m-%d"))
        start_date += timedelta(days=1)
    return daterange

    Depending on the time specified by the user (week, month, year), a relevant number if days (7, 30, 365) is passed to the get_daterange() function. The function gets the date of analysis and returns a list of dates of last 7, 30 or 365 days.

    The analysis then creates a list of sentiments from the entries from the dates returned by the get_daterange() function.

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

    Finally, there is the print_analysis(a) funciton which takes the list of sentiments created either by collecting the sentiments from all the entries or filtered entries from last week, month or year, and prints a heatmap like visual along with the number of positive, neutral and negative entries from the user's journal. The function prints characters instead of returning strings to keep the code shorter. It is also supposed to be just an overview of the sentiments of the user's entries so the required functionality of the function is kept limited.

    #### Exceptions:
    If the user passes in the commandline, a command that is not supported by the program, the program exits with the following text: "Optional arguments: prompt, analyse (week/ month/ year)"

    If the user tries to analyse their data without making any journal entries, due to the FileNotFound error, the program exits with the following text: "No journal entries found to analyse, get started today"



