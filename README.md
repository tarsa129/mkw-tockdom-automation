# MKWii Tockdom Automation

## Purpose
The [moderators of the Custom Mario Kart Wiiki](https://wiki.tockdom.com/wiki/Help:Contents#Wiiki_Team) spend a lot of time mass-editing wiki pages. The purpose of this project is to automate these processes to save on unnecessary manual work.  

## Features
### Obsolete (One-Time Conversions)
* Conversion of tables to Distribution-Info template on most distribution pages.
* Fixup of Distribution-Info templates to utilize {{PAGENAME}} template and convert CTGP Revolution type to My Stuff. 
* Conversion of slot information text to Slot-Info template. 

### Currently Active
* Update of track page Misc-Info templates to add wbz-id and image-id parameters.

### In-Progress
* Update of track page distribution lists

### Planned
* Update of "List Of" / News pages / Userlink pages for new releases.


## Setup
1. Install Python dependencies using the provided requirements.txt file.
2. Obtain Tockdom API key from [Tock](https://wiki.tockdom.com/wiki/User:Tock). Fill TOCKDOM_API_KEY variable in constants.py.
3. Create bot account using [the "Bot passwords" special page](https://wiki.tockdom.com/wiki/Special:BotPasswords). Fill in WIKI_BOT_USERNAME and WIKI_BOT_PASSWORD in constants.py.

## Running
The three arguments that you can pass in are 
* commandgroup
  * Defines the type of page / the part of the page that is edited
* action
  * Defines the specific action taken on the page element. Differs between commandgroups.     
* file
  * .csv file that allows for bulk processing and for more parameters to be sent in based on the commandgroup and action.
```
python basic_commands.py --commandgroup distros --action add --file path/to/file.csv
```
