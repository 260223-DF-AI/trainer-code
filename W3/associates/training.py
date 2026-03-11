import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.types import Integer, String, DateTime
from dotenv import load_dotenv
import os

# connection requirements (from CLI)
# username - 
# password - Authentication
# db name - what are we talking to
# port - 
# host - 

# Authentication  - Id verification
# Authorization - What are you allowed to do

#Connection String - Driver://Username:Password@Host:Port/Database
# secret file
# .env - environment variables

# gathering the connection string
load_dotenv()
CS = os.getenv("CS")
engine = create_engine(CS)

# prepping the query
query = "SELECT * FROM associates"
df = pd.read_sql(query, engine)
print(df)

df.to_sql(
    name = "processed",
    con = engine,
    index = False,
    if_exists = "replace",
    dtype = {
        "associate_id": Integer(),
        "first_name": String(50),
        "last_name": String(50),
        "email": String(115),
        "hire_date": DateTime(),
        "department": String(50)
    }
)

print("Wrote to DB")

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime

class Base(DeclarativeBase):
    pass

class Cohort(Base):
    __tablename__ = "cohorts"

    id: Mapped[int] = mapped_column(primary_key=True)
    start_date: Mapped[datetime] = mapped_column(default=datetime.now())
    curriculum: Mapped[str] = mapped_column(nullable=False)
    trainees: Mapped[list["Trainee"]] = relationship("trainees", back_populates="cohort")

class Trainee(Base):
    __tablename__ = "trainees"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    hire_date: Mapped[datetime] = mapped_column(default=datetime.now())
    department: Mapped[str] = mapped_column(nullable=False)

    cohort_id: Mapped[int] = mapped_column(ForeignKey("cohorts.id"))
    cohort: Mapped["Cohort"] = relationship("cohorts", back_populates="trainees")

Base.metadata.create_all(engine)