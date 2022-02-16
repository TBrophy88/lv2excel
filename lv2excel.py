#!/usr/bin/env python3
"""
This module collects data from Lost Vault web api and outputs an excel file.
"""

__author__ = "Tom Brophy"
__version__ = "0.1.0"
__license__ = "MIT"

import argparse
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import emoji


def main(args):
    """ Main entry point of the app """

    # make sure args are valid
    if not args.Tribe and not args.Player:
        print("Please specify a tribe(s) and/or player(s) to collect data on using -t or -p respectively")

    replacements = {}
    if args.Replace_names:
        names_to_replace = [x.strip() for x in args.Replace_names.split(',')]
        if len(names_to_replace) % 2 != 0:
            print("Names to replace must be a list of comma separated pairs")
            return -1
        for i in range(0, len(names_to_replace), 2):
            replacements[names_to_replace[i]] = names_to_replace[i+1]

    player_names = []
    if args.Tribe:
        tribes_to_check = [x.strip() for x in args.Tribe.split(',')]
        player_names.extend(get_tribe_data(tribes_to_check))

    if args.Player:
        player_names.extend([x.strip() for x in args.Player.split(',')])

    if len(player_names) < 1:
        print("Error with player_names")
    else:
        get_player_data(player_names, replacements)


def get_tribe_data(tribes):
    tribe_data = {
        'Name': [""] * len(tribes),
        'Level': [None] * len(tribes),
        'Members': [None] * len(tribes),
        'Reactor': [None] * len(tribes),
        'Rank': [None] * len(tribes),
        'Fame': [None] * len(tribes),
        'Power': [None] * len(tribes),
        'Message': [""] * len(tribes),
    }
    player_names = []

    for i in range(0, len(tribes)):
        name = tribes[i]
        print("Gathering data on " + name + " tribe.")
        tribe_url = "https://api.lost-vault.com/guilds/" + name
        html_text = requests.get(tribe_url).text
        soup = BeautifulSoup(html_text, 'html.parser')

        # tribe info
        tribe_data['Name'][i] = soup.body.contents[3].contents[1].contents[1].contents[5].contents[1].contents[0].strip()
        tribe_data['Level'][i] = soup.body.contents[5].contents[1].contents[1].contents[1].contents[0].strip()
        tribe_data['Members'][i] = soup.body.contents[5].contents[1].contents[3].contents[1].contents[0].strip()
        tribe_data['Reactor'][i] = soup.body.contents[5].contents[1].contents[5].contents[1].contents[0].strip()
        tribe_data['Rank'][i] = soup.body.contents[9].contents[1].contents[1].contents[1].contents[0].strip()
        tribe_data['Fame'][i] = soup.body.contents[9].contents[1].contents[3].contents[1].contents[0].strip()
        tribe_data['Power'][i] = soup.body.contents[9].contents[1].contents[5].contents[1].contents[0].strip()
        tribe_data['Message'][i] = soup.body.contents[7].contents[1].contents[0].strip()

        for n in range(0, int(tribe_data['Members'][i])):
            table_row_index = n * 2 + 1
            player_name = \
                soup.body.contents[7].contents[3].contents[3].contents[table_row_index].contents[1].contents[
                    1].contents[
                    3].contents[0].strip()
            player_names.append(player_name)

    tribe_df = pd.DataFrame(tribe_data)
    ts = int(time.time())
    filename = 'Tribe data_' + str(ts) + '.xlsx'
    tribe_df.to_excel(filename, sheet_name="tribe data", index=False)

    return player_names


