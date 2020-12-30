from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, MetaData, func
from sqlalchemy.orm import Session
#eng = create_engine('postgresql://sportsdb@45.33.40.215:5432/sportsdb')
eng = create_engine('postgresql://sportsdb@localhost:5432/sportsdb')
conn = eng.connect()
conn.execute("""SET TIME ZONE 'UTC';""")
metadata = MetaData()

metadata.reflect(eng, only=["donbest"])
Base = automap_base(metadata=metadata)
Base.prepare()

Donbest = Base.classes.donbest

session = Session(eng)
