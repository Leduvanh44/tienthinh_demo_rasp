import paho.mqtt.client as mqtt

# Cấu hình thông tin broker
BROKER = "test.mosquitto.org"
PORT = 1883
USERNAME = "client"
PASSWORD = "viam1234"

# Hàm callback khi kết nối thành công
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Kết nối thành công!")
        client.subscribe("test/topic")  # Đăng ký một topic để nhận dữ liệu
    else:
        print(f"Kết nối thất bại với mã lỗi {rc}")

# Hàm callback khi nhận được tin nhắn
def on_message(client, userdata, msg):
    print(f"Nhận được tin nhắn: {msg.topic} -> {msg.payload.decode()}")

# Tạo client MQTT
client = mqtt.Client()
# client.username_pw_set(USERNAME, PASSWORD)
# Kết nối đến broker
client.connect(BROKER, PORT, 60)

# Chạy vòng lặp lắng nghe dữ liệu
client.loop_forever()
