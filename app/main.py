from fastapi import FastAPI
from .database.database_connection import get_connection, close_connection

app = FastAPI()


@app.get('/')
def read_root():
    return {'message': 'hello world!'}


@app.get('/crime-by-area')
def crime_by_area():
    connection = get_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        query = """
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
        cursor.execute(query)
        items = cursor.fetchall()
        cursor.close()
        close_connection(connection)
        return items
    else:
        return {'error': 'failed to connect to the database'}


@app.get('/victim-profile')
def victim_profile():
    connection = get_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        query = """
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
        cursor.execute(query)
        items = cursor.fetchall()
        cursor.close()
        close_connection(connection)
        return items
    else:
        return {'error': 'failed to connect to the database'}
