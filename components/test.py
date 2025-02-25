import time
from components.classModbusMasterRTU import ModbusMasterRTU
from components.classModbusMasterTCP import ModbusMasterTCP
from classMqtt import MQTTClient, convert_data
testMbrtu = ModbusMasterRTU(port="/dev/ttyUSB0", baudrate=9600,
                           stopbits=1, bytesize=8, parity="E", timeout=1)

testMbtcp = ModbusMasterTCP(host='192.168.1.102')
testMqtt = MQTTClient(client_id="testMqtt", broker_address="20.39.193.159", port=1883)
testMqtt.connect()
# testMqtt.subscribe("/data/name")
# testMqtt.start_listening()
names = ["tempTD1", "velTD1"]
counts = [6, 4]
temp_values = [34.56, 37.67, 24.56, 27.67, 34.56, 37.67]
vel_values = [23.56, 34.56, 37.34, 45.67]

try:
    while True:
        st = time.time()
        temp0 = testMbrtu.read_float_from_registers(address=0, slave=1, register_type='holding')
        temp1 = testMbrtu.read_float_from_registers(address=2, slave=2, register_type='holding')
        temp2 = testMbrtu.read_float_from_registers(address=4, slave=3, register_type='holding')
        temp3 = testMbrtu.read_float_from_registers(address=6, slave=4, register_type='holding')
        temp4 = testMbrtu.read_float_from_registers(address=8, slave=5, register_type='holding')
        temp5 = testMbrtu.read_float_from_registers(address=10, slave=6, register_type='holding')
        vel0 = testMbrtu.read_float_from_registers(address=12, slave=7, register_type='holding')
        ed = time.time()
        vel1 = testMbtcp.read_float_from_registers(address=0, slave=1, register_type='holding')
        vel2 = testMbtcp.read_float_from_registers(address=2, slave=2, register_type='holding')
        vel3 = testMbtcp.read_float_from_registers(address=4, slave=3, register_type='holding')
        vel_values = [vel0, vel1, vel2, vel3]
        temp_values = [temp0, temp1, temp2, temp3, temp4, temp5]
        print(temp_values," | ", vel_values,  " time: ", ed - st)
        testMqtt.publish("Temp-Vel-Monitor/data", convert_data(names, counts, temp_values, vel_values))
        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nĐã dừng đọc dữ liệu")


