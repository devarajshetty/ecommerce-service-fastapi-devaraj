import os
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, Product, User
from app.config import settings

# Create DB if not exists
def create_DB_if_not_exists():
    url = settings.database_url
    # extract connection details
    db_name = url.rsplit("/", 1)[-1]
    admin_url = url.rsplit("/", 1)[0] + "/postgres"
    replaced_admin_url = admin_url.replace("postgresql+psycopg2", "postgresql")
    # print(replaced_admin_url,'replaced_admin_url')
    conn = psycopg2.connect(replaced_admin_url)
    conn.autocommit = True
    cur = conn.cursor()
    
    cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}';")
    exists = cur.fetchone()
    if not exists:
        cur.execute(f"CREATE DATABASE {db_name};")
        print(f"Database {db_name} created")
    else:
        print(f"Database {db_name} already exists")
    cur.close()
    conn.close()

# create_tables_and_insert_master_rows
def create_tables_and_insert_master_rows():
    engine = create_engine(settings.database_url, echo=True, future=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        #Seed Products
        if not db.query(Product).first():
            products = [
                Product(sku="psoas-1", name="Psoas Muscle Release Tool", price=30.0),
                Product(sku="hip-hook-10", name="Hip Hook Release Tool", price=10.0),
                Product(sku="davinci-5", name="Davinci Tool", price=25.0),
            ]
            db.add_all(products)

        ## Seed Users
        admin = User(
                username="admin",
                role="admin"
            )
        db.add(admin)
        user = User(
                username="aletha",
                role="user"
            )
        db.add(user)

        db.commit()
        print("Tables created and seed data inserted")
    finally:
        db.close()


if __name__ == "__main__":
    create_DB_if_not_exists()
    create_tables_and_insert_master_rows()