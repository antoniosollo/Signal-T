import pandas as pd
import pandas_ta as ta
import ccxt
import requests
import time


def getEMA(exchange, crypto, timeframe):
    markets = exchange.load_markets()
    ohlcv = exchange.fetch_ohlcv(crypto, timeframe)

    if len(ohlcv):        
        ema = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']).ta.ema(200)

        return round(ema[499], 1)


def getCurrentValue(exchange, crypto):
    lastValue = exchange.fetchTicker(crypto)['last']
    return round(lastValue, 1)


if __name__ == "__main__":
    API_TOKEN = ""
    CHAT_ID = ""

    while True:
        exchange = ccxt.binance()
        timeframe = "1d"

        markets = exchange.load_markets()
        symbols = exchange.symbols

        crypto_list = []

        for crypto in symbols:
            if "USDT" in crypto:
                crypto_list.append(crypto)

        min_percentage = [1.0, -2.0]
        max_percentage = [2.0, -2.0]

        for crypto in crypto_list:
            try:
                ema = getEMA(exchange, crypto, timeframe)
                currentValue = getCurrentValue(exchange, crypto)

                ema_alert = f"EMA 200 {crypto}: {ema}"
                crypto_alert = f"Valore attuale {crypto}: {currentValue}"

                percentage = round((currentValue-ema)*100/ema, 1)

                if percentage >= min_percentage[0] and percentage <= max_percentage[0]:
                    alert = f"Il valore attuale di {crypto} è sopra all'EMA 200 del {percentage}%"
                    text_message = f"{ema_alert}\n{crypto_alert}\n\n{alert}"

                    requests.post(f"https://api.telegram.org/bot{API_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={text_message}")
                elif percentage >= max_percentage[1] and percentage <= max_percentage[1]:
                    alert = f"Il valore attuale di {crypto} è sotto all'EMA 200 del {percentage}%"
                    text_message = f"{ema_alert}\n{crypto_alert}\n\n{alert}"

                    requests.post(f"https://api.telegram.org/bot{API_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={text_message}")
            except:
                pass


        time.sleep(600)