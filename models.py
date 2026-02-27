from sqlmodel import SQLModel, Field, create_engine

class Bio(SQLModel, table=True):
    first_name: str = Field(primary_key=True)
    last_name: str = Field(primary_key=True)
    number: int | None = None
    position: str | None = None
    height: str | None = None
    weight: int | None = None
    academic_class: str | None = None
    hometown: str | None = None
    high_school: str | None = None

class Stats(SQLModel, table=True):
    first_name: str = Field(primary_key=True, foreign_key="bio.first_name")
    last_name: str = Field(primary_key=True, foreign_key="bio.last_name")
    number: int | None = None 
    gp: int | None = None
    blk: int | None = None
    g: int | None = None
    a: int | None = None
    pts: int | None = None
    sh: int | None = None
    sh_pct: float | None = None
    plus_minus: int | None = None
    ppg: int | None = None
    shg: int | None = None
    fg: int | None = None
    gwg: int | None = None
    gtg: int | None = None
    otg: int | None = None
    htg: int | None = None
    uag: int | None = None
    pn_pim: str | None = None
    minutes: int | None = None
    maj: int | None = None
    oth: int | None = None

engine = create_engine('sqlite:///hockey.db')
SQLModel.metadata.create_all(engine)