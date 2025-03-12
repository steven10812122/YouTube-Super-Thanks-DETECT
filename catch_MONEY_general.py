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
        "USD": {"TWD": 32, "JPY": 110, "EUR": 0.92, "HKD": 7.8, "KRW": 1200, "MXN": 17, "BRL": 5, "RUB": 90, "INR": 83, "IDR": 15500, "THB": 35, "TRY": 31, "PLN": 4.3, "VND": 25000, "PHP": 55},
        "TWD": {"USD": 0.031, "JPY": 3.42, "EUR": 0.029, "HKD": 0.24, "KRW": 37.5, "MXN": 0.53, "BRL": 0.16, "RUB": 2.8, "INR": 2.6, "IDR": 480, "THB": 1.1, "TRY": 1, "PLN": 0.13, "VND": 770, "PHP": 1.7},
        "JPY": {"USD": 0.0091, "TWD": 0.29, "EUR": 0.0084, "HKD": 0.071, "KRW": 10.91, "MXN": 0.16, "BRL": 0.046, "RUB": 0.82, "INR": 0.75, "IDR": 140, "THB": 0.32, "TRY": 0.28, "PLN": 0.035, "VND": 210, "PHP": 0.47},
        "EUR": {"USD": 1.09, "TWD": 34.5, "JPY": 119.05, "HKD": 8.44, "KRW": 131.52, "MXN": 18.5, "BRL": 5.3, "RUB": 99, "INR": 90, "IDR": 16800, "THB": 38, "TRY": 33, "PLN": 4.6, "VND": 27000, "PHP": 60},
        "HKD": {"USD": 0.13, "TWD": 4.17, "JPY": 14.19, "EUR": 0.12, "KRW": 15.57, "MXN": 2.2, "BRL": 0.63, "RUB": 11.8, "INR": 10.7, "IDR": 2000, "THB": 4.5, "TRY": 4, "PLN": 0.55, "VND": 3200, "PHP": 7},
        "KRW": {"USD": 0.00083, "TWD": 0.026, "JPY": 0.092, "EUR": 0.0076, "HKD": 0.064, "MXN": 0.014, "BRL": 0.004, "RUB": 0.075, "INR": 0.068, "IDR": 12, "THB": 0.027, "TRY": 0.024, "PLN": 0.0033, "VND": 19, "PHP": 0.042},
        "MXN": {"USD": 0.059, "TWD": 1.88, "JPY": 6.25, "EUR": 0.054, "HKD": 0.45, "KRW": 70, "BRL": 0.29, "RUB": 5.3, "INR": 4.8, "IDR": 850, "THB": 2, "TRY": 1.8, "PLN": 0.25, "VND": 1500, "PHP": 3.3},
        "BRL": {"USD": 0.2, "TWD": 6.25, "JPY": 21.3, "EUR": 0.19, "HKD": 1.6, "KRW": 250, "MXN": 3.5, "RUB": 18.9, "INR": 16.7, "IDR": 2900, "THB": 6.8, "TRY": 6, "PLN": 0.82, "VND": 5100, "PHP": 11},
        "RUB": {"USD": 0.011, "TWD": 0.36, "JPY": 1.2, "EUR": 0.01, "HKD": 0.084, "KRW": 13, "MXN": 0.19, "BRL": 0.053, "INR": 0.9, "IDR": 160, "THB": 0.35, "TRY": 0.31, "PLN": 0.04, "VND": 260, "PHP": 0.58},
        "INR": {"USD": 0.012, "TWD": 0.38, "JPY": 1.3, "EUR": 0.011, "HKD": 0.094, "KRW": 15, "MXN": 0.21, "BRL": 0.06, "RUB": 1.1, "IDR": 180, "THB": 0.41, "TRY": 0.36, "PLN": 0.05, "VND": 290, "PHP": 0.65},
    }
    
    # If base currency and the given currency are the same, no conversion needed
    if currency == base_currency:
        return amount

    # Perform conversion if exchange rate is available
    if base_currency in exchange_rates[currency]:
        return amount * exchange_rates[currency][base_currency]
    
    return amount  # If no conversion is possible, return the original amount

def detect_base_currency_from_language(lang):
    if lang == "zh-Hant-TW":  # Traditional Chinese (Taiwan)
        return "TWD"
    elif lang == "zh-Hans-CN":  # Simplified Chinese (China)
        return "CNY"
    elif lang == "en-US":  # English (United States)
        return "USD"
    elif lang == "en-GB":  # English (United Kingdom)
        return "GBP"
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
    elif lang == "es-MX":  # Spanish (Mexico)
        return "MXN"
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
    elif lang == "id-ID":  # Indonesian (Indonesia)
        return "IDR"
    elif lang == "th-TH":  # Thai (Thailand)
        return "THB"
    elif lang == "tr-TR":  # Turkish (Turkey)
        return "TRY"
    elif lang == "pl-PL":  # Polish (Poland)
        return "PLN"
    elif lang == "vi-VN":  # Vietnamese (Vietnam)
        return "VND"
    elif lang == "tl-PH":  # Tagalog (Philippines)
        return "PHP"
    return "USD"

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
        "USD": 0,  # United States
        "TWD": 0,  # Taiwan
        "JPY": 0,  # Japan
        "EUR": 0,  # Eurozone
        "HKD": 0,  # Hong Kong
        "KRW": 0,  # South Korea
        "BRL": 0,  # Brazil
        "RUB": 0,  # Russia
        "INR": 0,  # India
        "GBP": 0,  # United Kingdom
        "MXN": 0,  # Mexico
        "IDR": 0,  # Indonesia
        "TRY": 0,  # Turkey
        "SAR": 0,  # Saudi Arabia
        "THB": 0,  # Thailand
        "VND": 0,  # Vietnam
        "PHP": 0,  # Philippines
        "PLN": 0,  # Poland
        "CAD": 0,  # Canada
        "AUD": 0   # Australia
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
            elif symbol in ["MX$", "Mex$"]:  # Mexican Peso
                currency = "MXN"
            elif symbol == "R$":  # Brazilian Real
                currency = "BRL"
            elif symbol == "₽":  # Russian Ruble
                currency = "RUB"
            elif symbol == "₹":  # Indian Rupee
                currency = "INR"
            elif symbol == "Rp":  # Indonesian Rupiah
                currency = "IDR"
            elif symbol == "฿":  # Thai Baht
                currency = "THB"
            elif symbol == "₺":  # Turkish Lira
                currency = "TRY"
            elif symbol == "zł":  # Polish Złoty
                currency = "PLN"
            elif symbol == "₫":  # Vietnamese Dong
                currency = "VND"
            elif symbol == "₱":  # Philippine Peso
                currency = "PHP"
            else:
                currency = "USD"  # Default to USD

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
