# Sentiment Analysis Project
This script scans through the posts of a given finance-related subreddit (particularly r/wallstreebets), detects all the mentioned stock tickers, and evaluates their sentiment based on the comment they belong to (negative becomes bearish and positive becomes bullish) using the nltk.sentiment.vader package.

### Results
<image src="/results/sentiment-analysis-small.PNG" />

### Notes
* The stock tickers used are from NASDAQ and NYSE. They can be found <a href="https://www.nasdaq.com/market-activity/stocks/screener?exchange=nasdaq&letter=0&render=download">here</a>.
* Each of the exchanges above have their corresponding csv file. Rename them to "nasdaq_tickers.csv" and "nyse_tickers.csv" respectively.
* The script also needs a praw.ini file with "[bot]" at the top of the file followed by the client_id and client_secret obtained from the reddit API site.
* Finally, it uses a file called "1-1000.txt" (1000 most frequently used words in english) found <a href="https://gist.github.com/deekayen/4148741">here</a>.
