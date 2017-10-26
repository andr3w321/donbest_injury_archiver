#!/bin/bash
python scrape_donbest_injuries.py --league nfl --save-db
python scrape_donbest_injuries.py --league ncf --save-db
python scrape_donbest_injuries.py --league nba --save-db
python scrape_donbest_injuries.py --league ncb --save-db
python scrape_donbest_injuries.py --league wnba --save-db
python scrape_donbest_injuries.py --league mlb --save-db
python scrape_donbest_injuries.py --league nhl --save-db
