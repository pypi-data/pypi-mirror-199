from ..client import Client
from .collection import Collection

class UserVoiceState:
    __tablename__ = 'UserVoiceStates'
    class Query:
        def __init__(self):
            self.client = Client()
        
        def get(self, id: int):
            row = self.client.exec_fetchone(f"SELECT * FROM UserVoiceStates WHERE DiscordId={id}")

            return None if row is None else UserVoiceState(row.DiscordId, row.DateLastUpdated, row.DateRecAdded)

        def filter_by(self, discord_id=None):
            sql = "SELECT * FROM UserVoiceStates"

            if discord_id is not None:
                sql += f" WHERE DiscordId={discord_id}"
            
            rows = self.client.exec_fetchall(sql)

            voicestates = []
            for row in rows:
                voicestates.append(UserVoiceState(row.DiscordId, row.DateLastUpdated, row.DateRecAdded))

            return Collection(voicestates)

    query = Query()

    def __init__(self, discord_id, date_last_updated, date_rec_added):
        self.DiscordId = discord_id
        self.DateLastUpdated = date_last_updated
        self.DateRecAdded = date_rec_added

    @property
    def id(self):
        return self.DiscordId

    @property
    def date_last_updated(self):
        return self.DateLastUpdated
    
    @property
    def date_rec_added(self):
        return self.DateRecAdded
