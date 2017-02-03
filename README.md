# hive-home

A tool to control your Hive thermostat to enable/disable your heating schedule dependant upon your mobile phones being connected to your home wifi.

The Hive Thermostat has a geolocation feature, however it doesn't actually turn your heating on/off for you, it just gives you alerts in the mobile app. This tool tries to mimic the Google Nest feature by turning the heating on/off based on whether you mobile phones are connected to your home wifi network. e.g. if it can't ping any mobile phones in your house then it assumes you are all out and turns the heating off. As soon as it can ping a phone, it assumes someone has come home and turns it back onto the schedule again.

Logic:
* If at least one phone responds then it turns the Hive on to use your schedule
* If no phones respond, it turns your heating off
* If you system is in BOOST mode, then it sleeps for 10 minutes before reassessing
* If you come home, it will take approx one minute to (if you use the default period config of 60sec) to turn the heating back on.

## Requirements:
1. Each of your mobile phones will need to be mapped to a static IP in your router/DHCP server. This is normally relaitvely straight forward if you have access to your broadband router. Once you have set them to static IPs, make a note of them as they will need to be added to the config file.
2. You will need a always-on computer to run this on, I use a little Ubuntu microserver, a Rasberry Pi would also do nicely.
3. It's written/tested to work against Python 3.x
4. It requires the PyYAML library (e.g. run: `pip3 install pyyaml`)

## Installation:
1. Sync the git respository locally
2. Edit the sample config file (etc/hive.yml) with your Hive username and password and the IP addresses you want to have monitored. Other configs you can play with are:
  1. `Log`: pretty self explanitory, note the logs rotate over 5 days. 
  2. `Period`: how long to wait in between pinging each IP
  3. `Limit`: how many failed ping attempts between turning the heating OFF
3. To deploy it run: `python3 hive.py --config <path to your config file> start`
4. Add it to your start sequence to run when your host reboots.

## Credits:
1. It uses a daemon module borrowed from [here](http://web.archive.org/web/20131017130434/http://www.jejik.com/articles/2007/02/a_simple_unix_linux_daemon_in_python/)
2. Hive API details at [Smartofthehome](http://www.smartofthehome.com/2016/05/hive-rest-api-v6/)

