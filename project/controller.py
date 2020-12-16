'''Controller for JSON data from ESPN'''
import project.consts
import project.utils


def extract_divisions(json_dict):
    '''Extract divisions from NFL JSON'''

    divisions = []
    for element in json_dict.get('teams').get('nfl'):
        division_name = element.get('name')
        division = (division_name,)
        divisions.append(division)

    divisions = tuple(divisions)
    return divisions


def extract_teams(json_dict):
    '''Extract teams from NFL JSON'''

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

    teams = tuple(teams)
    return teams


def extract_team_links(json_dict):
    '''Extract team links from NFL JSON'''

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
                    link = project.consts.BASE_URL + href
                    team_links_list.append((link_label, link))
                team_links.append(team_links_list)

    team_links = tuple(team_links)
    return team_links


def extract_roster(roster_json, team_abbr):
    '''Extract roster from JSON data and team abbr'''

    roster = []
    for group in roster_json.get("roster").get("groups"):
        for athlete in group.get("athletes"):
            athlete_tup = (
                athlete.get("name"),
                athlete.get("href"),
                athlete.get("uid"),
                athlete.get("guid"),
                athlete.get("height"),
                athlete.get("weight"),
                athlete.get("age"),
                athlete.get("position"),
                athlete.get("jersey"),
                athlete.get("headshot"),
                athlete.get("experience"),
                athlete.get("college"),
                team_abbr
            )
            roster.append(athlete_tup)

    roster = tuple(roster)
    return roster


def fetch_rosters(team_links):
    '''Get roster team data from espn site'''

    rosters = []
    for team_link_tup in team_links:
        team_abbr = team_link_tup[-1][1].split("/")[-2]
        for team_link in team_link_tup:
            if team_link[0] == 'roster':
                dir_name = team_link[1].split('/')[-2]
                file_paths = (dir_name, "roster.json")
                cache_path = project.utils.build_cache_path(*file_paths)
                roster_json = project.utils.query_local_cache(team_link[1], cache_path)
                roster = extract_roster(roster_json, team_abbr)
                rosters.append(roster)

    rosters = tuple(rosters)
    return rosters
