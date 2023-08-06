from ..client import Client
from .collection import Collection


class Game:
    __tablename__ = 'Games'

    class Query:
        def __init__(self):
            self.client = Client()

        def get(self, id: int):
            row = self.client.exec_fetchone(f"SELECT * FROM Games WHERE GameId={id}")

            return None if row is None else Game(game_id=row.GameId, name=row.Name, description=row.Description, date_rec_added=row.DateRecAdded)

        def filter_by(self, game_id=None, name=None):
            sql = "SELECT * FROM Games "

            if game_id is not None:
                sql += f"WHERE GameId={game_id} "
            elif name is not None:
                sql += f"WHERE Name='{name}' "

            sql += "ORDER BY GameId ASC"

            rows = self.client.exec_fetchall(sql)

            games = []
            for row in rows:
                games.append(Game(game_id=row.GameId, name=row.Name, description=row.Description, date_rec_added=row.DateRecAdded))

            return Collection(games)

    query = Query()

    def __init__(self, name, description, game_id=None, date_rec_added=None):
        self.GameId = game_id
        self.Name = name
        self.Description = description
        self.DateRecAdded = date_rec_added

    @property
    def id(self):
        return self.GameId

    @property
    def name(self):
        return self.Name

    @property
    def description(self):
        return self.Description

    @property
    def date_rec_added(self):
        return self.DateRecAdded
