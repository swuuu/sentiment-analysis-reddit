from data import *
import operator
import pandas as pd
import matplotlib.pyplot as plt
import praw
from nltk.sentiment.vader import SentimentIntensityAnalyzer


class SentimentAnalysisReddit:

    reddit = praw.Reddit("bot", user_agent="bot user agent")  # create reddit instance
    tickers = {}  # the number of occurrence of each stock ticker encountered in the subreddit
    tickers_sorted = {}  # the stock tickers but sorted in descending order by number of occurrence
    comments_of_word = {}  # for each word (key), add a list of all the comments it was found in

    def __init__(self, upvote_ratio, upvotes, subreddit_name, flairs_to_ignore, cutoff):
        """
        Creates a SentimentAnalysisReddit object
        Note 1: the sentiment analysis is mainly oriented for r/wallstreetbets
        Note 2: this class analyzes the top 10 hottest submissions of the subreddit
        although other finance related subreddits can be used as well
        :param upvote_ratio: posted will be considered
        if its upvote ratio exceeds upvote_ratio
        :param upvotes: number of upvotes needed for a comment to be
        considered
        :param subreddit_name: the subreddit of interest
        :param flairs_to_ignore: any flairs to ignore
        :param cutoff: cutoff for the list of most frequent words
        """
        self.upvote_ratio = upvote_ratio
        self.upvotes = upvotes
        self.subreddit_name = subreddit_name
        self.flairs_to_ignore = flairs_to_ignore
        self.cutoff = cutoff
        self.subreddit = self.reddit.subreddit(subreddit_name)
        self.count_ticker_frequency()

    def count_ticker_frequency(self):
        """
        Helper function for sentiment_analysis
        Scans through the top 10 hottest submissions of a subreddit
        For each submission, this parses the post's body and comments (top-level and 10 inner-comments)
        into words, counts the number of occurrences of a word being a ticker symbol (self.tickers),
        and stores the comment containing the occurrence in self.comment_of_words
        :return: None
        """
        # loop through the posts
        for submission in self.subreddit.hot(limit=10):

            # loop through each word in the submission body
            submission_body = submission.selftext
            words = submission_body.split(" ")
            for word in words:
                word = word.replace("$", "")
                # counting tickers
                if word.isupper() and word in self.tickers and word not in words_to_ignore:
                    self.tickers[word] += 1
                    self.comments_of_word[word].append(submission_body)
                elif word.isupper() and word not in words_to_ignore:
                    self.tickers[word] = 1
                    self.comments_of_word[word] = [submission_body]

            # loop through each comment
            submission.comment_sort = "new"
            comments = submission.comments
            submission.comments.replace_more(limit=10)  # resolve "MoreComments"
            for comment in comments:
                if comment.score > self.upvotes:
                    words = comment.body.split(" ")  # split into words
                    for word in words:
                        word = word.replace("$", "")
                        # counting tickers
                        if word.isupper() and word in self.tickers and word not in words_to_ignore:
                            self.tickers[word] += 1
                            self.comments_of_word[word].append(comment.body)
                        elif word.isupper() and word not in words_to_ignore:
                            self.tickers[word] = 1
                            self.comments_of_word[word] = [comment.body]

        # sort the symbols in reverse order of their frequency
        self.tickers_sorted = dict(sorted(self.tickers.items(), key=operator.itemgetter(1), reverse=True))

    def sentiment_analysis(self):
        """
        Plots the sentiment scores for each top self.top_cutoff stock symbols encountered
        using nltk.sentiment.vader
        The left-most stock symbol on the graph corresponds to the most frequent, and the right-most is the least
        frequent (last in self.cutoff)
        Negative maps to bearish, and positive maps to bullish
        The lexicon is updated with specific terms from r/wallstreetbets
        :return: None
        """
        analyzer = SentimentIntensityAnalyzer()
        analyzer.lexicon.update(financial_lexicon)
        scores = {}
        top_symbols = list(self.tickers_sorted.keys())[0:self.cutoff]  # get the most frequent mentioned stocks
        for symbol in top_symbols:
            # get the score for the symbol
            list_of_comments = self.comments_of_word[symbol]
            for a_comment in list_of_comments:
                score = analyzer.polarity_scores(a_comment)
                if symbol in scores:
                    for key, _ in score.items():
                        scores[symbol][key] += score[key]  # update the scores
                else:
                    scores[symbol] = score  # add to the dictionary
            # computing the average
            for sentiment, score in scores[symbol].items():
                scores[symbol][sentiment] = score / len(self.comments_of_word[symbol])

        df = pd.DataFrame.from_dict(scores)
        df = df.T
        df = df.drop(labels="compound", axis=1)
        df.plot(kind="bar", title=f"Sentiment analysis of the top {self.cutoff} stocks:", xlabel="stocks",
                ylabel="sentiment score (probability)")
        plt.legend(["Bearish", "Neutral", "Bullish"])
        plt.show()

    def plot_frequency_of_tickers(self, top_cutoff):
        """
        Plots the frequency of each stock ticker encountered and plots its bar graph
        :param top_cutoff: cutoff of the most frequently used tickers
        :return: None
        """
        most_frequent = {}
        counter = 0
        for key, value in self.tickers_sorted.items():
            if counter > top_cutoff:
                break
            most_frequent[key] = value
            counter += 1

        # plotting
        df = pd.DataFrame(most_frequent.items(), columns=["stock ticker", "count"], index=most_frequent.keys())
        df.plot(kind="bar", title=f"Top {top_cutoff} most frequently encountered stock tickers", xlabel="stock ticker",
                ylabel="count")
        plt.show()

    def plot_most_frequently_used_words(self, top_cutoff):
        """
        Get the top_cutoff most frequently used words on the subreddit and plots its bar graph
        Used to identify the common jargon of r/wallstreetbets
        :param top_cutoff: cutoff of the most frequently used words
        :return: None
        """
        word_count = {}  # for the most frequently used words
        # counting frequency of words
        for submission in self.subreddit.hot(limit=10):
            comments = submission.comments
            submission.comment_sort = "new"
            submission.comments.replace_more(limit=10)  # resolve "MoreComments"
            for comment in comments:
                if comment.score > self.upvotes:
                    words = comment.body.split(" ")
                    for word in words:
                        if word not in word_count and word.isupper():
                            word_count[word] = 0
                        elif word in word_count:
                            word_count[word] += 1

        # plotting most frequently used words
        submission_sorted = dict(sorted(word_count.items(), key=operator.itemgetter(1), reverse=True))

        # get the top_cutoff
        most_frequent = {}
        counter = 0
        for key, value in submission_sorted.items():
            if counter > top_cutoff:
                break
            most_frequent[key] = value
            counter += 1

        # plotting
        df = pd.DataFrame(most_frequent.items(), index=most_frequent.keys())
        df.plot(kind="bar", title=f"Top {top_cutoff} most frequently used words", xlabel="stock ticker",
                ylabel="count")
        plt.show()


if __name__ == "__main__":
    wsb_sentiment_analysis = SentimentAnalysisReddit(0.7, 2, "wallstreetbets", ["Meme"], 5)
    # wsb_sentiment_analysis.sentiment_analysis()
    # wsb_sentiment_analysis.plot_frequency_of_tickers(10)
    # wsb_sentiment_analysis.plot_most_frequently_used_words(50)
