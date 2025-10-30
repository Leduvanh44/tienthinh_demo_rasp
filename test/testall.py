from cModbusrtu import ModbusRTU
import paho.mqtt.client as mqtt
import time
import json
from datetime import datetime
BROKER = "45.117.177.157"
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
client.username_pw_set(USERNAME, PASSWORD)
client.on_connect = on_connect

client.will_set("TienThinh/Devices/CabinetMD8/Status", payload="offline", qos=1, retain=True)

client.connect(BROKER, PORT, 60)
client.loop_start()

try:
    last_publish_time = time.time()
    while True:
        st_time = time.time()
        try:
            vel0 = modbusMain.read_holding_registers(address=4097, count=1, unit=2)[0] / 100
            vel1 = modbusMain.read_holding_registers(address=4097, count=1, unit=3)[0] / 100
            vel2 = modbusMain.read_holding_registers(address=4097, count=1, unit=4)[0] / 100
            vel3 = modbusMain.read_holding_registers(address=0, count=1, unit=1)[0] * 50 / 4153
            vel4 = modbusMain.read_holding_registers(address=1, count=1, unit=1)[0] * 50 / 4153

            err_vel0 = modbusMain.read_holding_registers(address=32768, count=1, unit=2)[0]
            err_vel1 = modbusMain.read_holding_registers(address=32768, count=1, unit=3)[0]
            err_vel2 = modbusMain.read_holding_registers(address=32768, count=1, unit=4)[0]           

            temp0_pv = modbusMain.read_holding_registers(address=0, count=1, unit=5)[0]
            temp1_pv = modbusMain.read_holding_registers(address=0, count=1, unit=6)[0]
            temp3_pv = modbusMain.read_holding_registers(address=0, count=1, unit=8)[0]
            temp4_pv = modbusMain.read_holding_registers(address=0, count=1, unit=9)[0]
            temp5_pv = modbusMain.read_holding_registers(address=0, count=1, unit=10)[0]
            temp6_pv = modbusMain.read_holding_registers(address=0, count=1, unit=11)[0]

            temp0_sv = modbusMain.read_holding_registers(address=2, count=1, unit=5)[0]
            temp1_sv = modbusMain.read_holding_registers(address=2, count=1, unit=6)[0]
            temp3_sv = modbusMain.read_holding_registers(address=2, count=1, unit=8)[0]
            temp4_sv = modbusMain.read_holding_registers(address=2, count=1, unit=9)[0]
            temp5_sv = modbusMain.read_holding_registers(address=2, count=1, unit=10)[0]
            temp6_sv = modbusMain.read_holding_registers(address=2, count=1, unit=11)[0]

            temp0_alarm = modbusMain.read_holding_registers(address=20, count=1, unit=5)[0]
            temp1_alarm = modbusMain.read_holding_registers(address=20, count=1, unit=6)[0]
            temp3_alarm = modbusMain.read_holding_registers(address=20, count=1, unit=8)[0]
            temp4_alarm = modbusMain.read_holding_registers(address=20, count=1, unit=9)[0]
            temp5_alarm = modbusMain.read_holding_registers(address=20, count=1, unit=10)[0]
            temp6_alarm = modbusMain.read_holding_registers(address=20, count=1, unit=11)[0]
            
            modbusMain.close()
            modbusMain = ModbusRTU(port='/dev/ttyUSB0', baudrate=9600, parity='E', stopbits=1, bytesize=8, timeout=1)
            temp2_pv = modbusMain.read_holding_registers(address=130, count=1, unit=7)[0]
            temp2_sv = modbusMain.read_holding_registers(address=131, count=1, unit=7)[0]
            temp2_alarm_up = modbusMain.read_holding_registers(address=181, count=1, unit=7)[0]
            temp2_alarm_dowm = modbusMain.read_holding_registers(address=182, count=1, unit=7)[0]
            if ((temp2_pv < (temp2_sv + temp2_alarm_up)) and (temp2_pv > (temp2_sv - temp2_alarm_dowm))): 
                temp2_alarm = 0 
            else: 
                temp2_alarm = 1
            modbusMain.close()
            modbusMain = ModbusRTU(port='/dev/ttyUSB0', baudrate=9600, parity='N', stopbits=1, bytesize=8, timeout=1)

            vel_err = [err_vel0, err_vel1, err_vel2]
            vel_sv = [vel0, vel1, vel2, vel3, vel4]
            temp_pv = [temp0_pv, temp1_pv, temp2_pv, temp3_pv, temp4_pv, temp5_pv, temp6_pv]
            temp_sv = [temp0_sv, temp1_sv, temp2_sv, temp3_sv, temp4_sv, temp5_sv, temp6_sv]
            alarm_sv = [temp0_alarm, temp1_alarm, temp2_alarm, temp3_alarm, temp4_alarm, temp5_alarm, temp6_alarm]

            print(f"Dữ liệu đọc được: {vel_sv}, \n{alarm_sv}, \n{temp_pv}, \n{temp_sv}")
        except Exception as e:
            print(f"Lỗi khi đọc Modbus: {e}")

        # Đăng dữ liệu lên MQTT mỗi 5 phút
        if time.time() - last_publish_time >= 60*10:
            publish_data(client, "TienThinh/Devices/CabinetMD8/VelocityError", create_json_data(vel_err, velctrl_name))
            publish_data(client, "TienThinh/Devices/CabinetMD8/VelocitySetValue", create_json_data(vel_sv, velctrl_name))
            publish_data(client, "TienThinh/Devices/CabinetMD8/TempPresentValue", create_json_data(temp_pv, tempctrl_name))
            publish_data(client, "TienThinh/Devices/CabinetMD8/TempSetValue", create_json_data(temp_sv, tempctrl_name))
            publish_data(client, "TienThinh/Devices/CabinetMD8/TempAlarmValue", create_json_data(alarm_sv, tempctrl_name))
            last_publish_time = time.time()

        en_time = time.time()
        print(f"Thời gian đọc: {en_time - st_time}")
        time.sleep(300 - int(en_time - st_time))

except KeyboardInterrupt:
    print("\nĐã dừng đọc dữ liệu")
finally:
    print("Đang đóng kết nối Modbus...")
    modbusMain.close()
    client.loop_stop()
    client.disconnect()
    print("Kết nối Modbus và MQTT đã đóng.")