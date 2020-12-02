from bs4 import BeautifulSoup
import requests
import json

'''
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

'''

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
    if reload is True:
        # force reload cache
        print('Force reload')
        json_dict = get_remote_team_data()
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
            with open(file_name, 'w') as f:
                json.dump(json_dict, f)
    return json_dict


def main():
    json_dict = get_teams_data(reload=True)
    # print(json.dumps(json_dict, indent=2))


if __name__ == '__main__':
    main()
