# Sentiment Analysis Project
This script scans through the posts of a given finance-related subreddit (particularly r/wallstreebets), detects all the mentioned stock tickers, and evaluates their sentiment (negative becomes bearish and positive becomes bullish) using the nltk.sentiment.vader package.

### Results
<image src="/results/sentiment-analysis-small.PNG" />

### Notes
* The stock tickers used are from NASDAQ and NYSE. They can be found <a href="https://www.nasdaq.com/market-activity/stocks/screener?exchange=nasdaq&letter=0&render=download">here</a>.
