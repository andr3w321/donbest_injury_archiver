Script to archive donbest injury data for all their leagues.  

If you'd like to archive raw html(In case donbest changes their html format)
1. Add `python scrape_donbest_injuries.py --league nfl --data-dir ./data/ --save-html` to your crontab to save raw html files periodically.

 If you'd like to create a database
 1. Create a postgres database(google it)
 2. Create the donbest table with `psql -U db_user db_name < db_migrations/create-tables.sql` 
 3. Update your postgres db url in `model.py`
 4. Add `python scrape_donbest_injuries.py --league nfl --save-db` to your crontab to periodically scrape and update the injuries db
 
 Helper script to import old html files.
1.list dir
2.add quotes and full filename
3.pass to python script
ls -tr /home/janedoe/backup/sportsdb_backup/injury_data/html/nfl/ | sed 's,\(.*\),"/home/janedoe/backup/sportsdb_backup/injury_data/html/nfl/\1",' | xargs -L 1 python scrape_donbest_injuries.py --league nfl --import-old-html
