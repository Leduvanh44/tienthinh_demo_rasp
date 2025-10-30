import threading
from cModbusrtu import ModbusRTU
import paho.mqtt.client as mqtt
import time
import json
from datetime import datetime
import os
BROKER = "45.117.177.157"
PORT = 1883
USERNAME = "client"
PASSWORD = "viam1234"
# tempctrl_name = ["Nhiệt đầu vào", "Nhiệt trung tâm", "Nhiệt đầu ra", "Nhiệt ủ mềm", "Nhiệt tuần hoàn", "Before", "After"]
# velctrl_name = ["Quạt trộn nhiệt", "captang A", "captang B", "Khí đầu vào", "Quạt hút khói"]
tempctrl_name = ["MD08/HeatController/0", "MD08/HeatController/1", "MD08/HeatController/2", "MD08/HeatController/3", "MD08/HeatController/4", "MD08/HeatController/5", "MD08/HeatController/6"]
velctrl_name = ["MD08/FanInverter/0", "MD08/FanInverter/1", "MD08/FanInverter/2", "MD08/FanInverter/3", "MD08/FanInverter/4"]
shared_data = {
    "vel_err": [],
    "vel_sv": [],
    "vel_rpm": [],
    "temp_pv": [],
    "temp_sv": [],
    "alarm": [],
    "alarm_high": [],
    "alarm_low": [],

}
data_lock = threading.Lock()

client = mqtt.Client()
client.username_pw_set(USERNAME, PASSWORD)
client.will_set("TienThinh/MD08/Status", payload="offline", qos=1, retain=True)


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print(f"Failed to connect, return code {rc}")

client.on_connect = on_connect
client.connect(BROKER, PORT, 60)
client.loop_start()

def create_json_data(array, name_prefix):
    json_data = []
    for i, value in enumerate(array):
        json_data.append({
            "name": f"{name_prefix[i]}",
            "value": value,
            "timestamp": datetime.now().isoformat()
        })
    return json_data

def publish_data():
    log_dir = "data_logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    while True:
        time.sleep(20)
        with data_lock:
            vel_err = shared_data["vel_err"]
            vel_sv = shared_data["vel_sv"]
            temp_pv = shared_data["temp_pv"]
            temp_sv = shared_data["temp_sv"]
            alarm = shared_data["alarm"]
            alarm_high = shared_data["alarm_high"]
            alarm_low = shared_data["alarm_low"]
            vel_rpm = shared_data["vel_rpm"]
        try:
            vel_err_data = json.dumps(create_json_data(vel_err, velctrl_name))
            vel_sv_data = json.dumps(create_json_data(vel_sv, velctrl_name))
            temp_pv_data = json.dumps(create_json_data(temp_pv, tempctrl_name))
            temp_sv_data = json.dumps(create_json_data(temp_sv, tempctrl_name))
            alarm_data = json.dumps(create_json_data(alarm, tempctrl_name))
            alarm_low_data = json.dumps(create_json_data(alarm_low, tempctrl_name))
            alarm_high_data = json.dumps(create_json_data(alarm_high, tempctrl_name))
            vel_rpm_data = json.dumps(create_json_data(vel_rpm, velctrl_name))

            client.publish("TienThinh/MD08/PresentValue/HeatController", temp_pv_data, retain=True)
            client.publish("TienThinh/MD08/Error/HeatController", alarm_data, retain=True)
            client.publish("TienThinh/MD08/HighThresholdSetValue/HeatController", alarm_low_data, retain=True)
            client.publish("TienThinh/MD08/LowThresholdSetValue/HeatController", alarm_high_data, retain=True)
            client.publish("TienThinh/MD08/SetValue/FanInverter", vel_sv_data, retain=True)
            client.publish("TienThinh/MD08/Error/FanInverter", vel_err_data, retain=True)
            client.publish("TienThinh/MD08/SetValue/HeatController", temp_sv_data, retain=True)
            client.publish("TienThinh/MD08/PresentValue/FanInverter", vel_rpm_data, retain=True)

            current_date = datetime.now().strftime('%Y-%m-%d')
            filename = os.path.join(log_dir, f"data_{current_date}.txt")

            with open(filename, 'a') as file:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                file.write(f"[{timestamp}] VelocityError: {vel_err_data}\n")
                file.write(f"[{timestamp}] VelocitySetValue: {vel_sv_data}\n")
                file.write(f"[{timestamp}] TempPresentValue: {temp_pv_data}\n")
                file.write(f"[{timestamp}] TempSetValue: {temp_sv_data}\n")
                file.write(f"[{timestamp}] TempAlarmValue: {alarm_data}\n")
                file.write(f"[{timestamp}] TempAlarmLowThreshold: {alarm_low_data}\n")
                file.write(f"[{timestamp}] TempAlarmHighThreshold: {alarm_high_data}\n")
                file.write("\n")

            print(f"Dữ liệu đã được publish: {time.time()}")
        except Exception as e:
            print(f"Lỗi khi publish dữ liệu: {e}")


