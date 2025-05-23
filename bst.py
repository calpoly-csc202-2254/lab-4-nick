import sys
import unittest
from typing import *
from dataclasses import dataclass
sys.setrecursionlimit(10**6)

from typing import Any, Callable, Optional, Union

# Defines a BinTree node structure
@dataclass(frozen=True)
class Node:
    element: Any
    left: Optional['Node'] = None
    right: Optional['Node'] = None

# Union type for BinTree: either a Node or None
BinTree = Optional[Node]

# Definitions for the BinTree class
class frozenBinarySearchTree:
    def __init__(self, comes_before: Callable[[Any, Any], bool], tree: BinTree = None):
        self.comes_before = comes_before
        self.tree = tree

    def is_empty(self) -> bool:
        return self.tree is None

    def insert(self, value: Any) -> 'frozenBinarySearchTree':
        def insert_helper(tree: BinTree) -> BinTree:
            if tree is None:
                return Node(value)
            elif self.comes_before(value, tree.element):
                return Node(tree.element, insert_helper(tree.left), tree.right)
            else:
                return Node(tree.element, tree.left, insert_helper(tree.right))
        return frozenBinarySearchTree(self.comes_before, insert_helper(self.tree))

    def lookup(self, value: Any) -> bool:
        def lookup_helper(tree: BinTree) -> bool:
            if tree is None:
                return False
            elif (not self.comes_before(value, tree.element)) and (not self.comes_before(tree.element, value)):
                return True
            elif self.comes_before(value, tree.element):
                return lookup_helper(tree.left)
            else:
                return lookup_helper(tree.right)
        return lookup_helper(self.tree)

    def delete(self, value: Any) -> 'frozenBinarySearchTree':
        def find_min(tree: BinTree) -> Any:
            while tree and tree.left is not None:
                tree = tree.left
            return tree.element if tree else None

        def delete_helper(tree: BinTree) -> BinTree:
            if tree is None:
                return None
            if (not self.comes_before(value, tree.element)) and (not self.comes_before(tree.element, value)):
                # Node to delete found
                if tree.left is None:
                    return tree.right
                elif tree.right is None:
                    return tree.left
                else:
                    min_larger_node = find_min(tree.right)
                    return Node(min_larger_node, tree.left, delete_helper(tree.right))
            elif self.comes_before(value, tree.element):
                return Node(tree.element, delete_helper(tree.left), tree.right)
            else:
                return Node(tree.element, tree.left, delete_helper(tree.right))
        return frozenBinarySearchTree(self.comes_before, delete_helper(self.tree))

def example_fun(x : int) -> bool:
    return x < 142
