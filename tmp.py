from bs4 import BeautifulSoup
import requests
import json
import os
import sqlite3


def get_remote_team_data():
    '''Get NFL team data from espn site'''

    r = requests.get('https://www.espn.com/nfl/teams')
    soup = BeautifulSoup(r.text, 'lxml')

    for script_tag in soup.findAll('script'):
        if '__espnfitt__' in str(script_tag):
            break
    else:
        raise Exception('Script not found')

    data = str(script_tag)
    data = '='.join(data.split('=')[2:])
    data = ';'.join(data.split(';')[:-1])

    json_dict = json.loads(data)
    return json_dict


def get_teams_data(reload=False):
    file_name = 'cache/teams.json'
    os.makedirs('cache', exist_ok=True)
    if reload is True:
        # force reload cache
        print('Force reload')
        json_dict = get_remote_team_data()
        json_dict = json_dict.get('page').get('content')
        with open(file_name, 'w') as f:
            json.dump(json_dict, f)
    else:
        try:
            with open(file_name, 'r') as f:
                # cache hit
                print('Cache hit')
                json_dict = json.load(f)
        except FileNotFoundError:
            # cache miss, reload cache
            print('Cache miss')
            json_dict = get_remote_team_data()
            json_dict = json_dict.get('page').get('content')
            with open(file_name, 'w') as f:
                json.dump(json_dict, f)
    return json_dict


def temp(divisions):
    division_data = []
    for i, division in enumerate(divisions):
        division_data.append((i, division))

    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        cursor.execute('DROP TABLE IF EXISTS Division')
        cursor.execute('''
            CREATE TABLE Division(
                division_id INT NOT NULL PRIMARY KEY,
                division_name TEXT NOT NULL
            )
        ''')
        cursor.executemany('INSERT INTO Division VALUES (?, ?)', division_data)
        cursor.execute('SELECT * FROM Division')
        rows = cursor.fetchall()
    return rows


# class Team:
#     team_id = None
#     team_fullname = None
#     team_name = None
#     team_logo = None
#     team_abbr = None
#     team_division = None


# class Division:
#     division_name = None


def main():
    json_dict = get_teams_data()
    nfl_json = json_dict.get('teams').get('nfl')
    divisions = []
    for element in nfl_json:
        division = element.get('name')
        divisions.append(division)
        for team in element.get('teams'):
            team_id = team.get('id')
            team_fullname = team.get('name')
            team_name = team.get('shortName')
            team_logo = team.get('logo')
            team_abbr = team.get('abbrev')

    rows = temp(divisions)
    for row in rows:
        print(row)


if __name__ == '__main__':
    main()
