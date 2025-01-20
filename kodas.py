import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone
import time
import os

# Headers for the HTTP request
HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "lt;q=0.8",
    "cache-control": "max-age=0",
    "cookie": "stel_on=1; stel_ssid=10fc093f0b46f929e5_13686442030222303864",
    "sec-ch-ua": "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Brave\";v=\"132\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "sec-gpc": "1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
}

URL = "https://t.me/s/war_monitor"
OUTPUT_PATH = r"C:\Py\Telegram\output.txt"


def scrape_telegram():
    start_time = time.time()

    # Request data from the Telegram channel
    response = requests.get(URL, headers=HEADERS)
    if response.status_code != 200:
        print(f"Failed to fetch data: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    # Extract messages and timestamps
    messages = soup.find_all("div", class_="tgme_widget_message_bubble")
    times = soup.find_all("time", class_="time")

    data = []
    for message, time_tag in zip(messages, times):
        # Clean message content
        text_content = message.get_text(separator="\n", strip=True).replace("<br>", "\n")
        text_content = text_content.replace("monitor", "").strip()
        text_content = text_content.replace("Please open Telegram to view this post\nVIEW IN TELEGRAM", "").strip()

        # Skip empty messages
        if not text_content:
            continue

        # Extract timestamp and clean format
        timestamp = time_tag["datetime"]
        formatted_time = datetime.fromisoformat(timestamp).strftime("%Y-%m-%d %H:%M:%S")

        # Check for media
        media = message.find("video", src=True) or message.find("a", href=True)
        media_url = media["src"] if media and media.name == "video" else media["href"] if media else None

        # Skip entries with default Telegram URL
        if media_url == "https://t.me/war_monitor":
            media_url = None

        # Append cleaned data
        data.append((text_content, formatted_time, media_url))

    # Filter for last 24 hours
    last_day = (datetime.now(timezone.utc) - timedelta(days=1)).replace(tzinfo=None)
    last_day_data = [item for item in data if datetime.fromisoformat(item[1]).replace(tzinfo=None) >= last_day]
    summary = f"Last day provided {len(last_day_data)} elements:\n"

    # Prepare output for last day
    new_entries = [summary]
    for text, timestamp, media_url in last_day_data:
        # Format the entry
        entry = f"{text}\n\n{timestamp}"
        if media_url:
            entry += f"\nMedia: {media_url}"
        entry += f"\n-_-_-_-_-_-_-_-_-_-_-_-_-_"
        new_entries.append(entry)

    # Read existing content from the output file
    if os.path.exists(OUTPUT_PATH):
        with open(OUTPUT_PATH, "r", encoding="utf-8") as file:
            existing_content = file.read()
    else:
        existing_content = ""

    # Combine new entries with existing content
    combined_content = "\n\n".join(new_entries) + "\n\n" + existing_content

    # Write the updated content back to the file
    with open(OUTPUT_PATH, "w", encoding="utf-8") as file:
        file.write(combined_content)

    # Terminal feedback
    elapsed_time = time.time() - start_time
    print(f"Apdorota {len(data)} įrašų.")
    print(f"Paskutinę parą būta {len(last_day_data)} įrašų.")
    print(f"Išvesties kelias: {os.path.abspath(OUTPUT_PATH)}")
    print(f"Užtruko: {elapsed_time:.2f} sek.")


# Run the scraper
scrape_telegram()
