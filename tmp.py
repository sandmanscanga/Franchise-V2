from bs4 import BeautifulSoup
import requests
import json
import os
import sqlite3

URL = 'https://www.espn.com/nfl/teams'


def get_remote_data(url):
    '''Get NFL team data from espn site'''

    r = requests.get(url)
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
    json_dict = json_dict.get("page").get("content")
    return json_dict


def query_local_cache(url, filename, reload=False):
    '''Handle data cache
    
        Check for cache file
        If hit, load cache
        If miss, run remote func

    '''

    dir_path = '/'.join(filename.split('/')[:-1])
    os.makedirs(dir_path, exist_ok=True)
    if reload is True:
        # force reload cache
        print('Force reload')
        json_dict = get_remote_data(url)
        with open(filename, 'w') as f:
            json.dump(json_dict, f)
    else:
        try:
            with open(filename, 'r') as f:
                # cache hit
                print('Cache hit')
                json_dict = json.load(f)
        except FileNotFoundError:
            # cache miss, reload cache
            print('Cache miss')
            json_dict = get_remote_data(url)
            with open(filename, 'w') as f:
                json.dump(json_dict, f)
    return json_dict


# Database
# def create_division_table(divisions):
#     division_data = []
#     for i, division in enumerate(divisions):
#         division_data.append((i, division))

#     with sqlite3.connect('database.db') as db:
#         cursor = db.cursor()
#         cursor.execute('DROP TABLE IF EXISTS Division')
#         cursor.execute('''
#             CREATE TABLE Division(
#                 division_id INT NOT NULL PRIMARY KEY,
#                 division_name TEXT NOT NULL
#             )
#         ''')
#         cursor.executemany('INSERT INTO Division VALUES (?, ?)', division_data)
#         cursor.execute('SELECT * FROM Division')
#         rows = cursor.fetchall()
#     return rows

def parse_divisions(json_dict):
    divisions = []
    for element in json_dict.get('teams').get('nfl'):
        division = element.get('name')
        divisions.append((division,))
    return divisions


def parse_teams(json_dict):
    teams = []
    for nfl in json_dict.get('teams').get('nfl'):
        division = nfl.get('name')
        for element in nfl.get('teams'):
            team_id = element.get('id')
            team_fullname = element.get('name')
            team_name = element.get('shortName')
            team_abbr = element.get('abbrev')
            team = (team_id, team_fullname, team_name, team_abbr, division)
            teams.append(team)
    return teams


def parse_team_links(json_dict):
    team_links = []
    for column in json_dict.get('leagueTeams').get('columns'):
        for group in column.get('groups'):
            for team in group.get('tms'):
                team_links_list = []
                logo = team.get('p')
                team_links_list.append(('logo', logo))
                for lk in team.get('lk')[1:-2]:
                    link_label = lk.get('t')
                    href = lk.get('u')
                    link = f'https://www.espn.com{href}'
                    team_links_list.append((link_label, link))
                team_links.append(team_links_list)
    return team_links


def main():
    json_dict = query_local_cache(URL, "cache/teams.json")

    divisions = parse_divisions(json_dict)
    teams = parse_teams(json_dict)
    team_links = parse_team_links(json_dict)

    # fetch rosters for each team
    for team_link_tup in team_links:
        for team_link in team_link_tup:
            if team_link[0] == 'roster':
                dir_name = team_link[1].split('/')[-2]
                file_name = f'cache/{dir_name}/roster.json'
                roster_json = query_local_cache(team_link[1], file_name)
                return

    # for i, division in enumerate(divisions):
    #     print(i + 1, division)
    # for i, team in enumerate(teams):
    #     print(i + 1, team)
    # for i, href in enumerate(team_links):
    #     print(i + 1, href)

    # rows = create_division_table(divisions)
    # for row in rows:
    #     print(row)


if __name__ == '__main__':
    main()
