#!/usr/bin/python
import requests
#from bs4 import BeautifulSoup
from argparse import ArgumentParser
import datetime
import os.path

def retry_request(url):
    """ Get a url and return the request, try it up to 3 times if it fails initially"""
    session = requests.Session()
    session.mount("http://", requests.adapters.HTTPAdapter(max_retries=3))
    return session.get(url=url)

def get_donbest_league(league):
    """ Convert the usual league codes to donbest specific league code and return it"""
    if league == "ncf":
        return "ncaaf"
    elif league == "ncb":
        return "ncaab"
    else:
        return league

def create_dir(dir_path):
    """ Create directories if they don't already exist """
    if not os.path.exists(dir_path):
        print("Creating {}".format(dir_path))
        os.makedirs(dir_path)

def scrape_donbest_injuries(league, data_dir):
    league = get_donbest_league(league)

    # add trailing slash to data dir
    if data_dir[-1] != "/":
        data_dir += "/"

    # create directories if they don't already exist
    create_dir(data_dir)
    create_dir(data_dir + "html/")

    html_league_dir = data_dir + "html/" + league + "/"
    #data_league_dir = data_dir + league + "/"
    create_dir(html_league_dir)
    #create_dir(data_league_dir)

    # retrieve data
    url = "http://www.donbest.com/{}/injuries/".format(league)
    res = retry_request(url)
    now = datetime.datetime.utcnow()

    # save html
    html_filename = html_league_dir + "{}-{}.html".format(league, now)
    with open(html_filename, mode='wb') as localfile:
        localfile.write(res.content)

    # save data
    """
    data = res.text
    soup = BeautifulSoup(data, "lxml")
    """

parser = ArgumentParser()
#_ is used as a throwaway variable name
_ = parser.add_argument('--league', action='store', dest="league", help='specify the league to scrape (nfl, ncf, wnba, nba, mlb, nhl, ncb, cfl)', required=True)
_ = parser.add_argument('--data-dir', action='store', dest="data_dir", help='specify the directory where data will be saved. Default is "./data/"', required=False)
args = parser.parse_args()

if args.league not in ["nfl","ncf","wnba","nba","mlb","nhl","ncb","cfl"]:
    raise ValueError("Unknown league {}".format(args.league))

if args.data_dir is None:
    args.data_dir = "./data/"

scrape_donbest_injuries(args.league, args.data_dir)
