from __future__ import annotations
"""
Ensure you have read the introduction and task 1 and understand what 
is prohibited in this task.
This includes:
The ban on inbuilt sort methods .sort() or sorted() in this task.
And ensure your treasure data structure is not banned.
"""

from abc import ABC, abstractmethod
from typing import List, Union

from config import Tiles
from treasure import Treasure, generate_treasures
from data_structures.heap import MaxHeap

class Hollow(ABC):
    """
    Mystical troves of treasure that can be found in the maze
    There are two types of hollows that can be found in the maze:
    - Spooky Hollows: Each of these hollows contains unique treasures that can be found nowhere else in the maze.
    - Mystical Hollows: These hollows contain a random assortment of treasures like the spooky hollow however all mystical hollows are connected, so if you remove a treasure from one mystical hollow, it will be removed from all other mystical hollows.
    """

    def __init__(self) -> None:
        self.treasures = self.gen_treasures()
        self.restructure_hollow()

    @staticmethod
    def gen_treasures() -> List[Treasure]:
        """
        This is done here, so we can replace it later on in the auto marker.
        This method contains the logic to generate treasures for the hollows.

        Returns:
            List[Treasure]: A list of treasures that can be found in the maze
        """
        return generate_treasures()

    @abstractmethod
    def restructure_hollow(self):
        pass

    @abstractmethod
    def get_optimal_treasure(self, backpack_capacity: int) -> Treasure | None:
        pass

    def __len__(self) -> int:
        """
        After the restructure_hollow method is called, the treasures attribute should be updated
        don't create an additional attribute to store the number of treasures in the hollow.
        """
        return len(self.treasures)


class SpookyHollow(Hollow):
    def restructure_hollow(self) -> None:
        """
        Re-arranges the treasures into a MaxHeap, based on value-to-weight ratio.
        """
        treasures_with_ratios = [(-t.value / t.weight, t) for t in self.treasures]
        self.treasures_heap = MaxHeap.heapify(treasures_with_ratios)
        self.restructured_treasures = treasures_with_ratios  # Track remaining treasures

    def get_optimal_treasure(self, backpack_capacity: int) -> Union[Treasure, None]:
        """
        Removes the treasure with the best value-to-weight ratio that fits in the player's backpack.
        """
        while len(self.treasures_heap) > 0:
            ratio, treasure = self.treasures_heap.get_max()  # Extract the max treasure
            if treasure.weight <= backpack_capacity:
                # Ensure treasure is in the list before removing
                self.restructured_treasures.remove((ratio, treasure))  # Remove from the hollow
                return treasure  # Return the treasure that fits
        return None  # Return None if no treasure fits

    def __str__(self) -> str:
        return Tiles.SPOOKY_HOLLOW.value

    def __repr__(self) -> str:
        return str(self)


class MysticalHollow(Hollow):
    def restructure_hollow(self) -> None:
        """
        Re-arranges the treasures into a MaxHeap, based on value-to-weight ratio.
        """
        self.treasures_heap = MaxHeap.heapify([(-t.value / t.weight, t) for t in self.treasures])
        self.restructured_treasures = self.treasures.copy()  # Keep track of all treasures

    def get_optimal_treasure(self, backpack_capacity: int) -> Union[Treasure, None]:
        """
        Removes the treasure with the best value-to-weight ratio that fits in the player's backpack.
        """
        while len(self.treasures_heap) > 0:
            ratio, treasure = self.treasures_heap.get_max()  # Extract the max treasure
            if treasure.weight <= backpack_capacity:
                # Ensure treasure is removed from both current hollow and heap
                if treasure in self.restructured_treasures:
                    self.restructured_treasures.remove(treasure)
                
                # Remove the treasure from the heap without affecting others
                treasures_with_ratios = [(t.value / t.weight, t) for t in self.treasures if t != treasure]
                self.treasures_heap = MaxHeap.heapify(treasures_with_ratios)
                
                return treasure
        return None  # Return None if no treasure fits



    def __str__(self) -> str:
        return Tiles.MYSTICAL_HOWL.value

    def __repr__(self) -> str:
        return str(self)
