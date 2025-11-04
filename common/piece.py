from .pos import Pos

class Piece:
    """Représente une pièce sur un plateau"""
    def __init__(self, pos: Pos, level: int):
        self.pos = pos
        self.level = level

    def __str__(self) -> str:
        return f"{'pawn' if self.level == 0 else 'master'}{self.pos}"
    
    def __repr__(self) -> str:
        return str(self)
    
    def __eq__(self, other: Piece) -> bool:
        if self.level != other.level: return False
        if self.pos != other.pos: return False
        return True
    
    def to_dict(self):
        return {"pos": self.pos.to_dict(), "level": self.level}
    
    @classmethod
    def from_dict(cls, data):
        return cls(Pos.from_dict(data["pos"]), data["level"])