import os
import asyncio
import websockets
import signal
from transformers import pipeline
import alpaca_trade_api as tradeapi
from alpaca_trade_api import REST, Stream
from dotenv import load_dotenv

API_KEY= 'x7t5u2vq9p8t'
API_SECRET= 'ttq8j2kprfkhmjr86zfdefn3autke45wfqcp7wws3sqjz38kcxg2ruxbf8cfsqbf'

# Stream Client
stream_client = Stream(API_KEY, API_SECRET)

# Websocket 
async def echo(websocket):
    async for message in websocket:
        await websocket.send(message)

async def main():
    # Set the stop condition when receiving SIGTERM.
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)

    async with websockets.unix_serve(
        echo,
        path=f"{os.environ['SUPERVISOR_PROCESS_NAME']}.sock",
    ):
        await stop

if __name__ == "__main__":
    asyncio.run(main())
    
# Alpaca News 
async def news_data_handler(news):
    async with websockets.connect("wss://stream.data.alpaca.markets/v1beta1/news") as websocket:
        await websocket.send("Hello world!")
        await websocket.recv()
        print(news)

stream_client.subscribe_news(news_data_handler, "AAPL")

stream_client.run()

# Sentiment Analysis

# Classifier
classifier = pipeline('sentiment-analysis')

async def news_data_handler(news):
    
    summary = news.summary
    headline = news.headline

    relevant_text = summary + headline
    sentiment = classifier(relevant_text)
	
    if sentiment['label'] == 'POSITIVE' and sentiment['score'] > 0.95:
        rest_client.submit_order('AAPL', 100)
         
    elif sentiment['label'] == 'NEGATIVE' and sentiment['score'] > 0.95:
        rest_client.submit_order('AAPL', -100)

stream_client.subscribe_news(news_data_handler, 'AAPL')

stream_client.run()