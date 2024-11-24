import os
import orjson
from redis import Redis
from fastapi import FastAPI
from openai import OpenAI
from .models.CrimeByArea import map_crime_by_area
from .models.VictimProfile import map_victim_profile
from .dao.crime_by_area import CRIME_BY_AREA_QUERY, crime_by_area_req
from .dao.profile_victim import PROFILE_VICTIM_QUERY, profile_victim_req
from .llm_utils import create_prompt, generate_response


app = FastAPI()
redis_client = Redis(host='redis', port=6379, db=0)
XAI_API_KEY = os.getenv('XAI_API_KEY')
client = OpenAI(
    api_key=XAI_API_KEY,
    base_url='https://api.x.ai/v1'
)


@app.get('/')
def read_root():
    return {'message': 'hello world!'}


@app.get('/explain-crime-by-area')
def explain_crime_by_area():
    data = crime_by_area_req()
    llm_input = {
        'query': CRIME_BY_AREA_QUERY,
        'data': data,
        'schema': {
            "AREA": 'Area identifier',
            "AREA_NAME": 'Name of the area',
            "crime_code": 'Code representing the type of crime',
            "crime_desc": 'Description of the crime type',
            "committed_crimes": 'Number of crimes committed'
        }
    }

    prompt = create_prompt(
        llm_input['query'], 
        llm_input['schema'], 
        llm_input['data']
    )

    explanation = generate_response(client, prompt)
    return {'explanation': explanation}


@app.get('/explain-profile-victim')
def explain_profile_victim():
    data = profile_victim_req()
    llm_input = {
        'query': PROFILE_VICTIM_QUERY,
        'data': data,
        'schema': {
            'Vict_Sex': 'Victim sex',
            'Vict_Descent': 'Victim descent',
            'committed_crimes': 'Number of crimes committed against these victims',
            'average_victim_age': 'Average age of the victims'
        }
    }

    prompt = create_prompt(
        llm_input['query'], 
        llm_input['schema'], 
        llm_input['data']
    )

    explanation = generate_response(client, prompt)
    return {'explanation': explanation}


@app.get('/crime-by-area')
def crime_by_area():
    cache_key = 'crime-by-area'
    data = redis_client.get(cache_key)

    if data:
        print('Data is coming from redis')
        return orjson.loads(data)

    rows = crime_by_area_req()
    items = map_crime_by_area(rows)
    redis_client.set(
        cache_key,
        orjson.dumps([item.model_dump() for item in items]),
        ex=3600
    )
    return items


@app.get('/victim-profile')
def victim_profile():
    cache_key = 'victim-profile'
    data = redis_client.get(cache_key)

    if data:
        print('Data is coming from redis')
        return orjson.loads(data)
   
    rows = profile_victim_req()
    items = map_victim_profile(rows)
    redis_client.set(
        cache_key,
        orjson.dumps([item.model_dump() for item in items]),
        ex=3600
    )
    return items

