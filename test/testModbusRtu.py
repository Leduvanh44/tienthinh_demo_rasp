from pymodbus.client.sync import ModbusSerialClient

client = ModbusSerialClient(
    method='rtu',
    port='/dev/ttyUSB0',
    baudrate=9600,
    timeout=1,
    parity='E',
    stopbits=1,
    bytesize=8
)
while True:
    try:
        if client.connect():
            result = client.read_holding_registers(address=0, count=1, unit=7)
            print(result)
            client.close()
        else:
            print("oke")
    except KeyboardInterrupt:
        
        print("nhuw cc")