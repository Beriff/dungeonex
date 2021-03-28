"""Game module containing entity, object and game classes."""

from copy import deepcopy
from random import choice

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
    def __init__(self, symbol: str, health: int, position_x: int, position_y: int):
        self.symbol = symbol
        self.health = health
        self.position_x = position_x
        self.position_y = position_y
        self.focused = False
        self.level = 1

    def get_damage(self) -> int:
        """Returns randomized damage depending on Entity.level"""
        base_damage = self.level**3
        if choice([0,1]):
            if choice([0,1]):
                base_damage += round(base_damage/3)
                return base_damage
            base_damage -= round(base_damage/2)
            return base_damage
        return base_damage

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

    def approach(self, node_x: int, node_y: int, plr) -> None:
        """Simple approaching and hitting algorithm"""
        if self.position_x > node_x + 1:
            self.move_entity(-1, 0)
        elif self.position_y > node_y + 1:
            self.move_entity(0, -1)
        elif self.position_x < node_x - 1:
            self.move_entity(1, 0)
        elif self.position_y < node_y - 1:
            self.move_entity(0, 1)
        else:
            print(f'gonna do {self.get_damage()}')
            plr.apply_damage(self.get_damage())


class Player(Entity):
    """Focused entity of the Game.grid"""
    def __init__(self, symbol: str, health: int, position_x: int, position_y: int):
        self.symbol = symbol
        self.health = health
        self.position_x = position_x
        self.position_y = position_y
        self.focused = True
        self.level = 1
        self.exp = 0
        self.log = 'Player appeared!'

    def add_exp(self, amount: int) -> None:
        cap = self.level**3
        if amount + self.exp < cap:
            self.exp += amount
            self.log = f'+{self.exp} exp!'
        elif amount + self.exp == cap:
            self.level += 1
            self.exp = 0
            self.log = 'Level up!'
        elif amount + self.exp > cap:
            self.level += 1
            self.log = 'Level up!'
            self.add_exp(amount - cap)

rat_hero = Player(':rat:', 100, 5, 5)
enemy = Entity(':monkey:', 5, 2, 2)

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

    def test_entity_position(self, desired_x: int, desired_y: int) -> bool:
        """Returns true if some entity of Game.entities occupies the given coordinates"""
        for entity in self.entities:
            if not entity.focused:
                if entity.position_x == desired_x and entity.position_y == desired_y:
                    return True
        return False

    def get_entity_by_coords(self, insp_x: int, insp_y: int) -> int:
        """Returns *index* of the entity in Game.entities"""
        for i in range(0, len(self.entities)):
            if self.entities[i].position_x == insp_x and self.entities[i].position_y == insp_y:
                return i

    def move_focused_entity(self, dx: int, dy: int) -> bool:
        """Moves player. Returns false if player collides with a wall. Otherwise, returns true."""
        for entity in self.entities:
            if entity.focused:
                if not self.test_entity_position(entity.position_x + dx, entity.position_y + dy):
                    if entity.move_entity(dx, dy, self.grid):
                        self.update_entities()
                        return True
                    return False    
                #If player tries to move into entity's cell -> attack it
                if self.entities[self.get_entity_by_coords(entity.position_x + dx, entity.position_y + dy)].apply_damage(entity.get_damage()):
                    #if true then ^^^ entity is dead. Let's remove it
                    self.entities.pop(self.get_entity_by_coords(entity.position_x + dx, entity.position_y + dy))
                self.update_entities()
                return True



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
        """Calls approach() function of every entity except for player"""
        plr = self.get_focused_entity()
        for entity in self.entities:
            if not entity.focused:
                entity.approach(plr.position_x, plr.position_y, plr)
