#
# Title : oneliners
# Author: Jack Veraart
# Date  : 2020-07-05
#     
# Changelog :
#
# version 2.0.0 : Changed for new Domoticz API
# version 1.0.3 : Added block comment in configuration files by using /* and */ as delimiters
# version 1.0.2 : Added substitutions YYYY and YYYY-1 for fixed dates in current and previous year like 23-04-YYYY and 17-01-YYYY-1
#                 Added substitution LAST for fixed last "day in month" like 23-03-LAST where LAST becomes either this year or previous year
#                 Added substitutions for yyyy-mm-dd formats like for DD-MM-YYYY formats like yyyy-mm-dd-1 for yesterday
# version 1.0.1 : Extra logging and some extra comments
# version 1.0.0 : Initial version
#
"""
<plugin key="JacksOneLiners" name="Jacks OneLiners" author="Jack Veraart" version="2.0.0">
    <description>
        <font size="4" color="white">OneLiners </font><font color="white">...Notes...</font>
        <ul style="list-style-type:square">
            <li><font color="yellow">Below you specify the config file like myfile.conf </font></li>
            <li><font color="yellow">Add Admin account details below so I can import icons and create a room.</font></li>
            <li><font color="yellow">To develop your own plugin...check this web site... <a href="https://www.domoticz.com/wiki/Developing_a_Python_plugin" ><font color="cyan">Developing_a_Python_plugin</font></a></font></li>
        </ul>
    </description>
    <params>
        <param field="Mode1" label="Config file."       width="120px" default="oneliners.conf"/>

        <param field="Mode2" label="Interval."          width="120px">
            <options>
                <option label="10 sec." value="10"/>
                <option label="20 sec." value="20"/>
                <option label="30 sec." value="30"/>
                <option label="40 sec." value="40"/>
                <option label="50 sec." value="50"/>
                <option label=" 1 min." value="60"    default="true"/>
            </options>
        </param>

        <param field="Username" label="Username."       width="120px" default="admin"/>

        <param field="Password" label="Password."       width="120px" default="domoticz" password="true"/>

        <param field="Mode6" label="Debug."             width="75px">
            <options>
                <option label="True"  value="Debug"/>
                <option label="False" value="Normal"    default="true"/>
            </options>
        </param>
    </params>
</plugin>
"""
import Domoticz

# Prepare some global variables

StartupOK=0
HomeFolder=''   # plugin finds right value
LocalHostInfo=''# plugin finds right value
RoomName=''     # plugin finds right value

ConfigFile=''          # Mode1
HeartbeatInterval= 10  # 10 seconds
HeartbeatCountMax= 0   # = Mode 2 / HeartbeatInterval ; 
HeartbeatCounter = 1   # counts down from Max to 1 before actual refresh; start with 1 which forces an immediate refresh after startup

Base_id=1
Base_Image='JVNo'

DeviceLibrary={}

class BasePlugin:
    enabled = False
    def __init__(self):
        #self.var = 123
        return

# --------------------------------------------------------------------------------------------------------------------------------------------------------

    def onStart(self):

        global StartupOK
        global ConfigFile
        global RoomName
        
        global HeartbeatInterval
        global HeartbeatCountMax
        global HomeFolder

        global LocalHostInfo

        self.pollinterval = HeartbeatInterval  #Time in seconds between two polls

        if Parameters["Mode6"] == 'Debug':
#            self.debug = True
            Domoticz.Debugging(1)
#            DumpConfigToLog()
        else:
            Domoticz.Debugging(0)
#            DumpConfigToLog()

        Domoticz.Log("onStart called")
        
        try:
#
# Set some globals variables to right values
#            
            RoomName        =str(Parameters['Name'])
            ConfigFile      =str(Parameters["Mode1"])
            HeartbeatCountMax = int(int(Parameters["Mode2"]) / HeartbeatInterval)
            HomeFolder      =str(Parameters["HomeFolder"])
            Username        =str(Parameters["Username"])
            Password        =str(Parameters["Password"])

            LocalHostInfo     = "https://"+Username+":"+Password+"@"+GetDomoticzIP()+":"+GetDomoticzHTTPSPort()

            StartupOK = ImportImages()

