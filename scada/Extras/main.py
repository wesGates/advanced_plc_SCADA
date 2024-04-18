from pymodbus.client import ModbusTcpClient
import time
import json


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


def main():
    # Create our click PLC connection object
    click_plc_connection = connect_to_click_plc()

    # Create our objects for each PLC tag
    in_auto = plc_tag("In Auto", 16385, None)
    in_hand = plc_tag("In Hand", 16386, None)
    e_stop = plc_tag("E-Stop", 16387, None)
    motor_pulse_control = plc_tag("Motor Pulse Control", 16390, None)
    motor_direction_feedback = plc_tag("Motor Direction Feedback", 16389, None)
    motor_direction_control = plc_tag("Motor Direction Control", 16391, None)

    # Use this for changing stepper motor direction
    count = 0

    testing_tag_dict = {}

    # Run forever
    while True:
        # Read the selector switch and E-Stop coils
        ss_switch_and_e_stop = read_coils(click_plc_connection, in_auto.modbus_address, 3)
        in_auto.value = ss_switch_and_e_stop[0]
        in_hand.value = ss_switch_and_e_stop[1]
        e_stop.value = ss_switch_and_e_stop[2]

        # Take the coils we read from above and write those to a file
        testing_tag_dict[in_auto.name] = in_auto.value
        testing_tag_dict[in_hand.name] = in_hand.value
        testing_tag_dict[e_stop.name] = e_stop.value
        write_to_json_file("test.json" , testing_tag_dict)

        # if we are in auto and e stop not pressed
        if in_auto.value is True and e_stop.value is False:
            pulse_stepper(click_plc_connection, motor_pulse_control)
            count += 1
            if count == 200:
                count = 0
                change_motor_direction(click_plc_connection, motor_direction_feedback, motor_direction_control)

    close_connection_to_click(click_plc_connection)


if __name__ == '__main__':
    main()
