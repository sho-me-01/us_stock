from datetime import datetime
import yfinance as yf
class Stock:
    def __init__(self,ticker):
        self.ticker=ticker
        self.price=None
        self.low_52w=None
        self.high_52w=None
    def fetch(self):
        t=yf.Ticker(self.ticker).info
        self.price=t.get("currentPrice")
        self.low_52w=t.get("fiftyTwoWeekLow")
        self.high_52w=t.get("fiftyTwoWeekHigh")
    def print_info(self):
        print(f"{self.ticker}\n現在値:{self.price}\n52週高値{self.high_52w}\n52週低値{self.low_52w}")

def main():
    with open("tickers.txt",encoding="UTF-8") as f:
        for line in f:
            ticker=line.strip()
            stock=Stock(ticker)
            stock.fetch()
            stock.print_info()

if __name__=="__main__":
    main()

