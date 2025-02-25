from pymodbus.client import ModbusTcpClient
import struct

class ModbusMasterTCP:
    def __init__(self, host, port=502, timeout=1):
        self.client = ModbusTcpClient(
            host=host,
            port=port,
            timeout=timeout
        )
        self.connection = self.client.connect()
        if self.connection:
            print("Connect successfully to Device TCP")
        else:
            print("Cant connect to Device TCP")
    
    def close_connection(self):
        if self.client:
            self.client.close()
            print("Close connection modbus")
    
    # Read
    def read_holding_registers(self, address, count, slave=1):
        if self.connection:
            response = self.client.read_holding_registers(address=address, count=count, slave=slave)
            if not response.isError():
                return response.registers
            else:
                print("Error TCP when read 4x:", response)
                return None

    def read_coils(self, address, count, slave=1):
        if self.connection:
            response = self.client.read_coils(address=address, count=count, slave=slave)
            if not response.isError():
                return response.bits
            else:
                print("Error TCP when read 0x:", response)
                return None

    def read_discrete_inputs(self, address, count, slave=1):
        if self.connection:
            response = self.client.read_discrete_inputs(address=address, count=count, slave=slave)
            if not response.isError():
                return response.bits[0]
            else:
                print("Error TCP when read 1x:", response)
                return None

    def read_input_registers(self, address, count, slave=1):
        if self.connection:
            response = self.client.read_input_registers(address=address, count=count, slave=slave)
            if not response.isError():
                return response.registers
            else:
                print("Error TCP when read 3x:", response)
                return None

    def read_float_from_registers(self, address, slave=1, register_type='holding'):
        if register_type == 'holding':
            registers = self.read_holding_registers(address, 2, slave)
        elif register_type == 'input':
            registers = self.read_input_registers(address, 2, slave)
        else:
            print("Error TCP register_type!!!")
            return None
        if registers:
            combined_registers = struct.pack('>HH', registers[0], registers[1])
            value = struct.unpack('>f', combined_registers)[0]
            return value
        else:
            return None
    
    # Write 
    def write_single_coil(self, address, value, slave=1):
        if self.connection:
            response = self.client.write_coil(address=address, value=value, slave=slave)
            if not response.isError():
                print(f"Write sucessfully {value} to reg (0x) at {address}")
            else:
                print("Error TCP when write 0x:", response)

    def write_multiple_coils(self, address, values, slave=1):
        if self.connection:
            response = self.client.write_coils(address=address, values=values, slave=slave)
            if not response.isError():
                print(f"Write sucessfully {values} to regs (0x) at {address}")
            else:
                print("Error TCP when write 0x:", response)

    def write_single_register(self, address, value, slave=1):
        if self.connection:
            response = self.client.write_register(address=address, value=value, slave=slave)
            if not response.isError():
                print(f"Write sucessfully {value} to reg (4x) at {address}")
            else:
                print("Error TCP when write 4x:", response)

    def write_multiple_registers(self, address, values, slave=1):
        if self.connection:
            response = self.client.write_registers(address=address, values=values, slave=slave)
            if not response.isError():
                print(f"Write sucessfully {values} to regs (4x) at {address}")
            else:
                print("Error TCP when write 4x:", response)

    def write_single_register_float(self, address, value, slave=1):
        if self.connection:
            float_bytes = struct.pack('>f', value)  # Big-endian (MSB first)
            register_values = struct.unpack('>HH', float_bytes)
            response = self.client.write_registers(address=address, values=register_values, slave=slave)
            if not response.isError():
                print(f"Write sucessfully float value: {value} to reg (4x) at {address}")
            else:
                print("Error TCP when write 4x:", response)

    def write_multiple_registers_float(self, address, values, slave=1):
        if self.connection:
            register_values = []
            for value in values:
                float_bytes = struct.pack('>f', value)  # Big-endian (MSB first)
                register_values.extend(struct.unpack('>HH', float_bytes))
            response = self.client.write_registers(address=address, values=register_values, slave=slave)
            if not response.isError():
                print(f"Write sucessfully float values:{values} to regs (4x) at {address}")
            else:
                print("Error TCP when write 4x:", response)

if __name__ == "__main__":
    master = ModbusMasterTCP(host='169.254.117.247')  # Địa chỉ IP của thiết bị Modbus TCP slave
    # holdingRegister = master.read_discrete_inputs(address=0, count=1, slave=1)
    floatRegister = master.read_float_from_registers(address=0, slave=1, register_type='holding')
    print(floatRegister)
    # master.write_multiple_coils(address=4, values=[True, False, True])
    master.write_multiple_registers_float(address=6, values=[56.78, 90.12])
