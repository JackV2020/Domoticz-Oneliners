This Domoticz plugin was developed on a Raspberry Pi and may work on other platforms also.

This plugin manages Generic Custom Sensors for each item defined in the configuration file like oneliners.conf.

The filename oneliners.conf is a parameter on the setup page of the plugin so you may also create other .conf files and implement other hardware with that.

I also have :

    - a barometer (Wemos with bme280, is/will be in my github) and included a conf file for that.

    - an Omnik inverter for my solar panels and included the conf file for that.
    
When you create a hardware you need to give it a name.

A room will be created with that name and contain the sensors you defined in your conf file.

How to configure is described in oneliners.conf itself which already contains 19 example sensors so you may just install and run.

Updates of values in Domoticz are done every minute.

To install the plugin you need to get the contents in your plugin folder :

On a Raspberry Pi you could :

Start a terminal and go to your plugins folder and the next will get it for you into a oneliners folder : 

 ....../plugins$ git clone https://github.com/JackV2020/Domoticz-Oneliners.git oneliners

To get it into Domoticz restart your domoticz like :

    sudo systemctl restart domoticz

After this you can add a device of the Type 'Jacks OneLiners' and give it the name you want your room to have.

Thanks for reading and enjoy.
