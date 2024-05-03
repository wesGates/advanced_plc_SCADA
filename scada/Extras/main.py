from pymodbus.client import ModbusTcpClient
import time
import json
import requests
from datetime import datetime

""" See OneNote Advanced PLC > Lectures > 04/16 for startup information."""

""" Do this: 
1. In the command line, apply migrations for all tables in the database by navigating to '~\scada\' and running python manage.py migrate
2. Then run python manage.py runserver to start the web server. Click the IP address to see the webpage.
"""

class plc_tag():
    def __init__(self, name, modbus_address, value):
        self.name = name
        self.modbus_address = modbus_address
        self.value = value


def connect_to_click_plc():
    client = ModbusTcpClient('192.168.1.10', port="502")
    client.connect()
    return client


def disconnect_from_click_plc(client):
    print("Disconnecting from click PLC")
    client.close()


def read_coils(client, coil_number, number_of_coils=1):
    # Address the offset coil
    coil_number = coil_number - 1
    result = client.read_coils(coil_number, number_of_coils)
    result_list = result.bits[0:number_of_coils]
    return result_list


def write_modbus_coil(client, coil_number, value):
    coil_number = coil_number - 1
    result = client.write_coils(coil_number, value)


def write_to_json_file(file_name, data_dict):
    with open(file_name, "w") as file:
        json.dump(data_dict, file)


def create_data_structure_for_cache(*args):
    # Creating tag dictionary
    # IE: {'In hand': True, "In auto": False}

    result_dict = {}
    # Iterate through unknown number of objects
    for argument in args:
        result_dict[argument.name] = argument.value

    # Append a timestamp 
    now = datetime.now()
    result_dict["timestamp"] = now.strftime("%m/%d/%Y, %H:%M:%S")

    # Result dict = {"In Hand": True, ...., "timestamp": "04/24/2024, 3:37:15"}
    return result_dict


def send_data_to_webserver(data_dict, session):
    # Convert from python dict to JSON string
    # to be able to send to our django web server
    json_string = json.dumps(data_dict)

    # This is the site you are trying to send to
    site_url = 'http://localhost:8000/receive-stepper-data/'
    # These are some headers for your browser, I wouldn't worry about these
    headers = {'User-Agent': 'Mozilla/5.0'}

    # This is sending the data to the webserver
    r = session.post(site_url, data=json_string, headers=headers)

    # This is the webservers response, which if it is working
    # should be a response code of 200
    print(r.status_code)


def main():
    tag_dict = {}
    
    # Create a session with our webserver to speed things up
    session = requests.Session()

    # Create our click PLC connection object
    click_plc_connection = connect_to_click_plc()

    # Create our objects for each PLC tag
    in_auto = plc_tag("In Auto", 16385, None)
    in_hand = plc_tag("In Hand", 16386, None)
    e_stop = plc_tag("E-Stop", 16387, None)
    move_conveyor = plc_tag("Move Conveyor", 16388, None)

    # Run forever
    while True:
        # Read the selector switch and E-Stop coils
        data = read_coils(click_plc_connection, in_auto.modbus_address, 4)
        in_auto.value = data[0]
        in_hand.value = data[1]
        e_stop.value = data[2]
        move_conveyor.value = data[3]


        # Move the conveyor when inAuto mode is selected
        if in_auto.value is True and e_stop.value is False:
            write_modbus_coil(click_plc_connection, move_conveyor.modbus_address, True)

        if in_hand.value is True and e_stop.value is False:
            print("In hand")

        # setup tag dictionary with unlimited arguments
        tag_dict = create_data_structure_for_cache(
                                            in_auto,
                                            in_hand,
                                            e_stop,
                                            move_conveyor
                                        )
        send_data_to_webserver(tag_dict, session)

    disconnect_from_click_plc(click_plc_connection)


if __name__ == '__main__':
    main()
