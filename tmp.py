import json
import project.utils
import project.consts
import project.controller
from project.logger import LOGGER as Logger

LOGGER = Logger.get_logger('tmp')


def fetch_stat_types(team_link):
    stats_link = team_link[1][1]
    dir_name = team_link[1][1].split('/')[-2]
    file_paths = (dir_name, "stats.json")
    cache_path = project.utils.build_cache_path(*file_paths)
    stats_json = project.utils.query_local_cache(stats_link, cache_path)
    stat_dict_data = stats_json.get("stats").get("dictionary")

    stat_types = []
    for stat_key, value in stat_dict_data.items():
        stat_type = (
            stat_key,
            value.get("abbrev"),
            value.get("statName"),
            value.get("shortDesc"),
            value.get("desc"),
            value.get("group")
        )
        stat_types.append(stat_type)

    stat_types = tuple(stat_types)
    return stat_types


def main():
    nfl_url = project.consts.BASE_URL + "/nfl/teams"
    nfl_cache = project.utils.build_cache_path("nfl.json")
    nfl_json = project.utils.query_local_cache(nfl_url, nfl_cache)

    divisions = project.controller.extract_divisions(nfl_json)
    teams = project.controller.extract_teams(nfl_json)
    team_links = project.controller.extract_team_links(nfl_json)

    # fetch rosters for each team
    rosters = project.controller.fetch_rosters(team_links)

    stat_types = fetch_stat_types(team_links[0])
    print(json.dumps(stat_types))


if __name__ == '__main__':
    main()
