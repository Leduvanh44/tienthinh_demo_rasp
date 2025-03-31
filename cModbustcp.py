from pymodbus.client.sync import ModbusTcpClient
import struct
import time

class ModbusTCP:
    def __init__(self, host, port=502, timeout=1, max_retries=5, reconnect_delay=2):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.max_retries = max_retries
        self.reconnect_delay = reconnect_delay
        self.client = ModbusTcpClient(host, port=port, timeout=timeout)
        if not self.connect():
            raise ConnectionError("Không thể kết nối tới thiết bị Modbus Ethernet")

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
        if self.client.connected:
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
            if not self.client.connected:
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
            if not self.client.connected:
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
            if not self.client.connected:
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
            if not self.client.connected:
                print("Kết nối đã bị mất, thử kết nối lại...")
                if not self.reconnect():
                    print("Không thể kết nối lại!")
                    return False
            return self.write_single_register(address, value, unit)

    def close(self):
        self.client.close()

if __name__ == "__main__":
    host = "192.168.1.100"
    modbus_client = ModbusTCP(host)
    copperline_diameters = modbus_client.read_holding_registers(address=1, count=10, unit=1)
    max_diameters = modbus_client.read_holding_registers(address=38, count=24, unit=1)
    min_diameters = modbus_client.read_holding_registers(address=74, count=24, unit=1)
    # inputs = modbus_client.read_input_registers(address=1000, count=1, unit=1)[0]
    # err = modbus_client.read_holding_registers(address=203, count=1, unit=1)[0]
    # delta = modbus_client.read_holding_registers(address=54, count=1, unit=1)[0]
    print(f"Dữ liệu đọc được SV: {copperline_diameters}")
        # print(f"Dữ liệu đọc được PV: {inputs}")
        # print(f"Dữ liệu đọc được Alarm: {err}")
        # print(f"Dữ liệu đọc được delta: {delta}")

    # success = modbus_client.write_single_register(address=0, value=12345, unit=1)
    # if success:
    #     print("Ghi thành công!")
    modbus_client.close()