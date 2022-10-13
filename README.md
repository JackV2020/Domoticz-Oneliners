## Configurable oneliners plugin for Domoticz

This Domoticz plugin was developed on a Raspberry Pi and may work on other platforms.

No programming or lots of clicks to create and update Domoticz Devices and no clicking to put them in a Room.

The name is oneliners because the plugin reads a configuration file with single line commands and creates and updates a Device for each command.

Setting up a configuration file is easy. See the section "Your first configuration" below.

    The example in that section uses a simple command and there are also example files
    in the plugin folder with more usefull commands you may use and modify : 
    - get stock prices from the Internet, 
    - read data from your solar panel inverter, 
    - perform calculations using values of other Domoticz Devices defined in your configuration
      or from Domoticz Devices from other Hardware and maybe even from other Domoticz Servers
    - ......

To use the plugin you select it on the Hardware page, give in the name of your configuration file and give the Hardware a name.

Start the plugin and it creates a Domoticz Device for each oneliner command.

After creating the Domotics Devices it creates a Room with the name of your Hardware so it is easy to select on the Dashboard page.

Updates of values in Domoticz are done every minute.

### Below you find
[Installing the plugin](#installing-the-plugin)
<br>[Your first configuration](#your-first-configuration)
<br>[Basic commands](#basic-commands)
<br>[More advanced commands](#more-advanced-commands)
<br>[Substitutions](#substitutions)
<br>[Hiding Devices](#hiding-Devices)
<br>[Modifying a Device](#modifying-a-Device)


### Installing the plugin

To install the plugin you need to get something in your Domoticz folder :

On a Raspberry Pi you could :

Start a terminal and go to your Domoticz/plugins folder and the next will get it for you into a oneliners folder : 

 ......Domoticz/plugins$ git clone https://github.com/JackV2020/Domoticz-Oneliners.git oneliners

To get it loaded in Domoticz restart your Domoticz like :

    sudo systemctl restart Domoticz

After this you can start setting up configuration files.

After creating a configuration you can add Hardware of the Type 'Jacks OneLiners'.

#### Your first configuration

This example shows a very, very simple command and you will need and find very usefull examples in the other configuration files.

To get a hold of it just stick with this very simple example and look for more usefull commands later.


Each configuration file is located in the plugins/oneliners folder and holds one or more single line commands and with each command you need additional items.

The example for your first configuration is below. Put the 6 lines whithout empty lines between them in a new file mytest.conf.


line 1 the description:

Description=This should give you a value between 0 and 99

line 2 the name of the Device as it will be created in Domoticz:

Name=test

line 3 the type, ( I use Custom mostly and sometimes Text ):

Type=Custom

line 4 the image to be used, for now name it JVCloud :

Image=JVCloud

line 5 is the unit to be shown on the Device in Domoticz :

Units=TST

line 6 is the command which is executed to update the value :

Command=cat /proc/uptime | cut -d" " -f 1 | cut -d"." -f 2

What does this command do ?
/proc/uptime is a file with one line and the first value is the system uptime in seconds. The second value is the amount of time the system has been idle. We cut the line in parts delimited by a space " " and take the first part. Then we take that first part and cut it again using a "." and take the second part which is two decimals of the uptime.
This should result in a rather random number between 00 and 99.

It should look like :

    Description=This should give you a value between 0 and 99
    Name=test
    Type=Custom
    Image=JVCloud
    Units=TST
    Command=cat /proc/uptime | cut -d" " -f 1 | cut -d"." -f 2 

Save the file mytest.conf. 

Implement the plugin as Hardware named myfirsttest and give in the name mytest.conf as configuration file.

After you added the hardware you should have a Room named myfirsttest with a Device test with a cloud icon. The value may start at 0 but should turn to something else each minute or so.

Does not work ? >>> Please check the above and check and follow the notes on the Hardware page of the plugin. 

Now this works you can add more Devices to your configuration file. Just restart the plugin and they will appear in the Room.

    Names for Image for the icon in Domoticz can be found in the plugins/onliners/CustomIcons folder 
    and in Domoticz Setup >More Options > Custom Icons

Notes on commands :

    Always make sure to test the command on a command line before you activate it in Domoticz.
    Some commands may not work in Domoticz because you use properties of the terminal window process.
    To get a random number from 00 .. 99 in the terminal window you could use : echo $(( $RANDOM % 100 ))
    This does not work as a command in your config file because $RANDOM is part of a terminal process.

To remove a Device from Domoticz you just remove the Device from your configuration and restart the plugin.

### Basic commands

Basic commands are commands that return a single value like described above.
There is a command construction with curl I would like to describe.

A more usefull basic command is the next command which gives the value of the AEX exchange index :

    Description=AEX in €
    Name=stock> AEX
    Type=Custom
    Image=Euro
    Units=€
    Command=curl --connect-timeout 1 -s https://www.beleggen.nl/koersen/aex.aspx | grep 12272LastPrice | head -n 1 | cut -d "=" -f 2 | sed s/\;//

With curl you can get lots of information from web servers. 

So lets get a value from any Device in any Domoticz server. Does not seem to be usefull now but we will use the result in a more advanced command further below.

You know that in Domoticz you can find the idx of any Device in the 3rd column in Setup > Devices page. 

The command to get all the details of a Device on a Domoticz host with IP address 192.168.2.13 is :

curl -s 'http://[USERNAME:PASSWORD@]192.168.2.13:8080/json.htm?type=Devices&rid=[IDX]'

You can leave out the part of USERNAME and PASSWORD when you have no users and use :

curl -s 'http://192.168.2.13:8080/json.htm?type=Devices&rid=[IDX]'

With the next command you get all info on the Device with idx 1262 using user and secret as credentials :

curl -s 'http://user:secret@192.168.2.4:8080/json.htm?type=Devices&rid=1262'

Most of the times the value is in the data field so use :

curl -s 'http://user:secret@192.168.2.4:8080/json.htm?type=Devices&rid=1262' | grep Data | cut -d'"' -f 4

This will give you the value with the unit if any so you may need to remove that. Assume the answer is 123.23 L

Removing the last 2 characters ' L' can be done by adding | rev | cut -b 3- | rev

This reverses the string (L 32.321), cuts of the last part starting at position 3 (32.321) and reverses again. (123.23)

A fairly complete command to read the value is :

curl -s 'http://user:secret@192.168.2.4:8080/json.htm?type=Devices&rid=1262' | grep Data | cut -d'"' -f 4 | rev | cut -b 3- | rev

And the answer should now be be 123.23

Other examples giving 1 value can be found in the other configuration files.

You could also create something based on the command to look into the log of Domoticz :

curl 'http://user:secret@192.168.2.13:8080/json.htm?type=command&param=getlog&lastlogtime=0&loglevel=268435455' 2>/dev/null

When you have a user Jack in the system you could add | grep "'Jack'" | wc | tr -s " " | cut -d " " -f 2

and "audit" the logins like : 

Command=curl 'http://user:secret@192.168.2.13:8080/json.htm?type=command&param=getlog&lastlogtime=0&loglevel=268435455' 2>/dev/null | grep "'Jack'" | wc | tr -s " " | cut -d " " -f 2

### More advanced commands

More advanced commands do not return 1 single value but 2 values which can be combined by the plugin.
They may also use values from other Devices.

Advanced commands start with a prefix of 3 positions.

For a single command giving 2 results use the next prefix :

    '#+ '  : to add the two results of the command
    '#- '  : to substract them
    '#* '  : to multiply them
    '#/ '  : to devide them

Simple example to add 2 values which should result in a value 3.4 :

Command=#+ echo 1.2 2.2

A more complex command which gets the KB/s in and KB/s out of the interface eno1 and passes them to the plugin which adds them resulting in total network load : 

Command=#+ ifstat -i eno1 1 1 | grep -v eno1 | grep -v KB | tr -s " " | sed -e "s/^[ \t]*//"


For previously in your configuration file defined Devices use the next prefix :

    '@+ '  : to add the two results of two before defined sensors
    '@- '  : to substract them
    '@* '  : to multiply them
    '@/ '  : to devide them

Example to add 2 Devices ( assume you defined 2 Devices with names network input and network output )

Command=@+ "network input" "network output"

Note that here you need to put the names of the 2 Devices between double quotes. Always, also when the names do not contain spaces. These double quotes are expected by the plugin to find the Devices.

This is also where the long curl command from the previous section comes in. 
You could use that command to copy a value from any Device in any Domoticz server to let's say a Device named Remote Gas Copy. 

When you also defined a Device in your configuration named Local Gas you can calculate the total gas of 2 Domoticz servers like :

Command=@+ "Remote Gas Copy" "Local Gas"

For previously defined sensors use the next prefix to do something with an extra value

    'V+ '  : to add the value to the before defined sensor
    'V- '  : to substract the value
    'V* '  : to multiply by the value
    'V/ '  : to devide by the value

Example to substract a value from an existing one. 
Suppose you already read the total counter of your solar inverter with a curl command and put that in the Device Total Solar Energy.
When you have a value of 1234.56 on Januari 1st, the next will give you the production of this year.

Command=V- "Total Solar Energy" "1234.56"

Note that here you need to put the name and the value between double quotes. Always, also when the name does not contain spaces. These double quotes are expected by the plugin.

You will find more examples in the config files.

#### Substitution

Date substitution. To read date based data I needed two variable date formats in the curl command.

    DD-MM-YYYY   is translated by the plugin to todays date
    DD-MM-YYYY-1 is translated by the plugin to yesterdays date
    
    See P1meter.conf for details on how to use.
    When you see the commands it will be clear how to use.

#### Hiding Devices

When you use some or more advances commands you may have some Devices with intermediate results which you may want to hide from the Dashboard and your Room.

To hide a Device while keeping it available for data collection you would normally :

    In Domoticz select Setup > Devices, find your Device 
    and click on the white arrow in the blue circle to set it unused.
    Your Device will be hidden from the Dashboard etc. 
    but will still be updated by your oneliner.

Now when you want to hide a Device you put an extra line in your configuration for the Device you want to hide :

    ShowDevice=no

Remove the line or change the value to yes to show the Device again. Remember to activate the setting by restarting the plugin.
    
### Modifying a Device 

To change a description, image, units or command you make the change in your configuration file and restart the plugin. 

You can not change the type of the Device. When you want to change the type, you delete the Device from Domoticz, redefine your Device in your configuration and restart the plugin.

The most tricky thing is to rename a Device without losing data in Domoticz.
To rename a Device you need to first rename it in Domoticz and after that also in your configuration .
After reading the section "More advanced commands" above you understand that when you change a name of a Device you also need to change the commands using that Device.

Thanks for reading and enjoy.
