from ..client import Client
from .collection import Collection

class DailyClaim:
    __tablename__ = 'DailyClaims'

    class Query:
        def __init__(self):
            self.client = Client()

        def get(self, id: int):
            row = self.client.exec_fetchone(f"SELECT * FROM DailyClaims WHERE DiscordId={id}")

            return None if row is None else DailyClaim(row.DiscordId, row.DateLastClaimed, row.DateRecAdded)

        def filter_by(self, discord_id=None):
            sql = "SELECT * FROM DailyClaims"

            if discord_id is not None:
                sql += f" WHERE DiscordId={discord_id}"

            rows = self.client.exec_fetchall(sql)

            claims = []
            for row in rows:
                claims.append(DailyClaim(row.DiscordId, row.DateLastClaimed, row.DateRecAdded))

            return Collection(claims)

    query = Query()

    def __init__(self, discord_id, date_last_claimed, date_rec_added):
        self.DiscordId = discord_id
        self.DateLastClaimed = date_last_claimed
        self.DateRecAdded = date_rec_added

    @property
    def id(self):
        return self.DiscordId

    @property
    def date_last_claimed(self):
        return self.DateLastClaimed

    @property
    def date_rec_added(self):
        return self.DateRecAdded
