 Script to archive donbest injury data for all their leagues.  Simply add `python scrape_donbest_injuries.py --league nfl --data-dir ./data/` to your crontab.
 
 This is certainly an inefficient way of doing it as it's storing the same data multiple times.  I'd welcome a pull request if someone would like to create SQL db out of this.  Preferrably using postgresql.

 TODO: Parse the data and save it as a csv or into a db
