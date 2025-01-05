# edgeos-usb-serial-modem
Recipe for making a USB modem / dongle work under EdgeOS (ttyUSB)

Feedback and comments here: https://community.ui.com/questions/USBSerial-kernel-module/26178427-3838-4379-83f2-75ff62a18c3c (you will need an account to be able to see the discussion thread)

### 1. Enter configuration mode
```
configure
```
### 2. Add the Debian repositories
```
set system package repository stretch components 'main contrib non-free' 
set system package repository stretch distribution stretch
set system package repository stretch url http ://archive.debian.org/debian
```
### 3. Commit the changes and save the configuration
```
commit ; save
```
### 4. Update the local cache.
```
sudo apt-get update
```
> !!! WARNING: Do not use the "apt-get upgrade" command as it can break the customized Debian packages used in EdgeOS.
### 5. Search for the package you wish to install. In this example, the usb-modeswitch:
```
sudo apt-cache search usb-modeswitch
```
### 6. Install the package.
```
sudo apt-get install usb-modeswitch
```
```
	Reading package lists... Done
	Building dependency tree... Done
	The following additional packages will be installed:
	 libjim0.76 usb-modeswitch-data
	Suggested packages:
	 comgt wvdial
	The following NEW packages will be installed:
	 libjim0.76 usb-modeswitch usb-modeswitch-data
	0 upgraded, 3 newly installed, 0 to remove and 2 not upgraded.
	Need to get 215 kB of archives.
	After this operation, 722 kB of additional disk space will be used.
	Do you want to continue? [Y/n] Y
```
### 7. Exit configuration
```
exit
```
### 8. Add the missing kernel modules (thanks to @Lochnair):
https://build.lochnair.net/job/ubiquiti/job/kernel_e300/job/v2.0.9%252Fserial/5/

https://build.lochnair.net/job/ubiquiti/job/kernel_e300/job/v2.0.9%252Fserial/5/artifact/e300-modules.tar.bz2

Or use the [e300-modules.tar.bz2](e300-modules.tar.bz2) archive copied in this repo.

Extract the e300-modules.tar

Copy all the *.ko files from e300-modules/lib/modules/4.9.79-UBNT/kernel/drivers/usb/serial to /lib/modules/4.9.79-UBNT/kernel/drivers/usb/serial (if you use windows then WinSCP helps).

