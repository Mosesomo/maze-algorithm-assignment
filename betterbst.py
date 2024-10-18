from __future__ import annotations
from typing import List, Tuple, TypeVar
from data_structures.bst import BinarySearchTree

K = TypeVar('K')
I = TypeVar('I')

class BetterBST(BinarySearchTree[K, I]):
    def __init__(self, elements: List[Tuple[K, I]]) -> None:
        """
        Initialiser for the BetterBST class.
        We assume that the all the elements that will be inserted
        into the tree are contained within the elements list.

        First sort the elements list and then build a balanced tree from the sorted elements
        using the corresponding methods below.

        Args:
            elements(List[tuple[K, I]]): The elements to be inserted into the tree.

        Complexity:
            Best Case Complexity: O(n * log(n))
            Worst Case Complexity: O(n * log(n))
            where n is the number of elements in the list.
        """
        super().__init__()
        # Sorting elements using custom merge sort
        new_elements: List[Tuple[K, I]] = self.__sort_elements(elements)
        # Building the balanced BST using sorted elements
        self.__build_balanced_tree(new_elements)

    def __sort_elements(self, elements: List[Tuple[K, I]]) -> List[Tuple[K, I]]:
        """
        Custom merge sort to sort the elements based on their keys.
        We cannot use Python's built-in sorted() or .sort() as per the assignment restrictions.

        Args:
            elements (List[Tuple[K, I]]): The elements we wish to sort.

        Returns:
            list(Tuple[K, I]]) - elements after being sorted.

        Complexity:
            Best Case Complexity: O(n log n)
            Worst Case Complexity: O(n log n)
        """
        # Base case: if the list has 1 or fewer elements, it's already sorted
        if len(elements) <= 1:
            return elements
        
        # Find the middle index
        mid = len(elements) // 2
        
        # Recursively split and sort the left and right halves
        left_half = self.__sort_elements(elements[:mid])
        right_half = self.__sort_elements(elements[mid:])
        
        # Merge the sorted halves
        return self.__merge(left_half, right_half)
    
    def __merge(self, left: List[Tuple[K, I]], right: List[Tuple[K, I]]) -> List[Tuple[K, I]]:
        """
        Merge two sorted lists into one sorted list.

        Args:
            left (List[Tuple[K, I]]): Left sorted half.
            right (List[Tuple[K, I]]): Right sorted half.

        Returns:
            List[Tuple[K, I]] - Merged sorted list.

        Complexity:
            Best Case Complexity: O(n)
            Worst Case Complexity: O(n)
        """
        merged = []
        i = j = 0
        
        # Merge the left and right lists
        while i < len(left) and j < len(right):
            if left[i][0] <= right[j][0]:  # Compare based on the key (first item in the tuple)
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
        
        # Append any remaining elements
        while i < len(left):
            merged.append(left[i])
            i += 1
        
        while j < len(right):
            merged.append(right[j])
            j += 1
        
        return merged

    def __build_balanced_tree(self, elements: List[Tuple[K, I]]) -> None:
        """
        This method will build a balanced binary search tree from the sorted elements.
        We recursively choose the middle element to insert into the tree,
        ensuring balance. The left half of the list becomes the left subtree,
        and the right half becomes the right subtree.

        Args:
            elements (List[Tuple[K, I]]): The elements we wish to use to build our balanced tree.

        Returns:
            None

        Complexity:
            Best Case Complexity: O(n log n)
            Worst Case Complexity: O(n log n)

        Justification:
            The method is recursive. At each recursion, we split the list into two halves, which is O(log n)
            depth for the recursion tree. For each level, we perform O(n) work to insert the middle element.
            This results in O(n log n) complexity.
        """
        if not elements:
            return

        # Find the middle index of the sorted list
        mid = len(elements) // 2
        key, item = elements[mid]
        
        # Insert the middle element into the binary search tree
        self[key] = item

        # Recursively build the left and right subtrees
        self.__build_balanced_tree(elements[:mid])  # Left subtree
        self.__build_balanced_tree(elements[mid+1:])  # Right subtree


def in_order_traversal(node):
    """Helper function to perform in-order traversal of the tree."""
    if node is None:
        return []
    return in_order_traversal(node.left) + [(node.key, node.item)] + in_order_traversal(node.right)

# Testing the BetterBST with an example
elements = [(5, 'five'), (3, 'three'), (8, 'eight'), (1, 'one'), (4, 'four'), (7, 'seven'), (10, 'ten')]
bst = BetterBST(elements)

# Performing in-order traversal to check if the tree is balanced
sorted_elements = in_order_traversal(bst.root)
print("In-order traversal of the balanced BST:", sorted_elements)
