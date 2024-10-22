import os
import re
import zipfile
import json
import time
import asyncio
import aiohttp
import winsound
import requests  
from bs4 import BeautifulSoup
from pathlib import Path

# Iš kur ir į kur
output_dir = r"D:\Py\RC NTR\final2"
url = "https://www.registrucentras.lt/p/1092"
output_file = "RC_NTR.json"

# Ar tikrai yra išvesties aplankas
Path(output_dir).mkdir(parents=True, exist_ok=True)

async def fetch_zip(session, url):
    """Sugauvome ZIM bylas."""
    async with session.get(url) as response:
        if response.status == 200:
            zip_data = await response.read()
            return zip_data
        else:
            print(f"Nepavyko gauti nuorodos {url}: {response.status}")
            return None

def download_file(zip_data, zip_name):
    """Išsaugome ZIP į ivesties aplanką."""
    zip_path = os.path.join(output_dir, zip_name)
    with open(zip_path, 'wb') as f:
        f.write(zip_data)
    print(f"		Parsiūsta {zip_name}")

async def download_zip_files(zip_urls):
    """Lygiagrečiai siunčiamos bylos."""
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in zip_urls:
            tasks.append(fetch_zip(session, url))
        zip_data_list = await asyncio.gather(*tasks)

        # Išsaugom parsiūstus
        for i, zip_data in enumerate(zip_data_list):
            if zip_data:
                zip_name = re.sub(r'[?=]', '_', zip_urls[i].split('=')[-1])
                download_file(zip_data, zip_name)

def extract_json_from_zip(zip_name):
    """Išpakuojamos JSON bylos iš nurodytų archyvų."""
    zip_path = os.path.join(output_dir, zip_name)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for file in zip_ref.namelist():
            if file.endswith('.json'):
                json_path = os.path.join(output_dir, file)
                with zip_ref.open(file) as json_file:
                    with open(json_path, 'wb') as f:
                        f.write(json_file.read())
                print(f"			Išpakuota {file}")
                return json_path
    return None

def merge_json_files(json_files):
    """Daugelį bylų sujungiame į vieną."""
    merged_data = {"type": "FeatureCollection", "features": []}
    for idx, json_file in enumerate(json_files):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:  # Naudojame UTF-8 koduotę
                data = json.load(f)
                if idx == 0:
                    merged_data = data  # Pirmą bylą naudojam kaip bazę
                else:
                    # Paimam duomenų iš vidrinių bylų
                    merged_data['features'].extend(data['features'])
        except UnicodeDecodeError as e:
            print(f"Nepavyko perskaityt {json_file}: {e}")
        except Exception as e:
            print(f"Klaida apdorojant {json_file}: {e}")
    return merged_data

def main():
    start_time = time.time()

    # Sugaudome nuorodas
    print("Gaudome URL...")
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Atnaujinta URL gavimo logika
    zip_urls = []
    for link in soup.find_all('a', href=True):
        href = link.get('href')
        if href and 'aduomenys/?byla=' in href and href.endswith('.zip'):
            full_url = f"https://www.registrucentras.lt{href}"
            zip_urls.append(full_url)

    if not zip_urls:
        print("Nebuvo rasta archyvuotų bylų.")
        return

    # Parsiunčiam ZIP bylas
    print(f"	Surasta {len(zip_urls)} ZIP bylų. Pradedamas siuntimas...")
    asyncio.run(download_zip_files(zip_urls))

    # Urmu išpakuojame duomenis
    print("Išpakuojame bylas...")
    json_files = []
    for zip_name in os.listdir(output_dir):
        if zip_name.endswith('.zip'):
            json_file = extract_json_from_zip(zip_name)
            if json_file:
                json_files.append(json_file)

    # Suliejame bylas
    print(f"Suiejamos {len(json_files)} JSON (kažkiek užtruks)...")
    merged_data = merge_json_files(json_files)

    # Išsaugome išvesties bylą
    output_json_path = os.path.join(output_dir, output_file)
    with open(output_json_path, 'w', encoding='utf-8') as f:  # Nurodome UTF-8 koduotę
        json.dump(merged_data, f, ensure_ascii=False, indent=4)
    print(f"	Sulieti duomenys yra išsaugoti {output_json_path}")

    # Išvalymas
    print("Valomos laikinos bylos...")
    for zip_name in os.listdir(output_dir):
        if zip_name.endswith('.zip') or (zip_name.endswith('.json') and zip_name != output_file):
            os.remove(os.path.join(output_dir, zip_name))
            print(f"	Ištrinta {zip_name}")

    # Pabaigai
    end_time = time.time()
    elapsed_time = end_time - start_time
    elapsed_minutes, elapsed_seconds = divmod(int(elapsed_time), 60)
    print(f"\nProcesai užtruko {elapsed_minutes:02}:{elapsed_seconds:02}.")
    print(f"	Išvesties byla yra: {output_json_path}")
    print(f"Iš viso apdorota: {len(zip_urls)}")
    print(f"	Iš viso JSON elementų: {len(merged_data.get('features', []))}")

    # Grojam garsą
    winsound.Beep(1000, 500)  # Dažnis: 1000 Hz, Trukmę: 500 ms

if __name__ == "__main__":
    main()
