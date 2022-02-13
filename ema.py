import pandas as pd
import pandas_ta as ta
import ccxt
import requests
import time


def getEMA(exchange, crypto, timeframe, ema_type):
    markets = exchange.load_markets()
    ohlcv = exchange.fetch_ohlcv(crypto, timeframe)

    if len(ohlcv):        
        ema = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']).ta.ema(ema_type)

        return round(ema[499], 1)


def getCurrentValue(exchange, crypto):
    lastValue = exchange.fetchTicker(crypto)['last']
    return round(lastValue, 1)


if __name__ == "__main__":
    API_TOKEN = "5238732669:AAGFh7DY3d6vY-07coOzSPw8RWNBSCVoldQ"
    CHAT_ID = "-1001685587560"

    while True:
        exchange = ccxt.binance()
        timeframe = "1d"
        ema_type = 5

        markets = exchange.load_markets()
        symbols = exchange.symbols

        crypto_list = []

        for crypto in symbols:
            if "USDT" in crypto:
                crypto_list.append(crypto)

        min_percentage = [1.5, -1.5]
        max_percentage = [2.5, -2.5]

        for crypto in crypto_list:
            try:
                ema = getEMA(exchange, crypto, timeframe, ema_type)
                currentValue = getCurrentValue(exchange, crypto)

                ema_alert = f"EMA {ema_type} {crypto}: {ema}"
                crypto_alert = f"Valore attuale {crypto}: {currentValue}"

                print(f"\n{ema_alert}\n{crypto_alert}\n")

                if not ema == 0:
                    percentage = round((currentValue-ema)*100/ema, 1)

                if percentage >= min_percentage[0] and percentage <= max_percentage[0]:
                    alert = f"Il valore attuale di {crypto} ({currentValue}) è sopra all'EMA {ema_type} ({ema}) del {percentage}%"
                    
                    requests.post(f"https://api.telegram.org/bot{API_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={alert}")
                elif percentage >= max_percentage[1] and percentage <= max_percentage[1]:
                    alert = f"Il valore attuale di {crypto} ({currentValue}) è sotto all'EMA {ema_type} ({ema}) del {percentage}%"

                    requests.post(f"https://api.telegram.org/bot{API_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={alert}")
            except Exception as e:
                pass


        time.sleep(600)