from flask import Flask, render_template, make_response, send_file, redirect, url_for, request, jsonify
import numpy as np
import pandas as pd
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, SelectField, RadioField, HiddenField
from wtforms.validators import Required, Optional

app = Flask('density_graph_webapp')
app.config['SECRET_KEY'] = 'hard to guess string'

bootstrap = Bootstrap(app)

players = pd.read_csv('PLAYERS.csv')
players = players.sort_values('rating', ascending=False)
players['baggage'] = players['baggage'].fillna(' ')

picks_in_order = []
team_picks = []

class Team():
    def __init__(self, number, captains):
        self.number = number
        self.captains = dict(captains.T)
        self.roster = dict(captains.T)
        self.mens_total = 0
        self.womens_total = 0
        self.total = 0
        self.number_people = 0
        self.number_female = 0
        self.number_male = 0
        self.men = dict()
        self.women = dict()

        team_name = ''
        for cap in self.captains:
            team_name += self.captains[cap]['name'].split()[0]
            team_name += ', '
        self.team_name = team_name[:-2]

        for cap in self.roster:
            if self.roster[cap]['gender'] == 'M':
                self.men[cap] = self.roster[cap]
                self.number_male += 1
                self.mens_total += self.roster[cap]['rating']
            else:
                self.women[cap] = self.roster[cap]
                self.number_female += 1
                self.womens_total += self.roster[cap]['rating']
            self.total += self.roster[cap]['rating']
            self.number_people += 1

    def add(self, pid):
        if not players.loc[pid].baggage==' ':
            pid2 = players.loc[players[players['name']==players.loc[pid].baggage].index].index.values[0]
            pick = [pid, pid2]
            print(pick)
        else:
            pick = [pid]

        for p in pick:
            players.loc[p,'team'] = self.number
            player = players.loc[p]
            self.roster[p] = dict(player)
            if player.gender == 'M':
                self.men[p] = dict(player)
                self.number_male += 1
                self.mens_total += player['rating']
            else:
                self.women[p] = dict(player)
                self.number_female += 1
                self.womens_total += player['rating']
            self.number_people += 1
            self.total += player['rating']

    def remove_pick(self, pick):
        for p in pick:
            players.loc[p,'team'] = np.nan
            player = players.loc[p]
            self.roster.pop(p)
            if player['gender'] == 'M':
                self.men.pop(p)
                self.number_male += -1
                self.mens_total += -player['rating']
            else:
                self.women.pop(p)
                self.number_female += -1
                self.womens_total += -player['rating']
            self.number_people += -1
            self.total += -player['rating']

    def print_roster(self):
        for i in self.roster:
            print(self.roster[i]['name'])
    def print_team(self):
        print(self.number,self.total)

def get_logic(teams):
    all_picks = 0
    for i in teams:
        all_picks += teams[i].number_people
    if all_picks < 4*len(teams):
        return "pre"
    womens = False
    for i in teams:
        if teams[i].number_female < 4:
            return "womens"
    return "mens"

def next_pick(teams):
    logic = get_logic(teams)
    m = teams[1].total
    n = 1
    if logic == 'pre':
        for i in teams:
            if teams[i].total < m:
                m = teams[i].total
                n = i
    elif logic == 'womens':
        for i in teams:
            if teams[i].womens_total < m:
                m = teams[i].total
                n = i
    elif logic == 'mens':
        for i in teams:
            if teams[i].mens_total < m:
                m = teams[i].total
                n = i
    return n

teams = dict()
for ind in range(1,9):
    teams[ind] = Team(ind,players[players.team==ind])

tid = 1

@app.route('/winter-league', methods=['GET', 'POST'])
def winter_league():
    class NameForm(Form):
        submit = SubmitField('Draft!')
        team_names = [teams[i].team_name for i in teams]
        team_choices = zip(range(1,9),team_names)
        select_team = SelectField('For which team?', choices=team_choices, coerce=int, default=(next_pick(teams)))
        player_choices = zip(players[players.team.isnull()].index,players[players.team.isnull()]['name'])
        select_player = RadioField('Which player', choices=player_choices, coerce=int)
        player = HiddenField()
    class UndoForm(Form):
        undo = SubmitField('Undo last pick')

    undo_form = UndoForm()
    form = NameForm()

    if form.validate_on_submit():
        print('yes')
        print(form.select_player.data)

    if request.args.get('pick_no'):
        pick_no = int(request.args.get('pick_no'))
    else:
        pick_no = None

    return render_template('draft.html', players=players, pick=pick_no, logic=get_logic(teams),form=form,undo_form=undo_form, all_teams=teams, current_team=next_pick(teams))

@app.route('/draft', methods=('GET', 'POST'))
def submit():
    print(teams[next_pick(teams)].team_name)
    class NameForm2(Form):
        # name = StringField('Pick a place in the US:', validators=[Required()])
        submit = SubmitField('Draft!')
        team_names = [teams[i].team_name for i in teams]
        team_choices = zip(range(1,9),team_names)
        select_team = SelectField('For which team?', choices=team_choices, coerce=int, default=(next_pick(teams)))
        player = HiddenField()

    form = NameForm2()
    print('here')

    if form.player.data != 'None':
        teams[int(form.select_team.data)].add(players[players.name==form.player.data].index[0])
        teams[int(form.select_team.data)].print_roster()
        picks_in_order.append(int(players[players.name==form.player.data].index[0]))
        team_picks.append(int(form.select_team.data))
    return redirect(url_for('winter_league'))


@app.route('/undo', methods=('GET', 'POST'))
def undo():

    last_pick = picks_in_order.pop()
    last_team = team_picks.pop()
    print(len(players.ix[last_pick].baggage))
    if last_pick in players[players.baggage.isnull()].index:
        pid2 = players[players.name==players.ix[last_pick].baggage].index.values[0]
        pick = [last_pick, pid2]
    else:
        pick = [last_pick]
    print(teams[last_team])
    teams[last_team].remove_pick(pick)

    return redirect(url_for('winter_league'))


if __name__ == '__main__':
  app.run(debug=True)
