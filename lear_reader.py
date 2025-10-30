import pandas as pd
import json
import datetime
import os
import time
import paho.mqtt.client as mqtt
import re

BROKER = "45.117.177.157"
PORT = 1883
USERNAME = "client"
PASSWORD = "viam1234"
MQTT_TOPIC_PREFIX = "TienThinh/MD08/LearMachine"

client = mqtt.Client()
client.username_pw_set(USERNAME, PASSWORD)
client.connect(BROKER, PORT, 60)
client.loop_start()
while True:
    start_time = time.time()
    today_str = datetime.date.today().strftime("%Y-%m-%d")
    # today_str = "2025-03-10"
    base_dir = "/mnt/pcshare"

    output_folder = f"/home/pi/tienthinh_demo_rasp/lear/{today_str}"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Đã tạo thư mục: {output_folder}")
    grouped_data = {}
    for root, dirs, files in os.walk(base_dir):
        for filename in files:
            if filename.endswith(".xls") and today_str in filename:
                full_path = os.path.join(root, filename)
                print(full_path)

                try:
                    df = pd.read_excel(full_path, header=None)
                except Exception as e:
                    print(f"Lỗi khi đọc file {full_path}: {e}")
                    continue

                data_string = df.iloc[3, 1]
                match = re.search(r"(.*?)\s*[～¡«]\s*(.*?)\)", data_string)
                if match:
                    duration = match.group(1).split("(")[0]
                    starttime = match.group(1).split("(")[1]
                    endtime = match.group(2)
                else:
                    starttime = None
                    endtime = None
                    duration = None

                data_dict = {
                    "Line": df.iloc[1, 1],
                    "Length": df.iloc[2, 1],
                    "Speed": df.iloc[2, 3],
                    "Duration": duration,
                    "StartTime": starttime,
                    "EndTime": endtime,
                    "ReportDate": today_str,
                    "PinholeSet": {
                        "HVSet": df.iloc[12, 2],
                        "LeakageCurrentSV": df.iloc[13, 2],
                        "LengthofPhCSTD": df.iloc[14, 2],
                        "NumofPhCSTD": df.iloc[15, 2],
                        "PinholeUL30M": df.iloc[16, 2],
                        "PinholeAvgUL30M": df.iloc[17, 2],
                    },
                    "PinholeRes": {
                        "PinholeTotal": df.iloc[24, 2],
                        "ContinuousPinhole": df.iloc[25, 2],
                        "PinholeOV30M": df.iloc[26, 2],
                        "PinholeAvg30M": df.iloc[27, 2],
                    },
                }

                # Lấy phần tên topic từ filename
                topic_key = filename.split("#")[0]
                if topic_key not in grouped_data:
                    grouped_data[topic_key] = []
                grouped_data[topic_key].append(data_dict)

                # Lưu file JSON riêng nếu cần
                json_filename = os.path.splitext(filename)[0] + ".json"
                output_path = os.path.join(output_folder, json_filename)
                with open(output_path, "w", encoding="utf-8") as f:
                    json.dump(data_dict, f, indent=4, ensure_ascii=False)

    for topic_key, data_list in grouped_data.items():
        mqtt_topic = f"{MQTT_TOPIC_PREFIX}/{topic_key}"
        json_data = json.dumps(data_list, indent=4, ensure_ascii=False)
        client.publish(mqtt_topic, json_data, retain=True)
        print(f"Đã đăng MQTT: {mqtt_topic}")
    end_tỉme = time.time()
    time.sleep(60 * 30 - (end_tỉme - start_time))
