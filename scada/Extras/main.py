from pymodbus.client import ModbusTcpClient
import time
import json
from datetime import datetime


class plc_tag():
    def __init__(self, name, modbus_address, value):
        self.name = name
        self.modbus_address = modbus_address
        self.value = value


def connect_to_click_plc():
    client = ModbusTcpClient('192.168.0.10', port="502")
    client.connect()
    return client


def read_coils(client, coil_number, number_of_coils=1):
    # Address the offset coil
    coil_number = coil_number - 1
    result = client.read_coils(coil_number, number_of_coils)
    result_list = result.bits[0:number_of_coils]
    return result_list


def write_modbus_coil(client, coil_number, value):
    coil_number = coil_number - 1
    result = client.write_coils(coil_number, value)


def close_connection_to_click(client):
    client.close()


def pulse_stepper(client, motor_pulse_control):

    write_modbus_coil(client, motor_pulse_control.modbus_address, True)
    time.sleep(0.01)
    write_modbus_coil(client, motor_pulse_control.modbus_address, False)
    time.sleep(0.01)


def change_motor_direction(client, motor_direction_feedback, motor_direction_control):

    motor_direction = read_coils(client, motor_direction_feedback.modbus_address, 1)
    print("Changing motor direction")
    motor_direction = motor_direction[0]
    write_modbus_coil(client, motor_direction_control.modbus_address, not motor_direction)


def write_to_json_file(file_name, data_dict):
    with open(file_name, "w") as file:
        json.dump(data_dict, file)


def create_data_structure_for_cache(*args):
    result_dict = {}
    # Iterate through unknown number of objects
    for argument in args:
        result_dict[argument.name] = argument.value

    # # Append a timestamp 
    now = datetime.now()
    result_dict["timestamp"] = now.strftime("%m/%d/%Y, %H:%M:%S")

    return result_dict


def main():
    tag_dict = {}

    # Create our click PLC connection object
    click_plc_connection = connect_to_click_plc()

    # Create our objects for each PLC tag
    in_auto = plc_tag("In Auto", 16385, None)
    in_hand = plc_tag("In Hand", 16386, None)
    e_stop = plc_tag("E-Stop", 16387, None)
    motor_pulse_feedback = plc_tag("Motor Pulse Feedback", 16388, None)
    motor_direction_feedback = plc_tag("Motor Direction Feedback", 16389, None)
    motor_pulse_control = plc_tag("Motor Pulse Control", 16390, None)
    motor_direction_control = plc_tag("Motor Direction Control", 16391, None)

    # Use this for changing stepper motor direction
    count = 0

    # Run forever
    while True:
        # Read the selector switch and E-Stop coils
        data = read_coils(click_plc_connection, in_auto.modbus_address, 7)
        in_auto.value = data[0]
        in_hand.value = data[1]
        e_stop.value = data[2]
        motor_pulse_feedback.value = data[3]
        motor_direction_feedback.value = data[4]
        motor_pulse_control.value = data[5]
        motor_direction_control.value = data[6]

        # Pulse the stepper motor
        if in_auto.value is True and e_stop.value is False:
            pulse_stepper(click_plc_connection, motor_pulse_control)
            count += 1
            if count == 200:
                count = 0
                change_motor_direction(click_plc_connection, motor_direction_feedback, motor_direction_control)

        if in_hand.value is True and e_stop.value is False:
            print("In hand")

        # setup tag dictionary with unlimited arguments
        tag_dict = create_data_structure_for_cache(
                                            in_auto,
                                            in_hand,
                                            e_stop,
                                            motor_pulse_feedback,
                                            motor_direction_feedback,
                                            motor_pulse_control,
                                            motor_direction_control
                                        )
        # Write data to json file
        write_to_json_file("stepper_motor.json" , tag_dict)

    close_connection_to_click(click_plc_connection)


if __name__ == '__main__':
    main()
