from cModbusrtu import ModbusRTU
import time
modbusMain = ModbusRTU(port='/dev/ttyUSB1', baudrate=9600, parity='E', stopbits=1, bytesize=8, timeout=1)
modbusTmp = ModbusRTU(port='/dev/ttyUSB0', baudrate=4800, parity='N', stopbits=1, bytesize=8, timeout=1)
vel_sv = [23.56, 34.56, 37.34, 45.67, 12.56]
temp_pv = []
temp_sv = []
alarm_sv = []
try:
    while True:
        st_time = time.time()
        try:
            vel0 = modbusMain.read_holding_registers(address=4097, count=1, unit=1)[0]/100
            vel1 = modbusMain.read_holding_registers(address=4097, count=1, unit=2)[0]/100
            vel2 = modbusMain.read_holding_registers(address=4097, count=1, unit=3)[0]/100
            vel3 = modbusTmp.read_holding_registers(address=0, count=1, unit=1)[0]*50/4153
            vel4 = modbusTmp.read_holding_registers(address=1, count=1, unit=1)[0]*50/4153
            vel_sv = [vel0, vel1, vel2, vel3, vel4]

            temp0_pv = modbusMain.read_holding_registers(address=1, count=1, unit=4)[0]/100
            temp1_pv = modbusMain.read_holding_registers(address=1, count=1, unit=5)[0]/100
            temp2_pv = modbusMain.read_holding_registers(address=1, count=1, unit=6)[0]/100
            temp3_pv = modbusMain.read_holding_registers(address=1, count=1, unit=7)[0]/100
            temp4_pv = modbusMain.read_holding_registers(address=1, count=1, unit=8)[0]/100
            temp5_pv = modbusMain.read_holding_registers(address=1, count=1, unit=9)[0]/100
            temp6_pv = modbusMain.read_holding_registers(address=1, count=1, unit=10)[0]/100
            temp_pv = [temp0_pv, temp1_pv, temp2_pv, temp3_pv, temp4_pv, temp5_pv, temp6_pv]

            temp0_sv = modbusMain.read_holding_registers(address=2, count=1, unit=4)[0]/100
            temp1_sv = modbusMain.read_holding_registers(address=2, count=1, unit=5)[0]/100
            temp2_sv = modbusMain.read_holding_registers(address=2, count=1, unit=6)[0]/100
            temp3_sv = modbusMain.read_holding_registers(address=2, count=1, unit=7)[0]/100
            temp4_sv = modbusMain.read_holding_registers(address=2, count=1, unit=8)[0]/100
            temp5_sv = modbusMain.read_holding_registers(address=2, count=1, unit=9)[0]/100
            temp6_sv = modbusMain.read_holding_registers(address=2, count=1, unit=10)[0]/100
            temp_sv = [temp0_sv, temp1_sv, temp2_sv, temp3_sv, temp4_sv, temp5_sv, temp6_sv]

            temp0_alarm = modbusMain.read_holding_registers(address=21, count=1, unit=4)[0]/100
            temp1_alarm = modbusMain.read_holding_registers(address=21, count=1, unit=5)[0]/100
            temp2_alarm = modbusMain.read_holding_registers(address=21, count=1, unit=6)[0]/100
            temp3_alarm = modbusMain.read_holding_registers(address=21, count=1, unit=7)[0]/100
            temp4_alarm = modbusMain.read_holding_registers(address=21, count=1, unit=8)[0]/100
            temp5_alarm = modbusMain.read_holding_registers(address=21, count=1, unit=9)[0]/100
            temp6_alarm = modbusMain.read_holding_registers(address=21, count=1, unit=10)[0]/100
            alarm_sv = [temp0_alarm, temp1_alarm, temp2_alarm, temp3_alarm, temp4_alarm, temp5_alarm, temp6_alarm]
        except:
            print("Lỗi")
        en_time = time.time()
        print(f"Dữ liệu đọc được: {vel_sv}, {alarm_sv}, {temp_pv}, {temp_sv}")
        print(f"Thời gian đọc: {en_time - st_time}")
except KeyboardInterrupt:
    print("\nĐã dừng đọc dữ liệu (bạn nhấn Ctrl+C)")
finally:
    modbusMain.close()
    modbusTmp.close()