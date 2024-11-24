from pydantic import BaseModel


class VictimProfile(BaseModel):
    victim_sex: str
    victim_descent: str
    committed_crimes: int
    average_victim_age: float


def map_victim_profile(rows):
    return [VictimProfile(
        victim_sex=row['Vict_Sex'],
        victim_descent=row['Vict_Descent'],
        committed_crimes=row['committed_crimes'],
        average_victim_age=row['average_victim_age']
    ) for row in rows]
