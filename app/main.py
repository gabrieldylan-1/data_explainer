from redis import Redis
from fastapi import FastAPI
from pydantic import BaseModel
from .database.database_connection import get_connection, close_connection
import orjson


app = FastAPI()
redis_client = Redis(host='redis', port=6379, db=0)


class CrimeByArea(BaseModel):
    area: int
    area_name: str
    crime_code: int
    crime_desc: str
    committed_crimes: int


class VictimProfile(BaseModel):
    victim_sex: str
    victim_descent: str
    committed_crimes: int
    average_victim_age: float


def map_crime_by_area(rows):
    return [CrimeByArea(
        area=row['AREA'],
        area_name=row['AREA_NAME'],
        crime_code=row['crime_code'],
        crime_desc=row['crime_desc'],
        committed_crimes=row['committed_crimes']
    ) for row in rows]


def map_victim_profile(rows):
    return [VictimProfile(
        victim_sex=row['Vict_Sex'],
        victim_descent=row['Vict_Descent'],
        committed_crimes=row['committed_crimes'],
        average_victim_age=row['average_victim_age']
    ) for row in rows]


@app.get('/')
def read_root():
    return {'message': 'hello world!'}


@app.get('/crime-by-area')
def crime_by_area():
    cache_key = 'crime-by-area'
    data = redis_client.get(cache_key)

    if data:
        print('Data is coming from redis')
        return orjson.loads(data)

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
        rows = cursor.fetchall()
        cursor.close()
        close_connection(connection)

        items = map_crime_by_area(rows)
        redis_client.set(
            cache_key,
            orjson.dumps([item.model_dump() for item in items]),
            ex=3600
        )
        return items
    else:
        return {'error': 'failed to connect to the database'}


@app.get('/victim-profile')
def victim_profile():
    cache_key = 'victim-profile'
    data = redis_client.get(cache_key)

    if data:
        print('Data is coming from redis')
        return orjson.loads(data)

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
        rows = cursor.fetchall()
        cursor.close()
        close_connection(connection)
        items = map_victim_profile(rows)
        redis_client.set(
            cache_key,
            orjson.dumps([item.model_dump() for item in items]),
            ex=3600
        )
        return items
    else:
        return {'error': 'failed to connect to the database'}
