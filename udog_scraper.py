import requests
from ud_constants import *

class Underdog:
    def __init__(self) -> None:
        self.player_ids = {}
        self.teams = {}
        self.available_players = {}
        self.final = {}


        response = requests.get(UD_API_URL, headers=UD_HEADERS)
        self.data = response.json()
        players = self.data['players']
        appearances = self.data['appearances']
        lines = self.data['over_under_lines']
        for player in players:
            if player['sport_id'] == 'NBA':
                name = player['first_name'] + ' ' + player['last_name']
                player_id = player['id']
                self.player_ids[player_id] = name
                print(name)

        for appearence in appearances:
            player_id = appearence['player_id']
            if player_id in self.player_ids:
                name = self.player_ids[appearence['player_id']]
                appearence_id = appearence['id']
                self.available_players[appearence_id] = name

        for line in lines:
            appearence_id = line['over_under']['appearance_stat']['appearance_id']
            if appearence_id in self.available_players:
                name = self.available_players[line['over_under']['appearance_stat']['appearance_id']]
                line_val = line['stat_value']
                stat = self.formatStat(line['over_under']['appearance_stat']['stat'])
                if len(line['options']) > 1:
                    over_mult = line['options'][0]['payout_multiplier']
                    over_parlay_id = line['options'][0]['id']
                    self.final[name + ' O*' + stat] = (line_val,over_mult)
                    under_mult = line['options'][1]['payout_multiplier']
                    under_parlay_id = line['options'][1]['id']
                    self.final[name + ' U*' + stat] = (line_val,under_mult)
                else:
                    mult = line['options'][0]['payout_multiplier']
                    parlay_id = line['options'][0]['id']
                    OU = ' O*' if line['options'][0]['choice'] == 'higher' else ' U*'
                    self.final[name + OU + stat] = (line_val, mult)

    def formatStat(self, stat):
        conversion = {'three_points_made': 'threes',
                      'pts_rebs_ast': 'ptsrebast',
                      'pts_rebs': 'ptsreb',
                      'pts_asts': 'ptsast',
                      'rebs_asts': 'rebast',
                      'blks_stls': 'stlblk'}
        
        return conversion.get(stat,stat)

    def getData(self):
        return self.final
            

def main():
    ud = Underdog()
    print(ud.getData())

if __name__ == "__main__":
    main()
