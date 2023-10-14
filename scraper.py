import requests
from bs4 import BeautifulSoup
import time
import sqlite3

# SQLiteデータベースに接続
conn = sqlite3.connect('contact_data.db')
cursor = conn.cursor()

# テーブルを作成（存在しない場合のみ）
cursor.execute('''
CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY,
    kana TEXT,
    municipality TEXT,
    department TEXT,
    section TEXT,
    phone TEXT
)
''')

URL = "https://www.soumu.go.jp/main_sosiki/jichi_zeisei/czaisei/czaisei_seido/renraku_3_1.html"
response = requests.get(URL)
soup = BeautifulSoup(response.content, "html.parser")

# 連絡先情報を取得
contact_data = []
tables = soup.find_all("table", class_="style1")
for table in tables:
    rows = table.find_all("tr")
    kana = rows[0].find("th").text.strip()  # 五十音
    print("五十音:", kana)
    for row in rows[1:]:
        columns = row.find_all("td")
        municipality = columns[0].text.strip()
        department = columns[1].text.strip()
        section = columns[2].text.strip()
        phone = columns[3].text.strip()

        contact_data.append({
            "kana": kana,
            "municipality": municipality,
            "department": department,
            "section": section,
            "phone": phone
        })

        # データをデータベースに挿入
        cursor.execute('''
        INSERT INTO contacts (kana, municipality, department, section, phone)
        VALUES (?, ?, ?, ?, ?)
        ''', (kana, municipality, department, section, phone))
        print("Inserted data with ID:", cursor.lastrowid)

    # リクエストの間に5秒の間隔を設定
        time.sleep(5)

# データベースへの変更を確定
conn.commit()
conn.close()

# 結果を表示
for data in contact_data:
    print(data)

print("スクレイピングが完了しました。")
