# us_stock

米国株の銘柄リストを読み込んで、株価や指標をまとめて取得し、CSVに1日1回記録していくツールです。
自分で銘柄を見るときに、毎回いろいろなサイトを開かなくて済むように作りました。

## できること

- `tickers.txt` に書いた銘柄の情報を [yfinance](https://github.com/ranaroussi/yfinance) で取得
- 現在値・前日比・時価総額・PER・売上成長率・営業利益率・決算日などをターミナルに表示
- 取得した値を `stock.csv` に追記（同じ日に2回実行しても重複して記録しない）
- 存在しないティッカーや空行、小文字の入力があっても止まらずに続ける

## 使い方

Python 3.10以上を想定しています。

```bash
git clone https://github.com/sho-me-01/us_stock.git
cd us_stock
python -m venv .venv
# Windows: .venv\Scripts\activate
# Mac/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

`tickers.txt` に1行1銘柄でティッカーを書きます。

```
NVDA
AAPL
MSFT
QQQ
```

実行します。

```bash
python main.py
```

## 出力の例

ターミナルにはこのように表示されます（数値は例です）。

```
NVDA
現在値:180.5
前日比:1.23
プレマーケット値:不明
時価総額:4400000000000
実績PER:52.1
売上成長率:0.56
営業利益率:0.6
決算日:2026-11-20 06:20:00
```

同時に、`main.py` と同じフォルダの `stock.csv` に1銘柄1行で追記されます。
取れなかった項目は、表示では「不明」、CSVでは空欄になります。

## 構成

```
main.py         取得・表示・CSV書き込み
tickers.txt     取得したい銘柄のリスト
requirements.txt
```

`main.py` の中は、取得と表示を `Stock` クラス、CSVへの書き込みを `write_csv()` に分けています。
表示用には「不明」に置き換えた値、CSVには元の値を使うようにして、あとで分析しやすくしています。

## 今後やりたいこと

- GitHub Actionsで毎日自動で実行して、データを貯める
- 貯めたデータをpandasで集計・グラフ化する
- そのデータで株価の予測モデルを作り、「前日と同じ値」という単純な予測より当たるのかを確かめる

## 注意

取得したデータは参考用で、投資の判断を勧めるものではありません。
