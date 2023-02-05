from data import teams
import requests
from datetime import date

def get_sports_data(league, team):

    year = date.today().year
    year_int = int(year)

    league_url = league.lower()
    league.replace(" ", "-")
    if league == "MLB":
        sport = "baseball"
    elif league == "NBA":
        sport = "basketball"
    elif league == "NFL":
        sport = "football"
    elif league == "NCAAB":
        sport = "basketball"
        league_url = "mens-college-basketball"
    elif league == "NCAAF":
        sport = "football"
        league_url = "college-football"
    elif league == "Premier-League":
        sport = "soccer"
        league_url = "eng.1"
        print("it's Premier-League")
    elif league == "La-Liga":
        sport = "soccer"
        league_url = "esp.1"
    elif league == "Bundesliga":
        sport = "soccer"
        league_url = "ger.1"
    elif league == "Serie-A":
        sport = "soccer"
        league_url = "ita.1"
    elif league == "Ligue-1":
        sport = "soccer"
        league_url = "fra.1"
    elif league == "MLS":
        sport = "soccer"
        league_url = "usa.1"
    else:
        sport = "hockey"

    team_info = dict()
    team_info['team_color'] = ""
    team_info['team_color_alt'] = ""
    team_info['away_name'] = ""
    team_info['home_name'] = ""
    team_info['away_score'] = ""
    team_info['home_score'] = ""
    team_info['home_abbrev'] = ""
    team_info['away_abbrev'] = ""
    team_info['home_first_color'] = ''
    team_info['home_second_color'] = ''
    team_info['away_first_color'] = ''
    team_info['away_second_color'] = ''
    team_info['period'] = ""
    team_info['last_home_score'] = ""
    team_info['last_away_score'] = ""
    team_info['last_home_name'] = ""
    team_info['last_home_abbrev'] = ""
    team_info['last_away_abbrev'] = ""
    team_info['last_home_first_color'] = ''
    team_info['last_home_second_color'] = ''
    team_info['last_away_first_color'] = ''
    team_info['last_away_second_color'] = ''
    team_info['last_time'] = 'F'



    id = teams[league][team]
    team_endpoint = "http://site.api.espn.com/apis/site/v2/sports/{0}/{1}/teams/{2}".format(sport, league_url, id)
    team_info['offseason'] = False

    request = requests.get(team_endpoint)
    parsed = request.json()
    request.close()

    team_info['team_color'] = parsed["team"]["color"]
    if 'alternateColor' in parsed["team"]:
        team_info['team_color_alt'] = parsed["team"]["alternateColor"]
    else:
        team_info['team_color_alt'] = team_info['team_color']

    reset_record = False
    if league == "NCAAF" or league == "NFL":
        team_info['record'] = parsed["team"]["record"]
        if league == "NFL":
            team_info['record'] = parsed["team"]["record"]["items"][0]["summary"]
        if len(team_info['record']) == 0:
            team_info['record'] = '0-0'
        curr_game_id = parsed["team"]["nextEvent"] # professional sports record parsing and NCAAB
        team_info['away_score'] = "0"
        team_info['home_score'] = "0"
        team_info['home_abbrev'] = parsed["team"]["abbreviation"]
        team_info['away_abbrev'] = "TBD"
    else:
        team_info['record'] = parsed["team"]["record"]["items"][0]["summary"]
        if len(parsed["team"]["nextEvent"]) > 0:
            curr_game_id = parsed["team"]["nextEvent"][0]["id"] # professional sports record parsing and NCAAB
        else:
            curr_game_id = []
            reset_record = False

    # if team is in offseason, this overrides the LED display
    if len(curr_game_id) == 0:
        print('offseason')
        team_info['offseason'] = True
        if reset_record == True:
            print("reset record")
            team_info['record'] = "0-0"

        year = str(year_int-1)

        if league == "NCAAF":
            year = str(year_int-2)

        prev_game_endpoint = "http://site.api.espn.com/apis/site/v2/sports/{0}/{1}/teams/{2}/schedule?season={3}".format(sport, league_url, id, year)
        request = requests.get(prev_game_endpoint)
        parsed = request.json()
        request.close()

        last_game_index = len(parsed['events']) - 1

        prev_info = parsed['events'][last_game_index]["competitions"][0]["competitors"]
        team_info['last_home_score'] = prev_info[0]["score"]["displayValue"]
        team_info['last_away_score'] = prev_info[1]["score"]["displayValue"]
        team_info['last_home_name'] = prev_info[0]["team"]["shortDisplayName"]
        team_info['last_away_name'] = prev_info[1]["team"]["shortDisplayName"]
        team_info['last_home_abbrev'] = prev_info[0]["team"]["abbreviation"]
        team_info['last_away_abbrev'] = prev_info[1]["team"]["abbreviation"]

        prev_game_id = parsed['events'][last_game_index]["competitions"][0]["id"]
        prev_game_endpoint = "http://site.api.espn.com/apis/site/v2/sports/{0}/{1}/scoreboard/{2}".format(sport, league_url, prev_game_id)
        request = requests.get(prev_game_endpoint)
        parsed = request.json()
        request.close()

        team_info['last_home_first_color'] = parsed["competitions"][0]["competitors"][0]["team"]["color"]

        team_info['last_away_first_color'] = parsed["competitions"][0]["competitors"][1]["team"]["color"]

        if 'alternateColor' in parsed["competitions"][0]["competitors"][0]["team"]:
            team_info['last_home_second_color'] = parsed["competitions"][0]["competitors"][0]["team"]["alternateColor"]
        if 'alternateColor' in parsed["competitions"][0]["competitors"][1]["team"]:
            team_info['last_away_second_color'] = parsed["competitions"][0]["competitors"][1]["team"]["alternateColor"]

        return team_info

        # return here


    curr_game_endpoint = "http://site.api.espn.com/apis/site/v2/sports/{0}/{1}/scoreboard/{2}".format(sport, league_url, curr_game_id)
    request = requests.get(curr_game_endpoint)
    parsed = request.json()
    request.close()

    team_info['home_score'] = parsed["competitions"][0]["competitors"][0]["score"]
    team_info['away_score'] = parsed["competitions"][0]["competitors"][1]["score"]
    team_info['home_name'] = parsed["competitions"][0]["competitors"][0]["team"]["shortDisplayName"]
    team_info['away_name'] = parsed["competitions"][0]["competitors"][1]["team"]["shortDisplayName"]
    team_info['home_abbrev'] = parsed["competitions"][0]["competitors"][0]["team"]["abbreviation"]
    team_info['away_abbrev'] = parsed["competitions"][0]["competitors"][1]["team"]["abbreviation"]
    team_info['home_first_color'] = parsed["competitions"][0]["competitors"][0]["team"]["color"]
    team_info['away_first_color'] = parsed["competitions"][0]["competitors"][1]["team"]["color"]

    if 'alternateColor' in parsed["competitions"][0]["competitors"][1]["team"]:
        team_info['away_second_color'] = parsed["competitions"][0]["competitors"][1]["team"]["alternateColor"]
    if 'alternateColor' in parsed["competitions"][0]["competitors"][0]["team"]:
        team_info['home_second_color'] = parsed["competitions"][0]["competitors"][0]["team"]["alternateColor"]

    team_info['period']= parsed["status"]["period"]

    if sport == "soccer":
        year = int(year) - 1
        year = str(year)

    prev_game_endpoint = "http://site.api.espn.com/apis/site/v2/sports/{0}/{1}/teams/{2}/schedule?season={3}".format(sport, league_url, id, year)
    request = requests.get(prev_game_endpoint)
    parsed = request.json()
    request.close()

    i = 0
    while i < len(parsed['events']) and parsed['events'][i]["id"] != curr_game_id:
        i +=1

    last_game_index = i - 1

    prev_info = parsed['events'][last_game_index]["competitions"][0]["competitors"]
    team_info['last_home_score'] = prev_info[0]["score"]["displayValue"]
    team_info['last_away_score'] = prev_info[1]["score"]["displayValue"]

    score = team_info['last_home_score'] + '-' + team_info['last_away_score']

    if score == '0-0' and sport != "soccer":
        last_game_index -= 1

    if sport == "soccer":
        last_game_index = 0

    prev_info = parsed['events'][last_game_index]["competitions"][0]["competitors"]
    team_info['last_home_score'] = prev_info[0]["score"]["displayValue"]
    team_info['last_away_score'] = prev_info[1]["score"]["displayValue"]
    team_info['last_home_name'] = prev_info[0]["team"]["shortDisplayName"]
    team_info['last_away_name'] = prev_info[1]["team"]["shortDisplayName"]
    team_info['last_home_abbrev'] = prev_info[0]["team"]["abbreviation"]
    team_info['last_away_abbrev'] = prev_info[1]["team"]["abbreviation"]

    prev_game_id = parsed['events'][last_game_index]["competitions"][0]["id"]
    prev_game_endpoint = "http://site.api.espn.com/apis/site/v2/sports/{0}/{1}/scoreboard/{2}".format(sport, league_url, prev_game_id)
    request = requests.get(prev_game_endpoint)
    parsed = request.json()
    request.close()

    team_info['last_home_first_color'] = parsed["competitions"][0]["competitors"][0]["team"]["color"]
    team_info['last_home_second_color'] = parsed["competitions"][0]["competitors"][0]["team"]["alternateColor"]
    team_info['last_away_first_color'] = parsed["competitions"][0]["competitors"][1]["team"]["color"]
    team_info['last_away_second_color'] = parsed["competitions"][0]["competitors"][1]["team"]["alternateColor"]

    if 'alternateColor' in parsed["competitions"][0]["competitors"][1]["team"]:
        team_info['last_away_second_color'] = parsed["competitions"][0]["competitors"][1]["team"]["alternateColor"]
    if 'alternateColor' in parsed["competitions"][0]["competitors"][0]["team"]:
        team_info['last_home_second_color'] = parsed["competitions"][0]["competitors"][0]["team"]["alternateColor"]

    return team_info

# print("Barcelona:\n")
# print(get_sports_data("La-Liga", "FC Barcelona"))
#
# print("\n\n")
#
# print("Madrid:\n")
# print(get_sports_data("La-Liga", "Real Madrid"))
#
# print("\n\n")

# print("SOX:\n")
# print(get_sports_data("MLB", "Chicago White Sox"))
#
# print("\n\n")
#
# print("BULLS:\n")
# print(get_sports_data("NBA", "Chicago Bulls"))
#
# print("\n\n")
#
# print("BEARS:\n")
# print(get_sports_data("NFL", "Chicago Bears"))
#
# print("\n\n")
#
# print("HAWKS:\n")
# print(get_sports_data("NHL", "Chicago Blackhawks"))
#
# print("\n\n")
#
# print("Illini BB:\n")
# print(get_sports_data("NCAAB", "Illinois Fighting Illini"))
#
# print("\n\n")
#
# print("Illini FB:\n")
# print(get_sports_data("NCAAF", "Illinois Fighting Illini"))
