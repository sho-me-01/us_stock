from datetime import datetime
from pathlib import Path
import csv
import logging

import yfinance as yf

logging.getLogger("yfinance").setLevel(logging.CRITICAL)

# 実行する場所に関係なく、main.pyと同じフォルダのファイルを使う
BASE_DIR = Path(__file__).resolve().parent
TICKERS_PATH = BASE_DIR / "tickers.txt"
CSV_PATH = BASE_DIR / "stock.csv"


def change_none(value):
    if value is None:
        return "不明"
    return value


class Stock:
    def __init__(self, ticker):
        self.ticker = ticker
        self.price = None
        self.regularMarketChangePercent = None
        self.preMarketChangePercent = None
        self.marketCap = None
        self.trailingPE = None
        self.revenueGrowth = None
        self.operatingMargins = None
        self.date = None
        self.date_now = None
        self.volume = None
        self.averageVolume = None
        self.targetMeanPrice = None
        self.numberOfAnalystOpinions = None
        self.forwardPE = None
        self.epsForward = None

    def fetch(self):
        t = yf.Ticker(self.ticker).info
        # ETFはcurrentPriceがないことがあるのでregularMarketPriceも見る
        self.price = t.get("currentPrice") or t.get("regularMarketPrice")
        if self.price is None:
            raise ValueError(f"{self.ticker}は存在しないティッカーです")
        self.regularMarketChangePercent = t.get("regularMarketChangePercent")
        self.preMarketChangePercent = t.get("preMarketChangePercent")
        self.marketCap = t.get("marketCap")
        self.trailingPE = t.get("trailingPE")
        self.revenueGrowth = t.get("revenueGrowth")
        self.operatingMargins = t.get("operatingMargins")
        # ETFなど決算日がない銘柄はNoneのままにする
        earnings = t.get("earningsTimestamp")
        if earnings is not None:
            self.date = datetime.fromtimestamp(earnings)
        self.date_now = datetime.now()
        self.volume = t.get("volume")
        self.averageVolume = t.get("averageVolume")
        self.targetMeanPrice = t.get("targetMeanPrice")
        self.numberOfAnalystOpinions = t.get("numberOfAnalystOpinions")
        self.forwardPE = t.get("forwardPE")
        self.epsForward = t.get("epsForward")

    def dic(self):
        return {
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
            "出来高": self.volume,
            "平均出来高": self.averageVolume,
            "目標株価": self.targetMeanPrice,
            "アナリスト数": self.numberOfAnalystOpinions,
            "決算日": self.date,
            "記録日": self.date_now,
        }

    def print_info(self):
        print(
            f"{self.ticker}\n"
            f"現在値:{self.price}\n"
            f"前日比:{change_none(self.regularMarketChangePercent)}\n"
            f"プレマーケット値:{change_none(self.preMarketChangePercent)}\n"
            f"時価総額:{change_none(self.marketCap)}\n"
            f"実績PER:{change_none(self.trailingPE)}\n"
            f"売上成長率:{change_none(self.revenueGrowth)}\n"
            f"営業利益率:{change_none(self.operatingMargins)}\n"
            f"決算日:{change_none(self.date)}"
        )


def recorded_today(csv_path):
    """今日の記録日の行がすでにCSVにあるか調べる"""
    if not csv_path.exists():
        return False
    today_date = datetime.today().date()
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for line in reader:
            date = datetime.fromisoformat(line["記録日"]).date()
            if date == today_date:
                return True
    return False


def write_csv(rows, csv_path=CSV_PATH):
    if not rows:
        print("書き込むデータがありません")
        return False
    if recorded_today(csv_path):
        print("記録済み")
        return False

    file_exists = csv_path.exists()
    with open(csv_path, "a", encoding="utf-8", newline="") as f:
        fieldnames = list(rows[0].keys())
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        for line in rows:
            writer.writerow(line)
    return True


def main():
    all_info = []
    with open(TICKERS_PATH, encoding="utf-8") as f:
        for line in f:
            ticker = line.strip().upper()
            if not ticker:
                continue
            try:
                stock = Stock(ticker)
                stock.fetch()
                all_info.append(stock.dic())
                stock.print_info()
            except ValueError as e:
                print(e)
    write_csv(all_info)


if __name__ == "__main__":
    main()
