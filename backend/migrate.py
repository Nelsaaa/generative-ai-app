from sqlalchemy import create_engine, MetaData, Table, text
from sqlalchemy.exc import OperationalError

DATABASE_URL = "sqlite:///sessions.db"
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Reflet de la table existante
sessions = Table('sessions', metadata, autoload_with=engine)

# Fonction pour ajouter une colonne si elle n'existe pas déjà
def add_column_if_not_exists(connection, table_name, column_definition):
    try:
        connection.execute(text(f'ALTER TABLE {table_name} ADD COLUMN {column_definition}'))
    except OperationalError as e:
        if "duplicate column name" in str(e):
            print(f"Column {column_definition.split()[0]} already exists.")
        else:
            raise

# Ajout des nouvelles colonnes
with engine.connect() as conn:
    add_column_if_not_exists(conn, 'sessions', 'theme VARCHAR')
    add_column_if_not_exists(conn, 'sessions', 'num_characters INTEGER')
    add_column_if_not_exists(conn, 'sessions', 'location VARCHAR')
    add_column_if_not_exists(conn, 'sessions', 'era VARCHAR')
    add_column_if_not_exists(conn, 'sessions', 'genre VARCHAR')
    add_column_if_not_exists(conn, 'sessions', 'ending_type VARCHAR')
    add_column_if_not_exists(conn, 'sessions', 'character_names VARCHAR')

print("Migration completed successfully.")
