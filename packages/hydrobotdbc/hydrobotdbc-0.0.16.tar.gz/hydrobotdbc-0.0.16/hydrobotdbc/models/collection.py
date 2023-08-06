class Collection:
    def __init__(self, items):
        self.items = items
        self.__item_count__ = len(items)
    
    def first(self):
        try:
            return self.items[0]
        except Exception:
            return None
    
    def __len__(self):
        return self.__item_count__
