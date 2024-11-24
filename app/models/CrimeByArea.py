from pydantic import BaseModel


class CrimeByArea(BaseModel):
    area: int
    area_name: str
    crime_code: int
    crime_desc: str
    committed_crimes: int


def map_crime_by_area(rows):
    return [CrimeByArea(
        area=row['AREA'],
        area_name=row['AREA_NAME'],
        crime_code=row['crime_code'],
        crime_desc=row['crime_desc'],
        committed_crimes=row['committed_crimes']
    ) for row in rows]
