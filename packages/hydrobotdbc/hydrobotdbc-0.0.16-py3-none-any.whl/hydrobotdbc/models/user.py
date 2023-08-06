from ..client import Client
from .collection import Collection
from flask_login import UserMixin

class User(UserMixin):
    __tablename__ = 'Users'

    class Query:
        def __init__(self):
            self.client = Client()
        
        def get(self, id: int):
            row = self.client.exec_fetchone(f"SELECT * FROM Users WHERE DiscordId={id}")

            return None if row is None else User(row.DiscordId, row.UserName, row.Discriminator, row.HydroBux, row.Meows) 

        def filter_by(self, discord_id=None, user_name=None, discriminator=None):
            sql = "SELECT * FROM Users "

            if discord_id is not None:
                sql += f"WHERE DiscordId={discord_id} "
            elif user_name is not None:
                sql += f"WHERE UserName='{user_name}' "
            elif discriminator is not None and user_name is not None:
                sql += f"WHERE UserName='{user_name}' AND Discriminator={discriminator} "

            sql += "ORDER BY DiscordId ASC"
            
            rows = self.client.exec_fetchall(sql)

            users = []
            for row in rows:
                users.append(User(row.DiscordId, row.UserName, row.Discriminator, row.HydroBux, row.Meows) )

            return Collection(users)

    query = Query()

    def __init__(self, discord_id, username, discriminator, hydrobux, meows):
        self.DiscordId = discord_id
        self.UserName = username
        self.Discriminator = discriminator
        self.HydroBux = hydrobux
        self.Meows = meows

    @property
    def id(self):
        return self.DiscordId

    @property
    def name(self):
        return self.UserName
    
    @property
    def discriminator(self):
        return self.Discriminator
    
    @property
    def hydrobux(self):
        return self.HydroBux
    
    @property
    def meows(self):
        return self.Meows
