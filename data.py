import pandas

data_nasdaq = pandas.read_csv("nasdaq_tickers.csv")
data_nyse = pandas.read_csv("nyse_tickers.csv")

# stock symbols
symbols = data_nasdaq["Symbol"].tolist() + data_nyse["Symbol"].tolist()

# some stock symbols have the same name as some words
words_to_ignore = [
    "I",
    "FANG",
    "FUND",
    "HALO",
    "LIFE",
    "NEO",
    "NEXT",
    "PLUS",
    "RICK",
    "RAIL",
    "TEAM",
    "UK",
    "UNIT",
    "VERB",
    "SAIL",
    "COLD",
    "FUN",
    "GOLD",
]

# either -1 or 1
financial_lexicon = {
    # source: https://www.investopedia.com/wallstreetbets-slang-and-memes-5111311
    "bear": -1,
    "tendies": 1,
    "moon": 1,
    "diamond": 1,
    "paper": -1,
    "YOLO": 1,
    "apes": 1,
    # source: https://www.wallstreetbets.shop/blogs/news/dissecting-the-unique-lingo-and-terminology-used-in-the-subreddit-r-wallstreetbets
    "bearish": -1,
    "bullish": 1,
    "BTFD": 1,
    "DD": 1,
    "GUH": -1,
    "rocket": 1,
    "pump": 1,
    "dump": 1,
    "stonks": -1,
    "💎": 1,
    # other
    "buy": 1,
    "sell": -1,
    "long": 1,
    "short": -1,
    "call": 1,
    "put": -1,
    "close": -1,

}