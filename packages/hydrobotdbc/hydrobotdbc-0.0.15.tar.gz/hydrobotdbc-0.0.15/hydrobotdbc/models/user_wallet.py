from ..client import Client
from .collection import Collection

class UserWallet:
    __tablename__ = 'UserWallets'
    class Query:
        def __init__(self):
            self.client = Client()
        
        def get(self, id: int):
            row = self.client.exec_fetchone(f"SELECT * FROM UserWallets WHERE DiscordId={id} ORDER BY Active DESC")

            return None if row is None else UserWallet(row.DiscordId, row.WalletId, row.Active)

        def filter_by(self, discord_id=None, wallet_id=None, active=None):
            sql = "SELECT * FROM UserWallets "

            if discord_id is not None:
                sql += f"WHERE DiscordId={discord_id}"
            elif wallet_id is not None:
                sql += f"WHERE WalletId={wallet_id}"
            elif active is not None:
                sql += f"WHERE Active={active}"

            rows = self.client.exec_fetchall(sql)

            wallets = []
            for row in rows:
                wallets.append(UserWallet(row.DiscordId, row.WalletId, row.Active))

            return Collection(wallets)

    query = Query()

    def __init__(self, discord_id, wallet_id, active):
        self.DiscordId = discord_id
        self.WalletId = wallet_id
        self.Active = active


    @property
    def id(self):
        return self.DiscordId

    @property
    def wallet_id(self):
        return self.WalletId
    
    @property
    def active(self):
        return self.Active
