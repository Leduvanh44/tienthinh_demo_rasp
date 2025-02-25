from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import struct
import time

class ModbusRTU:
    def __init__(self, port, baudrate=9600, parity='N', stopbits=1, bytesize=8, timeout=1, max_retries=5, reconnect_delay=2):
        self.port = port
        self.baudrate = baudrate
        self.parity = parity
        self.stopbits = stopbits
        self.bytesize = bytesize
        self.timeout = timeout
        self.max_retries = max_retries
        self.reconnect_delay = reconnect_delay
        self.client = ModbusClient(
            method='rtu',
            port=port,
            baudrate=baudrate,
            parity=parity,
            stopbits=stopbits,
            bytesize=bytesize,
            timeout=timeout
        )
        if not self.connect():
            raise ConnectionError("Không thể kết nối tới thiết bị Modbus RTU")

    def connect(self):
        attempts = 0
        while attempts < self.max_retries:
            if self.client.connect():
                print("Kết nối thành công!")
                return True
            else:
                attempts += 1
                print(f"Không thể kết nối, thử lại {attempts}/{self.max_retries}...")
                time.sleep(self.reconnect_delay)
        print("Không thể kết nối sau nhiều lần thử.")
        return False

    def reconnect(self):
        print("Thử kết nối lại...")
        if self.client.is_open():
            self.client.close()
        return self.connect()

    def read_holding_registers(self, address, count, unit=1):
        try:
            result = self.client.read_holding_registers(address, count, unit=unit)
            if result.isError():
                print(f"Lỗi khi đọc thanh ghi: {result} ID: {unit}")
                return [-1]
            return result.registers
        except Exception as e:
            print(f"Lỗi khi đọc: {e}")
            if not self.client.is_open():
                print("Kết nối đã bị mất, thử kết nối lại...")
                if not self.reconnect():
                    print("Không thể kết nối lại!")
                    return None
            return self.read_holding_registers(address, count, unit)

    def read_input_registers(self, address, count, unit=1):
        try:
            result = self.client.read_input_registers(address, count, unit=unit)
            if result.isError():
                print(f"Lỗi khi đọc thanh ghi input: {result} ID: {unit}")
                return [-1]
            return result.registers
        except Exception as e:
            print(f"Lỗi khi đọc: {e}")
            if not self.client.is_open():
                print("Kết nối đã bị mất, thử kết nối lại...")
                if not self.reconnect():
                    print("Không thể kết nối lại!")
                    return None
        return self.read_input_registers(address, count, unit)


    def read_float(self, address, unit=1):
        try:
            result = self.client.read_holding_registers(address, 2, unit=unit)
            if result.isError():
                print(f"Lỗi khi đọc thanh ghi: {result}")
                return None
            
            registers = result.registers
            combined = (registers[0] << 16) + registers[1]

            float_value = struct.unpack('>f', struct.pack('>I', combined))[0]
            return float_value

        except Exception as e:
            print(f"Lỗi khi đọc: {e}")
            if not self.client.is_open():
                print("Kết nối đã bị mất, thử kết nối lại...")
                if not self.reconnect():
                    print("Không thể kết nối lại!")
                    return None
            return self.read_float(address, unit)

    def write_single_register(self, address, value, unit=1):
        try:
            result = self.client.write_register(address, value, unit=unit)
            if result.isError():
                print(f"Lỗi khi ghi giá trị: {result}")
                return False
            return True
        except Exception as e:
            print(f"Lỗi khi ghi: {e}")
            if not self.client.is_open():
                print("Kết nối đã bị mất, thử kết nối lại...")
                if not self.reconnect():
                    print("Không thể kết nối lại!")
                    return False
            return self.write_single_register(address, value, unit)

    def close(self):
        self.client.close()

if __name__ == "__main__":
    port = '/dev/ttyUSB0'  
    modbus_client = ModbusRTU(port)
    registers = modbus_client.read_holding_registers(address=0, count=1, unit=5)[0]
    inputs = modbus_client.read_input_registers(address=1000, count=1, unit=5)[0]
    err = modbus_client.read_holding_registers(address=203, count=1, unit=5)[0]
    delta = modbus_client.read_holding_registers(address=54, count=1, unit=5)[0]
    
    if registers:
        print(f"Dữ liệu đọc được SV: {registers}")
        print(f"Dữ liệu đọc được PV: {inputs}")
        print(f"Dữ liệu đọc được Alarm: {err}")
        print(f"Dữ liệu đọc được delta: {delta}")

    # success = modbus_client.write_single_register(address=0, value=12345, unit=1)
    # if success:
    #     print("Ghi thành công!")

    modbus_client.close()
