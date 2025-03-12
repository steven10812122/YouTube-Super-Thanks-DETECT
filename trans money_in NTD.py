import time
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

VIDEO_URL = "your youtube video url"

def convert_to_twd(amount, currency):
    exchange_rates = {"USD": 32, "TWD": 1, "JPY": 0.22, "EUR": 35, "HKD": 8.2, "KRW": 0.026}
    return amount * exchange_rates.get(currency, 1)

def get_youtube_donations(video_url):
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    print("Opening YouTube page...")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(video_url)
    time.sleep(10)  # Ensure the page is fully loaded
    print("YouTube page loaded")

    donations = []
    last_height = driver.execute_script("return document.documentElement.scrollHeight")

    print("Scrolling the page to load all comments and Super Thanks content...")
    driver.execute_script("window.scrollTo(0, 500);")
    time.sleep(5)
    # Continue scrolling until the page height does not increase
    while True:
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(3)
        
        # Check the page height, stop scrolling if no new content is loaded
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    try:
        more_buttons = driver.find_elements(By.XPATH, "//yt-formatted-string[text()='Show more']")
        for button in more_buttons:
            button.click()
            time.sleep(3)
    except:
        pass
    
    # Scrape all Super Thanks amounts from comments
    comment_threads = driver.find_elements(By.CSS_SELECTOR, "ytd-comment-thread-renderer")
    
    for thread in comment_threads:
        try:
            # Attempt to find the Super Thanks amount in each comment
            donation_element = thread.find_element(By.CSS_SELECTOR, "span#comment-chip-price")
            donations.append(donation_element.text)
        except:
            pass  # Skip if the comment does not contain an amount
    
    driver.quit()
    
    print("Scraped Super Thanks donation amounts:")
    for donation in donations:
        print(donation)
    
    return donations

def extract_donations(donations):
    currency_totals = {
        "USD": 0,
        "TWD": 0,
        "JPY": 0,
        "EUR": 0,
        "HKD": 0,
        "KRW": 0
    }
    pattern = re.compile(r"(US\$|NT\$|¥|€|HK\$|₩|\$)\s?(\d+[,.]?\d*)")
    donation_data = []  # To store amount information
    
    for donation in donations:
        match = pattern.search(donation)
        if match:
            symbol = match.group(1)
            amount_str = match.group(2).replace(",", "")
            
            try:
                amount = float(amount_str)
            except ValueError:
                continue

            if symbol in ["$", "NT$"]:
                # Treat all "$" and "NT$" as New Taiwan Dollar (TWD)
                currency = "TWD"
            elif symbol in ["US$", "USD"]:
                currency = "USD"
            elif symbol == "¥":
                currency = "JPY"
            elif symbol == "€":
                currency = "EUR"
            elif symbol == "HK$":
                currency = "HKD"
            elif symbol == "₩":
                currency = "KRW"
            else:
                currency = "TWD"
            
            # Only convert non-TWD amounts
            if currency != "TWD":
                amount = convert_to_twd(amount, currency)
            
            currency_totals[currency] += amount
            # Save each amount
            donation_data.append({"Amount": amount, "Currency": currency})
    
    return currency_totals, donation_data

def save_to_excel(donation_data):
    # Use pandas to save to an Excel file
    df = pd.DataFrame(donation_data)
    df.to_excel("super_thanks_donations2.xlsx", index=False)
    print("Amounts have been saved to the Excel file: super_thanks_donations.xlsx")

if __name__ == "__main__":
    donations = get_youtube_donations(VIDEO_URL)
    currency_totals, donation_data = extract_donations(donations)
    
    print("Total Super Thanks donations by currency:")
    for currency, total in currency_totals.items():
        print(f"{currency}: {total:.2f}")
    
    total_twd = sum(currency_totals.values())  # Directly use the amounts already converted to TWD
    print(f"\nTotal amount (TWD): {total_twd:.2f}")
    
    # Save each amount to the Excel file
    save_to_excel(donation_data)
