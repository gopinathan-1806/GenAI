import pyautogui
import time
from datetime import datetime

import subprocess

subprocess.run([
    "screencapture",
    "excel_sheet.png"
])

pyautogui.FAILSAFE = True 
pyautogui.PAUSE = 0.5

print("Step 1: Opening the chrome browser")
time.sleep(2)

# Fix 1: Added interval to ensure macOS registers the shortcut     
pyautogui.hotkey('command', 'space', interval=0.1)
time.sleep(1)

# Fix 2: Added interval=0.1 to simulate human typing speed
pyautogui.write('chrome', interval=0.1)
time.sleep(1)

# Fix 3: Changed 'enter' to 'return' for Mac Spotlight compatibility
pyautogui.press('return')
time.sleep(3)

print("Step 2: Opening new tab and navigating to the URL")
time.sleep(2)

pyautogui.hotkey('command', 't')
time.sleep(1)
pyautogui.write('Amazon Share price', interval=0.1)
time.sleep(1)
pyautogui.press('return')
time.sleep(3)

print("Step 3: Copying the stock price")
time.sleep(2)

# pyautogui.moveTo(-500, 500, duration=1)
# pyautogui.doubleClick()
# time.sleep(1)
pyautogui.hotkey('command', 'a', interval=0.1)
time.sleep(3)
pyautogui.hotkey('command', 'c', interval=0.1)
time.sleep(2)

print("Step 4: Opening excel")
time.sleep(2)
pyautogui.hotkey('command', 'space', interval=0.1)
time.sleep(1)
pyautogui.write('excel', interval=0.1)
time.sleep(1)
pyautogui.press('return')
time.sleep(3)
pyautogui.press('return')  # Press return to open a new workbook
time.sleep(3)

print("Step 5: Creating new row in excel and pasting the stock price")
time.sleep(2)
pyautogui.write('Date', interval=0.1)
time.sleep(1)
pyautogui.press('tab')
time.sleep(1)
pyautogui.write('Stock Price', interval=0.1)
time.sleep(1)
pyautogui.press('tab')
time.sleep(1)
pyautogui.write('Comments', interval=0.1)
time.sleep(1)
pyautogui.press('return')
time.sleep(1)
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
pyautogui.write(current_time, interval=0.1)
time.sleep(1)
pyautogui.press('tab')
time.sleep(1)
pyautogui.hotkey('command', 'v')
time.sleep(1)
pyautogui.press('tab')
time.sleep(1)
pyautogui.write('Stock price copied from moneycontrol.com', interval=0.1)
time.sleep(3)
pyautogui.hotkey('command', 's')
time.sleep(1)
pyautogui.write('daily_report_2026-08-26.xlsx', interval=0.1)
time.sleep(2)
pyautogui.press('return')
time.sleep(2)

print("Step 6: Take a screenshot of the excel sheet")
time.sleep(2)
subprocess.run(["screencapture", "excel_sheet.png"])
