from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

from config import Directions, Tiles
from hollows import Hollow, MysticalHollow, SpookyHollow
from treasure import Treasure


class Position:
    def __init__(self, row: int, col: int) -> None:
        """
        Args:
            row(int): Row number in this maze cell position
            col(int): Column number in this maze cell position
        """
        self.row: int = row
        self.col: int = col

    def __eq__(self, value: object) -> bool:
        return isinstance(value, Position) and value.row == self.row and value.col == self.col

    def __repr__(self):
        return str(self)

    def __str__(self) -> str:
        return f"({self.row}, {self.col})"


@dataclass
class MazeCell:
    tile: str | Hollow
    position: Position
    visited: bool = False

    def __str__(self) -> str:
        return str(self.tile)

    def __repr__(self) -> str:
        return f"'{self.tile}'"


class Maze:
    directions: dict[Directions, Tuple[int, int]] = {
        Directions.UP: (-1, 0),
        Directions.DOWN: (1, 0),
        Directions.LEFT: (0, -1),
        Directions.RIGHT: (0, 1),
    }

    def __init__(self, start_position: Position, end_positions: List[Position], walls: List[Position], hollows: List[tuple[Hollow, Position]], rows: int, cols: int) -> None:
        """
        Constructs the maze you should never be interacting with this method.
        Please take a look at `load_maze_from_file` & `sample1`

        Args:
            start_position(Position): Starting position in the maze.
            end_positions(List[Position]): End positions in the maze.
            walls(List[Position]): Walls in the maze.
            hollows(List[Position]): Hollows in the maze.
            rows(int): Number of rows in the maze.
            cols(int): Number of columns in the maze.

        Complexity:
            Best Case Complexity: O(_create_grid)
            Worst Case Complexity: O(_create_grid)
        """
        self.start_position: Position = start_position
        self.end_positions: List[Position] = end_positions
        self.rows: int = rows
        self.cols: int = cols
        self.grid: List[List[MazeCell]] = self._create_grid(walls, hollows, end_positions)

    def _create_grid(self, walls: List[Position], hollows: List[(Hollow, Position)], end_positions: List[Position]) -> List[List[MazeCell]]:
        """
        Args:
            walls(List[Position]): Walls in the maze.
            hollows(List[Position]): Hollows in the maze.
            end_positions(List[Position]): End positions in the maze.

        Return:
            List[MazeCell]: The generated maze grid.

        Complexity:
            Best Case Complexity: O(N) where N is the number of cells in the maze.
            Worst Case Complexity: O(N) where N is the number of cells in the maze.
        """
        grid: List[List[MazeCell]] = [[MazeCell(' ', Position(i, j))
                                       for j in range(self.cols)] for i in range(self.rows)]
        grid[self.start_position.row][self.start_position.col] = MazeCell(
            Tiles.START_POSITION.value, self.start_position)
        for wall in walls:
            grid[wall.row][wall.col].tile = Tiles.WALL.value
        for hollow, pos in hollows:
            grid[pos.row][pos.col].tile = hollow
        for end_position in end_positions:
            grid[end_position.row][end_position.col].tile = Tiles.EXIT.value
        return grid

    @staticmethod
    def validate_maze_file(maze_name: str) -> None:
        """
        Mazes must have the following:
        - A start position (P)
        - At least one exit (E)
        - All rows must have the same number of columns
        - Tiles are representations can be found in config.py
        - At least one treasure

        Args:
            maze_name(str): The name of the maze.

        Raises:
            ValueError: If maze_name is invalid.

        Complexity:
            Best Case Complexity: O(N) where N is the number of cells in the maze.
            Worst Case Complexity: O(N) where N is the number of cells in the maze.

            Assuming dictionary operations can be done on O(1) time.
        """
        tile_count: dict[str, int] = {}
        with open(f"./mazes/{maze_name}", 'r') as f:
            lines: List[str] = f.readlines()
            cols: int = len(lines[0].strip())
            for line in lines:
                if len(line.strip()) != cols:
                    raise ValueError(f"Uneven columns in {maze_name} ensure all rows have the same number of columns")
                # Check tiles
                for tile in line.strip():
                    if tile not in tile_count:
                        tile_count[tile] = 1
                    else:
                        tile_count[tile] += 1
        if 'P' not in tile_count or 'E' not in tile_count:
            raise ValueError(f"Missing start or end position in {maze_name}")

        if tile_count['P'] > 1:
            raise ValueError(f"Multiple start positions found in {maze_name}")

        # Check we have at least one treasure
        if not (Tiles.SPOOKY_HOLLOW.value in tile_count or Tiles.MYSTICAL_HOLLOW.value in tile_count):
            raise ValueError(f"No treasures found in {maze_name}")

        valid_types: List[str] = [tile.value for tile in Tiles]
        invalid_tiles: List[str] = [tile for tile in tile_count if tile not in valid_types]
        if invalid_tiles:
            raise ValueError(f"Invalid tile(s) found in {maze_name} ({invalid_tiles})")

    @classmethod
    def load_maze_from_file(cls, maze_name: str) -> Maze:
        """
        Args:
            maze_name(str): The maze name to load the maze from.

        Return:
            Maze: The newly created maze instance.

        Complexity:
            Best Case Complexity: O(N) where N is the number of cells in the maze.
            Worst Case Complexity: O(N) where N is the number of cells in the maze.

            For small mazes we assume the lists we not need to resize.
        """
        cls.validate_maze_file(maze_name)
        end_positions, walls, hollows = [], [], []
        mystical_hollow: MysticalHollow = MysticalHollow()
        start_position: Position | None = None
        with open(f"./mazes/{maze_name}", 'r') as f:
            lines: List[str] = f.readlines()
            rows: int = len(lines)
            cols: int = len(lines[0].strip())
            for i, line in enumerate(lines):
                for j, tile in enumerate(line.strip()):
                    if tile == Tiles.START_POSITION.value:
                        start_position: Position = Position(i, j)
                    elif tile == Tiles.EXIT.value:
                        end_positions.append(Position(i, j))
                    elif tile == Tiles.WALL.value:
                        walls.append(Position(i, j))
                    elif tile == Tiles.SPOOKY_HOLLOW.value:
                        hollows.append((SpookyHollow(), Position(i, j)))
                    elif tile == Tiles.MYSTICAL_HOLLOW.value:
                        hollows.append((mystical_hollow, Position(i, j)))
        assert start_position is not None
        return Maze(start_position, end_positions, walls, hollows, rows, cols)

    def is_valid_position(self, position: Position) -> bool:
        """
        Checks if the position is within the maze and not blocked by a wall.

        Args:
            position (Position): The position to check.

        Returns:
            bool - True if the position is within the maze and not blocked by a wall.

        Complexity:
            Best Case Complexity: TODO
            Worst Case Complexity: TODO
        """
        if 0 <= position.row < self.rows and 0 <= position.col < self.cols:
            # Check if the tile is not a wall
            return self.grid[position.row][position.col].tile != Tiles.WALL.value
        return False

    def get_available_positions(self, current_position: Position) -> List[Position]:
        """
        Returns a list of all the new possible you can move to from your current position.

        Args:
            current_position (Position): Your current position.

        Returns:
            List[Position] - A list of all the new possible you can move to from your current position.

        Complexity:
            Best Case Complexity: TODO
            Worst Case Complexity: TODO
        """

        valid_positions = []
        for direction, (row_delta, col_delta) in self.directions.items():
            new_position = Position(current_position.row + row_delta, current_position.col + col_delta)
            if self.is_valid_position(new_position):
                valid_positions.append(new_position)
        return valid_positions

    def find_way_out(self) -> List[Position] | None:
        """
        Finds a way out of the maze in some cases there may be multiple exits
        or no exits at all.

        Returns:
            List[Position]: The path from start to exit, or None if no path exists.
        """
        
        def dfs(position: Position, path: List[Position]) -> List[Position] | None:
            if position in self.end_positions:  # Found an exit
                return path + [position]
            
            # Mark the current position as visited
            self.grid[position.row][position.col].visited = True
            
            # Explore neighboring cells
            for next_position in self.get_available_positions(position):
                if not self.grid[next_position.row][next_position.col].visited:
                    result = dfs(next_position, path + [position])
                    if result:
                        return result  # Found a valid path
            
            return None

        # Start DFS from the start position
        return dfs(self.start_position, [])


    def take_treasures(self, path: List[MazeCell], backpack_capacity: int) -> List[Treasure] | None:
        collected_treasures = []
        current_capacity = backpack_capacity

        for cell in path:
            if isinstance(cell.tile, Hollow):
                treasure = cell.tile.get_optimal_treasure(current_capacity)
                if treasure and treasure.weight <= current_capacity:
                    # Remove the treasure from all mystical hollows
                    for hollow in self.grid:
                        if isinstance(hollow, MysticalHollow):
                            if treasure in hollow.treasures:
                                hollow.treasures.remove(treasure)
                    collected_treasures.append(treasure)
                    current_capacity -= treasure.weight

        return collected_treasures if collected_treasures else None


    
    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        """
        Returns the grid in a human-readable format.

        Complexity:
        Best Case Complexity: O(n) where n is the number of cells in the maze.
        Worst Case Complexity: O(n) where n is the number of cells in the maze.
        """
        my_grid: str = ""
        for row in self.grid:
            my_grid += "" if my_grid == "" else "\n"
            my_grid += str(row)

        return my_grid


def sample1() -> None:
    maze = Maze.load_maze_from_file("sample.txt")
    print(maze)


def sample2() -> None:
    maze = Maze.load_maze_from_file("sample2.txt")
    print(maze)
    # Samples as to how the grid / maze cells work
    r, c = 4, 0  # row 4, col 0
    print(maze.grid[r][c].position, type(maze.grid[r][c]), f"Visited: {maze.grid[r][c].visited}")
    print(maze.grid[r][c].tile, type(maze.grid[r][c].tile))
    r, c = 2, 3  # row 2, col 3
    print(maze.grid[r][c].position, type(maze.grid[r][c]), f"Visited: {maze.grid[r][c].visited}")
    print(maze.grid[r][c].tile, type(maze.grid[r][c].tile))


if __name__ == "__main__":
    sample1()