# Create devices as configured in oneliners.conf

            if StartupOK == 1:
            
                StartupOK = CreateDevices()
            
            if StartupOK == 1:
                
                Domoticz.Log('onStartup OK')

                Domoticz.Heartbeat(HeartbeatInterval)

            else:
                
                Domoticz.Log('ERROR starting up')
            
        except:

            StartupOK = 0

            Domoticz.Log('ERROR starting up')

# --------------------------------------------------------------------------------------------------------------------------------------------------------

    def onStop(self):
        Domoticz.Log("onStop called")

    def onConnect(self, Connection, Status, Description):
        Domoticz.Log("onConnect called")

    def onMessage(self, Connection, Data):
        Domoticz.Log("onMessage called")

    def onCommand(self, Unit, Command, Level, Hue):
        Domoticz.Log("onCommand called")

    def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
        Domoticz.Log("Notification: " + Name + "," + Subject + "," + Text + "," + Status + "," + str(Priority) + "," + Sound + "," + ImageFile)

    def onDisconnect(self, Connection):
        Domoticz.Log("onDisconnect called")

# --------------------------------------------------------------------------------------------------------------------------------------------------------
    
    def onHeartbeat(self):
        
        global HeartbeatCounter
        
        if StartupOK == 1:
            
#            Domoticz.Debug("onHeartbeat called "+str(HeartbeatCounter))
#            Domoticz.Log("onHeartbeat called "+str(HeartbeatCounter))

            if HeartbeatCounter == 1:
                
#                Domoticz.Debug('Update Monitors')
#                Domoticz.Log('Update Monitors')

                for Device in DeviceLibrary:
                    
                    GetValue(Device)
#                    Domoticz.Log("DeviceLibrary[Device]['sValue'] : "+DeviceLibrary[Device]['sValue'])
                    Devices[DeviceLibrary[Device]['Unit']].Update(  nValue=0, sValue=DeviceLibrary[Device]['sValue'])
#                    Domoticz.Log(Devices[DeviceLibrary[Device]['Unit']].Name + "  "+Devices[DeviceLibrary[Device]['Unit']].sValue)
            
                HeartbeatCounter = HeartbeatCountMax
            
            else:

                HeartbeatCounter = HeartbeatCounter - 1
            
# --------------------------------------------------------------------------------------------------------------------------------------------------------

global _plugin
_plugin = BasePlugin()

def onStart():
    global _plugin
    _plugin.onStart()

def onStop():
    global _plugin
    _plugin.onStop()

def onConnect(Connection, Status, Description):
    global _plugin
    _plugin.onConnect(Connection, Status, Description)

def onMessage(Connection, Data):
    global _plugin
    _plugin.onMessage(Connection, Data)

def onCommand(Unit, Command, Level, Hue):
    global _plugin
    _plugin.onCommand(Unit, Command, Level, Hue)

def onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile):
    global _plugin
    _plugin.onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile)

def onDisconnect(Connection):
    global _plugin
    _plugin.onDisconnect(Connection)

def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

    # Generic helper functions
