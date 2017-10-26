Script to archive donbest injury data for all their leagues(nfl, ncf, wnba, nba, ncb, mlb, nhl, cfl)

If you'd like to archive raw html(In case donbest changes their html format)
1. Add `python scrape_donbest_injuries.py --league nfl --data-dir ./data/ --save-html` to your crontab to save raw html files periodically.

If you'd like to create a database
1. Create a postgres database(google it)
2. Create the donbest table with `psql -U db_user db_name < db_migrations/create-tables.sql` 
3. Update your postgres db url in `model.py`
4. Install dependencies `pip install -r requirements.txt`
5. Add `python scrape_donbest_injuries.py --league nfl --save-db` to your crontab to periodically scrape and update the injuries db
 
Helper script to import old html files.
1. list dir
2. add quotes and full filename
3. pass to python script

`ls -tr /home/janedoe/backup/sportsdb_backup/injury_data/html/nfl/ | sed 's,\(.*\),"/home/janedoe/backup/sportsdb_backup/injury_data/html/nfl/\1",' | xargs -L 1 python scrape_donbest_injuries.py --league nfl --import-old-html`

Once you're done, query away `select date,player_name,position,injury,status,created_at,removed_at from donbest where league = 'nfl' and team_name = 'Carolina' order by team_name,player_name,created_at;`

    date    |   player_name    | position |   injury    |                           status                            |          created_at           |          removed_at           

------------+------------------+----------+-------------+-------------------------------------------------------------+-------------------------------+-------------------------------

 2017-09-04 | Brenton Bersin   | WR       | Shoulder    | IR                                                          | 2017-09-14 20:34:30.622174+00 | 

 2017-09-18 | Cam Newton       | QB       | Ankle       | probable Sunday vs. New Orleans                             | 2017-09-18 16:05:02.764936+00 | 2017-09-25 00:05:02.635407+00

 2017-09-04 | Charles Johnson  | DE       | Knee        | IR                                                          | 2017-09-14 20:34:30.622174+00 | 2017-10-21 08:05:02.399739+00

 2017-10-20 | Charles Johnson  | DE       | Groin       | is "?" Sunday vs. Chicago                                   | 2017-10-21 08:05:02.399739+00 | 2017-10-21 16:05:02.515986+00

 2017-10-21 | Charles Johnson  | DE       | Groin       | is probable Sunday vs. Chicago                              | 2017-10-21 16:05:02.515986+00 | 2017-10-23 00:05:02.252212+00

 2017-09-10 | Cole Luke        | CB       | Ankle       | "?" Sunday vs. Buffalo                                      | 2017-09-14 20:34:30.622174+00 | 2017-09-16 16:05:02.698472+00

 2017-09-16 | Cole Luke        | CB       | Ankle       | probable Sunday vs. Buffalo                                 | 2017-09-16 16:05:02.698472+00 | 2017-09-18 00:05:02.205002+00

 2017-09-29 | Curtis Samuel    | WR       | Undisclosed | expected to miss Sunday vs. New England                     | 2017-09-30 00:05:02.244005+00 | 2017-09-30 16:05:03.533826+00

 2017-09-30 | Curtis Samuel    | WR       | Back        | expected to miss Sunday vs. New England                     | 2017-09-30 16:05:03.533826+00 | 2017-10-02 00:05:02.358365+00

 2017-10-01 | Curtis Samuel    | WR       | Back        | "?" Sunday vs. Detroit                                      | 2017-10-02 00:05:02.358365+00 | 2017-10-07 16:05:02.353571+00

 2017-10-07 | Curtis Samuel    | WR       | Back        | probable Sunday vs. Detroit                                 | 2017-10-07 16:05:02.353571+00 | 2017-10-09 00:05:02.400745+00

 2017-09-29 | Daeshon Hall     | DE       | Knee        | "?" Sunday vs. New England                                  | 2017-09-29 16:05:01.836153+00 | 2017-09-30 00:05:02.244005+00

 2017-09-29 | Daeshon Hall     | DE       | Knee        | doubtful Sunday vs. New England                             | 2017-09-30 00:05:02.244005+00 | 2017-09-30 16:05:03.533826+00

 2017-09-30 | Daeshon Hall     | DE       | Knee        | expected to miss Sunday vs. New England                     | 2017-09-30 16:05:03.533826+00 | 2017-10-02 00:05:02.358365+00

 2017-10-01 | Daeshon Hall     | DE       | Knee        | "?" Sunday vs. Detroit                                      | 2017-10-02 00:05:02.358365+00 | 2017-10-07 16:05:02.353571+00

 2017-10-07 | Daeshon Hall     | DE       | Knee        | probable Sunday vs. Detroit                                 | 2017-10-07 16:05:02.353571+00 | 2017-10-09 00:05:02.400745+00

 2017-10-01 | Damiere Byrd     | WR       | Forearm     | injured last game, "?" Sunday vs. Detroit                   | 2017-10-02 00:05:02.358365+00 | 2017-10-04 16:05:01.928685+00

 2017-10-04 | Damiere Byrd     | WR       | Forearm     | IR                                                          | 2017-10-04 16:05:01.928685+00 | 
