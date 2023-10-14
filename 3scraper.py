# ライブラリのインポート
import requests
from bs4 import BeautifulSoup
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

# スクレイピング対象のURL
URL = "https://www.soumu.go.jp/main_sosiki/jichi_zeisei/czaisei/czaisei_seido/renraku_3_1.html"
response = requests.get(URL)
soup = BeautifulSoup(response.content, "html.parser")

# 連絡先情報を取得
contact_data = []
tables = soup.find_all("table", class_="tableList")  # すべての都道府県のテーブルを取得

for table in tables:
    rows = table.find_all("tr")[1:]  # ヘッダー行を除外
    for row in rows:
        columns = row.find_all("td")
        if len(columns) != 5:  # 列数が5でない場合はスキップ
            continue
        kana = columns[0].text.strip()
        municipality = columns[1].text.strip()
        department = columns[2].text.strip()
        section = columns[3].text.strip()
        phone = columns[4].text.strip()

        contact_data.append((kana, municipality, department, section, phone))

# データベースに保存
cursor.executemany('''
INSERT INTO contacts (kana, municipality, department, section, phone)
VALUES (?, ?, ?, ?, ?)
''', contact_data)

# 変更をコミット
conn.commit()

# データベース接続を閉じる
conn.close()

print("スクレイピングが完了しました")
