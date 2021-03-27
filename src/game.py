"""Game module containing entity, object and game classes."""

from copy import deepcopy
from typing import Callable

game_instances = {}

class GameObject:
    """Basic memeber of Game.grid"""
    def __init__(self, symbol: str, collidable: bool, damaging: bool, damage: int = 0):
        self.symbol = symbol
        self.collidable = collidable
        self.damaging = damaging

    def add_to_grid(self, grid: list, pos_x: int, pos_y: int) -> None:
        """Adds object to Game.grid"""
        grid[pos_y][pos_x] = self

base_floor = GameObject(':black_large_square:', False, False)
base_wall = GameObject(':green_square:', True, False)

class Entity:
    """Basic member of Game.entities"""
    def __init__(self, symbol: str, health: int, position_x: int, position_y: int, brain: Callable[[int, int], None]):
        self.symbol = symbol
        self.health = health
        self.position_x = position_x
        self.position_y = position_y
        self.focused = False
        self.brain = brain

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
                    if isinstance(grid[self.position_y + dy][self.position_x + dx], GameObject) and not grid[self.position_y + dy][self.position_x + dx].collidable:
                        self.position_x += dx
                        self.position_y += dy

                        # Trivial checks:
                        if grid[self.position_y + dy][self.position_x + dx].damaging:
                            self.apply_damage(grid[self.position_y + dy][self.position_x + dx].damage)

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

class Player(Entity):
    """Focused entity of the Game.grid"""
    def __init__(self, symbol: str, health: int, position_x: int, position_y: int):
        self.symbol = symbol
        self.health = health
        self.position_x = position_x
        self.position_y = position_y
        self.focused = True

rat_hero = Player(':rat:', 100, 5, 5)

class Game:
    """Main object of the game containing active grid and entities."""
    def __init__(self, grid_size_x: int, grid_size_y: int):
        self.grid = []
        self.entities = []

        for y in range(grid_size_y + 1):
            row = []
            for x in range(grid_size_x + 1):
                row.append(base_floor)
            self.grid.append(row)

    def get_layered_grid(self) -> list:
        """Returns a list with objects and entities in it."""
        result = deepcopy(self.grid)

        for entity in self.entities:
            result[entity.position_y][entity.position_x] = entity

        return result

    def get_printable(self) -> str:
        """Returns a printable string containing entities and grid"""
        result = ""

        for k in self.get_layered_grid():
            for i in k:
                result += i.symbol
            result += "\n"

        return result

    def move_focused_entity(self, dx: int, dy: int) -> bool:
        for entity in self.entities:
            if entity.focused:
                return entity.move_entity(dx, dy, self.grid)

    def _generate_basic_grid(self) -> None:
        """Generates closed area using base_wall and base_floor"""
        for x in range(0, len(self.grid[0])):
            self.grid[0][x] = base_wall
            self.grid[len(self.grid) - 1][x] = base_wall
        for y in range(0, len(self.grid)):
            self.grid[y][0] = base_wall
            self.grid[y][len(self.grid[0]) - 1] = base_wall

    def get_focused_entity(self) -> Player:
        """Returns an active Player object"""
        for entity in self.entities:
            if entity.focused:
                return entity

    def update_entities(self) -> None:
        """Calls brain() function of every entity except for player"""
        plr = self.get_focused_entity()
        for entity in self.entities:
            if not entity.focused:
                entity.brain(plr.position_x, plr.position_y)
