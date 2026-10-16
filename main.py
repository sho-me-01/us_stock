from datetime import datetime
import yfinance as yf
import logging
logging.getLogger("yfinance").setLevel(logging.CRITICAL)
def change_none(title):
    if title is None:
        title="不明"
        return title
    else:
            return title
class Stock:
    def __init__(self,ticker):
        self.ticker=ticker
        self.price=None
        self.regularMarketChangePercent=None
        self.preMarketChangePercent=None
        self.marketCap=None
        self.trailingPE=None
        self.revenueGrowth=None
        self.operatingMargins=None
        self.date=None
    def fetch(self):
        t=yf.Ticker(self.ticker).info
        self.price=t.get("currentPrice")
        if None is t.get("currentPrice"):
            raise NameError(f"{self.ticker}\n{self.ticker}は存在しないティッカーです")
        self.regularMarketChangePercent=t.get("regularMarketChangePercent")
        self.preMarketChangePercent=t.get("preMarketChangePercent")
        self.marketCap=t.get("marketCap")
        self.trailingPE=t.get("trailingPE")
        self.revenueGrowth=t.get("revenueGrowth")
        self.operatingMargins=t.get("operatingMargins")
        self.date=datetime.fromtimestamp(t.get("earningsTimestamp"))
        
    def print_info(self):
        print(f"{(self.ticker)}\n現在値:{(self.price)}\n前日比{change_none(self.regularMarketChangePercent)}\nプレマーケット値{change_none(self.preMarketChangePercent)}\n時価総額{change_none(self.marketCap)}\n実績PER{change_none(self.trailingPE)}\n売上成長率{change_none(self.revenueGrowth)}\n営業利益率{change_none(self.operatingMargins)}\n決算日{change_none(self.date)}")

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
            except NameError as e:
                print(e)
if __name__=="__main__":
    main()

