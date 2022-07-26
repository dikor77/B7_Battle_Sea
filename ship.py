class Ship:
    """
    Класс корабль\n
    coords - список координат, list of tuples [(),(),()]
    """
    def __init__(self, coords: list) -> None:
        self.coords: list = coords
        self.hit_count = 0

    @property
    def size(self):
        return len(self.coords)
    
    
    @property
    def status(self):
        """0 - целый, 1 - ранен, 2 - убит"""
        if self.hit_count <= 0:
            return 0
        elif self.hit_count >= self.size:
            return 2
        else:
            return 1