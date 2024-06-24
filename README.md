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
* if on an older version of Python (`python3 --version` output is before 3.11):
  `pip3 install tomli`
* copy `config.template.toml` to `config.toml`
* edit the `config.toml` file accordingly
* Run the app: `python3 ./main.py`

## Finding the port of the USB device

If only one USB device is plugged in, the port is typically `/dev/ttyUSB0`.

If multiple USB devices are plugged in, the port can change at each reboot, which isn't convenient. One way to circumvent this (tested on rasbpian) is:
1. Plug-in the EnOcean device after the raspberry has completed booting
2. Run `dmesg` from command prompt
3. You should get some output similar to this towards the end:
```
usb 1-1.2: new full-speed USB device number 6 using dwc_otg
usb 1-1.2: New USB device found, idVendor=0403, idProduct=6001, bcdDevice= 6.00
usb 1-1.2: New USB device strings: Mfr=1, Product=2, SerialNumber=3
usb 1-1.2: Product: EnOcean USB 300U DA
usb 1-1.2: Manufacturer: EnOcean GmbH
usb 1-1.2: SerialNumber: XXXYYYZZZ
usbcore: registered new interface driver ftdi_sio
usbserial: USB Serial support registered for FTDI USB Serial Device
ftdi_sio 1-1.2:1.0: FTDI USB Serial Device converter detected
usb 1-1.2: Detected FT232R
usb 1-1.2: FTDI USB Serial Device converter now attached to ttyUSB2
```
4. Edit `/etc/udev/rules.d/99-com.rules` and add a line similar to this one: 
```
SUBSYSTEM=="tty", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6001", SYMLINK+="ttyEnocean"
```
5. Reboot the device; if all goes well, there should now be a symlink to the Enocean device:
```
pi@rasberry:~ $ ls -AlF /dev/ttyEnocean 
lrwxrwxrwx 1 root root 7 Jun 23 20:24 /dev/ttyEnocean -> ttyUSB2
```
6. Add this to conf.toml
```
[enocean]
port = "/dev/ttyEnocean"     # USB path the EnOcean USB stick is plugged-in. 
```

## FAQ

Q: Why am I getting warning "It looks like you're parsing an XML document using an HTML parser." ?
A: it's a minor bug in one of the dependent libs [enocean/protocol/eep.py](https://github.com/kipe/enocean/blob/80a253bcea1e3cb99295f53f04c0558190dca5f3/enocean/protocol/eep.py#L25)

Q: I get a warning similar to "Received signal from non-Hubitat mapped EnOcean device 1234, button Button BO" even though it's mapped in the config file. What's wrong?
A: Typical button names are BO (Bravo Oscar) and BI (Bravo India). The second character after B is a letter, not a digit.

