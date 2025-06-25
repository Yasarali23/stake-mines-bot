import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from telegram import Bot

# 🔧 CONFIGURATION
TELEGRAM_TOKEN = "7844013584:AAGIqhJ0RgoQC8VxcJ1VOd6WwyzB2CECTDo"
CHAT_ID = "@Yasarcjo"

URL = "https://stake.com/casino/games/mines"
CHROMEDRIVER_PATH = "./chromedriver"

def start_browser():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=options)
    driver.get(URL)
    print("✅ Stake Mines page opened.")
    return driver

def get_tile_states(driver):
    # NOTE: Update the selector as per actual Stake site. Below is an example!
    tile_elements = driver.find_elements("xpath", '//div[contains(@class,"tile")]')

    results = []
    for i, tile in enumerate(tile_elements):
        classes = tile.get_attribute("class")
        if "revealed" in classes and "bomb" in classes:
            results.append((i+1, "💣 Mine"))
        elif "revealed" in classes:
            results.append((i+1, "✅ Safe"))
        else:
            results.append((i+1, "🕳️ Hidden"))

    return results

def send_to_telegram(message):
    bot = Bot(token=TELEGRAM_TOKEN)
    bot.send_message(chat_id=CHAT_ID, text=message)

def main():
    driver = start_browser()
    print("⏳ Waiting for login...")
    time.sleep(30)  # Give user time to log in

    while True:
        try:
            tiles = get_tile_states(driver)
            msg = "🎮 *Stake Mines Live Status:*\n\n"
            for tile in tiles:
                msg += f"Tile {tile[0]} → {tile[1]}\n"
            send_to_telegram(msg)
            time.sleep(60)  # Wait 1 min
        except Exception as e:
            print("⚠️ Error:", e)
            break

if __name__ == "__main__":
    main()
