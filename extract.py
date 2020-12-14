'''Extract JSON data from ESPN'''


def extract_divisions(json_dict):
    divisions = []
    for element in json_dict.get('teams').get('nfl'):
        division_name = element.get('name')
        division = (division_name,)
        divisions.append(division)
    return divisions


def extract_teams(json_dict):
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


def extract_team_links(json_dict):
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


def extract_roster(roster_json, team_abbr):
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
    return roster
