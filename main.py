import tkinter as tk
from textblob import TextBlob
from newspaper import Article


# Create the common widgets for SummarizeGUI and SavedGUI
def widgets(self):
    # make title label
    title_label = tk.Label(self.root, text="Title")
    title_label.pack()

    # make title box and user cant change
    self.title = tk.Text(self.root, height=1, width=140)
    self.title.config(state='disabled', bg='#dddddd')
    self.title.pack()

    # make author label
    author_label = tk.Label(self.root, text="Author")
    author_label.pack()

    # make author box and user cant change
    self.author = tk.Text(self.root, height=1, width=140)
    self.author.config(state='disabled', bg='#dddddd')
    self.author.pack()

    # make publication label
    publication_label = tk.Label(self.root, text="Publishing Date")
    publication_label.pack()

    # make publication box and user cant change
    self.publication = tk.Text(self.root, height=1, width=140)
    self.publication.config(state='disabled', bg='#dddddd')
    self.publication.pack()

    # make summary label
    summary_label = tk.Label(self.root, text="Summary")
    summary_label.pack()

    # make summary box and user cant change
    self.summary = tk.Text(self.root, height=20, width=140)
    self.summary.config(state='disabled', bg='#dddddd')
    self.summary.pack()

    # make sentiment label
    sentiment_label = tk.Label(self.root, text="Sentiment Analysis")
    sentiment_label.pack()

    # make sentiment box and user cant change
    self.sentiment = tk.Text(self.root, height=1, width=140)
    self.sentiment.config(state='disabled', bg='#dddddd')
    self.sentiment.pack()

    # make home button
    home_button = tk.Button(self.root, text="Go to Home", command=self.destroy)
    home_button.pack(side=tk.BOTTOM, pady=5)


# Function for changing the contents of SummarizeGUI and SavedGUI
def change_contents(self, title, author, publication, summary, sentiment):
    # Allows content to be changed
    self.title.config(state='normal')
    self.author.config(state='normal')
    self.publication.config(state='normal')
    self.summary.config(state='normal')
    self.sentiment.config(state='normal')

    # Changing the contents
    self.title.delete('1.0', 'end')
    self.title.insert('1.0', title)

    self.author.delete('1.0', 'end')
    self.author.insert('1.0', author)

    self.publication.delete('1.0', 'end')
    self.publication.insert('1.0', publication)

    self.summary.delete('1.0', 'end')
    self.summary.insert('1.0', summary)

    self.sentiment.delete('1.0', 'end')
    self.sentiment.insert('1.0', sentiment)

    # Stopping the contents from being changed
    self.title.config(state='disabled')
    self.author.config(state='disabled')
    self.publication.config(state='disabled')
    self.summary.config(state='disabled')
    self.sentiment.config(state='disabled')


