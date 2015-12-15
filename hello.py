from flask import Flask, render_template, make_response, send_file, redirect, url_for, request, jsonify
import numpy as np
import pandas as pd
# from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
# from flask.ext.moment import Moment
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, SelectField, RadioField, HiddenField
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
        self.number_people = 0
        self.number_female = 0
        self.number_male = 0

        team_name = ''
        for cap in self.captains:
            team_name += self.captains[cap]['name'].split()[0]
            team_name += ', '
        self.team_name = team_name[:-2]

        for cap in self.roster:
            if self.roster[cap]['gender'] == 'M':
                self.number_male += 1
                self.mens_total += self.roster[cap]['rating']
            else:
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
                self.number_male += 1
                self.mens_total += player['rating']
            else:
                self.number_female += 1
                self.womens_total += player['rating']
            self.number_people += 1
            self.total += player['rating']

    def remove(self, pick):
        for player in pick:
            self.roster.remove(player)
            if pick[player]['gender'] == 'M':
                self.number_male += -1
                self.mens_total += -pick[player]['rating']
            else:
                self.number_female += -1
                self.womens_total += -pick[player]['rating']
            self.number_people += -1
            self.total += -pick[player]['rating']
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


class NameForm(Form):
    # name = StringField('Pick a place in the US:', validators=[Required()])
    submit = SubmitField('Draft!')
    team_names = [teams[i].team_name for i in teams]
    team_choices = zip(range(1,9),team_names)
    select_team = SelectField('For which team?', choices=team_choices, coerce=int, default=(next_pick(teams)))
    player_choices = zip(players[players.team.isnull()].index,players[players.team.isnull()]['name'])
    select_player = RadioField('Which player', choices=player_choices, coerce=int)
    player = HiddenField()

# class TeamDropdown(Form):
#     # name = StringField('Pick a place in the US:', validators=[Required()])
#     team_names = []
#     for i in teams:
#         team_names.append(teams[i].team_name)
#     team_choices = zip(range(1,9),team_names)
#     # team_choices =
#     select_team = SelectField('Select team', choices=team_choices, validators=[Optional()])
#     submit = SubmitField('Submit')

# pick = None
tid = 1
# for i in (teams[tid].roster):
#     print(teams[tid].roster[i])
# print(teams[tid].roster)
# next_pick = None

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    # print('here1')
    # team_selection = TeamDropdown()
    # team_selection.select_team.default=1
    # team_selection.process()
    if form.validate_on_submit():
        # print(next_pick)
        print('yes')
        print(form.select_player.data)

    if request.args.get('pick_no'):
        pick_no = int(request.args.get('pick_no'))
        # next_pick = pick_no
    else:
        pick_no = None


    # print(team_selection)
    # if team_selection.is_submitted():
    #     # print(team_selection.data)
    #
    #     return render_template('index.html', players=players, pick=pick, drafting_team=teams,form=form,teams_menu=team_selection, current_team=next_pick('pre'))

        # form.name.data = ''
    # print('tid')
    # print(tid)
    return render_template('index.html', players=players, pick=pick_no, logic=get_logic(teams),form=form,all_teams=teams, current_team=next_pick(teams))

@app.route('/<int:pid>', methods=['GET', 'POST'])
def highlight_pid(pid=None):
    class NameForm2(Form):
        # name = StringField('Pick a place in the US:', validators=[Required()])
        submit = SubmitField('Draft!')
        team_names = [teams[i].team_name for i in teams]
        team_choices = zip(range(1,9),team_names)
        select_team = SelectField('For which team?', choices=team_choices, coerce=int, default=(next_pick(teams)))
        player_choices = zip(players[players.team.isnull()].index,players[players.team.isnull()]['name'])
        select_player = RadioField('Which player', choices=player_choices, coerce=int)
        player = HiddenField()


    form = NameForm2()
    print(pid)
    # team_selection = TeamDropdown()
    # team_selection.select_team()
    # print('here int')
    # print(form)
    # print(form.select_team.data)
    # print(form.submit.data)
    # if form.submit.data:
    #     print('here2')
    #     print(form.select_team.data)
    #     teams[form.select_team.data].add(pid)
    #     teams[form.select_team.data].print_roster()
    #     pid = None
    #
    # if form.validate_on_submit():
    #     print('here')
    #     return redirect(url_for('draft'))
        # teams[form.select_team].add(pid)
        # teams[form.select_team].print_roster()
        # return render_template('index.html', players=players, pick=pid, drafting_team=teams,form=form,all_teams=teams, current_team=next_pick('pre'))
    # return redirect(url_for('index', pick_no=pid))
    return render_template('index.html', players=players, pick=pid, logic=get_logic(teams),form=form,all_teams=teams, current_team=next_pick(teams))
#
@app.route('/draft', methods=('GET', 'POST'))
def submit():
    form = NameForm()
    print('here')
    print(int(form.select_team.data))
    print(int(form.player.data))

    teams[int(form.select_team.data)].add(int(form.player.data))
    teams[int(form.select_team.data)].print_roster()
        # pid = None
    return render_template('index.html', players=players, pick=None, logic=get_logic(teams),form=form,all_teams=teams, current_team=next_pick(teams))

#
# @app.route('/get_team')
# def get_team():
#     form = NameForm()
#     team_selection = TeamDropdown()
#     team_selection.select_team.default=1
#     team_selection.process()
#
#     tid = int(request.args.get('selected_team'))
#     teams[tid].print_roster()
#     # print(tid)
#     return render_template('index.html', players=players, pick=pid,    drafting_team=teams,form=form,teams_menu=team_selection,all_teams=teams, current_team=next_pick('pre'))
    # return jsonify(tid=tid)

    # return app.root_path
# # FLASK FUNCTIONS
# @app.route('/graph/<place>', methods=['GET', 'POST'])
# def graph(place=None):
#
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
#
# @app.route('/team/<int:tid>', methods=['GET', 'POST'])
# def tid(tid=1):
#
#     form = NameForm()
#     team_selection = TeamDropdown()
#     team_selection.select_team(default=tid)
#     print(tid)
#     if form.validate_on_submit():
#         teams[next_pick('pre')].add(pid)
#         # form.name.data = ''
#         pid = None
#     return render_template('index.html', players=players, pick=pid, drafting_team=teams[next_pick('pre')].roster,form=form,teams_menu=team_selection, next_team=teams[tid].roster)


if __name__ == '__main__':
  app.run(debug=True)
