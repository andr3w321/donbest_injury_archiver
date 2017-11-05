#!/usr/bin/python
import requests
from argparse import ArgumentParser
import datetime
import os.path
from bs4 import BeautifulSoup
from model import Donbest, conn, session
from sqlalchemy import exc
from dateutil import parser
import pytz

def find_current_injuries(league):
    """ Retrieve a list of injuries from db for a specific league where remoaved_at is null """
    current_injuries = session.query(Donbest).filter_by(league = league, removed_at = None).all()
    if len(current_injuries) < 1:
        print("WARNING: No current injuries found for {}".format(league))
    return current_injuries

def upsert_injury(current_injuries, injury):
    """ Add a new injury if fail to find a match from current injuries """
    # convert date string to date
    month, day, abbr_year = injury["Date"].split("/")
    injury["Date"] = datetime.date(2000 + int(abbr_year), int(month), int(day))

    # make a copy in memory, so can delete and return
    remaining_current_injuries = list(current_injuries)

    #search for injury in db with same league, team_name, player_name, date
    db_match = False
    for i in range(0, len(current_injuries)):
        if current_injuries[i].league == injury["League"] and \
        current_injuries[i].date == injury["Date"] and \
        current_injuries[i].team_name == injury["Team"] and \
        current_injuries[i].player_name == injury["Player"] and \
        current_injuries[i].position == injury["Pos"] and \
        current_injuries[i].injury == injury["Injury"] and \
        current_injuries[i].is_red == injury["is_red"] and \
        current_injuries[i].status == injury["Status"]:
            db_match = True
            del remaining_current_injuries[i]

    if db_match is False:
        db_donbest = Donbest()
        db_donbest.created_at = injury["created_at"]
        db_donbest.league = injury["League"]
        db_donbest.date = injury["Date"]
        db_donbest.team_name = injury["Team"]
        db_donbest.player_name = injury["Player"]
        db_donbest.position = injury["Pos"]
        db_donbest.injury = injury["Injury"]
        db_donbest.is_red = injury["is_red"]
        db_donbest.status = injury["Status"]

        # search for duplicates
        duplicates = session.query(Donbest).filter_by(league = db_donbest.league, \
                                                    date = db_donbest.date, \
                                                    team_name = db_donbest.team_name, \
                                                    player_name = db_donbest.player_name, \
                                                    position = db_donbest.position, \
                                                    injury = db_donbest.injury, \
                                                    is_red = db_donbest.is_red, \
                                                    status = db_donbest.status).all()
        if len(duplicates) > 0:
            print("Duplicate found for", db_donbest.league, db_donbest.date, db_donbest.team_name, db_donbest.player_name, db_donbest.position, db_donbest.injury, db_donbest.is_red, db_donbest.status, db_donbest.created_at)
            # if we search all duplicates and any of them has a null removed_at, don't add
            add_back = True
            for duplicate in duplicates:
                print(duplicate.removed_at, type(duplicate.removed_at))
                if duplicate.removed_at is None:
                    add_back = False
                    print("dont add back previously removed injury")
            if add_back:
                print("adding back previously removed injury")
                session.add(db_donbest)
        else:
            session.add(db_donbest)
    return remaining_current_injuries
        
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

def scrape_donbest_injuries(league, data_dir, save_html, save_db, old_html_filename):
    donbest_league = get_donbest_league(league)

    # retrieve data
    if old_html_filename is None:
        url = "http://www.donbest.com/{}/injuries/".format(donbest_league)
        res = retry_request(url)
        data = res.text
        now = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)
    else:
        data = open(old_html_filename)
        filename_date_str = old_html_filename.split(".html",1)[0].split("-",1)[1]
        now = parser.parse(filename_date_str + "+00")

    if save_html:
        # add trailing slash to data dir
        if data_dir[-1] != "/":
            data_dir += "/"

        # create directories if they don't already exist
        create_dir(data_dir)
        create_dir(data_dir + "html/")

        html_league_dir = data_dir + "html/" + league + "/"
        create_dir(html_league_dir)

        # save html
        html_filename = html_league_dir + "{}-{}.html".format(league, now)
        with open(html_filename, mode='wb') as localfile:
            localfile.write(res.content)

    if save_db or old_html_filename is not None:
        current_injuries = find_current_injuries(league)

        soup = BeautifulSoup(data, "lxml")
        # find table, class=statistics_table
        tables = soup.find_all("table", class_="statistics_table")
        if len(tables) != 1:
            print("No injuries found or too many donbest data tables error.", league)
        else:
            trs = tables[0].find_all("tr")

            donbest_injuries = []
            for tr in trs:
                # donbest labels
                ths = tr.find_all("th")
                if len(ths) > 0:
                    donbest_labels = []
                    for th in ths:
                        if "statistics_cellrightborder" in th.get("class"):
                            donbest_labels.append(th.text)
                # donbest injuries
                tds = tr.find_all("td")
                if len(tds) > 0:
                    if "statistics_table_alternateRow" in tds[0].get("class"):
                        donbest_updated_at_text = tds[0].text.strip()
                    elif "statistics_table_header" in tds[0].get("class"):
                        donbest_team_name = tds[0].text
                    elif "statistics_cellrightborder" in tds[0].get("class"):
                        injury = {}
                        injury["created_at"] = now
                        injury["League"] = league
                        injury["Team"] = donbest_team_name
                        for i in range(0, len(tds)):
                            injury[donbest_labels[i]] = tds[i].text
                            # is red or not
                            if donbest_labels[i] == "Player":
                                if tds[i].get("style") is not None and "color:Red" in tds[i].get("style"):
                                    injury["is_red"] = 1
                                else:
                                    injury["is_red"] = 0
                        donbest_injuries.append(injury)

            # remove duplicate donbest injuries
            donbest_injuries = list({ repr(each): each for each in donbest_injuries}.values())
            # upsert
            for injury in donbest_injuries:
                current_injuries = upsert_injury(current_injuries, injury)
            # remove all left over injuries
            for cur_inj in current_injuries:
                # make sure we're not removing injuries before they were created when importing old html files
                if now > cur_inj.created_at:
                    cur_inj.removed_at = now
            session.commit()
            conn.close()

aparser = ArgumentParser()
#_ is used as a throwaway variable name
_ = aparser.add_argument('--league', action='store', dest="league", help='specify the league to scrape (nfl, ncf, wnba, nba, mlb, nhl, ncb, cfl)', required=True)
_ = aparser.add_argument('--data-dir', action='store', dest="data_dir", help='specify the directory where data will be saved. Default is "./data/"', required=False)
_ = aparser.add_argument('--save-html', action='store_true', dest="save_html", help='save raw html file', required=False)
_ = aparser.add_argument('--save-db', action='store_true', dest="save_db", help='save data to database', required=False)
_ = aparser.add_argument('--import-old-html', action='store', dest="old_html_filename", help='import an old archived html file into db', required=False)
args = aparser.parse_args()

if args.league not in ["nfl","ncf","wnba","nba","mlb","nhl","ncb","cfl"]:
    raise ValueError("Unknown league {}".format(args.league))

if args.data_dir is None:
    args.data_dir = "./data/"

if args.save_html is False and args.save_db is False and args.old_html_filename is None:
    raise ValueError("Must give either option --save-db or --save-html or --import-old-html for script to do anything")

scrape_donbest_injuries(args.league, args.data_dir, args.save_html, args.save_db, args.old_html_filename)