# Class for creating a GUI for summarizing articles
class SummarizeGUI:
    # initializing variables
    def __init__(self, home_instance):
        # create window, title, and instance of HomeGUI(used for switching between windows).
        self.home_instance = home_instance
        self.root = tk.Tk()
        self.root.title("News Summarizer")

        # initializing all variables in the summary
        self.title = None
        self.author = None
        self.publication = None
        self.summary = None
        self.sentiment = None
        self.url_text = None

        # initializing dictionary for text file
        self.article_info = {
            "Title": "",
            "Author": "",
            "Publish Date": "",
            "Summary": "",
            "Sentiment": ""
        }

        # calling the create_widgets() function to build the GUI.
        self.create_widgets()

    # This function is for displaying the article summary
    def display_article(self, article):
        # Analyze the article then change the contents
        analysis = TextBlob(article.text)
        change_contents(self, article.title, article.authors, article.publish_date, article.summary, f'Polarity: {analysis.polarity} Sentiment: {"positive" if analysis.polarity > 0 else "negative" if analysis.polarity < 0 else "neutral"}')

        # This updates the dictionary with the summary
        self.article_info["Title"] = article.title
        self.article_info["Author"] = article.authors
        self.article_info["Publish Date"] = str(article.publish_date)
        self.article_info["Summary"] = article.summary
        self.article_info["Sentiment"] = f'Polarity: {analysis.polarity} Sentiment: {"positive" if analysis.polarity > 0 else "negative" if analysis.polarity < 0 else "neutral"}'

    # This summarizes the article
    def summarize(self):
        url = self.url_text.get('1.0', "end").strip()
        article = Article(url)
        article.download()
        article.parse()
        article.nlp()

        # Call the function to display the article summary
        self.display_article(article)

    # This saves the summary into a text file using the dictionary
    def save_summary(self):
        saved_data = {
            "Title": self.article_info["Title"],
            "Author": self.article_info["Author"],
            "Publish Date": self.article_info["Publish Date"],
            "Summary": self.article_info["Summary"],
            "Sentiment": self.article_info["Sentiment"]
        }

        # Writes content into the text file
        with open("file.txt", "w") as file:
            for key, value in saved_data.items():
                file.write(f"{key}: {value}\n")

    # Creates the GUI by calling the widgets function and also  adding a little bit of it's own unique attributes
    def create_widgets(self):
        widgets(self)

        # Create URL Label
        url_label = tk.Label(self.root, text ="URL")
        url_label.pack()

        # Make state enabled so users can enter URL
        self.url_text = tk.Text(self.root, height=1, width=140)
        self.url_text.pack()

        # Make summarize button
        summarize_button = tk.Button(self.root, text="Summmarize", command=self.summarize)
        summarize_button.pack(pady=5)

        # Make save button
        save_button = tk.Button(self.root, text="Save Summary", command=self.save_summary)
        save_button.pack(pady=5)

    # So when you click "Go To Home" the GUI will destroy itself and reopen the HomeGUI
    def destroy(self):
        self.root.destroy()
        self.home_instance.show_home()

    # Run the window
    def run(self):
        self.root.mainloop()


# GUI for saved summary
class SavedGUI:
    # initializing variables
    def __init__(self, home_instance, saved_data):
        # create window, title, and instance of HomeGUI(used for switching between windows).
        self.home_instance = home_instance
        self.root = tk.Tk()
        self.root.title("Saved Summary")

        # initializing variables
        self.title = None
        self.author = None
        self.publication = None
        self.summary = None
        self.sentiment = None

        # create widgets and call the display_saved_data function
        widgets(self)
        self.display_saved_data(saved_data)

    # display the saved summary without allowing the user to change anything
    def display_saved_data(self, saved_data):
        # Change the contents of saved summary
        change_contents(self, saved_data.get("Title", ""), saved_data.get("Author", ""), saved_data.get("Publish Date", ""), saved_data.get("Summary", ""), saved_data.get("Sentiment", ""))

    # Function to destroy window and reopen home window
    def destroy(self):
        self.root.destroy()
        self.home_instance.show_home()

    # Run the window
    def run(self):
        self.root.mainloop()


# GUI for home window
class HomeGUI:
    # initializing variables
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Article Summarizer")
        self.root.geometry('600x400')

        self.create_widgets()

    def show_saved_summary(self):
        self.root.withdraw()
        # Read the file and put it in a dictionary called saved_data
        file_path = 'file.txt'
        with open(file_path, 'r') as file:
            saved_data = {}
            current_key = None

            for line in file:
                if line.strip():
                    key_value = line.split(':', 1)
                    if len(key_value) == 2:
                        current_key = key_value[0].strip()
                        saved_data[current_key] = key_value[1].strip()
                    elif current_key:
                        saved_data[current_key] += f'\n{line.strip()}'

            # Open an instance of SavedGUI with the retrieved saved data
            SavedGUI(self, saved_data).run()

    # Open the SummarizeGUI and hide the home window.
    def create_new_summary(self):
        self.root.withdraw()
        SummarizeGUI(self)

    # Create the HomeGUI
    def create_widgets(self):
        # Header
        header_label = tk.Label(self.root, text="Article Summarizer", font=("Helvetica", 24), pady=20)
        header_label.pack()

        # Button to check saved summaries
        check_saved_button = tk.Button(self.root, text="Check Saved Summary", command=self.show_saved_summary)
        check_saved_button.pack(pady=10)

        # Button to create a new summary
        create_summary_button = tk.Button(self.root, text="Create New Summary", command=self.create_new_summary)
        create_summary_button.pack(pady=10)

    # Show home window
    def show_home(self):
        self.root.update()
        self.root.deiconify()

    # Run the window
    def run(self):
        self.root.mainloop()


# Create an instance of HomeGUI and run it
def main():
    home_instance = HomeGUI()
    home_instance.run()


main()


