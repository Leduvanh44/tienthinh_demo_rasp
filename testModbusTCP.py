from pymodbus.client import ModbusTcpClient
import time 
client = ModbusTcpClient('200.200.200.190', port=502)  
connection = client.connect()
try:
    while True:
        if connection:
            result = client.read_holding_registers(0, 10)  
            print(result.registers)
            time.sleep(1)
except KeyboardInterrupt:
    print("\nĐã dừng đọc dữ liệu")
    client.close()