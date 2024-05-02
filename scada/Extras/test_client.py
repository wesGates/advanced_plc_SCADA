import time
from pymodbus.client import ModbusTcpClient
import threading

# Advanced PLCs Python Code from 03/19/2024
# This code is written in the Pep 8 styling guide and is checked via pycodestyle


class PLCTag():
    def __init__(self, name, modbus_address, value):
        self.name = name
        self.modbus_address = modbus_address
        self.value = value


def connect_to_plc():
    # Attempting to create connection to click PLC
    # Return client object for other functions

    print("Attempting to connect to AVEVA TCP server")
    aveva_obj = ModbusTcpClient('192.168.1.10', port='502')
    # aveva_obj = ModbusTcpClient('127.0.0.1', port='48010')

    # Attempt to connect to the PLC
    aveva_obj.connect()

    # Return our PLC object
    return aveva_obj


def disconnect_from_click_plc(client):
    print("Disconnecting from click PLC")
    client.close()


def read_coils(client, coil_number, number_of_coils=1):
    # Address the offset coil
    coil_number = coil_number -1
    result = client.read_coils(coil_number, number_of_coils)
    result_list = result.bits[0:number_of_coils]
    return result_list


def write_modbus_coils(client, coil_address, value):

    result = None
    # Take care of the offset between pymodbus and the click plc
    # coil_address = coil_address - 1
    coil_address = coil_address - 1

    # pymodbus built in write coil function
    result = client.write_coil(coil_address, value)

    return result


def main():
    # Create client object for the click PLC
    # and connect to the PLC
    client = connect_to_plc()

    # Selector Switch and E-Stop Objects
    e_stop = PLCTag("E-Stop", 16387, None)
    print("E-stop modbus_address: ", e_stop.modbus_address)

    # Initialize E_stop as True
    e_stop.value = True

    try:
        while True:

            e_stop.value = read_coils(client, e_stop.modbus_address, 1)

            # Debugging print statements
            print("-------------------------")
            print(e_stop.name, ":", e_stop.value)
            time.sleep(1)

            # # Get the opposite value of the current motor direction (for alternating spin direction)
            # e_stop.value = not e_stop.value
            # print("Estop status:", e_stop.value)
            write_modbus_coils(client, e_stop.modbus_address, True)

            # # Toggle the Spin Motor CCW/CW lamps based on spin direction
            # if e_stop.value is True:
            #     write_modbus_coils(client, e_stop.modbus_address, True)
            # else:
            #     write_modbus_coils(client, e_stop.modbus_address, False)

            # time.sleep(1)

    # except EStopException:
    #     print("E-stop pressed, stopping program.")
    #     stop_event.set()

    except KeyboardInterrupt:
        # This allows you to stop the main program and thread safely using Ctrl+C
        print("Stopping...")
        # stop_event.set()
   

    disconnect_from_click_plc(client)


if __name__ == '__main__':
    main()
