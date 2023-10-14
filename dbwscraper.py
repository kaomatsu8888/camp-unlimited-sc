import sqlite3
import csv

# SQLiteデータベースに接続
conn = sqlite3.connect('contact_data.db')
cursor = conn.cursor()

# データを取得
cursor.execute("SELECT kana, municipality, department, section, phone FROM contacts")
rows = cursor.fetchall()

# CSVファイルに書き込み
with open('contacts_export.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["kana", "municipality", "department", "section", "phone"])  # ヘッダーを書き込み
    writer.writerows(rows)

print("CSVファイルにエクスポートが完了しました。")

# データベース接続を閉じる
conn.close()
