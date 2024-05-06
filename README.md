# Hubitat - EnOcean integration

This app allows for associating [EnOcean kinetic switches](https://www.enocean.com/en/products/kinetic-switches/) to 
[Hubitat](https://hubitat.com/) virtual switch devices.

## Pre-requisites

* A Hubitat hub.
* [EnOcean kinetic switches](https://www.enocean.com/en/products/kinetic-switches/)
* An EnOcean USB receiver. Tested with [this one](https://www.enocean-alliance.org/product/usb-300-usb-gateway-single-packaging/)
* A device running Linux on the same LAN as the Hubitat hub that will be receiving the EnOcean switch presses through the USB receiver. Tested on Raspberry pi 3.
* Python 3.7+ and pip3 installed on the device with the EnOcean USB receiver. Run `sudo apt-get install python3-pip` if missing.

## Setup

* create virtual switches in Hubitat
* export them in MakerAPI
* sync code locally
* `pip3 install -r requirements.txt`
* copy `config.template.toml` to `config.toml`
* edit the config.toml file accordingly
* Run the app: `python3 ./main.py`

## FAQ

Q: What's up with the "It looks like you're parsing an XML document using an HTML parser." warning?
A: it's a minor bug in one of the dependent libs [enocean/protocol/eep.py](https://github.com/kipe/enocean/blob/80a253bcea1e3cb99295f53f04c0558190dca5f3/enocean/protocol/eep.py#L25)

Q: I put the button name form logs, logs says device not found in mapper. What's wrong?
A: Typical button names are BO (Bravo Oscar) and BI (Bravo India). The second character after B is a letter, not a digit.

