import time
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

VIDEO_URL = "your yt url"

def convert_to_base_currency(amount, currency, base_currency):
    # This function converts a given amount from a foreign currency to the base currency
    exchange_rates = {
        "USD": {"TWD": 32, "JPY": 110, "EUR": 0.92, "HKD": 7.8, "KRW": 1200},
        "TWD": {"USD": 0.031, "JPY": 3.42, "EUR": 0.029, "HKD": 0.24, "KRW": 37.5},
        "JPY": {"USD": 0.0091, "TWD": 0.29, "EUR": 0.0084, "HKD": 0.071, "KRW": 10.91},
        "EUR": {"USD": 1.09, "TWD": 34.5, "JPY": 119.05, "HKD": 8.44, "KRW": 131.52},
        "HKD": {"USD": 0.13, "TWD": 4.17, "JPY": 14.19, "EUR": 0.12, "KRW": 15.57},
        "KRW": {"USD": 0.00083, "TWD": 0.026, "JPY": 0.092, "EUR": 0.0076, "HKD": 0.064},
    }
    
    # If base currency and the given currency are the same, no conversion needed
    if currency == base_currency:
        return amount

    # Perform conversion if exchange rate is available
    if base_currency in exchange_rates[currency]:
        return amount * exchange_rates[currency][base_currency]
    
    return amount  # If no conversion is possible, return the original amount

def detect_base_currency_from_language(lang):
    # Ensure the lang variable is in full format like 'ja-JP', 'zh-Hant-TW', etc.
    if lang == "zh-Hant-TW":  # Traditional Chinese (Taiwan)
        return "TWD"
    elif lang == "en-US":  # English (United States)
        return "USD"
    elif lang == "ja-JP":  # Japanese (Japan)
        return "JPY"
    elif lang == "ko-KR":  # Korean (South Korea)
        return "KRW"
    elif lang == "de-DE":  # German (Germany)
        return "EUR"
    elif lang == "fr-FR":  # French (France)
        return "EUR"
    elif lang == "es-ES":  # Spanish (Spain)
        return "EUR"
    elif lang == "pt-BR":  # Portuguese (Brazil)
        return "BRL"
    elif lang == "ru-RU":  # Russian (Russia)
        return "RUB"
    elif lang == "it-IT":  # Italian (Italy)
        return "EUR"
    elif lang == "ar-SA":  # Arabic (Saudi Arabia)
        return "SAR"
    elif lang == "hi-IN":  # Hindi (India)
        return "INR"
    # Add more language cases as needed
    return "USD"  # Default to USD if no match


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
    
    # Get the lang attribute from the <html> tag to detect language
    lang = driver.execute_script("return document.documentElement.lang")
    print(f"Detected language: {lang}")
    
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
    
    return donations, lang

def extract_donations(donations, base_currency):
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

            # Determine currency based on symbol
            if symbol in ["$", "NT$"]:
                currency = "TWD"  # If symbol is $ or NT$, treat as TWD
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

            # Convert the amount to the base currency
            converted_amount = convert_to_base_currency(amount, currency, base_currency)
            currency_totals[base_currency] += converted_amount  # Add converted amount to base currency total
            # Save each amount
            donation_data.append({"Amount": converted_amount, "Currency": base_currency})
    
    return currency_totals, donation_data

def save_to_excel(donation_data):
    # Use pandas to save to an Excel file
    df = pd.DataFrame(donation_data)
    df.to_excel("super_thanks_donations_converted.xlsx", index=False)
    print("Amounts have been saved to the Excel file: super_thanks_donations_converted.xlsx")

if __name__ == "__main__":
    donations, lang = get_youtube_donations(VIDEO_URL)
    base_currency = detect_base_currency_from_language(lang)  # Adjust this dynamically based on detected language
    currency_totals, donation_data = extract_donations(donations, base_currency)
    
    print(f"\nTotal Super Thanks donations by currency (converted to {base_currency}):")
    for currency, total in currency_totals.items():
        print(f"{currency}: {total:.2f}")
    
    total_base_currency = sum(currency_totals.values())  # Sum based on the base currency
    print(f"\nTotal amount ({base_currency}): {total_base_currency:.2f}")
    
    # Save each amount to the Excel file
    save_to_excel(donation_data)
