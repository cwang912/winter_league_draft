from flask import Flask, render_template, make_response, send_file, redirect, url_for, request, jsonify
import numpy as np
import pandas as pd
# from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
# from flask.ext.moment import Moment
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import Required, Optional

app = Flask('density_graph_webapp')
app.config['SECRET_KEY'] = 'hard to guess string'

bootstrap = Bootstrap(app)

players = pd.read_csv('PLAYERS.csv')
players = players.sort_values('rating', ascending=False)
players['baggage'] = players['baggage'].fillna(' ')

class Team():
    def __init__(self, number, captains):
        self.number = number
        self.captains = dict(captains.T)
        self.roster = dict(captains.T)
        self.mens_total = 0
        self.womens_total = 0
        self.total = 0
        team_name = ''
        for cap in self.captains:
            team_name += self.captains[cap]['name']
            team_name += ', '
        self.team_name = team_name[:-2]

        for cap in self.roster:
            if self.roster[cap]['gender'] == 'M':
                self.mens_total += self.roster[cap]['rating']
            else:
                self.womens_total += self.roster[cap]['rating']
            self.total += self.roster[cap]['rating']

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
            # print(player)
            self.roster[p] = dict(player)
            # print(player)
            # print(type(player))
            if player.gender == 'M':
                self.mens_total += player['rating']
            else:
                self.womens_total += player['rating']
            self.total += player['rating']

    def remove(self, pick):
        for player in pick:
            self.roster.remove(player)
            if pick[player]['gender'] == 'M':
                self.mens_total += -pick[player]['rating']
            else:
                self.womens_total += -pick[player]['rating']
            self.total += -pick[player]['rating']
    def print_roster(self):
        for i in self.roster:
            print(self.roster[i]['name'])
    def print_team(self):
        print(self.number,self.total)

def next_pick(logic='pre'):
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


class NameForm(Form):
    # name = StringField('Pick a place in the US:', validators=[Required()])
    submit = SubmitField('Submit')


class TeamDropdown(Form):
    # name = StringField('Pick a place in the US:', validators=[Required()])
    team_names = []
    for i in teams:
        team_names.append(teams[i].team_name)
    team_choices = zip(range(1,9),team_names)
    # team_choices =
    select_team = SelectField('Select team', choices=team_choices, validators=[Optional()])
    submit = SubmitField('Submit')

pick = None
tid = 1
for i in (teams[tid].roster):
    print(teams[tid].roster[i])
# print(teams[tid].roster)

@app.route('/', methods=['GET', 'POST'])
def index():
    name = None
    form = NameForm()
    team_selection = TeamDropdown()
    team_selection.select_team.default=1
    team_selection.process()
    print(teams)
    if team_selection.is_submitted():
        # print(team_selection.data)
        # team_selection.select_team(default=team_selection.data['select_team'])
        team_selection
        print('something')
        print(team_selection.data['select_team'])
        print(team_selection.select_team)
        team_selection= TeamDropdown()
        # display_team = team_selection.data['select_team']
        # team_selection = TeamDropdown()
        return render_template('index.html', players=players, pick=pick, team=teams[next_pick('pre')].roster,form=form,teams_menu=team_selection)

        # form.name.data = ''
    print('tid')
    print(tid)
    return render_template('index.html', players=players, pick=pick,    drafting_team=teams[next_pick('pre')].roster,form=form,teams_menu=team_selection,all_teams=teams)
#
# @app.route('/team/<int:tid>', methods=['GET', 'POST'])
# def tid(tid=1):
#     name = None
#     form = NameForm()
#     team_selection = TeamDropdown()
#     team_selection.select_team(default=tid)
#     print(tid)
#     if form.validate_on_submit():
#         teams[next_pick('pre')].add(pid)
#         # form.name.data = ''
#         pid = None
#     return render_template('index.html', players=players, pick=pid, drafting_team=teams[next_pick('pre')].roster,form=form,teams_menu=team_selection, next_team=teams[tid].roster)


@app.route('/<int:pid>', methods=['GET', 'POST'])
def pid(pid=None):
    name = None
    form = NameForm()
    team_selection = TeamDropdown()
    team_selection.select_team(default=tid)

    if form.validate_on_submit():
        teams[next_pick('pre')].add(pid)
        teams[tid].print_roster()
        pid = None
    return render_template('index.html', players=players, pick=pid, drafting_team=teams[next_pick('pre')].roster,form=form,teams_menu=team_selection,all_teams=teams)


@app.route('/get_team')
def get_team():
    name = None
    form = NameForm()
    team_selection = TeamDropdown()
    team_selection.select_team.default=1
    team_selection.process()

    tid = int(request.args.get('selected_team'))
    teams[tid].print_roster()
    print(tid)
    return render_template('index.html', players=players, pick=pid, drafting_team=teams[next_pick('pre')].roster,form=form,teams_menu=team_selection, next_team=teams[tid].roster)
    # return jsonify(tid=tid)

    # return app.root_path
# # FLASK FUNCTIONS
# @app.route('/graph/<place>', methods=['GET', 'POST'])
# def graph(place=None):
#     name = None
#     form = NameForm()
#     if form.validate_on_submit():
#         name = form.name.data
#         return redirect(url_for('graph', place=name))
#     return render_template("index.html", form=form, name=place)
#
# @app.route('/fig/<place>')
# def fig(place):
#     df = pd.read_csv('data/tracts.csv')
#     line = plot_fun(place, df)
#     # Generate the plot
#     #f = cStringIO.StringIO()
#     plt.savefig(f, format='png')
#     # Serve up the data
#     f.seek(0)
#     # data = f.read()
#     return send_file(f, mimetype='image/png')
#

if __name__ == '__main__':
  app.run(debug=True)
