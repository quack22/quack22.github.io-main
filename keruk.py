import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import os

# Mendapatkan konten dari website
response = requests.get("https://www.republika.co.id/")
web_content = response.text

# Membuat objek BeautifulSoup
soup = BeautifulSoup(web_content, "html.parser")

# Memeriksa apakah file data.json ada dan tidak kosong
data_file = "hasil.json"
if os.path.isfile(data_file) and os.path.getsize(data_file) > 0:
    with open(data_file, "r") as file:
        news_data = json.load(file)
else:
    news_data = []

# Mengambil judul yang sudah ada dalam data
alreadyDoneTitle = {item["Judul"] for item in news_data}

# Menemukan semua berita dalam halaman
news_items = soup.find_all("li", class_="list-group-item list-border conten1")

# Memproses setiap berita
for item in news_items:
    title = item.h3.get_text()
    if title not in alreadyDoneTitle:
        category = item.find("span", class_="kanal-info").get_text()
        upload_time_raw = item.find("div", class_="date").get_text().split("-")
        publish_time = upload_time_raw[1].strip()
        scraping_time = datetime.now().strftime("%d %b %Y %H:%M:%S")
        news_link = item.find("a")["href"]

        # Menambahkan berita baru ke dalam data
        news_data.append({
            "Judul": title,
            "Kategori": category,
            "Publish": publish_time,
            "Scraping": scraping_time,
            "Link": news_link,
        })

# Menyimpan data kembali ke dalam file data.json
with open(data_file, "w") as file:
    json.dump(news_data, file, indent=2)