def read_modbus():
    while True:
        st = time.time()
        try:
            modbusMain = ModbusRTU(port='/dev/ttyUSB0', baudrate=9600, parity='N', stopbits=1, bytesize=8, timeout=1)
            time.sleep(3)
            vel0 = modbusMain.read_holding_registers(address=4097, count=1, unit=2)[0] / 100
            time.sleep(0.1)
            vel1 = modbusMain.read_holding_registers(address=4097, count=1, unit=3)[0] / 100
            time.sleep(0.1)
            vel2 = modbusMain.read_holding_registers(address=4097, count=1, unit=4)[0] / 100
            time.sleep(0.1)
            vel3 = modbusMain.read_holding_registers(address=0, count=1, unit=1)[0] * 50 / 3974
            time.sleep(0.1)
            vel4 = modbusMain.read_holding_registers(address=1, count=1, unit=1)[0] * 70 * 1.4 / 3974
            time.sleep(0.1)
            err_vel0 = modbusMain.read_holding_registers(address=32768, count=1, unit=2)[0]
            time.sleep(0.1)
            err_vel1 = modbusMain.read_holding_registers(address=32768, count=1, unit=3)[0]
            time.sleep(0.1)
            err_vel2 = modbusMain.read_holding_registers(address=32768, count=1, unit=4)[0]
            time.sleep(0.1)

            temp0_pv = modbusMain.read_input_registers(address=1000, count=1, unit=5)[0]
            time.sleep(0.1)
            temp1_pv = modbusMain.read_holding_registers(address=0, count=1, unit=6)[0]
            time.sleep(0.1)
            temp3_pv = modbusMain.read_holding_registers(address=0, count=1, unit=8)[0]
            time.sleep(0.1)
            temp4_pv = modbusMain.read_holding_registers(address=0, count=1, unit=9)[0]
            time.sleep(0.1)
            temp5_pv = modbusMain.read_holding_registers(address=0, count=1, unit=10)[0]
            time.sleep(0.1)
            temp6_pv = modbusMain.read_holding_registers(address=0, count=1, unit=11)[0]
            time.sleep(0.1)

            temp0_sv = modbusMain.read_holding_registers(address=0, count=1, unit=5)[0]
            time.sleep(0.1)
            temp1_sv = modbusMain.read_holding_registers(address=2, count=1, unit=6)[0]
            time.sleep(0.1)
            temp3_sv = modbusMain.read_holding_registers(address=2, count=1, unit=8)[0]
            time.sleep(0.1)
            temp4_sv = modbusMain.read_holding_registers(address=2, count=1, unit=9)[0]
            time.sleep(0.1)
            temp5_sv = modbusMain.read_holding_registers(address=2, count=1, unit=10)[0]
            time.sleep(0.1)
            temp6_sv = modbusMain.read_holding_registers(address=2, count=1, unit=11)[0]
            time.sleep(0.1)

            temp0_alarm = modbusMain.read_holding_registers(address=203, count=1, unit=5)[0]
            time.sleep(0.1)
            if (temp0_alarm == 1): 
                temp0_alarm = temp0_pv
            temp1_alarm = modbusMain.read_holding_registers(address=20, count=1, unit=6)[0]
            time.sleep(0.1)
            if (temp1_alarm == 1): 
                temp1_alarm = temp1_pv
            temp3_alarm = modbusMain.read_holding_registers(address=20, count=1, unit=8)[0]
            time.sleep(0.1)
            if (temp3_alarm == 1): 
                temp3_alarm = temp3_pv
            temp4_alarm = modbusMain.read_holding_registers(address=20, count=1, unit=9)[0]
            time.sleep(0.1)
            if (temp4_alarm == 1): 
                temp4_alarm = temp4_pv
            temp5_alarm = modbusMain.read_holding_registers(address=20, count=1, unit=10)[0]
            time.sleep(0.1)
            if (temp5_alarm == 1): 
                temp5_alarm = temp5_pv
            temp6_alarm = modbusMain.read_holding_registers(address=20, count=1, unit=11)[0]
            time.sleep(0.1)
            if (temp6_alarm == 1): 
                temp6_alarm = temp6_pv



            temp0_alarm_val = modbusMain.read_holding_registers(address=54, count=1, unit=5)[0]
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

            modbusMain.close()
            time.sleep(3)
            modbusMain = ModbusRTU(port='/dev/ttyUSB0', baudrate=9600, parity='E', stopbits=1, bytesize=8, timeout=1)
            time.sleep(3)
            temp2_pv = modbusMain.read_holding_registers(address=130, count=1, unit=7)[0]
            time.sleep(0.1)
            temp2_sv = modbusMain.read_holding_registers(address=131, count=1, unit=7)[0]
            time.sleep(0.1)
            temp2_alarm_up = modbusMain.read_holding_registers(address=181, count=1, unit=7)[0]
            time.sleep(0.1)
            temp2_alarm_dowm = modbusMain.read_holding_registers(address=182, count=1, unit=7)[0]
            time.sleep(0.1)
            if ((temp2_pv < (temp2_sv + temp2_alarm_up)) and (temp2_pv > (temp2_sv - temp2_alarm_up))): 
                temp2_alarm = 0 
            else: 
                temp2_alarm = temp2_pv
            modbusMain.close()
            time.sleep(3)
            with data_lock:
                shared_data["vel_err"] = [err_vel0, err_vel1, err_vel2]
                shared_data["vel_sv"] = [vel0, vel1, vel2, vel3, vel4]
                shared_data["temp_pv"] = [temp0_pv, temp1_pv, temp2_pv, temp3_pv, temp4_pv, temp5_pv, temp6_pv]
                shared_data["temp_sv"] = [temp0_sv, temp1_sv, temp2_sv, temp3_sv, temp4_sv, temp5_sv, temp6_sv]
                shared_data["alarm"] = [temp0_alarm, temp1_alarm, temp2_alarm, temp3_alarm, temp4_alarm, temp5_alarm, temp6_alarm]
                shared_data["alarm_high"] = [temp0_sv + temp0_alarm_val, temp1_sv + temp1_alarm_val, temp2_sv + temp2_alarm_up, temp3_sv + temp3_alarm_val, temp4_sv + temp4_alarm_val, temp5_sv + temp5_alarm_val, temp6_sv + temp6_alarm_val]
                shared_data["alarm_low"] = [temp0_sv - temp0_alarm_val, temp1_sv - temp1_alarm_val, temp2_sv - temp2_alarm_up, temp3_sv - temp3_alarm_val, temp4_sv - temp4_alarm_val, temp5_sv - temp5_alarm_val, temp6_sv - temp6_alarm_val]
                shared_data["vel_rpm"] = [vel0*24.88, vel1*5.63, vel2*5.6, vel3*52.523, vel4*29.8]
        except Exception as e:
            print(f"Lỗi khi đọc Modbus: {e}")
        en = time.time()
        time.sleep(3)


modbus_thread = threading.Thread(target=read_modbus, daemon=True)
mqtt_thread = threading.Thread(target=publish_data, daemon=True)

modbus_thread.start()
mqtt_thread.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Kết thúc chương trình")
finally:
    client.loop_stop()
    client.disconnect()
