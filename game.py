"""Game module containing entity, object and game classes."""

class Object:
    """Basic memeber of Game.grid"""
    def __init__(self, symbol: str, collidable: bool, damaging: bool, position_x: int, position_y: int):
        self.symbol = symbol
        self.collidable = collidable
        self.damaging = damaging

        self.position_x = position_x
        self.position_y = position_y

    def add_to_grid(self, grid: list) -> None:
        """Adds object to Game.grid"""
        grid[self.position_x][self.position_y] = self

class Entity:
    """Basic member of Game.entities"""
    def __init__(self, symbol: str, health: int, position_x: int, position_y: int):
        self.symbol = symbol
        self.health = health
        self.position_x = position_x
        self.position_y = position_y

    def apply_damage(self, damage: int) -> bool:
        """Returns true if damage applied is higher than entity's HP"""
        if damage >= self.health:
            return True
        self.health -= damage
        return False

    def move_entity(self, dx: int, dy: int, grid: list = False, strict_mode: bool = True) -> bool:
        """Changes entity's position. If grid is provided, checks will entity move out of bounds.
        If strict mode is enabled then will move entity only if it won't be out of bounds (recommended)."""
        if grid:
            size_y = len(grid)
            size_x = len(grid[0])

            if self.position_x + dx >= 0 and self.position_x + dx <= size_x:
                if self.position_y + dy >= 0 and self.position_y + dy <= size_y:
                    #Initial grid object conditions: if grid member is object and is not collidable
                    if grid[self.position_y + dy][self.position_x + dx] is Object and not grid[self.position_y + dy][self.position_x + dx].collidable:
                        self.position_x += dx
                        self.position_y += dy

                        return True
            if not strict_mode:
                self.position_x += dx
                self.position_y += dy
            return False

        if self.position_x + dx >= 0 and self.position_y >= 0:
            self.position_x += dx
            self.position_y += dy
            return True
        if not strict_mode:
            self.position_x += dx
            self.position_y += dy
            return False
        return False

class Game:
    """Main object of the game containing active grid and entities."""
    def __init__(self, grid_size_x: int, grid_size_y: int):
        self.grid = []
        self.entities = []

        for y in range(grid_size_y):
            row = []
            for x in range(grid_size_x):
                row.append(None)
            self.grid.append(row)