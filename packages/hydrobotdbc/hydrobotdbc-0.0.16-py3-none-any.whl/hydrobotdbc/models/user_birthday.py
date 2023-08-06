from ..client import Client
from .collection import Collection

class UserBirthday:
    __tablename__ = 'UserBirthdays'
    class Query:
        def __init__(self):
            self.client = Client()
        
        def get(self, id: int):
            row = self.client.exec_fetchone(f"SELECT * FROM UserBirthdays WHERE DiscordId={id}")

            return None if row is None else UserBirthday(row.DiscordId, row.Month, row.Day, row.Year) 

        def filter_by(self, discord_id=None):
            sql = "SELECT * FROM UserBirthdays "

            if discord_id is not None:
                sql += f"WHERE DiscordId={discord_id} "

            sql += "ORDER BY Month, Day, Year ASC"
            
            rows = self.client.exec_fetchall(sql)

            birthdays = []
            for row in rows:
                birthdays.append(UserBirthday(row.DiscordId, row.Month, row.Day, row.Year))

            return Collection(birthdays)

    query = Query()

    def __init__(self, discord_id, month, day, year):
        self.DiscordId = discord_id
        self.Month = month
        self.Day = day
        self.Year = year

    @property
    def id(self):
        return self.DiscordId

    @property
    def month(self):
        return self.Month
    
    @property
    def day(self):
        return self.Day
    
    @property
    def year(self):
        return self.Year
