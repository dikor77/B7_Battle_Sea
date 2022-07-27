class Dot:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
    

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y


    def __repr__(self) -> str:
        return f"Dot({self.x}, {self.y})"

    def __hash__(self) -> int:
        return hash((self.x, self.y))

