class Pos:
    """Représente une position relative ou absolue sur un plateau"""
    def __init__(self, li: int, co: int):
        self.li = li
        self.co = co

    def __str__(self) -> str:
        return f"({self.li}, {self.co})"
    
    def __repr__(self) -> str:
        return str(self)
    
    def __eq__(self, other: Pos) -> bool:
        if self.li != other.li: return False
        if self.co != other.co: return False
        return True
    
    def __add__(self, other: Pos) -> Pos:
        return Pos(self.li + other.li, self.co + other.co)
    
    def __getitem__(self, index: int) -> int:
        if index == 0: return self.li
        if index == 1: return self.co
        return 0
    
    def to_dict(self):
        return {"li": self.li, "co": self.co}
    
    @classmethod
    def from_dict(cls, data):
        return cls(data["li"], data["co"])
    
    def invert(self) -> Pos:
        """Inverse une position"""
        return Pos(-self.li, -self.co)
    
    def exists(self) -> bool:
        """Vérifie si cette position pourrait exister sur un plateau 5x5"""
        return 0 <= self.li <= 4 and 0 <= self.co <= 4