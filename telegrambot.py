import logging
import requests
import bs4
from requests import Session
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Start Command
def start(update, context):
    update.message.reply_text('I am ready, ser...')

# Help Command
def help(update, context):
    update.message.reply_text("""/bagprice - Shows the current price of your bags, ser...
/ethgas - Shows the current Ethereum gas in gwei, ser...
/feargreed - Shows the current Fear and Greed index, ser...""")

# Price Command
def bagprice(update, context):

    # CMC API Info
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = {
    'symbol':'BTC,ETH,DRIP',
    }
    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': 'ENTER API KEY',
    }

    #CMC API Grab
    session = Session()
    session.headers.update(headers)
    response = session.get(url, params=parameters).json()
    btc = str(round(response['data']['BTC']['quote']['USD']['price'],2))
    eth = str(round(response['data']['ETH']['quote']['USD']['price'],2))
    drip = str(round(response['data']['DRIP']['quote']['USD']['price'],2))

    #Print Prices
    update.message.reply_text("YOUR BAGS, SER:\nBTC = $" + btc + "\nETH = $" + eth + "\nDRIP = $" + drip)

# Eth Gas Command
def ethgas(update, context):

    # Convert webpage to lxml
    url = requests.get("https://www.coinmarketcap.com")
    soup = bs4.BeautifulSoup(url.text,"lxml")

    # Element Data
    gas_var = soup.select("div>span>span>a")

    # Print Eth Gas
    update.message.reply_text(f'Ethereum Gas is Currently: {gas_var[0].getText()}')

# Fear / Greed Index Command
def feargreed(update, context):

    # FGI API Info
    url = 'https://fear-and-greed-index.p.rapidapi.com/v1/fgi'
    headers = {
    'X-RapidAPI-Host': 'fear-and-greed-index.p.rapidapi.com',
    'X-RapidAPI-Key': 'ENTER API KEY'
    }

   #FGI API Grab
    response = requests.request("GET", url, headers=headers).json()
    sentiment = response['fgi']['now']['valueText']
    value = str(response['fgi']['now']['value'])

    # Print FG Index
    update.message.reply_text("Sentiment: " + sentiment + "\nValue: " + value)
    
# Log Error Function
def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater("ENTER API KEY", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("bagprice", bagprice))
    dp.add_handler(CommandHandler("ethgas", ethgas))
    dp.add_handler(CommandHandler("feargreed", feargreed))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
