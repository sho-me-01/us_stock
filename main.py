from datetime import datetime
import yfinance as yf
import logging
logging.getLogger("yfinance").setLevel(logging.CRITICAL)
class Stock:
    def __init__(self,ticker):
        self.ticker=ticker
        self.price=None
        self.low_52w=None
        self.high_52w=None
    def fetch(self):
        t=yf.Ticker(self.ticker).info
        if None is t.get("currentPrice"):
            raise IndentationError(f"{self.ticker}は存在しないティッカーです")
        
        self.price=t.get("currentPrice")
        self.low_52w=t.get("fiftyTwoWeekLow")
        self.high_52w=t.get("fiftyTwoWeekHigh")
    def print_info(self):
        print(f"{self.ticker}\n現在値:{self.price}\n52週高値{self.high_52w}\n52週低値{self.low_52w}")

def main():
    with open("tickers.txt",encoding="UTF-8") as f:
        for line in f:
            if line=="\n":
                continue
            try:
                ticker=line.strip().upper()
                stock=Stock(ticker)
                stock.fetch()
                stock.print_info()
            except IndentationError as e:
                print(e)
if __name__=="__main__":
    main()

