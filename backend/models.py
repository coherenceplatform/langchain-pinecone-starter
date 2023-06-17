import os
import json

from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLITE_FILE_NAME = "database.db"

# Set up the database and session
engine = create_engine(f"sqlite:///{SQLITE_FILE_NAME}")
Session = sessionmaker(bind=engine)
session = Session()


Base = declarative_base()


class Document(Base):
    __tablename__ = "documents"

    id = Column(String, primary_key=True)  # Use the file path as the unique id
    provider = Column(String)
    title = Column(String)
    data = Column(Text)  # Store the metadata as a JSON string

    def to_dict(self):
        data = json.loads(self.data) or {}
        return {
            "seo_title": data.get("seo_title", self.title),
            "title": self.title,
            "id": self.id,
            "description": data.get("description", self.title),
            "keywords": data.get("keywords", []),
            "source_url": data.get("Source URL", "https://example.com/pdf1.pdf"),
            "provider": self.provider,
        }


def reset_db():
    print(f"Removing DB file: {SQLITE_FILE_NAME}")
    if os.path.exists(SQLITE_FILE_NAME):
        os.remove(SQLITE_FILE_NAME)

    print(f"Creating empty schema...")
    Base.metadata.create_all(engine)
    print(f"Created empty schema, all set...")
