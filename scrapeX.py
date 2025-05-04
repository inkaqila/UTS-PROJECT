from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# Setup driver
path_to_driver = r"D:\chromedriver-win64\chromedriver-win64\chromedriver.exe"
service = Service(executable_path=path_to_driver)
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=service, options=options)

# Login manual
print("Silakan login ke Twitter di browser...")
driver.get("https://twitter.com/login")
input("Setelah login selesai, tekan ENTER di terminal ini...")

# Keyword 
queries = [
    "bela jurnalis", "dukung tempo", "teror jurnalis", "kantor media diserang"
]

# Inisialisasi
data = []
unique_texts = set()
scroll_pause = 3
max_scrolls = 3000

for query in queries:
    print(f"\n🔍 Mulai scraping keyword: {query}")
    search_url = f"https://twitter.com/search?q={query.replace(' ', '%20')}&src=typed_query&f=live"
    driver.get(search_url)
    time.sleep(5)

    last_height = driver.execute_script("return document.body.scrollHeight")
    tweet_found = False

    for scroll in range(max_scrolls):
        print(f"📜 Scroll ke-{scroll+1} untuk keyword: {query}")
        tweets = driver.find_elements(By.XPATH, '//article[@data-testid="tweet"]')

        for tweet in tweets:
            try:
                text_elem = tweet.find_element(By.XPATH, './/div[@data-testid="tweetText"]')
                text = text_elem.text.strip()

                if text in unique_texts:
                    continue

                time_elem = tweet.find_element(By.XPATH, './/time')
                timestamp = time_elem.get_attribute("datetime")

                data.append({
                    "platform": "twitter",
                    "keyword": query,
                    "komentar": text,
                    "timestamp": timestamp,
                    "sentimen": ""
                })
                unique_texts.add(text)
                tweet_found = True
            except:
                continue

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            print(f"✅ Scroll selesai untuk keyword: {query}")
            break
        last_height = new_height

    if not tweet_found:
        print(f"⚠️ Tidak ada tweet yang ditemukan untuk keyword: {query}")

# Simpan ke CSV
df = pd.DataFrame(data)
df.to_csv("komentar_twitter_selenium19.csv", index=False)
print(f"\n✅ Berhasil simpan {len(df)} komentar ke komentar_twitter_selenium19.csv")

driver.quit()
