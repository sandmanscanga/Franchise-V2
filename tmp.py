import json
import utils
import extract
from logger import LOGGER as Logger

LOGGER = Logger.get_logger('tmp')

URL = 'https://www.espn.com/nfl/teams'


def fetch_rosters(team_links):
    '''Get roster team data from espn site'''

    rosters = []
    for team_link_tup in team_links:
        team_abbr = team_link_tup[-1][1].split("/")[-2]
        for team_link in team_link_tup:
            if team_link[0] == 'roster':
                dir_name = team_link[1].split('/')[-2]
                file_name = f'cache/{dir_name}/roster.json'
                roster_json = utils.query_local_cache(team_link[1], file_name)
                roster = extract.extract_roster(roster_json, team_abbr)
                rosters.append(roster)
    return rosters


def gen_players(rosters):
    for roster in rosters:
        for player in roster:
            yield player


def main():
    nfl_json = utils.query_local_cache(URL, "cache/teams.json")

    divisions = extract.extract_divisions(nfl_json)
    teams = extract.extract_teams(nfl_json)
    team_links = extract.extract_team_links(nfl_json)

    # fetch rosters for each team
    rosters = fetch_rosters(team_links)
    for player in gen_players(rosters):
        LOGGER.info(json.dumps(player))


if __name__ == '__main__':
    main()