def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Log( "'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Log("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Log("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Log("Device ID:       '" + str(Devices[x].ID) + "'")
        Domoticz.Log("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Log("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Log("Device sValue:   '" + Devices[x].sValue + "'")
        Domoticz.Log("Device LastLevel: " + str(Devices[x].LastLevel))
    return
    
def DumpConfigToLogDebugs():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug( "'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Debug("Device ID:       '" + str(Devices[x].ID) + "'")
        Domoticz.Debug("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Debug("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
        Domoticz.Debug("Device LastLevel: " + str(Devices[x].LastLevel))
    return
    

# --------------------------------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------  Image Management Routines  -----------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------------------

def GetDomoticzHTTPSPort():

    try:
        import subprocess
    except:
        Domoticz.Log("python3 is missing module subprocess")

    try:
        import time
    except:
        Domoticz.Log("python3 is missing module time")

    try:
        Domoticz.Debug('GetDomoticzHTTPSPort check startup file')
        pathpart=Parameters['HomeFolder'].split('/')[3]
        searchfile = open("/etc/init.d/"+pathpart+".sh", "r")
        for line in searchfile:
            if ("-sslwww" in line) and (line[0:11]=='DAEMON_ARGS'):
                HTTPSPort=str(line.split(' ')[2].split('"')[0])
                HTTPSPort = HTTPSPort.replace('\\n','') # remove EOL
        searchfile.close()
        Domoticz.Debug('GetDomoticzHTTPSPort looked in: '+"/etc/init.d/"+pathpart+".sh"+' and found port: '+HTTPSPort)
    except:
        Domoticz.Debug('GetDomoticzHTTPSPort check running process')
        command='ps -ef | grep domoticz | grep sslwww | grep -v grep | tr -s " "'
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

        timeouts=0

        result = ''
        while timeouts < 10:
            p_status = process.wait()
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                HTTPSPort=str(output)
                HTTPSPort = HTTPSPort[HTTPSPort.find('-sslwww'):]
                HTTPSPort = HTTPSPort[HTTPSPort.find(' ')+1:]
                HTTPSPort = HTTPSPort[:HTTPSPort.find(' ')]
                HTTPSPort = HTTPSPort.replace('\\n','') # remove EOL
            else:
                time.sleep(0.2)
                timeouts=timeouts+1
        Domoticz.Log('GetDomoticzHTTPSPort looked at running process and found port: '+HTTPSPort)

    return HTTPSPort

# --------------------------------------------------------------------------------------------------------------------------------------------------------
def GetImageDictionary():

    import json
    import requests

    try:
        mydict={}

        url=LocalHostInfo+'/json.htm?type=command&param=custom_light_icons'

        response=requests.get(url, verify=False)
        data = json.loads(response.text)
        for Item in data['result']:
            mydict[str(Item['imageSrc'])]=int(Item['idx'])

    except:
        mydict={}
    
    return mydict

# --------------------------------------------------------------------------------------------------------------------------------------------------------

def ImportImages():
#
# Import ImagesToImport if not already loaded
#
    try :
        import glob
    except:
        Domoticz.Log("python3 is missing module glob")

    global ImageDictionary
    
    MyStatus=1
    
    ImageDictionary=GetImageDictionary()
    
    if ImageDictionary == {}:
        Domoticz.Log("Please modify your setup to have Admin access. (See Hardware setup page of this plugin.)")      
        MyStatus = 0
    else:

        for zipfile in glob.glob(HomeFolder+"CustomIcons/*.zip"):
            importfile=zipfile.replace(HomeFolder,'')
            try:
                Domoticz.Image(importfile).Create()
                Domoticz.Debug("ImportImages Imported/Updated icons from "  + importfile)
            except:
                MyStatus = 0
                Domoticz.Log("ImportImages ERROR can not import icons from "  + importfile)

        if (MyStatus == 1) : 
            ImageDictionary=GetImageDictionary()
            Domoticz.Debug('ImportImages Oke')

    return MyStatus

# --------------------------------------------------------------------------------------------------------------------------------------------------------

def GetDomoticzIP():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

# --------------------------------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------  Device Creation Routines  ------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------------------
def CreateDevice(deviceunit,devicename,devicetype,devicelogo="",devicedescription="",sAxis="",InitialValue=0.0,ShowDevice=1):
    
    if deviceunit not in Devices:

        if ImageDictionary == {}:
            firstimage=0
            firstimagename='NoImage'
            Domoticz.Log("ERROR I can not access the image library. Please modify the hardware setup to have the right Username and Password.")      
        else:
            firstimage=int(str(ImageDictionary.values()).split()[0].split('[')[1][:-1])
            firstimagename=str(ImageDictionary.keys()).split()[0].split('[')[1][1:-2]
#            Domoticz.Debug("First image id: " + str(firstimage) + " name: " + firstimagename)
            Domoticz.Log("First image id: " + str(firstimage) + " name: " + firstimagename)

        if firstimage != 0: # we have a dictionary with images and hopefully also the image for devicelogo

            try:

                deviceoptions={}
                deviceoptions['Custom']="1;"+sAxis
                Domoticz.Device(Name=devicename, Unit=deviceunit, TypeName=devicetype, Used=1, Image=ImageDictionary[devicelogo], Description=devicedescription).Create()
                Devices[deviceunit].Update(nValue=Devices[deviceunit].nValue, sValue=str(InitialValue), Used=ShowDevice)
                Domoticz.Log("Created device : " + devicename + " with '"+ devicelogo + "' icon and options "+str(deviceoptions)+' Value '+str(InitialValue))
            except:

# when devicelogo does not exist, use the first image found, (TypeName values Text and maybe some others will use standard images for that TypeName.)

                try:
                    Domoticz.Device(Name=devicename, Unit=deviceunit, TypeName=devicetype, Used=1, Image=firstimage, Description=devicedescription).Create()
                    Devices[deviceunit].Update(nValue=Devices[deviceunit].nValue, sValue=str(InitialValue), Used=ShowDevice)
                    Domoticz.Log("Created device : " + devicename+ " with '"+ firstimagename + "' icon and Value "+str(InitialValue))
                except:
                    Domoticz.Log("ERROR Could not create device : " + devicename)
#
# The next puts the right name, axis, image and description in the device
#
    try:

        NewName = devicename

        deviceoptions={}
        deviceoptions['Custom']="1;"+sAxis

        Devices[deviceunit].Update(nValue=Devices[deviceunit].nValue, sValue=Devices[deviceunit].sValue, Name=NewName, Options=deviceoptions, Image=ImageDictionary[devicelogo], Description=devicedescription, Used=ShowDevice)

        Domoticz.Debug("Updated "+NewName)
    except:
        Domoticz.Log("Update Failed")
        dummy=1

# --------------------------------------------------------------------------------------------------------------------------------------------------------
def CreateDevices():

    global DeviceLibrary
    global ConfigFile
#
# Suppose there are no changes for the Room, even when not created yet
#    
    Recreate = False
    
    DeviceLibrary={}
    Name=''
    Type=''
    ShowDevice='yes'
    Units=''
    Command=''
    MyStatus=1
    CommentBlock = False
#    ConfigFile='oneliners.conf'
    try:
        TheConfigFile=open(HomeFolder+ConfigFile, "r")
        TheConfigFile.close
        for Line in TheConfigFile:

            CommentBlock = CommentBlock or  ( Line[:2] == '/*' )

#        if Line[0] != '#' and Line.replace(' ','').replace('\t','') != '\n':    # skip comments and empty lines
#            if Line[0] not in ['#', ' ', '\t', '\n' ] and Line.replace(' ','').replace('\t','') != '\n':    # skip comments and empty lines
            if (not CommentBlock) and (Line[0] not in ['#', ' ', '\t', '\n' ] and Line.replace(' ','').replace('\t','') != '\n' ) :    # skip comments and empty lines

                Line=Line.replace('\n','')                  # remove EOL
#                Domoticz.Log('------------------------------------')
#                Domoticz.Log(Line)
                if Line.split('=')[0] == 'Name':
                    Name = Line.split('=')[1]
                elif Line.split('=')[0] == 'Description':
                    Description = Line.split('=')[1]
                elif Line.split('=')[0] == 'Type':
                    Type = Line.split('=')[1]
                elif Line.split('=')[0] == 'ShowDevice':
                    ShowDevice = Line.split('=')[1]
                elif Line.split('=')[0] == 'Image':
                    Image = Line.split('=')[1]
                elif Line.split('=')[0] == 'Units':
                    Units = Line.split('=')[1]
                elif Line.split('=')[0] == 'Command':
                    Command = Line.split('=',1)[1]
#                    Domoticz.Log(Command)
                    DeviceEntry={}
                    DeviceEntry['Name']   = Name
                    DeviceEntry['Description']   = Description
                    DeviceEntry['Type']   = Type
                    if (ShowDevice == "yes"):
                        DeviceEntry['ShowDevice'] = 1
                    else:
                        DeviceEntry['ShowDevice'] = 0
                    DeviceEntry['Image']  = Image
                    DeviceEntry['Units']  = Units
                    DeviceEntry['Command']= Command
                    DeviceEntry['Unit']   = -1
                    DeviceLibrary[Name]   = DeviceEntry
# force default value
                    ShowDevice = 'yes'
#                    Domoticz.Log(str(DeviceEntry))
                else:
                    Domoticz.Log('Error Line: '+Line)
                    MyStatus=-1
#        Domoticz.Log(str(DeviceLibrary))
            if ( Line[:2] == '*/' ) :
                CommentBlock = False
    except:
        MyStatus = -1
        Domoticz.Log('Error opening config file: '+HomeFolder+ConfigFile)

    if MyStatus == 1:
#
# Check which devices I already have created during a previous startup
#        
        for Unit in Devices:
            if Devices[Unit].Name in DeviceLibrary:
                DeviceLibrary[Devices[Unit].Name]['Unit'] = Unit
#
# Create new devices
#    
        for Device in DeviceLibrary:
            if DeviceLibrary[Device]['Unit'] == -1:
                Recreate = True
                Domoticz.Log('Need to create '+str(Device))
                Unit = 1
                while Unit in Devices:
                    Unit = Unit + 1
                DeviceLibrary[Device]['Unit'] = Unit
                CreateDevice(Unit,Device,DeviceLibrary[Device]['Type'],DeviceLibrary[Device]['Image'],DeviceLibrary[Device]['Description'],DeviceLibrary[Device]['Units'],0,int(DeviceLibrary[Device]['ShowDevice']))
            else:
                Domoticz.Debug('May need to update '+str(Device))
                CreateDevice(DeviceLibrary[Device]['Unit'],Device,DeviceLibrary[Device]['Type'],DeviceLibrary[Device]['Image'],DeviceLibrary[Device]['Description'],DeviceLibrary[Device]['Units'],0,int(DeviceLibrary[Device]['ShowDevice']))
#
# Delete devices which are not in the config file anymore
#                
        DeleteOne=1
        while DeleteOne == 1: # My implementation of repeat until, make sure to get into the loop and immediately make sure to get out of it
            DeleteOne = 0
            for Unit in Devices: # inner loop to find what to delete
                if not Devices[Unit].Name in DeviceLibrary:
                    DeleteOne = 1                                               # stay in the loop because we may have to do our thing again
                    UnitToDelete = Unit
                    Item=Devices[Unit].Name
            if DeleteOne == 1: # out of the inner loop it is safe to delete
                Domoticz.Log('.....')
                Domoticz.Log('.....Delete  my own device:  **'+Item+'**  Unit: **'+str(UnitToDelete)+'**')
                Devices[UnitToDelete].Delete()
                Domoticz.Log('.....Deleted my own device:  **'+Item+'**  Unit: **'+str(UnitToDelete)+'**')

#
# (Re-)Create Room
#
        RoomIdx=CreateRoom( RoomName, Recreate)
        if (RoomIdx == 0):
            MyStatus = 0
#
# Add all items from configuration file to Room if not already in
#
# Note that the order in the config file determines the order in the room
#
        if (MyStatus == 1):

            Domoticz.Debug('CreateDevices put devices in room')

            for Device in DeviceLibrary:
                Addition = AddToRoom(RoomIdx,Devices[DeviceLibrary[Device]['Unit']].ID)
                if (Addition == 0):
                    MyStatus = 0

    return MyStatus
# --------------------------------------------------------------------------------------------------------------------------------------------------------
def CreateRoom(RoomName, Recreate):

    try:
        import json
    except:
        Domoticz.Log("python3 is missing module json")
        
    try:
        import requests
    except:
        Domoticz.Log("python3 is missing module requests")
    
    idx=0

    try:

        Domoticz.Debug('Check if Room Exists')
        
        url=LocalHostInfo+'/json.htm?type=command&param=getplans&order=name&used=true'
        Domoticz.Debug('Check Room '+url)
        response=requests.get(url, verify=False)
#        response=requests.get(url)
        data = json.loads(response.text)

        if 'result' in data.keys():
            for Item in data['result']:
                if str(Item['Name']) == RoomName:
                    idx=int(Item['idx'])
                    Domoticz.Debug('Found Room '+RoomName+' with idx '+str(idx))

        if (idx != 0) and Recreate :
            url=LocalHostInfo+'/json.htm?idx='+str(idx)+'&param=deleteplan&type=command'
            Domoticz.Log('Delete Room '+url)
            response=requests.get(url, verify=False)
#            response=requests.get(url)
            idx = 0
        
        if idx == 0 :
            url=LocalHostInfo+'/json.htm?name='+RoomName+'&param=addplan&type=command'
            Domoticz.Log('Create Room '+url)
            response=requests.get(url, verify=False)
#            response=requests.get(url)
            data = json.loads(response.text)
            Domoticz.Log('CreateRoom Created Room'+str(data))
            idx=int(data['idx'])
    except:
        Domoticz.Log('ERROR CreateRoom Failed')
        idx=0

    Domoticz.Debug('CreateRoom status should not be 0 : '+str(idx))
    
    return idx
# --------------------------------------------------------------------------------------------------------------------------------------------------------
def AddToRoom(RoomIDX,ItemIDX):

    try:
        import json
    except:
        Domoticz.Log("python3 is missing module json")
        
    try:
        import requests
    except:
        Domoticz.Log("python3 is missing module requests")
    
    status=1

    try:
        url=LocalHostInfo+'/json.htm?activeidx='+str(ItemIDX)+'&activetype=0&idx='+str(RoomIDX)+'&param=addplanactivedevice&type=command'
        response=requests.get(url, verify=False)
#        response=requests.get(url)
        data = json.loads(response.text)
    except:
        Domoticz.Log('ERROR AddRoom Failed')
        status=0

    Domoticz.Debug('AddToRoom status should not be 0 : '+str(status))
    
    return status

# --------------------------------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------  Hardware Routines --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------------------

def GetValue(Device):

    global DeviceLibrary

    try:
        import subprocess
    except:
        Domoticz.Log("python3 is missing module subprocess")
    try:
        import time
    except:
        Domoticz.Log("python3 is missing module time")
 
    try:
        from datetime import date
        from datetime import timedelta
        from datetime import datetime
    except:
        Domoticz.Log("python3 is missing module datetime")

    command=DeviceLibrary[Device]['Command']
#    Domoticz.Log("Command : "+command)

# replace date strings upper case
    if command.find("DD-MM-YYYY-1") > -1 :              # yesterday = DD-MM-YYYY-1
        today = date.today()
        yesterday = today - timedelta(days = 1)
        d1 = yesterday.strftime("%d-%m-%Y")
        command = command.replace('DD-MM-YYYY-1',d1)    # today = DD-MM-YYYY
    if command.find("DD-MM-YYYY") > -1 :
        today = date.today()
        d1 = today.strftime("%d-%m-%Y")
        command = command.replace('DD-MM-YYYY',d1)
    if command.find("YYYY-1") > -1 :                    # last year fixed day and month like 23-11-YYYY-1
        current_year = date.today().year
        d1 = str(current_year - 1)
        command = command.replace('YYYY-1',d1)
    if command.find("-YYYY") > -1 :
        current_year = date.today().year
        d1 = str(current_year)
        command = command.replace('YYYY',d1)
    if command.find("-LAST") > -1 : # like 23-11-LAST
        today = datetime.now()

        date_start=command.find("LAST") - 6
        check_day   = int(command[date_start:date_start+2])
        check_month = int(command[date_start+3:date_start+5])
        the_year  = date.today().year
        check_date  = datetime(the_year, check_month, check_day)
        
        if ( check_date > today):
            the_year = the_year - 1
            
        command = command.replace(command[date_start:date_start+6]+'LAST',command[date_start:date_start+6]+str(the_year))

# replace date strings lower case
    if command.find("yyyy-mm-dd-1") > -1 :              # yesterday = yyyy-mm-dd
        today = date.today()
        yesterday = today - timedelta(days = 1)
        d1 = yesterday.strftime("%Y-%m-%d")
        command = command.replace('yyyy-mm-dd-1',d1)
    if command.find("yyyy-mm-dd") > -1 :                # today = yyyy-dd-mm
        today = date.today()
        d1 = today.strftime("%Y-%m-%d")
        command = command.replace('yyyy-mm-dd',d1)
    if command.find("yyyy-1-") > -1 :                   # last year fixed day and month like yyyy-1-11-23
        current_year = date.today().year
        d1 = str(current_year - 1)
        command = command.replace('yyyy-1',d1)
    if command.find("yyyy-") > -1 :                      # this year fixed day and month like yyyy-11-23
        current_year = date.today().year
        d1 = str(current_year)
        command = command.replace('yyyy',d1)
    if command.find("last-") > -1 :                      # last valid date for date month like last-11-23
        today = datetime.now()

        date_start=command.find("last")
        check_day   = int(command[date_start+8:date_start+10])
        check_month = int(command[date_start+5:date_start+7])
        the_year  = date.today().year
        check_date  = datetime(the_year, check_month, check_day)
        
        if ( check_date > today):
            the_year = the_year - 1
            
#        command = command.replace(command[date_start:date_start+6]+'LAST',command[date_start:date_start+6]+str(the_year))
        command = command.replace('last'+command[date_start+4:date_start+10],str(the_year)+command[date_start+4:date_start+10])
# add / substract etc. existing devices
    if command.find('@+') == 0:
        Sources=command[command.find('"'):]
        Source1=Sources[1:Sources.find('"',2)]
        Source2=Sources[Sources.find('"',len(Source1)+2)+1:-1]
        result=str(float(DeviceLibrary[Source1]['sValue'])+float(DeviceLibrary[Source2]['sValue']))
    elif command.find('@-') == 0:
        Sources=command[command.find('"'):]
        Source1=Sources[1:Sources.find('"',2)]
        Source2=Sources[Sources.find('"',len(Source1)+2)+1:-1]
        result=str(float(DeviceLibrary[Source1]['sValue'])-float(DeviceLibrary[Source2]['sValue']))
    elif command.find('@*') == 0:
        Sources=command[command.find('"'):]
        Source1=Sources[1:Sources.find('"',2)]
        Source2=Sources[Sources.find('"',len(Source1)+2)+1:-1]
        result=str(float(DeviceLibrary[Source1]['sValue'])*float(DeviceLibrary[Source2]['sValue']))
    elif command.find('@/') == 0:
        Sources=command[command.find('"'):]
        Source1=Sources[1:Sources.find('"',2)]
        Source2=Sources[Sources.find('"',len(Source1)+2)+1:-1]
        result=str(float(DeviceLibrary[Source1]['sValue'])/float(DeviceLibrary[Source2]['sValue']))
    elif command.find('V+') == 0:
        Sources=command[command.find('"'):]
        Source=Sources[1:Sources.find('"',2)]
        Value=Sources[Sources.find('"',len(Source)+2)+1:-1]
        result=str(float(DeviceLibrary[Source]['sValue'])+float(Value))
    elif command.find('V-') == 0:
        Sources=command[command.find('"'):]
        Source=Sources[1:Sources.find('"',2)]
        Value=Sources[Sources.find('"',len(Source)+2)+1:-1]
        result=str(float(DeviceLibrary[Source]['sValue'])-float(Value))
    elif command.find('V*') == 0:
        Sources=command[command.find('"'):]
        Source=Sources[1:Sources.find('"',2)]
        Value=Sources[Sources.find('"',len(Source)+2)+1:-1]
        result=str(float(DeviceLibrary[Source]['sValue'])*float(Value))
    elif command.find('V/') == 0:
        Sources=command[command.find('"'):]
        Source=Sources[1:Sources.find('"',2)]
        Value=Sources[Sources.find('"',len(Source)+2)+1:-1]
        result=str(float(DeviceLibrary[Source]['sValue'])/float(Value))
# prepare add / substract etc.  2 results
    else:
        if command.find('#+') == 0:
            command = command[3:]
            action = '+'
        elif command.find('#-') == 0:
            command = command[3:]
            action = '-'
        elif command.find('#*') == 0:
            command = command[3:]
            action = '*'
        elif command.find('#/') == 0:
            command = command[3:]
            action = '/'
        else:
            action = ''
        
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

        timeouts=0

        result = ''
        while timeouts < 10:

            p_status = process.wait()

            output = process.stdout.readline()

            if output == '' and process.poll() is not None:
                break

            if output:
                
#                Domoticz.Log("output :>"+str(output)+"<")
                            
                result=str(output.strip())[2:-1]

#                Domoticz.Log("result :>"+str(result)+"<")

# actual add / substract etc. 2 results

                if action == '+':
                    result=str(float(result.split(' ')[0])+float(result.split(' ')[1]))

                if action == '-':
                    result=str(float(result.split(' ')[0])-float(result.split(' ')[1]))

                if action == '*':
                    result=str(float(result.split(' ')[0])*float(result.split(' ')[1]))

                if action == '/':
                    result=str(float(result.split(' ')[0])/float(result.split(' ')[1]))

                timeouts=10
            else:
                time.sleep(0.2)
                timeouts=timeouts+1

    DeviceLibrary[Device]['sValue'] = result

    return
        
# --------------------------------------------------------------------------------------------------------------------------------------------------------
