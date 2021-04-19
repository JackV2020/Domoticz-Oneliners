This plugin manages Generic Custom Sensors for each item defined in the configuration file oneliners.conf.

Manages means adding, changing, removing and updating the sensors in Domoticz .

How to configure is described in oneliners.conf itself which already contains 17 example sensors

Each sensor needs :
 - Description
    This goes into the description of the device
 - Name
    The name of the device
 - Type=Custom
    The type, at this moment only Custom is supported
 - Image
    The name of the Image (the plugin comes with a folder CustomImages)
 - Units
    The units for the value
 - Command
    The oneliner to get a float value

At this moment only the Type Custom is supported which results in a Custom Sensor.
Other types may be introduced in the future, who knows ;-)

After changing the oneliners.conf file the plugin needs a restart.

Updates of values in Domoticz are done every minute.

To install the plugin you need to get the contents of the zip file oneliners.zip

On a Raspberry Pi you could :
Start a terminal and go to your plugins folder and the next wget command will download a zip file, unpack and remove the zipfile :

....../plugins$ wget https://raw.githubusercontent.com/JackV2020/Domoticz-Oneliners/main/oneliners.zip -O oneliners.zip && unzip -o oneliners.zip && rm oneliners.zip

Now to get it into Domoticz restart your domoticz like :

    sudo systemctl restart domoticz

After this you can add a device of the Type 'Jacks OneLiners'.

When you do not like the Type name 'Jacks OneLiners' feel free to edit plugin.py and modify it before you actually add your hardware.


Thanks for reading and enjoy.
