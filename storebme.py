import time, os, sys, signal
import smbus2
import bme280
import sqlite3

BME280_ADDR = 0x76
BUS_NO = 1
DBNAME = 'weather.sqlite3'

def store_values(values):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    sql = "INSERT INTO bme(dt,temp,hum,press) VALUES(datetime('now', '+9 hours'),?,?,?)"
    cur.execute(sql,(values[0],values[1],values[2]))
    conn.commit()
    conn.close()

def signal_handler(sig, handler):
    sys.exit()

# テーブル作成
if not os.path.exists(DBNAME):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    cur.execute("CREATE TABLE bme(id INTEGER PRIMARY KEY AUTOINCREMENT, dt TEXT,temp REAL, hum REAL, press REAL)")
    conn.commit()
    conn.close()

# BME280
i2c = smbus2.SMBus(BUS_NO)
bme280.load_calibration_params(i2c, BME280_ADDR)

# signal
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# メインループ
while True:
    data = bme280.sample(i2c, BME280_ADDR)
    store_values([data.temperature,data.humidity,data.pressure ])
    time.sleep(60)