### 9. Update the module(s) dependencies
```
depmod -a
```
### 10. Insert the USB Modem and check if it is detected by the system and the drivers are loaded:
```
lsusb
```
```
	Bus 004 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
	Bus 003 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
	Bus 002 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
	Bus 001 Device 003: ID 12d1:1465 Huawei Technologies Co., Ltd. K3765 HSPA
	Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
```
```
lsusb -t
```
```
	/: Bus 04.Port 1: Dev 1, Class=root_hub, Driver=xhci-hcd/1p, 5000M
	/: Bus 03.Port 1: Dev 1, Class=root_hub, Driver=xhci-hcd/1p, 480M
	/: Bus 02.Port 1: Dev 1, Class=root_hub, Driver=xhci-hcd/1p, 5000M
	/: Bus 01.Port 1: Dev 1, Class=root_hub, Driver=xhci-hcd/1p, 480M
		|__ Port 1: Dev 31, If 0, Class=Vendor Specific Class, Driver=option, 480M
		|__ Port 1: Dev 31, If 1, Class=Vendor Specific Class, Driver=, 480M
		|__ Port 1: Dev 31, If 2, Class=Vendor Specific Class, Driver=option, 480M
		|__ Port 1: Dev 31, If 3, Class=Vendor Specific Class, Driver=option, 480M
		|__ Port 1: Dev 31, If 4, Class=Mass Storage, Driver=usb-storage, 480M
		|__ Port 1: Dev 31, If 5, Class=Mass Storage, Driver=usb-storage, 480M
```
If you see at lease one port on a bus for which the "Driver=option" then you are in business.
### 11. Check the system messages just to make sure there are no errors:
```
dmesg
```
```
	[36991.448940] usb 1-1: new high-speed USB device number 30 using xhci-hcd
	[36991.619567] usb 1-1: New USB device found, idVendor=12d1, idProduct=15ca
	[36991.619577] usb 1-1: New USB device strings: Mfr=1, Product=2, SerialNumber=3
	[36991.619582] usb 1-1: Product: HUAWEI Mobile
	[36991.619587] usb 1-1: Manufacturer: HUAWEI
	[36991.619591] usb 1-1: SerialNumber: FFFFFFFFFFFFFFFF
	[36991.664042] usb-storage 1-1:1.0: USB Mass Storage device detected
	[36991.664245] scsi host0: usb-storage 1-1:1.0
	[36992.491759] usb 1-1: USB disconnect, device number 30
	[36993.439060] usb 1-1: new high-speed USB device number 31 using xhci-hcd
	[36993.609882] usb 1-1: New USB device found, idVendor=12d1, idProduct=1506
	[36993.609892] usb 1-1: New USB device strings: Mfr=1, Product=2, SerialNumber=0
	[36993.609897] usb 1-1: Product: HUAWEI Mobile
	[36993.609902] usb 1-1: Manufacturer: HUAWEI
	[36993.976144] option 1-1:1.0: GSM modem (1-port) converter detected
	[36993.976359] usb 1-1: GSM modem (1-port) converter now attached to ttyUSB0
	[36993.977027] option 1-1:1.2: GSM modem (1-port) converter detected
	[36993.977212] usb 1-1: GSM modem (1-port) converter now attached to ttyUSB1
	[36993.977432] option 1-1:1.3: GSM modem (1-port) converter detected
	[36993.977597] usb 1-1: GSM modem (1-port) converter now attached to ttyUSB2
	[36993.977928] usb-storage 1-1:1.4: USB Mass Storage device detected
	[36993.978135] scsi host0: usb-storage 1-1:1.4
	[36993.978521] usb-storage 1-1:1.5: USB Mass Storage device detected
	[36993.978693] scsi host1: usb-storage 1-1:1.5
	[36995.042810] scsi 1:0:0:0: Direct-Access   HUAWEI  TF CARD Storage 2.31 PQ: 0 ANSI: 2
	[36995.043462] scsi 0:0:0:0: CD-ROM      HUAWEI  Mass Storage   2.31 PQ: 0 ANSI: 2
	[36995.045170] sd 1:0:0:0: [sda] Attached SCSI removable disk
```
### 12. Optional (enable usb_modeswitch logging)
If you are not sure that the **usb_modeswitch** does its thing then try **enable logging in the /etc/usb_modeswitch.conf**. After inserting the dongle you shall see the content of the log file **/var/log/usb_modeswitch_1-1**:
```
	USB_ModeSwitch log from Tue Dec 31 00:37:49 EET 2024

	Use global config file: /etc/usb_modeswitch.conf
	Raw parameters: {--switch-mode} {1-1:1.0} 
	Use top device dir /sys/bus/usb/devices/1-1
	Check class of first interface ...
	 Interface 0 class is 08.

	----------------
	USB values from sysfs:
	 manufacturer	HUAWEI Technology
	 product	HUAWEI Mobile
	 serial	
	----------------
	bNumConfigurations is 1 - don't check for active configuration
	Found packed config collection /usr/share/usb_modeswitch/configPack.tar.gz
	ConfigList: pack/12d1:1520 pack/12d1:#linux
	SCSI attributes not needed, move on
	Check config: pack/12d1:1520
	! matched. Read config data
	Extract config 12d1:1520 from collection /usr/share/usb_modeswitch/configPack.tar.gz
	Command line:
	usb_modeswitch -W -D -u -1 -b 1 -g 3 -v 12d1 -p 1520 -f $flags(config)


	Verbose debug output of usb_modeswitch and libusb follows
	(Note that some USB errors are to be expected in the process)
	--------------------------------


	Read long config from command line


	 * usb_modeswitch: handle USB devices with multiple modes
	 * Version 2.5.0 (C) Josua Dietze 2017
	 * Based on libusb1/libusbx


	 ! PLEASE REPORT NEW CONFIGURATIONS !


	DefaultVendor= 0x12d1
	DefaultProduct= 0x1520
	TargetVendor=  0x12d1
	TargetProduct= 0x1465
	HuaweiNewMode=1
	System integration mode enabled


	Use given bus/device number: 001/003 ...
	Look for default devices ...
	 bus/device number matched
	 found USB ID 12d1:1520
	  vendor ID matched
	  product ID matched
	 Found devices in default mode (1)
	Get the current device configuration ...
	Use interface number 0
	 with class 8
	Use endpoints 0x01 (out) and 0x81 (in)


	USB description data (for identification)
	-------------------------
	Manufacturer: HUAWEI Technology
		 Product: HUAWEI Mobile
	 Serial No.: not provided
	-------------------------
	Using standard Huawei switching message
	Looking for active driver ...
	 OK, driver detached
	Set up interface 0
	Use endpoint 0x01 for message sending ...
	Trying to send message 1 to endpoint 0x01 ...
	 OK, message successfully sent
	Read the response to message 1 (CSW) ...
	 Response reading failed (error -9)
	 Device is gone, skip any further commands
	ok:busdev
	--------------------------------
	(end of usb_modeswitch output)


	Check success of mode switch for max. 20 seconds ...
	 Wait for device file system (1 sec.) ...
	 Wait for device file system (2 sec.) ...
	 Wait for device file system (3 sec.) ...
	 Wait for device file system (4 sec.) ...
	 Wait for device file system (5 sec.) ...
	 Read attributes ...
	 All attributes matched
	Mode switching was successful, found 12d1:1465 (HUAWEI Technology: HUAWEI Mobile)
	Logger is /usr/bin/logger
	Check for AVOID_RESET_QUIRK kernel attribute
	 AVOID_RESET_QUIRK activated


	All done, exit
```
### 13. Testing the serial connection
As there is no miniterm or screen tools available, for easily testing the serial connection I used the python's pyserial 2.7 library.

