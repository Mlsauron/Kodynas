import os
import zipfile
import requests
import json
import time
from datetime import timedelta

# RC URL sąrašas
urls = [
  "https://www.registrucentras.lt/aduomenys/?byla=gis_pub_parcels_11.zip",
    "https://www.registrucentras.lt/aduomenys/?byla=gis_pub_parcels_12.zip",
    "https://www.registrucentras.lt/aduomenys/?byla=gis_pub_parcels_13.zip",
    "https://www.registrucentras.lt/aduomenys/?byla=gis_pub_parcels_15.zip",
    "https://www.registrucentras.lt/aduomenys/?byla=gis_pub_parcels_18.zip",
    "https://www.registrucentras.lt/aduomenys/?byla=gis_pub_parcels_19.zip",
    "https://www.registrucentras.lt/aduomenys/?byla=gis_pub_parcels_21.zip",
    "https://www.registrucentras.lt/aduomenys/?byla=gis_pub_parcels_23.zip",
    "https://www.registrucentras.lt/aduomenys/?byla=gis_pub_parcels_25.zip",
    "https://www.registrucentras.lt/aduomenys/?byla=gis_pub_parcels_27.zip",
    "https://www.registrucentras.lt/aduomenys/?byla=gis_pub_parcels_29.zip",
    "https://www.registrucentras.lt/aduomenys/?byla=gis_pub_parcels_30.zip",
    "https://www.registrucentras.lt/aduomenys/?byla=gis_pub_parcels_32.zip",
    "https://www.registrucentras.lt/aduomenys/?byla=gis_pub_parcels_33.zip",
    "https://www.registrucentras.lt/aduomenys/?byla=gis_pub_parcels_34.zip",
    "https://www.registrucentras.lt/aduomenys/?byla=gis_pub_parcels_36.zip",
    "https://www.registrucentras.lt/aduomenys/?byla=gis_pub_parcels_38.zip",
    "https://www.registrucentras.lt/aduomenys/?byla=gis_pub_parcels_39.zip",
    "https://www.registrucentras.lt/aduomenys/?byla=gis_pub_parcels_41.zip",
    "https://www.registrucentras.lt/aduomenys/?byla=gis_pub_parcels_42.zip",
    "https://www.registrucentras.lt/aduomenys/?byla=gis_pub_parcels_43.zip",
    "https://www.registrucentras.lt/aduomenys/?byla=gis_pub_parcels_45.zip",
    "https://www.registrucentras.lt/aduomenys/?byla=gis_pub_parcels_46.zip",
    "https://www.registrucentras.lt/aduomenys/?byla=gis_pub_parcels_47.zip",
    "https://www.registrucentras.lt/aduomenys/?byla=gis_pub_parcels_48.zip",
    "https://www.registrucentras.lt/aduomenys/?byla=gis_pub_parcels_49.zip",
    "https://www.registrucentras.lt/aduomenys/?byla=gis_pub_parcels_52.zip",
    "https://www.registrucentras.lt/aduomenys/?byla=gis_pub_parcels_53.zip",
    "https://www.registrucentras.lt/aduomenys/?byla=gis_pub_parcels_54.zip",
    "https://www.registrucentras.lt/aduomenys/?byla=gis_pub_parcels_55.zip",
    "https://www.registrucentras.lt/aduomenys/?byla=gis_pub_parcels_56.zip",
    "https://www.registrucentras.lt/aduomenys/?byla=gis_pub_parcels_57.zip",
    "https://www.registrucentras.lt/aduomenys/?byla=gis_pub_parcels_58.zip",
    "https://www.registrucentras.lt/aduomenys/?byla=gis_pub_parcels_59.zip",
    "https://www.registrucentras.lt/aduomenys/?byla=gis_pub_parcels_61.zip",
    "https://www.registrucentras.lt/aduomenys/?byla=gis_pub_parcels_62.zip",
    "https://www.registrucentras.lt/aduomenys/?byla=gis_pub_parcels_63.zip",
    "https://www.registrucentras.lt/aduomenys/?byla=gis_pub_parcels_65.zip",
    "https://www.registrucentras.lt/aduomenys/?byla=gis_pub_parcels_66.zip",
    "https://www.registrucentras.lt/aduomenys/?byla=gis_pub_parcels_67.zip",
    "https://www.registrucentras.lt/aduomenys/?byla=gis_pub_parcels_68.zip",
    "https://www.registrucentras.lt/aduomenys/?byla=gis_pub_parcels_69.zip",
    "https://www.registrucentras.lt/aduomenys/?byla=gis_pub_parcels_71.zip",
    "https://www.registrucentras.lt/aduomenys/?byla=gis_pub_parcels_72.zip",
    "https://www.registrucentras.lt/aduomenys/?byla=gis_pub_parcels_73.zip",
    "https://www.registrucentras.lt/aduomenys/?byla=gis_pub_parcels_74.zip",
    "https://www.registrucentras.lt/aduomenys/?byla=gis_pub_parcels_75.zip",
    "https://www.registrucentras.lt/aduomenys/?byla=gis_pub_parcels_77.zip",
    "https://www.registrucentras.lt/aduomenys/?byla=gis_pub_parcels_78.zip",
    "https://www.registrucentras.lt/aduomenys/?byla=gis_pub_parcels_79.zip",
    "https://www.registrucentras.lt/aduomenys/?byla=gis_pub_parcels_81.zip",
    "https://www.registrucentras.lt/aduomenys/?byla=gis_pub_parcels_82.zip",
    "https://www.registrucentras.lt/aduomenys/?byla=gis_pub_parcels_84.zip",
    "https://www.registrucentras.lt/aduomenys/?byla=gis_pub_parcels_85.zip",
    "https://www.registrucentras.lt/aduomenys/?byla=gis_pub_parcels_86.zip",
    "https://www.registrucentras.lt/aduomenys/?byla=gis_pub_parcels_87.zip",
    "https://www.registrucentras.lt/aduomenys/?byla=gis_pub_parcels_88.zip",
    "https://www.registrucentras.lt/aduomenys/?byla=gis_pub_parcels_89.zip",
    "https://www.registrucentras.lt/aduomenys/?byla=gis_pub_parcels_91.zip",
    "https://www.registrucentras.lt/aduomenys/?byla=gis_pub_parcels_94.zip"
]
    # Nurodykite tinkamą kelią į jūsų aplankus:
output_dir = r"D:\Py\RC NTR\output"
os.makedirs(output_dir, exist_ok=True)

start_time = time.time()

def download_file(url, output_path):
    response = requests.get(url)
    with open(output_path, 'wb') as file:
        file.write(response.content)

def extract_zip(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

def merge_json_files(json_files):
    merged_data = None
    feature_count = 0

    for idx, json_file in enumerate(json_files):
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            if idx == 0:
                # Pirmąjai bylai paimama visa struktūra
                merged_data = data
                print(f"Suliejama byla {idx + 1}/{len(json_files)}: Naudojama pilna struktūra.")
            else:
                # Vidurinėms ir paskutinei bylai paimama tik EI
                merged_data['features'].extend(data['features'])
                print(f"Suliejama byla {idx + 1}/{len(json_files)}: Paimami JSON bylos {len(data['features'])} elementai.")

            feature_count += len(data['features'])
    
    return merged_data, feature_count

def cleanup(files_to_delete):
    for idx, file in enumerate(files_to_delete):
        if os.path.exists(file):
            os.remove(file)
            print(f"Valoma {idx + 1}/{len(files_to_delete)}: Ištrinta {file}")

def main():
    json_files = []
    zip_files = []
    
    # Parsiunčiam ir išpakuojam bylas
    for idx, url in enumerate(urls):
        zip_name = os.path.join(output_dir, url.split('=')[-1])
        json_name = zip_name.replace('.zip', '.json')
        
        # Parsiunčiam bylas
        print(f"Parsisiunčiama ({idx + 1}/{len(urls)}): {zip_name}")
        download_file(url, zip_name)
        zip_files.append(zip_name)

        # Išpakuojame bylas
        print(f"Išpakuojama ({idx + 1}/{len(urls)}): {zip_name}")
        extract_zip(zip_name, output_dir)

        # Manom, jog ZIP byloje tėra viena .json byla su tokiu pačiu vardu, kaip ir archyvo.
        json_files.append(json_name)

    # Suliejamos visos json bylos
    print("\nSuliejamos bylos...")
    merged_json, feature_count = merge_json_files(json_files)

    # Išsaugoma sulieta byla
    merged_output = os.path.join(output_dir, "merged.json")
    with open(merged_output, 'w', encoding='utf-8') as f:
        json.dump(merged_json, f, ensure_ascii=False, indent=4)

    # Išvalomos panaudotos ir nereikalingos bylos (zip ir json)
    print("\nValomos laikinos bylos...")
    cleanup(zip_files + json_files)

    # Aprašomas progresas
    end_time = time.time()
    elapsed_time = str(timedelta(seconds=int(end_time - start_time)))
    print(f"\nPraėjo laiko: {elapsed_time}")
    print(f"Iš viso sulieta bylų: {len(json_files)}")
    print(f"Sulietas JSON'as yra: {merged_output}")

if __name__ == "__main__":
    main()
