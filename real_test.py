from cModbusrtu import ModbusRTU
import paho.mqtt.client as mqtt
import time
import json
from datetime import datetime
BROKER = "20.39.193.159"
PORT = 1883

modbusMain = ModbusRTU(port='/dev/ttyUSB0', baudrate=9600, parity='N', stopbits=1, bytesize=8, timeout=1)
# modbusTmp = ModbusRTU(port='/dev/ttyUSB0', baudrate=9600, parity='E', stopbits=1, bytesize=8, timeout=1)

vel_sp = []
temp2_pv = 0
temp2_sv = 0
while True:
    vel3 = modbusMain.read_holding_registers(address=0, count=1, unit=1)[0]*50/4153
    vel4 = modbusMain.read_holding_registers(address=1, count=1, unit=1)[0]*50/4153
    vel0 = modbusMain.read_holding_registers(address=4097, count=1, unit=2)[0] / 100
    vel1 = modbusMain.read_holding_registers(address=4097, count=1, unit=3)[0] / 100
    vel2 = modbusMain.read_holding_registers(address=4097, count=1, unit=4)[0] / 100
    vel_sp = [vel0, vel1, vel2, vel3, vel4]
    print(vel_sp)

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

    modbusMain.close()
    modbusMain = ModbusRTU(port='/dev/ttyUSB0', baudrate=9600, parity='E', stopbits=1, bytesize=8, timeout=1)
    temp2_pv = modbusMain.read_holding_registers(address=130, count=1, unit=7)[0]
    temp2_sv = modbusMain.read_holding_registers(address=131, count=1, unit=7)[0]
    modbusMain.close()
    modbusMain = ModbusRTU(port='/dev/ttyUSB0', baudrate=9600, parity='N', stopbits=1, bytesize=8, timeout=1)

    temp_pv = [temp0_pv, temp1_pv, temp2_pv, temp3_pv, temp4_pv, temp5_pv, temp6_pv]
    temp_sv = [temp0_sv, temp1_sv, temp2_sv, temp3_sv, temp4_sv, temp5_sv, temp6_sv]
    print(temp_sv)
    print(temp_pv)
    time.sleep(5)