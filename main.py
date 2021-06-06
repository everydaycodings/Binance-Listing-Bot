from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support import expected_conditions as EC 
import time
import re
import datetime
from binance.client import Client
from binance.enums import *
from  datetime import datetime, timezone, date


ignored_word = "Cross Margin|Binance Launchpool|Isolated Margin|Innovation Zone|USDT-Margined|Trading Pairs|Stock Token"
previous_event = []
previous_event.append("giga")
asset_list = []
finding_asset_list = []
all_assest_list = []
asset_char = ["(", ")"]
asset = {}

try:

    api_key = "Your Binance API Key"
    api_secret = "Your Binance API Secret Key"
    client = Client(api_key, api_secret)
    
    # Uncomment this if you are using testing test api of Binance (https://testnet.binance.vision/)
    client.API_URL = 'https://testnet.binance.vision/api'


except:
    print("ERROR: Bot Couldnot get access to the Binance Account.")



while True:
   
   with webdriver.Firefox() as driver:
      wait = WebDriverWait(driver, 5)
      driver.get("https://www.binance.com/en/support/announcement/c-48?navId=48")


      latest_info = WebDriverWait(driver, 100).until( 
         EC.presence_of_element_located((By.CSS_SELECTOR, "a.css-1ej4hfo:nth-child(1)")) 
      )
      url = driver.find_element_by_css_selector("a.css-1ej4hfo:nth-child(1)").get_attribute("href")
      text = latest_info.text




   if text == previous_event[-1]:
      print("Previously Added Event")

   else:

      previous_event.append(text)
      # To get if ignored_word is there in the text string
      filtered_word = re.findall(ignored_word, text, flags=re.IGNORECASE)


      if filtered_word == []:
                                                                           
         latest_info_dec_click_link = driver.find_element_by_css_selector("a.css-1ej4hfo:nth-child(1)").click()

         get_dec = WebDriverWait(driver, 10).until( 
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.css-3fpgoh:nth-child(2) > span:nth-child(1)"))
         )
         listing_description = get_dec.text

         #print("{}\n[{}]".format(text, url))
         listing_asset = text.replace('Binance Will List ', '').split()
         last = str(listing_asset[-1])
         removed_char = re.sub('[^A-Za-z0-9 ]+', '', last)

         #BNBUSDT in List Form
         asset_list.append("{}USDT".format(removed_char))

         #BNB/USDT in List Form
         finding_asset_list.append("{}/USDT".format(removed_char))
         
         #BNB/USDT in str() form
         finding_asset = "{}/USDT".format(removed_char)

         #BNBUSDT in str() form
         conformed_listing_asset = "{}USDT".format(removed_char)
         
         # To get if ignored_word is there in the listing_description string
         filtered_asset = re.findall(finding_asset, listing_description, flags=re.IGNORECASE)

         print(filtered_asset)
         if filtered_asset == finding_asset_list:
            print(finding_asset,"Pair Found")

            #Date And time is stored in dictionry format in tradable_asset_with_time
            match = re.search('\d{4}-\d{2}-\d{2}', listing_description)
            date = datetime.datetime.strptime(match.group(), '%Y-%m-%d').date()
            asset[conformed_listing_asset] = str(date)
            print(asset)

         else:
            print("Not Found")


      else:
         print("Not a Spot Listing Event")

   today = date.today()
   todays_date = today.strftime("{}%y-%m-%d").format("20")
   

   asset_key = []
   asset_value = []

   for assetkey, assetvalue in asset.items():
      asset_key.append(assetkey)
      asset_value.append(asset_value)

   
   if todays_date in asset_value:

      while True:

         info = client.get_all_tickers()
         for i in info:
            all_assest_list.append(i["symbol"])

         if asset_key in all_assest_list:
            print("Bought", asset_key)
            print("sold")
         else:
            print("Not Yet Arrived")
            break


   else:
      print("Today Is Not A Day")
