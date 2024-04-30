import requests
from bs4 import BeautifulSoup

def scrape_player_props():
    url = "https://www.rotowire.com/betting/nba/player-props.php"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    scripts = soup.find("div", id="props-table-list").find_all("script")
    bet_types = ['points', 'rebounds', 'assists', 'threes', 'blocks', 'steals', 'turnovers', 'ptsrebast', 'ptsreb', 'ptsast', 'rebast', 'stlblk']
    data_dict = {}
    check_for_null = ("null", "")

    
    for i in range(12):
        pts_script = str(scripts[i])
        data_idx = pts_script.index("data:")
        data = pts_script[data_idx:].split("]")[0] #extracts actual data from embedded javascript script
        data = data[7:] #gets rid of unnecessary chars at the start of string
        data_lst = data.split("},")
        for player_info in data_lst:
            player_info = player_info.split(",")
            player_name = player_info[4][8:-1]
            id_str_u = player_name + ' U*' + bet_types[i]
            id_str_o = player_name + ' O*' + bet_types[i]
            data_dict[id_str_u] = {}
            data_dict[id_str_o] = {}

            player_info = sorted(player_info[9:])

            betrivers_line = None if any(null in player_info[0] for null in check_for_null) else float(player_info[0].split(":")[1][1:-1])
            data_dict[id_str_o]["betrivers_line"] = betrivers_line
            data_dict[id_str_u]["betrivers_line"] = betrivers_line
            data_dict[id_str_o]["betrivers_odds"] = None if any(null in player_info[1] for null in check_for_null) else int(player_info[1].split(":")[1][1:-1])
            data_dict[id_str_u]["betrivers_odds"] = None if any(null in player_info[2] for null in check_for_null) else int(player_info[2].split(":")[1][1:-1])

            draftkings_line = None if any(null in player_info[3] for null in check_for_null) else float(player_info[3].split(":")[1][1:-1])
            data_dict[id_str_o]["draftkings_line"] = draftkings_line
            data_dict[id_str_u]["draftkings_line"] = draftkings_line
            data_dict[id_str_o]["draftkings_odds"] = None if any(null in player_info[4] for null in check_for_null) else int(player_info[4].split(":")[1][1:-1])
            data_dict[id_str_u]["draftkings_odds"] = None if any(null in player_info[5] for null in check_for_null) else int(player_info[5].split(":")[1][1:-1])

            fanduel_line = None if any(null in player_info[6] for null in check_for_null) else float(player_info[6].split(":")[1][1:-1])
            data_dict[id_str_o]["fanduel_line"] = fanduel_line
            data_dict[id_str_u]["fanduel_line"] = fanduel_line
            data_dict[id_str_o]["fanduel_odds"] = None if any(null in player_info[7] for null in check_for_null) else int(player_info[7].split(":")[1][1:-1])
            data_dict[id_str_u]["fanduel_odds"] = None if any(null in player_info[8] for null in check_for_null) else int(player_info[8].split(":")[1][1:-1])
            
            mgm_line = None if any(null in player_info[9] for null in check_for_null) else float(player_info[9].split(":")[1][1:-1])
            data_dict[id_str_o]["mgm_line"] = mgm_line
            data_dict[id_str_u]["mgm_line"] = mgm_line
            data_dict[id_str_o]["mgm_odds"] = None if any(null in player_info[10] for null in check_for_null) else int(player_info[10].split(":")[1][1:-1])
            data_dict[id_str_u]["mgm_odds"] = None if any(null in player_info[11] for null in check_for_null) else int(player_info[11].split(":")[1][1:-1])

            pointsbet_line = None if any(null in player_info[12] for null in check_for_null) else float(player_info[12].split(":")[1][1:-1])
            data_dict[id_str_o]["pointsbet_line"] = pointsbet_line
            data_dict[id_str_u]["pointsbet_line"] = pointsbet_line
            data_dict[id_str_o]["pointsbet_odds"] = None if any(null in player_info[13] for null in check_for_null) else int(player_info[13].split(":")[1][1:-1])
            data_dict[id_str_u]["pointsbet_odds"] = None if any(null in player_info[14] for null in check_for_null) else int(player_info[14].split(":")[1][1:-1])

    return data_dict


def main():
    scrape_player_props()


if __name__ == "__main__":
    main()
