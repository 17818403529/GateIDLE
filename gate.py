import csv
import os
import wget
import gzip
import ccxt
from random import random
from urllib.error import HTTPError


class Gate:
    def __init__(self):
        self.dir = {
            "deals": "D://Data Source//deals",
            "klines": "D://Data Source//klines",
        }

    def download(self, year, month, market, biz="spot", _type="deals"):

        filename = "{}-{}{}.csv.gz".format(market, year, month)

        path = os.path.join(self.dir["deals"], filename)

        url = "https://download.gatedata.org/{}/{}/{}{}/{}".format(
            biz, _type, year, month, filename
        )

        try:
            wget.download(url, path)
            self.unzip(path)
            os.remove(path)
        except:
            pass

    def unzip(self, path):

        gz_file = gzip.GzipFile(path)

        unzipped = path.replace(".gz", "")
        with open(unzipped, "wb+") as file:
            file.write(gz_file.read())

        gz_file.close()
    
    def transform_klines(self, file_name):

        path = os.path.join(self.dir["deals"], file_name)

        with open(path, "r", newline="") as f:
            data = list(csv.reader(f))

        result = []
        current_ts = float(data[0][0]) // 60 * 60
        kline = [current_ts, float(data[0][2]), 0, float(data[0][2]), 0, 0]

        for i in data:
            if float(i[0]) - current_ts < 60:
                price, volume = float(i[2]), float(i[3])

                if price > kline[2]:  # high
                    kline[2] = price

                if price < kline[3]:  # low
                    kline[3] = price

                kline[4] = price  # close

                kline[5] += volume  # volume

            else:
                result.append(kline)
                current_ts = float(i[0]) // 60 * 60
                kline = [current_ts, float(i[2]), 0, float(i[2]), 0, 0]

        path = os.path.join(self.dir["klines"], file_name)
        with open(path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(result)

def find_high_volumes():
    
    exchange = ccxt.gateio()
    tickers = exchange.fetch_tickers()

    markets = []

    for i in tickers.keys():
        if i.split("/")[1] == "USDT":
            ticker = tickers[i]
            if ticker["quoteVolume"] > 1e6:
                markets.append(i.replace("/","_"))
    
    return markets

def foo():
    gt = gate.Gate()
    
    year = 2024
    for market in find_high_volumes():
        if random() > 0.9:
            for month in ["01", "02", "03", "04", "05", "06"]:
                if random() > 0.3:
                    gt.download(year, month, market)
                    try:
                        gt.transform_klines("{}-{}{}.csv".format(market, year, month))
                    except:
                        pass

if __name__ == "__main__":
    gate = Gate()
    print(gate.dir)

