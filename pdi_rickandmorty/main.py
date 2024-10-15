import requests
import pandas as pd
import mysql.connector
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s', filename='')

# Obtain api data
def get_api_data(url):
    api_data = []
    try:
        while url:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                api_data.extend(data.get('results', []))
                url = data.get('next')
            else:
                logging.error('Failed to retrieve data from API. Error: %(response.status_code)d')
                return []
        return api_data
    except Exception as e:
        logging.error('An error occurred: %(e)s}')
        return []

# Connect to MySQL database
def create_mysql_connection():
    try:
        connection = mysql.connector.connect(
            host='db',
            user='user',
            password='password',
            database='mydatabase'
        )
        return connection
    except mysql.connector.Error as err:
        logging.error(f"Error: {err}")
        return None

# Create tables in MySQL
def create_tables(connection):
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS characters (
        id INT PRIMARY KEY,
        name VARCHAR(255),
        status VARCHAR(50),
        species VARCHAR(50),
        type VARCHAR(50),
        gender VARCHAR(50),
        image VARCHAR(255),
        episode VARCHAR(255),
        url JSON,
        created VARCHAR(50),
        origin_name VARCHAR(255),
        origin_url VARCHAR(255),
        location_name VARCHAR(255),
        location_url VARCHAR(255)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS locations (
        id INT PRIMARY KEY,
        name VARCHAR(255),
        type VARCHAR(50),
        dimension VARCHAR(255),
        residents JSON,
        url VARCHAR(255),
        created VARCHAR(50)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS episodes (
        id INT PRIMARY KEY,
        name VARCHAR(255),
        air_date VARCHAR(50),
        episode VARCHAR(50),
        characters JSON,
        url VARCHAR(255),
        created VARCHAR(50)
    );
    """)

    connection.commit()
    cursor.close()

# Insert data into MySQL tables
def insert_data(connection, table, df):
    cursor = connection.cursor()

    if table == 'characters':
        for _, row in df.iterrows():
            cursor.execute("""
                INSERT INTO characters (id, name, status, species, type, gender, image, episode, url, created, origin_name, origin_url, location_name, location_url)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                row['id'], row['name'], row['status'], row['species'], row['type'], row['gender'],
                row['image'], str(row['episode']), row['url'], row['created'],
                row['origin.name'], row['origin.url'], row['location.name'], row['location.url']
            ))

    elif table == 'locations':
        for _, row in df.iterrows():
            cursor.execute("""
                INSERT INTO locations (id, name, type, dimension, residents, url, created)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                row['id'], row['name'], row['type'], row['dimension'],
                str(row['residents']), row['url'], row['created']
            ))

    elif table == 'episodes':
        for _, row in df.iterrows():
            cursor.execute("""
                INSERT INTO episodes (id, name, air_date, episode, characters, url, created)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                row['id'], row['name'], row['air_date'], row['episode'],
                str(row['characters']), row['url'], row['created']
            ))

    connection.commit()
    cursor.close()

# Main
def main():
    # Define API URLs
    api_url = {
        "characters": "https://rickandmortyapi.com/api/character",
        "locations": "https://rickandmortyapi.com/api/location",
        "episodes": "https://rickandmortyapi.com/api/episode"
    }

    # Get data from API
    data = {key: get_api_data(url) for key, url in api_url.items()}

    # Normalize the JSON data into pandas DataFrames
    df = {key: pd.json_normalize(value) for key, value in data.items()}

    # Connect to MySQL
    connection = create_mysql_connection()
    if connection is None:
        logging.error("Failed to connect to the database.")
        return

    # Create tables
    create_tables(connection)

    # Insert data into tables
    insert_data(connection, 'characters', df['characters'])
    insert_data(connection, 'locations', df['locations'])
    insert_data(connection, 'episodes', df['episodes'])

    connection.close()

if __name__ == '__main__':
    main()