import json
import os
from datetime import datetime
from django.conf import settings
from stepper_motor import models

def read_json_file(filename):
    # Hardcoded route for out json file
    hardcoded_json_route = os.path.join(
                                settings.BASE_DIR,
                                "Extras/stepper_motor.json"
                            )

    # open the hardcoded json file
    with open(hardcoded_json_route) as f:
        stepper_motor_dict = json.load(f)
        # print(stepper_motor_dict)

    return stepper_motor_dict


def save_data():
    # Gather our data
    stepper_motor_dict = read_json_file("")

    # Pull out the timestamp and remove from dict
    time_stamp = stepper_motor_dict['timestamp']
    # YYYY-MM-DD HH:MM:ss
    updated_timestamp = datetime.strptime(
                                            time_stamp,
                                            "%m/%d/%Y, %H:%M:%S"
                                            )
    # print(updated_timestamp)

    
    del stepper_motor_dict['timestamp']

    # Iterate through remaining dictionary
    # TODO: save data
    for key, value in stepper_motor_dict.items():
        print(updated_timestamp, key, value)
        TempDataPoint = models.StepperMotorDataPoint(
                                                        tag_name=key,
                                                        tag_value=value,
                                                        timestamp=updated_timestamp,
                                                    )
        TempDataPoint.save()