from ..client import Client
from .collection import Collection

class UserSession:
    __tablename__ = 'UserSessions'
    class Query:
        def __init__(self):
            self.client = Client()
        
        def get(self, id: int):
            row = self.client.exec_fetchone(f"SELECT * FROM UserSessions WHERE DiscordId={id}")

            return None if row is None else UserSession(row.DiscordId, row.SessionGuid, row.Active, row.ExpirationDate)

        def filter_by(self, discord_id=None, session_guid=None):
            sql = "SELECT * FROM UserSessions "

            if discord_id is not None:
                sql += f"WHERE DiscordId={discord_id}"
            elif session_guid is not None:
                sql += f"WHERE SessionGuid='{session_guid}'"

            rows = self.client.exec_fetchall(sql)

            sessions = []
            for row in rows:
                sessions.append(UserSession(row.DiscordId, row.SessionGuid, row.Active, row.ExpirationDate))

            return Collection(sessions)

    query = Query()

    def __init__(self, discord_id, guid, active, expiration_date):
        self.DiscordId = discord_id
        self.SessionGuid = guid
        self.Active = active
        self.ExpirationDate = expiration_date

    @property
    def id(self):
        return self.DiscordId

    @property
    def guid(self):
        return self.SessionGuid
    
    @property
    def active(self):
        return self.Active

    @property
    def expiration_date(self):
        return self.ExpirationDate
