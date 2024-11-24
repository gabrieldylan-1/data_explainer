from ..database.database_connection import get_connection, close_connection

PROFILE_VICTIM_QUERY = """
    SELECT
        Vict_Sex,
        Vict_Descent,
        COUNT(*) AS committed_crimes,
        ROUND(AVG(Vict_Age)) AS average_victim_age
    FROM Crime
    WHERE Vict_Sex IN ('F', 'M')
    GROUP BY
        Vict_Sex,
        Vict_Descent
    ORDER BY committed_crimes DESC;
"""


def profile_victim_req():
    connection = get_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(PROFILE_VICTIM_QUERY)
        rows = cursor.fetchall()
        cursor.close()
        close_connection(connection)
        return rows
    else:
        return {'error': 'failed to connect to the database'}