Check it out it here: https://pypi.org/project/pyserial/2.7/#files.

Download it from here: https://files.pythonhosted.org/packages/df/c9/d9da7fafaf2a2b323d20eee050503ab08237c16b0119c7bbf1597d53f793/pyserial-2.7.tar.gz

Or from this repo: [pyserial-2.7.tar.gz](pyserial-2.7.tar.gz)

Get the Source Distribution **pyserial-2.7.tar.gz** and extract it somewhere on the router and install it in python using:
```
python setup.py install
```
This will install the pySerial library which comes with a very useful program in the subfolder **serial/tools/miniterm.py**
### 14. Start the miniterm.py and fire some AT commands:
```
python miniterm.py
```
```
	--- Available ports:
	--- /dev/ttyS0      ttyS0
	--- /dev/ttyS1      ttyS1
	--- /dev/ttyS2      ttyS2
	--- /dev/ttyS3      ttyS3
	--- /dev/ttyS4      ttyS4
	--- /dev/ttyS5      ttyS5
	--- /dev/ttyUSB0     HUAWEI HUAWEI Mobile
	--- /dev/ttyUSB1     HUAWEI HUAWEI Mobile
	--- /dev/ttyUSB2     HUAWEI HUAWEI Mobile
	Enter port name:/dev/ttyUSB0
	--- Miniterm on /dev/ttyUSB0: 9600,8,N,1 ---
	--- Quit: Ctrl+] | Menu: Ctrl+T | Help: Ctrl+T followed by Ctrl+H ---

	AT
	OK

	ATZ
	OK

	AT+CMGF=1
	OK

	AT+CSDH=1
	OK

	AT+CSMP=17,167,0,0
	OK

	AT+CMGS="PhoneNumberHere"
	> Hello from EdgeOS!
	>
	+CMGS: 184
	OK
	--- exit ---
```
> Note: press Ctrl+] to exit miniterm.py
### Other things
If you wish to **see if/which drivers are loaded** then run:
```
cat /proc/tty/drivers
```
```
	/dev/tty             /dev/tty        5       0 system:/dev/tty
	/dev/console         /dev/console    5       1 system:console
	/dev/ptmx            /dev/ptmx       5       2 system
	usbserial            /dev/ttyUSB   188 0-511 serial
	serial               /dev/ttyS       4 64-69 serial
	pty_slave            /dev/pts      136 0-1048575 pty:slave
	pty_master           /dev/ptm      128 0-1048575 pty:master
	octeon_pci_console   /dev/ttyPCI     4      96 serial
```
If the **cdc_ether drivers interferes with your setup** then you may prevent it from loading by issuing:
```
echo "blacklist cdc_ether" | sudo tee -a /etc/modprobe.d/blacklist.conf
```
To **manually reset an usb device**:
```
usb_modeswitch -W -v 0x12d1 -p 0x1465 -R
```
(get the vendor and product codes from the `lsusb` command)

**Poorman's solution to test serial communication:**
- start two ssh sessions to the router/host
- on the first session run `cat -v < /dev/ttyUSB0` (it will display the output from ttyUSB0)
- on the second session send the AT commands: `echo -ne 'ATZ' > /dev/ttyUSB0`
### References:
- Add Debian repositories/packages: https://help.ui.com/hc/en-us/articles/205202560-EdgeRouter-Add-Debian-Packages-to-EdgeOS
