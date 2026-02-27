from sqlmodel import Session
from models import engine
from stats_factory_stats_only import generate_stats_from_stats_new

with Session(engine) as session:
    stats = generate_stats_from_stats_new()
    session.add_all(stats)
    session.commit()

