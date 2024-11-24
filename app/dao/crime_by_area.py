from ..database.database_connection import get_connection, close_connection

CRIME_BY_AREA_QUERY = """
    SELECT
        AREA,
        AREA_NAME,
        Crm_Cd AS crime_code,
        Crm_Cd_Desc AS crime_desc,
        COUNT(AREA_NAME) AS committed_crimes
    FROM Crime
    GROUP BY
        AREA,
        AREA_NAME,
        Crm_Cd,
        Crm_Cd_Desc
    ORDER BY committed_crimes DESC;
"""


def crime_by_area_req():
    connection = get_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(CRIME_BY_AREA_QUERY)
        rows = cursor.fetchall()
        cursor.close()
        close_connection(connection)
        return rows
    else:
        return {'error': 'failed to connect to the database'}
