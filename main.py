from datetime import datetime
import yfinance as yf
import logging
import csv
import os
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
        self.date_now=None
        self.valume=None
        self.averageVolume=None
        self.targetMeanPrice=None
        self.numberOfAnalystOpinions=None
        self.forwardPE=None
        self.epsForward=None
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
        self.date_now=datetime.now()
        self.valume=t.get("volume")
        self.averageVolume=t.get("averageVolume")
        self.targetMeanPrice=t.get("targetMeanPrice")
        self.numberOfAnalystOpinions=t.get("numberOfAnalystOpinions")
        self.forwardPE=t.get("forwardPE")
        self.epsForward=t.get("epsForward")
        
    def dic(self):
            return{
            "ティッカー": self.ticker,
            "現在値": self.price,
            "前日比": self.regularMarketChangePercent,
            "プレマーケット値": self.preMarketChangePercent,
            "時価総額": self.marketCap,
            "実績PER": self.trailingPE,
            "予想PER": self.forwardPE,
            "予想EPS": self.epsForward,
            "売上成長率": self.revenueGrowth,
            "営業利益率": self.operatingMargins,
            "出来高": self.valume,
            "平均出来高": self.averageVolume,
            "目標株価": self.targetMeanPrice,
            "アナリスト数": self.numberOfAnalystOpinions,
            "決算日": self.date,
            "記録日": self.date_now,
        }


        
    def print_info(self):
        print(f"{(self.ticker)}\n現在値:{(self.price)}\n前日比{change_none(self.regularMarketChangePercent)}\nプレマーケット値{change_none(self.preMarketChangePercent)}\n時価総額{change_none(self.marketCap)}\n実績PER{change_none(self.trailingPE)}\n売上成長率{change_none(self.revenueGrowth)}\n営業利益率{change_none(self.operatingMargins)}\n決算日{change_none(self.date)}")
def write_csv(rows):
    csv_file_path=r"C:\Users\shota\us_stock\stock.csv"
    file_exists=os.path.exists(csv_file_path)
    with open(csv_file_path,"a",encoding="UTF-8",newline="") as f:
        fieldnames = list(rows[0].keys())
        writer=csv.DictWriter(f,fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader
        for line in rows:
            writer.writerow(line)

def main():
    with open("tickers.txt",encoding="UTF-8") as f:
        all_info=[]
        for line in f:
            if line=="\n":
                continue
            try:
                ticker=line.strip().upper()
                stock=Stock(ticker)
                stock.fetch()
                info=stock.dic()
                all_info.append(info)

                stock.print_info()
            except NameError as e:
                print(e)
        print(all_info)
        write_csv(all_info)

            

if __name__=="__main__":
    main()