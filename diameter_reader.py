from cModbustcp import ModbusTCP
import paho.mqtt.client as mqtt
import time
import json
from datetime import datetime
import threading

# BROKER = "test.mosquitto.org"
BROKER = "45.117.177.157"
PORT = 1883
USERNAME = "client"
PASSWORD = "viam1234"

shared_data = {
    "copperline_diameters": [],
    "max_diameters": [],
    "min_diameters": [],
    "copperline_num": 0,
    "caliper_time": 0,
    "copperline_error": [],
}
data_lock = threading.Lock()

client = mqtt.Client()
client.username_pw_set(USERNAME, PASSWORD)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print(f"Failed to connect, return code {rc}")

client.on_connect = on_connect
client.connect(BROKER, PORT, 60)
client.loop_start()

def create_json_data(sensor_name, values):
    timestamp = datetime.now().isoformat()
    data_list = [{
        "name": f"{sensor_name}/{i+1}",
        "value": value,
        "timestamp": timestamp
    } for i, value in enumerate(values)]
    return json.dumps(data_list)

def publish_data():
    PUBLISH_INTERVAL = 30
    while True:
        time.sleep(PUBLISH_INTERVAL)
        with data_lock:
            current_diameters = shared_data["copperline_diameters"]
            max_diameters = shared_data["max_diameters"]
            min_diameters = shared_data["min_diameters"]
            copperline_num = shared_data["copperline_num"]
            caliper_time = shared_data["caliper_time"]
            diameters_state = shared_data["copperline_error"]
        try:
            current_timestamp = datetime.now().isoformat()
            client.publish(
                "TienThinh/MD08/CopperWirePiameters/CurrentCopperlinePiameters",
                create_json_data("MD08/WireDiameter", current_diameters),
                retain=True
            )
            client.publish(
                "TienThinh/MD08/CopperWirePiameters/MaxCopperlinePiameters",
                create_json_data("MD08/MaxWireDiameter", max_diameters),
                retain=True
            )
            client.publish(
                "TienThinh/MD08/CopperWirePiameters/MinCopperlinePiameters",
                create_json_data("MD08/MinWireDiameter", min_diameters),
                retain=True
            )
            caliper_payload = json.dumps({
                "name": "MD08/CaliperTime",
                "value": caliper_time,
                "timestamp": current_timestamp
            })
            client.publish("TienThinh/MD08/CopperWirePiameters/CaliperTime", caliper_payload, retain=True)
            current_wire_payload = json.dumps({
                "name": "MD08/CurrentWireNumber",
                "value": copperline_num,
                "timestamp": current_timestamp
            })
            client.publish("TienThinh/MD08/CopperWirePiameters/CurrentWireNumber", current_wire_payload, retain=True)
            
            client.publish(
                "TienThinh/MD08/CopperWirePiameters/CopperlineState",
                create_json_data("MD08/WireDiameter", diameters_state),
                retain=True
            )
            print(f"Data published at {current_timestamp}")
        except Exception as e:
            print(f"Error publishing data: {e}")

def read_modbus():
    id_st = 0
    while True:
        try:
            host = "192.168.1.100"
            modbus_client = ModbusTCP(host)
            # print("Start to read modbus...")
            copperline_diameters = modbus_client.read_holding_registers(address=id_st+1, count=24, unit=1)
            max_diameters = modbus_client.read_holding_registers(address=id_st+38, count=24, unit=1)
            min_diameters = modbus_client.read_holding_registers(address=id_st+74, count=24, unit=1)
            copperline_num = modbus_client.read_holding_registers(address=id_st+0, count=1, unit=1)[0]
            caliper_time = modbus_client.read_holding_registers(address=id_st+110, count=1, unit=1)[0]
            copperline_diameters = [x / 10000 for x in copperline_diameters]
            max_diameters = [x / 10000 for x in max_diameters]
            min_diameters = [x / 10000 for x in min_diameters]
            diameter_errs = []
            for i, diameter in enumerate(copperline_diameters):
                if diameter == 0:
                    diameter_errs.append("nonmanufacturing")
                else:
                    if diameter > max_diameters[i]:
                        diameter_errs.append("high")
                    elif diameter < min_diameters[i]:
                        diameter_errs.append("low")
                    else:
                        diameter_errs.append("manufacturing")
            print(diameter_errs)
            time.sleep(0.1)
            modbus_client.close()
            with data_lock:
                shared_data["copperline_diameters"] = copperline_diameters
                shared_data["max_diameters"] = max_diameters
                shared_data["min_diameters"] = min_diameters
                shared_data["copperline_num"] = copperline_num
                shared_data["caliper_time"] = caliper_time
                shared_data["copperline_error"] = diameter_errs
        except Exception as e:
            print(f"Error reading Modbus: {e}")
            time.sleep(1) 

if __name__ == "__main__":
    modbus_thread = threading.Thread(target=read_modbus, daemon=True)
    mqtt_thread = threading.Thread(target=publish_data, daemon=True)

    modbus_thread.start()
    mqtt_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Program terminated")
    finally:
        client.loop_stop()
        client.disconnect()
