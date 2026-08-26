"""
Stock Price Reporter — pyautogui automation (macOS)
----------------------------------------------------
Searches each company's share price on Google via Chrome,
copies the price, writes all 5 into a new Excel workbook,
saves it, and takes a screenshot.

Requirements:
    pip install pyautogui pyperclip pillow
    Microsoft Excel must be installed on this Mac.
"""

import pyautogui
import pyperclip
import subprocess
import time
from datetime import datetime

# ── settings ─────────────────────────────────────────────────────────────────
pyautogui.FAILSAFE = True   # move mouse to top-left corner to abort
pyautogui.PAUSE    = 0.4    # small global delay between every call

STOCKS = [
    ("Amazon",    "Amazon share price"),
    ("Google",    "Google share price"),
    ("Apple",     "Apple share price"),
    ("Microsoft", "Microsoft share price"),
    ("Nvidia",    "Nvidia share price"),
]

today      = datetime.now().strftime("%Y-%m-%d")
timestamp  = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
excel_file = f"stock_prices_{today}.xlsx"
screenshot = f"stock_prices_{today}.png"

# ── helper ────────────────────────────────────────────────────────────────────
def pause(seconds):
    time.sleep(seconds)

# ─────────────────────────────────────────────────────────────────────────────
# STEP 1 — Open Chrome
# ─────────────────────────────────────────────────────────────────────────────
print("Step 1: Opening Chrome ...")
pyautogui.hotkey('command', 'space', interval=0.1)
pause(1)
pyautogui.write('chrome', interval=0.1)
pause(1)
pyautogui.press('return')
pause(3)

# ─────────────────────────────────────────────────────────────────────────────
# STEP 2 — Fetch each stock price from Google
# ─────────────────────────────────────────────────────────────────────────────
prices = {}

for company, search_query in STOCKS:
    print(f"Step 2: Fetching price for {company} ...")

    # open a new tab and search
    pyautogui.hotkey('command', 't')
    pause(1)
    pyautogui.hotkey('command', 'l')   # focus address bar
    pause(0.5)
    pyautogui.hotkey('command', 'a')   # select any existing text
    pause(0.3)
    pyautogui.write(search_query, interval=0.08)
    pause(0.5)
    pyautogui.press('return')
    pause(4)   # wait for Google results to load

    # Google shows the price in a large element — click the address bar,
    # select all page text and copy it so we can parse the price from clipboard
    pyautogui.hotkey('command', 'a', interval=0.1)
    pause(1)
    pyautogui.hotkey('command', 'c', interval=0.1)
    pause(1)

    clipboard_text = pyperclip.paste()

    # Parse price: look for the first token that looks like a number (e.g. 185.23)
    price_value = "N/A"
    for token in clipboard_text.replace(',', '').split():
        # strip common currency symbols
        clean = token.lstrip('$£€').strip()
        try:
            float(clean)
            # accept only plausible share price range
            if 0.01 < float(clean) < 100000:
                price_value = clean
                break
        except ValueError:
            continue

    prices[company] = price_value
    print(f"  {company}: {price_value}")

# ─────────────────────────────────────────────────────────────────────────────
# STEP 3 — Open Excel
# ─────────────────────────────────────────────────────────────────────────────
print("Step 3: Opening Excel ...")
pyautogui.hotkey('command', 'space', interval=0.1)
pause(1)
pyautogui.write('excel', interval=0.1)
pause(1)
pyautogui.press('return')
pause(4)

# Press return/enter to dismiss any splash screen / open a blank workbook
pyautogui.press('return')
pause(3)

# ─────────────────────────────────────────────────────────────────────────────
# STEP 4 — Type the header row
# ─────────────────────────────────────────────────────────────────────────────
print("Step 4: Writing header row ...")

def type_cell(value, move_next='tab'):
    pyautogui.write(str(value), interval=0.08)
    pause(0.3)
    pyautogui.press(move_next)
    pause(0.3)

# Headers:  #  |  Company  |  Ticker  |  Price (USD)  |  Fetched At
type_cell('#')
type_cell('Company')
type_cell('Ticker')
type_cell('Price (USD)')
type_cell('Fetched At', move_next='return')

# ─────────────────────────────────────────────────────────────────────────────
# STEP 5 — Type one data row per stock
# ─────────────────────────────────────────────────────────────────────────────
print("Step 5: Writing stock data rows ...")

TICKERS = {
    "Amazon":    "AMZN",
    "Google":    "GOOGL",
    "Apple":     "AAPL",
    "Microsoft": "MSFT",
    "Nvidia":    "NVDA",
}

for idx, (company, _) in enumerate(STOCKS, start=1):
    ticker = TICKERS[company]
    price  = prices[company]
    print(f"  Writing row {idx}: {company} — {price}")

    type_cell(idx)
    type_cell(company)
    type_cell(ticker)
    type_cell(price)
    type_cell(timestamp, move_next='return')

# ─────────────────────────────────────────────────────────────────────────────
# STEP 6 — Save the workbook
# ─────────────────────────────────────────────────────────────────────────────
print("Step 6: Saving the workbook ...")
pyautogui.hotkey('command', 's')
pause(2)

# Type filename in the Save dialog
pyautogui.hotkey('command', 'a')   # clear any default name
pause(0.5)
pyautogui.write(excel_file, interval=0.08)
pause(1)
pyautogui.press('return')
pause(2)

# If Excel asks "Keep in xlsx format?" press Return to confirm
pyautogui.press('return')
pause(2)

print(f"  Saved as {excel_file}")

# ─────────────────────────────────────────────────────────────────────────────
# STEP 7 — Take a screenshot
# ─────────────────────────────────────────────────────────────────────────────
print("Step 7: Taking screenshot ...")
pause(1)
screen = pyautogui.screenshot()
screen.save(screenshot)
print(f"  Screenshot saved as {screenshot}")

print(f"\n✅  Done — {len(STOCKS)} stocks written to {excel_file}")
