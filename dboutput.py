import sqlite3

# SQLiteデータベースに接続
conn = sqlite3.connect('contact_data.db')
cursor = conn.cursor()

# municipalityの項目を取得
cursor.execute("SELECT municipality FROM contacts")
municipalities = cursor.fetchall()

# ターミナル上に表示
for municipality in municipalities:
    print(municipality[0])

# データベース接続を閉じる
conn.close()