import psycopg2
from psycopg2 import sql

try:
    # Establish a connection to the database
    connection = psycopg2.connect(
        database="nickdeanmatt",
        user="nickdeanmatt",
        password="adminpass",
        host="ambari-node5.csc.calpoly.edu",
        port="3306",
    )

    # Create a cursor object
    cursor = connection.cursor()

    # Add the rating column to the table
    cursor.execute(
        """
        ALTER TABLE playlist_tracks 
        ADD COLUMN rating INT;
        """
    )

    # Update all existing rows to have a rating of 4
    cursor.execute(
        """
        UPDATE playlist_tracks 
        SET rating = 4;
        """
    )

    # Commit the changes to the database
    connection.commit()
    print("Column added successfully and all rows updated.")

except (Exception, psycopg2.Error) as error:
    print("Error occurred:", error)

finally:
    # Close the database connection
    if connection:
        cursor.close()
        connection.close()
        print("Connection closed.")