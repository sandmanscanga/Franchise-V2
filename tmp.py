from bs4 import BeautifulSoup
import requests
import json

"""
def get_remote_data():
    # make web request
    # return data


def get_team_data(reload=False):
    # if reload is False:
        # first check cache
        # if cache miss:
            # data = get_remote_data()
            # write data to disk
        # else
            # load data from cache
    # else:
        # data = get_remote_data()
        # write data to disk
    # return data


def main():
    data = get_team_data()

"""


def get_teams_data():
    r = requests.get("https://www.espn.com/nfl/teams")
    soup = BeautifulSoup(r.text, "lxml")

    target = None
    for script_tag in soup.findAll("script"):
        if "__espnfitt__" in str(script_tag):
            target = script_tag
            break
    else:
        print("Script not found!")
        return

    data = str(target)
    data = "=".join(data.split("=")[2:])
    data = ";".join(data.split(";")[:-1])
    json_dict = json.loads(data)
    return json_dict


def main():
    json_dict = get_teams_data()
    with open("dump.json", "w") as f:
        json.dump(json_dict, f)


if __name__ == "__main__":
    main()
