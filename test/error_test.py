from cModbusrtu import ModbusRTU
import paho.mqtt.client as mqtt
import time
import json
from datetime import datetime
BROKER = "20.39.193.159"
PORT = 1883
tempctrl_name = ["Nhiệt đầu vào", "Nhiệt trung tâm", "Nhiệt đầu ra", "Nhiệt ủ mềm", "Nhiệt tuần hoàn", "Before", "After"]
velctrl_name = ["Quạt trộn nhiệt", "captang A", "captang B", "Khí đầu vào", "Quạt hút khói"]

modbusMain = ModbusRTU(port='/dev/ttyUSB0', baudrate=9600, parity='N', stopbits=1, bytesize=8, timeout=1)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print(f"Failed to connect, return code {rc}")

def create_json_data(array, name_prefix):
    json_data = []
    for i, value in enumerate(array):
        json_data.append({
            "name": f"{name_prefix[i]}",
            "value": value,
            "timestamp": datetime.now().isoformat()
        })
    return json_data

def publish_data(client, topic, data):
    try:
        client.publish(topic, json.dumps(data))
        print(f"Published to {topic}: {data}")
    except Exception as e:
        print(f"Failed to publish to {topic}: {e}")

client = mqtt.Client()
client.on_connect = on_connect

client.will_set("TienThinh/Devices/CabinetMD8/Status", payload="offline", qos=1, retain=True)

client.connect(BROKER, PORT, 60)
client.loop_start()

try:
    last_publish_time = time.time()
    while True:
        st_time = time.time()
        try:
            temp0_alarm_val = modbusMain.read_holding_registers(address=301, count=1, unit=5)[0]
            time.sleep(0.1)
            temp1_alarm_val = modbusMain.read_holding_registers(address=301, count=1, unit=6)[0]
            time.sleep(0.1)
            temp3_alarm_val = modbusMain.read_holding_registers(address=301, count=1, unit=8)[0]
            time.sleep(0.1)
            temp4_alarm_val = modbusMain.read_holding_registers(address=301, count=1, unit=9)[0]
            time.sleep(0.1)
            temp5_alarm_val = modbusMain.read_holding_registers(address=301, count=1, unit=10)[0]
            time.sleep(0.1)
            temp6_alarm_val = modbusMain.read_holding_registers(address=301, count=1, unit=11)[0]
            time.sleep(0.1)

            print(temp0_alarm_val, temp1_alarm_val, temp3_alarm_val)
            time.sleep(1)
        except Exception as e:
            print(f"Lỗi khi đọc Modbus: {e}")

        # Đăng dữ liệu lên MQTT mỗi 5 phút
        # if time.time() - last_publish_time >= 60*10:
        #     publish_data(client, "TienThinh/Devices/CabinetMD8/VelocitySetVal", create_json_data(vel_sv, velctrl_name))
        #     publish_data(client, "TienThinh/Devices/CabinetMD8/TempPresentVal", create_json_data(temp_pv, tempctrl_name))
        #     publish_data(client, "TienThinh/Devices/CabinetMD8/TempSetVal", create_json_data(temp_sv, tempctrl_name))
        #     publish_data(client, "TienThinh/Devices/CabinetMD8/TempAlarmVal", create_json_data(alarm_sv, tempctrl_name))
        #     last_publish_time = time.time()

        # en_time = time.time()
        # print(f"Thời gian đọc: {en_time - st_time}")
        # time.sleep(300 - int(en_time - st_time))

except KeyboardInterrupt:
    print("\nĐã dừng đọc dữ liệu")
finally:
    print("Đang đóng kết nối Modbus...")
    modbusMain.close()
    client.loop_stop()
    client.disconnect()
    print("Kết nối Modbus và MQTT đã đóng.")