def get_player_data(names, replacements):
    player_data = {
        'Name': [""] * int(len(names)),
        'Tribe': [""] * int(len(names)),
        'Level': [""] * int(len(names)),
        'Power': [""] * int(len(names)),
        'Rank': [""] * int(len(names)),
        'Fame': [""] * int(len(names)),
        'Class': [""] * int(len(names)),
        'Strength': [""] * int(len(names)),
        'Agility': [""] * int(len(names)),
        'Endurance': [""] * int(len(names)),
        'Intelligence': [""] * int(len(names)),
        'Luck': [""] * int(len(names)),
        'Explores': [""] * int(len(names)),
        'Quests': [""] * int(len(names)),
        'Monsters': [""] * int(len(names)),
        'Caravan(hrs)': [""] * int(len(names)),
        'Vault': [""] * int(len(names)),
        'Survival': [""] * int(len(names)),
        'Message': [""] * int(len(names)),
    }

    for i in range(0, len(names)):
        player_name = names[i]
        if player_name in replacements:
            player_name = replacements[player_name]
        pn_url = player_name.lower()
        pn_url = remove_emojis(pn_url)
        pn_url = pn_url.replace(" ", "-")
        pn_url = pn_url.replace("!", "")
        pn_url = pn_url.replace(".", "")

        player_url = "https://api.lost-vault.com/players/" + pn_url
        print("Gathering data on player " + player_name + ".")
        player_html_text = requests.get(player_url).text
        player_soup = BeautifulSoup(player_html_text, 'html.parser')

        if len(player_soup.body.contents) < 5:
            continue

        name_text = player_soup.body.contents[3].contents[1].contents[1].contents[5].contents[1].contents[0].strip()
        player_name = name_text[name_text.find("]") + 1:].strip()
        tribe_name = name_text[1:name_text.find("]")].strip()
        player_data['Name'][i] = player_name
        player_data['Tribe'][i] = tribe_name
        player_data['Level'][i] = int(
            player_soup.body.contents[9].contents[1].contents[1].contents[1].contents[0].strip().replace(",", ""))
        player_data['Power'][i] = int(
            player_soup.body.contents[9].contents[1].contents[7].contents[1].contents[0].strip().replace(",", ""))
        player_data['Rank'][i] = int(
            player_soup.body.contents[9].contents[1].contents[3].contents[1].contents[0].strip().replace(",", ""))
        player_data['Fame'][i] = int(
            player_soup.body.contents[9].contents[1].contents[5].contents[1].contents[0].strip().replace(",", ""))
        if len(player_soup.body.contents[3].contents[1].contents[1].contents[5].contents[1].contents[1].contents) > 1:
            player_data['Class'][i] = \
                player_soup.body.contents[3].contents[1].contents[1].contents[5].contents[1].contents[1].contents[
                    2].strip()
        else:
            player_data['Class'][i] = \
                player_soup.body.contents[3].contents[1].contents[1].contents[5].contents[1].contents[1].contents[
                    0].strip()
        player_data['Strength'][i] = int(
            player_soup.body.contents[5].contents[1].contents[1].contents[1].contents[0].strip().replace(",", ""))
        player_data['Agility'][i] = int(
            player_soup.body.contents[5].contents[1].contents[3].contents[1].contents[0].strip().replace(",", ""))
        player_data['Endurance'][i] = int(
            player_soup.body.contents[5].contents[1].contents[5].contents[1].contents[0].strip().replace(",", ""))
        player_data['Intelligence'][i] = int(
            player_soup.body.contents[5].contents[1].contents[7].contents[1].contents[0].strip().replace(",", ""))
        player_data['Luck'][i] = int(
            player_soup.body.contents[5].contents[1].contents[9].contents[1].contents[0].strip().replace(",", ""))
        player_data['Explores'][i] = int(
            player_soup.body.contents[13].contents[1].contents[1].contents[1].contents[0].strip().replace(",", ""))
        player_data['Quests'][i] = int(
            player_soup.body.contents[13].contents[1].contents[3].contents[1].contents[0].strip().replace(",", ""))
        player_data['Monsters'][i] = int(
            player_soup.body.contents[13].contents[1].contents[5].contents[1].contents[0].strip().replace(",", ""))
        player_data['Caravan(hrs)'][i] = int(
            player_soup.body.contents[13].contents[1].contents[7].contents[1].contents[0].strip().replace(",", "")[:-1])
        player_data['Vault'][i] = int(
            player_soup.body.contents[13].contents[1].contents[9].contents[1].contents[0].strip().replace(",", ""))
        player_data['Survival'][i] = int(
            player_soup.body.contents[13].contents[1].contents[11].contents[1].contents[0].strip().replace(",", ""))
        if len(player_soup.body.contents[7].contents[1].contents) > 3:
            player_data['Message'][i] = player_soup.body.contents[7].contents[1].contents[3].contents[0].strip()

    player_df = pd.DataFrame(player_data)
    ts = int(time.time())
    filename = 'Player Data_' + str(ts) + '.xlsx'
    player_df.to_excel(filename, sheet_name="player data", index=False)


def remove_emojis(text):
    return emoji.get_emoji_regexp().sub(r'', text)


if __name__ == "__main__":
    """ This is executed when run from the command line """

    # parse args and pass to main method
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--Tribe", help="Target tribe(s) to collect data on, comma separated")
    parser.add_argument("-p", "--Player", help="Target player(s) to collect data on, comma separated")
    parser.add_argument("-r", "--Replace-names", help="Replace players names with their API 'name'.  Must be "
                                                      "comma separated pairs in quotes, for example: 'current name, "
                                                      "replacement, current name, replacement' etc")
    parsed_args = parser.parse_args()
    main(parsed_args)
