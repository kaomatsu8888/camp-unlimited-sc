# ライブラリのインポート
import requests
from bs4 import BeautifulSoup
import csv

# スクレイピング対象のURLリスト
base_url = "https://aroundjapan-rv.com/Driveguide/parking_place/auto_camp/auto_camp-"
urls = [base_url + f"{i:02}" for i in range(1, 9)]  # 01から08までのURLを生成

camp_data = []

# ヘッダー情報を追加
camp_data.append(["都道府県", "施設名", "住所", "電話番号"])

for url in urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # オートキャンプ場情報を取得
    tables = soup.find_all("table", class_="tablepress")  # すべてのテーブルを取得

    for table in tables:
        rows = table.find_all("tr")[1:]  # ヘッダー行を除外
        for row in rows:
            columns = row.find_all("td")
            if len(columns) < 4:  # 列数が4未満の場合はスキップ
                continue
            prefecture = columns[0].text.strip()
            facility_name = columns[1].text.strip()
            address = columns[2].text.strip()
            phone = columns[3].text.strip()

            camp_data.append([prefecture, facility_name, address, phone])

# CSVファイルに保存
with open('camp_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(camp_data)

print("スクレイピングが完了し、CSVファイルに保存しました")
