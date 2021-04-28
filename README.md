This Domoticz plugin was developed on a Raspberry Pi and may work on other platforms also.

This plugin manages Generic Custom Sensors for each item defined in the configuration file oneliners.conf.

There is a screenshot of the basic implementation in the screenshots folder.

How to configure is described in oneliners.conf itself which already contains 19 example sensors so you may just install and run.

Updates of values in Domoticz are done every minute.

To install the plugin you need to get the contents in your plugin folder :

On a Raspberry Pi you could :

Start a terminal and go to your plugins folder and the next will get it for you into a oneliners folder : 

 ....../plugins$ git clone https://github.com/JackV2020/Domoticz-Oneliners.git oneliners

later when you want to check for updates you go into the folder and issue git pull :
 ....../plugins/oneliners$ git pull
 Note that an update will give you a new oneliners.conf and overwrite yours.
 So before updating make sure to have a backup copy of yours.

To get it into Domoticz restart your domoticz like :

    sudo systemctl restart domoticz

After this you can add a device of the Type 'Jacks OneLiners'.

Thanks for reading and enjoy.
