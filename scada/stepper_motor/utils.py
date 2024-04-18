import json
import os
from django.conf import settings

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