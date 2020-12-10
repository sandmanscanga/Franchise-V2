import json
import utils
import extract
# import sqlite3

URL = 'https://www.espn.com/nfl/teams'


"""
{
"name": "Darryl Johnson",
"href": "http://www.espn.com/nfl/player/_/id/3957672/darryl-johnson",
"uid": "s:20~l:28~a:3957672",
"guid": "d627a4afa02ffbc9251af98cdcee845c",
"id": "3957672",
"height": "6' 6\"",
"weight": "253 lbs",
"age": 23,
"position": "DE",
"jersey": "92",
"birthDate": "04/04/97",
"headshot": "https://a.espncdn.com/i/headshots/nfl/players/full/3957672.png",
"lastName": "Darryl Johnson",
"experience": 2,
"college": "North Carolina A&T",
"birthPlace": "Kingsland, GA"
},

"""

def parse_roster(roster_json, team_abbr):
    roster = []
    for group in roster_json.get("roster").get("groups"):
        for athlete in group.get("athletes"):
            name = athlete.get("name")
            link = athlete.get("href")
            uid = athlete.get("uid")
            guid = athlete.get("guid")
            height = athlete.get("height")
            weight = athlete.get("weight")
            age = athlete.get("age")
            position = athlete.get("position")
            jersey = athlete.get("jersey")
            headshot = athlete.get("headshot")
            experience = athlete.get("experience")
            college = athlete.get("college")
            athlete = (
                name, link, uid, guid, height, weight,
                age, position, jersey, headshot,
                experience, college, team_abbr
            )
            roster.append(athlete)
    return roster


def fetch_rosters(team_links):
    '''Get roster team data from espn site'''

    rosters = []
    for team_link_tup in team_links:
        team_abbr = team_link_tup[-1][1].split("/")[-2]
        for team_link in team_link_tup:
            if team_link[0] == 'roster':
                dir_name = team_link[1].split('/')[-2]
                file_name = f'cache/{dir_name}/roster.json'
                roster_json = query_local_cache(team_link[1], file_name)
                roster = parse_roster(roster_json, team_abbr)
                rosters.append(roster)
    return rosters


def gen_players(rosters):
    for roster in rosters:
        for player in roster:
            yield player


def main():
    nfl_json = query_local_cache(URL, "cache/teams.json")

    divisions = parse_divisions(nfl_json)
    teams = parse_teams(nfl_json)
    team_links = parse_team_links(nfl_json)

    # fetch rosters for each team
    rosters = fetch_rosters(team_links)
    for player in gen_players(rosters):
        print(json.dumps(player))

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
