import yfinance as yf
import pandas_ta as ta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Step 1: Fetch market data and detect pattern
data = yf.download("EURUSD=X", period="1d", interval="5m")
data['SMA_short'] = ta.sma(data['Close'], length=3)
data['SMA_long'] = ta.sma(data['Close'], length=5)

if data['SMA_short'].iloc[-2] < data['SMA_long'].iloc[-2] and data['SMA_short'].iloc[-1] > data['SMA_long'].iloc[-1]:
    signal = 'buy'
elif data['SMA_short'].iloc[-2] > data['SMA_long'].iloc[-2] and data['SMA_short'].iloc[-1] < data['SMA_long'].iloc[-1]:
    signal = 'sell'
else:
    signal = 'hold'

print(f"Trade signal: {signal}")

# Step 2: Automate Olymp Trade login and trade simulation
driver = webdriver.Chrome()  # Or specify path: webdriver.Chrome(executable_path='path_to_chromedriver')
try:
    driver.get("https://olymptrade.com/")
    time.sleep(5)

    # Click login button to open login form
    login_button = driver.find_element(By.XPATH, "//button[contains(text(),'Log in')]")
    login_button.click()
    time.sleep(3)

    # Enter credentials (replace with your demo account credentials)
    email_input = driver.find_element(By.NAME, "email")
    email_input.send_keys("your_email@example.com")
    password_input = driver.find_element(By.NAME, "password")
    password_input.send_keys("your_password")
    password_input.send_keys(Keys.RETURN)
    time.sleep(10)  # Wait for login and dashboard load

    # Based on signal, click buy or sell button (update selectors as needed)
    if signal == 'buy':
        buy_button = driver.find_element(By.CSS_SELECTOR, ".buy-button-selector")
        buy_button.click()
        print("Buy trade placed")
    elif signal == 'sell':
        sell_button = driver.find_element(By.CSS_SELECTOR, ".sell-button-selector")
        sell_button.click()
        print("Sell trade placed")
    else:
        print("No trade placed")

    time.sleep(5)

finally:
    driver.quit()
