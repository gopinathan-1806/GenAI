from playwright.sync_api import sync_playwright
from datetime import datetime

print("Starting Playwright script...")
print("Script started at:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

with sync_playwright() as p:
    # Launch a new browser instance
    browser = p.chromium.launch(headless=False)  # Set headless=True for headless mode
    context = browser.new_context()
    page = context.new_page()

    # Navigate to Google
    print("Navigating to Google...")
    page.goto("https://www.cricbuzz.com/", wait_until="load")

    # Take a screenshot of the results page
    screenshot_path = f"playwright_search_results_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png"
    page.screenshot(path=screenshot_path)
    print(f"Screenshot saved to {screenshot_path}")

    # Close the browser
    browser.close()
