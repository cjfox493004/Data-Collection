from sqlmodel import Session
from models import engine
from bio_factory_roster import generate_bios_from_roster

with Session(engine) as session:
    bios = generate_bios_from_roster()
    session.add_all(bios)
    session.commit()