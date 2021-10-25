from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.core.serializers import serialize
import requests
import requests_cache
from requests_cache import CachedSession
import json
import os
import time
from datetime import date
import datetime
from .forms import MatchForm
import ast

API_KEY = '530bbc7b369643ae837cd05fa3f135cd'
headers = {'X-Auth-Token': API_KEY}
base_url = 'http://api.football-data.org/v2/'

requests_cache.install_cache('football_data_cache', backend='sqlite', expire_after=180)


def index(request):
    match_uri = 'matches/'
    team_uri = 'teams/'
    date_to = date.today()
    date_from = date_to - datetime.timedelta(days=7)
    url = f"{base_url}{match_uri}?dateFrom={date_from}&dateTo={date_to}"

    r = requests.get(url, headers=headers)
    json = r.json()

    matches = sorted(json['matches'], key=lambda k: k['utcDate'], reverse=True)

    return render(request, 'index.html', {'matches': matches})


def competitions(request):
    league = ['PL', 'BL1', 'SA', 'PD', 'FL1']
    uri = [f'competitions/{league[0]}/standings?',
           f'competitions/{league[1]}/standings?',
           f'competitions/{league[2]}/standings?',
           f'competitions/{league[3]}/standings?',
           f'competitions/{league[4]}/standings?']

    r_pl = requests.get(base_url + uri[0], headers=headers)
    r_bl1 = requests.get(base_url + uri[1], headers=headers)
    r_sa = requests.get(base_url + uri[2], headers=headers)
    r_pd = requests.get(base_url + uri[3], headers=headers)
    r_fl1 = requests.get(base_url + uri[4], headers=headers)

    r_pl_json = r_pl.json()
    r_bl1_json = r_bl1.json()
    r_sa_json = r_sa.json()
    r_pd_json = r_pd.json()
    r_fl1_json = r_fl1.json()

    r_pl_standings = r_pl_json['standings'][0]['table']
    r_bl1_standings = r_bl1_json['standings'][0]['table']
    r_sa_standings = r_sa_json['standings'][0]['table']
    r_pd_standings = r_pd_json['standings'][0]['table']
    r_fl1_standings = r_fl1_json['standings'][0]['table']

    data = {
        'r_pl_json': r_pl_json,
        'r_bl1_json': r_bl1_json,
        'r_sa_json': r_sa_json,
        'r_pd_json': r_pd_json,
        'r_fl1_json': r_fl1_json,
        'r_pl_standings': r_pl_standings,
        'r_bl1_standings': r_bl1_standings,
        'r_sa_standings': r_sa_standings,
        'r_pd_standings': r_pd_standings,
        'r_fl1_standings': r_fl1_standings,

    }

    return render(request, 'competitions.html', {'data': data})


def scorers(request):
    league = ['PL', 'BL1', 'SA', 'PD', 'FL1']

    uri = [f'competitions/{league[0]}/scorers',
           f'competitions/{league[1]}/scorers',
           f'competitions/{league[2]}/scorers',
           f'competitions/{league[3]}/scorers',
           f'competitions/{league[4]}/scorers']

    r_pl = requests.get(base_url + uri[0], headers=headers).json()
    r_bl1 = requests.get(base_url + uri[1], headers=headers).json()
    r_sa = requests.get(base_url + uri[2], headers=headers).json()
    r_pd = requests.get(base_url + uri[3], headers=headers).json()
    r_fl1 = requests.get(base_url + uri[4], headers=headers).json()

    pl_scorers = r_pl['scorers']
    bl_scorers = r_bl1['scorers']
    sa_scorers = r_sa['scorers']
    pd_scorers = r_pd['scorers']
    fl1_scorers = r_fl1['scorers']

    data = {
        'pl_scorers': pl_scorers,
        'bl_scorers': bl_scorers,
        'sa_scorers': sa_scorers,
        'pd_scorers': pd_scorers,
        'fl1_scorers': fl1_scorers,

    }

    return render(request, 'scorers.html', {'data': data})


# def match(request):
#     match_uri = 'matches/'
#     team_uri = 'teams/'
#
#     url = 'https://api.football-data.org/v2/matches/?id=308649'
#
#     r = requests.get(url, headers={'X-Auth-Token': '530bbc7b369643ae837cd05fa3f135cd'})
#     json = r.json()
#
#     r2 = requests.get(base_url + team_uri, headers=headers)
#     json1 = r2.json()
#     data = {
#
#     }
#
#     return render(request, 'match.html', {'json': json})