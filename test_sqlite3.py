import sqlite3

DBNAME = "test.sqlite3"         # データベースファイル名
conn = sqlite3.connect(DBNAME)  # SQLite3に接続
cur = conn.cursor()             # カーソルを得る
cur.execute("SQL文....)         # SQLを発行
conn.commit()                   # コミット
data = cur.fetchall()           # 結果をdataに格納
conn.close()                    # データベースを閉じる
