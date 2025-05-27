from flask import Flask, render_template_string, request, redirect, url_for
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import threading
import time

app = Flask(__name__)

# Replace these with your Olymp Trade credentials
OLYMP_TRADE_EMAIL = 'your_email@example.com'
OLYMP_TRADE_PASSWORD = 'your_password'

# Simple HTML template for the web UI
HTML_TEMPLATE = '''
<!doctype html>
<title>Olymp Trade Bot</title>
<h2>Olymp Trade Bot</h2>
<form method=post>
  <label for="coin">Select Coin:</label>
  <select name="coin" id="coin">
    <option value="BTCUSD">BTC/USD</option>
    <option value="ETHUSD">ETH/USD</option>
    <option value="LTCUSD">LTC/USD</option>
  </select><br><br>
  <label for="amount">Trade Amount (USD):</label>
  <input type="number" id="amount" name="amount" min="1" required><br><br>
  <input type="submit" value="Start Trading">
</form>
<p>{{ message }}</p>
'''

def run_bot(coin, amount):
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Open Olymp Trade login page
        driver.get("https://olymptrade.com/en/login")

        time.sleep(3)  # Wait for page to load

        # Login
        email_input = driver.find_element(By.NAME, "email")
        password_input = driver.find_element(By.NAME, "password")
        email_input.send_keys(OLYMP_TRADE_EMAIL)
        password_input.send_keys(OLYMP_TRADE_PASSWORD)

        login_button = driver.find_element(By.XPATH, "//button[contains(text(),'Log in')]")
        login_button.click()

        time.sleep(5)  # Wait for login to complete

        # Navigate to the trading page for the selected coin
        # This URL pattern may change; adjust accordingly
        trade_url = f"https://olymptrade.com/en/trade/{coin}"
        driver.get(trade_url)

        time.sleep(5)  # Wait for trading page to load

        # Set trade amount
        amount_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Amount']")
        amount_input.clear()
        amount_input.send_keys(str(amount))

        # Example: Place a "Call" trade (buy)
        call_button = driver.find_element(By.CSS_SELECTOR, "button[data-test='call-button']")
        call_button.click()

        # Wait to observe the trade
        time.sleep(10)

    except Exception as e:
        print(f"Error in bot: {e}")
    finally:
        driver.quit()

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''
    if request.method == 'POST':
        coin = request.form['coin']
        amount = request.form['amount']

        # Run the bot in a separate thread to avoid blocking Flask
        threading.Thread(target=run_bot, args=(coin, amount), daemon=True).start()
        message = f"Started trading {coin} with amount ${amount}."

    return render_template_string(HTML_TEMPLATE, message=message)

if __name__ == '__main__':
    app.run(debug=True)
