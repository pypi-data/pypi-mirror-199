from ..client import Client
from .collection import Collection

class Wallet():
    __tablename__ = 'Wallets'

    class Query:
        def __init__(self):
            self.client = Client()
        
        def get(self, id: int):
            row = self.client.exec_fetchone(f"SELECT * FROM Wallets WHERE WalletId={id}")

            return None if row is None else Wallet(row.WalletId, row.Name, row.Image, row.Cost) 

        def filter_by(self, wallet_id=None, name=None, image=None):
            sql = "SELECT * FROM Wallets "

            if wallet_id is not None:
                sql += f"WHERE WalletId={wallet_id} "
            elif name is not None:
                sql += f"WHERE Name='{name}' "
            elif image is not None:
                sql += f"WHERE Image='{image}' "

            sql += "ORDER BY WalletId ASC"
            
            rows = self.client.exec_fetchall(sql)

            wallets = []
            for row in rows:
                wallets.append(Wallet(row.WalletId, row.Name, row.Image, row.Cost))

            return Collection(wallets)

    query = Query()

    def __init__(self, wallet_id, name, image, cost):
        self.WalletId = wallet_id
        self.Name = name
        self.Image = image
        self.Cost = cost

    @property
    def id(self):
        return self.WalletId

    @property
    def name(self):
        return self.Name
    
    @property
    def image(self):
        return self.Image

    @property
    def cost(self):
        return self.Cost
