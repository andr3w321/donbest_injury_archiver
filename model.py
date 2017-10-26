from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, MetaData, func
from sqlalchemy.orm import Session
#eng = create_engine('postgresql://DB_NAME@HOST:PORT/DB_NAME')
conn = eng.connect()
conn.execute("""SET TIME ZONE 'UTC';""")
metadata = MetaData()

metadata.reflect(eng, only=["donbest"])
Base = automap_base(metadata=metadata)
Base.prepare()

Donbest = Base.classes.donbest

session = Session(eng)
