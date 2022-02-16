# lv2excel
A python script that collects and organizes Lost Vault player data into excel format.
This is an extremely early/beta/incomplete script and may not work as expected or AT ALL.  If you have problems or suggestions, let me know and I will do what I can.



Requirements:
	-python3
	-argparse
	-requests
	-time
	-BeautifulSoup4
	-pandas
	-emoji
	
	
	
	
Installation

-Download lv2excel.py
-Install python3 on your computer
-Run the following command after python is installed:
pip3 install argparse requests time BeautifulSoup4 pandas emoji




Usage

Open your terminal and navigate to the folder with lv2excel.py

The script can then be executed with the command:
python3 lv2excel.py

optional arguments:
  -h, --help            show this help message and exit
  -t TRIBE, --Tribe TRIBE
                        Target tribe(s) to collect data on, comma separated
  -p PLAYER, --Player PLAYER
                        Target player(s) to collect data on, comma separated
  -r REPLACE_NAMES, --Replace-names REPLACE_NAMES
                        Replace players names with their API 'name'. Must be comma separated pairs in quotes, for
                        example: 'current name, replacement, current name, replacement' etc


You must use either the -p or -t arguments for this script to do anything (it needs something to check to function, that's the whole point..)

If you wish to check multiple tribes or players at once, enter them as comma separated values in single quotes as the value for the argument.  For example:

python3 lv2excel.py -t 'tribe1, tribe2, tribe3'
python3 lv2excel.py -p 'player1, player2' -t 'tribe10, tribe11'




Notes

To get the tribe name for lookup, go into the game app, navigate to the tribes page and click on the share button in the top right corner.  The link shared will look like this:

https://api.lost-vault.com/guilds/***TRIBE NAME***/

the ***TRIBE NAME*** is the bit that you use as the value of the -t argument in the command line execution of this script.

Similarly, you can find the true API name of a player by navigating to their stats page in game and clicking on the share button in the top right corner.  The link shared will look like this:

https://api.lost-vault.com/players/***PLAYER NAME***/

Again, the ***PLAYER NAME*** is the bit you would use as the value of the -p argument.

The names may not be what you expect.  As far as I can tell, names which have been changed in game still use the original name in the API, and names with "unusual" characters are assigned completely different names for the api (like "user-123")

You can run this script on a tribe and then see which players info is not collected.  Double check in game if their API name is the same as their ingame name.  If their API name is different than their ingame name you can use the -r argument to replace their in game name with their API name like this:

python3 lv2excel.py -t tribe_name -r 'weird_name_1, user-123, person_with_new_name, persons_old_name'

