import mysql.connector

def fetch_rows_as_dicts(host, username, password, database, query):
    # Establish a database connection
    connection = mysql.connector.connect(
        host=host,
        user=username,
        password=password,
        database=database
    )

    try:
        # Create a cursor object to execute SQL queries
        cursor = connection.cursor()
        # Execute the SQL query
        cursor.execute(query)

        # Get the column names from the cursor description
        column_names = [desc[0] for desc in cursor.description]

        # Fetch all rows as dictionaries
        rows_as_dicts = []
        for row in cursor.fetchall():
            # Create a dictionary for each row
            row_dict = dict(zip(column_names, row))
            rows_as_dicts.append(row_dict)

        return rows_as_dicts

    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()



def get_last_student_id(host, username, password, database):
    connection = mysql.connector.connect(
        host=host,
        user=username,
        password=password,
        database=database
    )
    try:
        # Establish a database connection
        cursor = connection.cursor()

        # Execute a SQL query to get the last student_id value
        query = "SELECT MAX(student_id) FROM students"
        cursor.execute(query)

        # Fetch the result
        last_student_id = cursor.fetchone()[0]

        return last_student_id

    except Exception as e:
        print("Error:", e)
        return None

    finally:
        # Close the cursor and the database connection
        cursor.close()
        connection.close()



def refresh_student_ids(host, username, password, database):
    connection = mysql.connector.connect(
        host=host,
        user=username,
        password=password,
        database=database
    )
    try:
        # Establish a database connection
        cursor = connection.cursor()

        # Execute the SQL query to refresh student IDs
        refresh_query = """
        SET @new_student_id := 0;
        UPDATE students
        SET student_id = (@new_student_id := @new_student_id + 1)
        ORDER BY student_id;
        """
        cursor.execute(refresh_query)
        
        # Commit the changes to the database
        connection.commit()

        print("Student IDs refreshed successfully.")

    except Exception as e:
        print("Error:", e)

    finally:
        # Close the cursor and the database connection
        cursor.close()
        connection.close()

    


















def insert_student(host, username, password, database, student_name, student_age, student_mark):
    # Establish a database connection
    connection = mysql.connector.connect(
        host=host,
        user=username,
        password=password,
        database=database
    )
    
    try:
        # Create a cursor object to execute SQL queries
        cursor = connection.cursor()

        # Define the INSERT SQL query
        insert_query = "INSERT INTO students ( name, age, mark) VALUES (%s, %s, %s)"

        # Specify the values to be inserted
        values = ( student_name, student_age, student_mark)

        # Execute the INSERT query with the specified values
        cursor.execute(insert_query, values)

        # Commit the changes to the database
        connection.commit()

        

    except mysql.connector.Error as error:
        # Handle any database errors
        print("Error inserting student:", error)

    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()




def delete_student(host, username, password, database, student_id):
    # Establish a database connection
    connection = mysql.connector.connect(
        host=host,
        user=username,
        password=password,
        database=database
    )
    
    try:
        # Create a cursor object to execute SQL queries
        cursor = connection.cursor()

        # Define the DELETE SQL query
        delete_query = "DELETE FROM students WHERE student_id = %s"

        # Specify the student_id to be deleted
        values = (student_id,)

        # Execute the DELETE query with the specified student_id
        cursor.execute(delete_query, values)

        # Commit the changes to the database
        connection.commit()

    except mysql.connector.Error as error:
        # Handle any database errors
        print("Error deleting student:", error)

    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()








def select_student_by_id(student_id, host, user, password, database):

    try:
        # Create a connection to the MySQL database
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        # Create a cursor to execute SQL queries
        cursor = conn.cursor()

        # Execute the SQL query to select the student by ID
        cursor.execute("SELECT * FROM students WHERE student_id = %s", (student_id,))
        student = cursor.fetchone()

        return student

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

    finally:
        # Close the cursor and the database connection when done
        if conn.is_connected():
            cursor.close()
            conn.close()






import mysql.connector

def update_row_by_id(host, username, password, database, table, row_id, new_data):
    # Create a database connection
    connection = mysql.connector.connect(
        host=host,
        user=username,
        password=password,
        database=database
    )

    cursor = connection.cursor()

    try:
        # Define the SQL query to update the row
        update_query = f"UPDATE {table} SET name = %s, age = %s, mark = %s WHERE student_id = %s"

        # Execute the query with the new data and row ID
        cursor.execute(update_query, (new_data['name'], new_data['age'], new_data['mark'], row_id))

        # Commit the changes
        connection.commit()

        print(f"Row with ID {row_id} updated successfully.")
    except Exception as e:
        print(f"Error updating row with ID {row_id}: {str(e)}")
    finally:
        cursor.close()
        connection.close()

