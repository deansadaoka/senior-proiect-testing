import mysql.connector

# Function to get data from a table
def get_data_from_table(local_conn, table_name):
    cursor = local_conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    data = cursor.fetchall()
    cursor.close()
    return data

# Function to insert data into a table
def insert_data_to_table(remote_conn, table_name, data):
    cursor = remote_conn.cursor()
    for row in data:
        if table_name == "tracks":
            placeholders = ', '.join(['%s'] * (len(row)+1))
            query = f"INSERT INTO {table_name} VALUES ({placeholders})"
        else:
            placeholders = ', '.join(['%s'] * len(row))
            query = f"INSERT INTO {table_name} VALUES ({placeholders})"
        try:
            if (table == "tracks"):
                new_row = []
                for r in row:
                    new_row.append(r)
                new_row.insert(9, '')
                cursor.execute(query, new_row)
            else:
                cursor.execute(query, row)
        except mysql.connector.errors.IntegrityError as e:
            print(table_name)
        except mysql.connector.errors.DataError as e:
            print(e)
            print(table_name)
            print(row)
            print(placeholders)
            exit(1)
    remote_conn.commit()
    cursor.close()

# Database connection configurations
local_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'adminpass',
    'database': 'SeniorProject'  # Replace with your source database name
}

remote_config = {
    'host': 'ambari-node5.csc.calpoly.edu',
    'user': 'nickdeanmatt',
    'password': 'adminpass',
    'database': 'nickdeanmatt'  # Replace with your destination database name
}

# Connect to the local and remote databases
local_conn = mysql.connector.connect(**local_config)
remote_conn = mysql.connector.connect(**remote_config)

# List of table names to copy
# tables = [
#     'artists', 'albums', 'tracks', 'users',
#     'friends', 'friend_requests', 'playlists'
# ]
tables = [
    'tracks', 'users',
    'friends', 'friend_requests', 'playlists'
]

# Loop through tables, get data from local server, and insert it into the remote server
for table in tables:
    data = get_data_from_table(local_conn, table)
    insert_data_to_table(remote_conn, table, data)

# Close the connections
local_conn.close()
remote_conn.close()

print("Data transfer completed.")
