import paho.mqtt.client as mqtt
import time
import json

# MQTT broker
BROKER = "20.41.104.186"
PORT = 1883

# Định nghĩa các mảng dữ liệu
vel_sv = [0, 1, 2, 3, 4]
temp_pv = [10, 11, 12, 13, 14, 15, 16]
temp_sv = [20, 21, 22, 23, 24, 25, 26]
alarm_sv = [0, 1, 0, 1, 0, 1, 0]


# Hàm tạo JSON cho một mảng
def create_json_data(array, name_prefix):
    json_data = []
    for i, value in enumerate(array):
        json_data.append({
            "name": f"{name_prefix}{i}",
            "value": value,
            "timestamp": time.time()
        })
    return json_data

# Hàm đăng dữ liệu lên MQTT
def publish_data(client, topic, data):
    try:
        client.publish(topic, json.dumps(data))
        print(f"Published to {topic}: {data}")
    except Exception as e:
        print(f"Failed to publish to {topic}: {e}")

# Hàm callback khi kết nối thành công
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print(f"Failed to connect, return code {rc}")

# Tạo kết nối MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.connect(BROKER, PORT, 60)

# Vòng lặp chính
client.loop_start()  # Bắt đầu vòng lặp mạng của MQTT

try:
    while True:
        # Tạo dữ liệu JSON cho từng topic
        vel_data = create_json_data(vel_sv, "vel")
        temp_pv_data = create_json_data(temp_pv, "temp_pv")
        temp_sv_data = create_json_data(temp_sv, "temp_sv")
        alarm_sv_data = create_json_data(alarm_sv, "alarm_sv")

        # Đăng dữ liệu lên các topic
        publish_data(client, "TienThinh/Devices/CabinetMD8/VelSetVal", vel_data)
        publish_data(client, "TienThinh/Devices/CabinetMD8/TempPresentVal", temp_pv_data)
        publish_data(client, "TienThinh/Devices/CabinetMD8/TempSetVal", temp_sv_data)
        publish_data(client, "TienThinh/Devices/CabinetMD8/TempAlarmVal", alarm_sv_data)

        # Chờ 5 phút trước khi đăng lại
        time.sleep(5 * 60)

except KeyboardInterrupt:
    print("Stopped by user")
finally:
    client.loop_stop()  # Dừng vòng lặp mạng
    client.disconnect()  # Ngắt kết nối MQTT
