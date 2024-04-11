# Advanced PLC SCADA Template Spring 2024 - Version 1.0
## General Description
This is the basic template for the University of Idaho Advanced PLC classes SCADA system for tying together all other portions of the class. These systems include but are not limited to:
  - The AutomationDirect BRX PLC Controlling the Fischertechnik Mini Fatcory 4.0
  - The KOYO Click PLC Controlling the Stepper Motor
  - The Schneider Electric (S.E) Modicon M172 PLC W/ Various Hardware and the S.E. Smart Thermostat
  - The Lenze C300 PLC Controlling the VFD W/ a 240VAC 3 Phase Motor Attached

## Install and Setup
- Clone repository
- Rename scada/local_settings.sample.py to scada/local_setting.py
- Fill in necessary info in local_setting.py
- Pip install -r requirements.txt
- Run py manage.py migrate

## Running The Code
- Run py manage.py runserver

## Authors
Hunter Hawkins - hawk5052@vandals.uidaho.edu

## License
This project is licensed under the [MIT License](LICENSE.md), which means it is free for anyone to use, modify, and distribute.
