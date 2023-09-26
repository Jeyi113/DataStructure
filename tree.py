# Copyright 2013, Michael H. Goldwasser
#
# Developed for use with the book:
#
#        Data Structures and Algorithms in Python
#        Michael T. Goodrich, Roberto Tamassia, and Michael H. Goldwasser
#        John Wiley & Sons, 2013
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.    If not, see <http://www.gnu.org/licenses/>.

import collections
class Tree:
    """Abstract base class representing a tree structure."""

    #------------------------------- nested Position class -------------------------------
    class Position:
        """An abstraction representing the location of a single element within a tree.

        Note that two position instaces may represent the same inherent location in a tree.
        Therefore, users should always rely on syntax 'p == q' rather than 'p is q' when testing
        equivalence of positions.
        """

        def element(self):
            """
            Return the element stored at this Position.
            
            :raises NotImplementedError: if there's no implementation of this function in the subclass, it raises NotImplementedError with the message 'must be implemented by subclass'
            """
            raise NotImplementedError('must be implemented by subclass')

        def __eq__(self, other):
            """
            Return True if other Position represents the same location.
            
            :raises NotImplementedError: if there's no implementation of this function in the subclass, it raises NotImplementedError with the message 'must be implemented by subclass'
            """
            raise NotImplementedError('must be implemented by subclass')

        def __ne__(self, other):
            """
            Return True if other does not represent the same location.
            
            :return: True if other does not represent the same location with self, otherwise, False.
            """
            return not (self == other)                        # opposite of __eq__

    # ---------- abstract methods that concrete subclass must support ----------
    def root(self):
        """
        Return Position representing the tree's root (or None if empty).
        
        :raises NotImplementedError: if there's no implementation of this function in the subclass, it raises NotImplementedError with the message 'must be implemented by subclass'
        """
        raise NotImplementedError('must be implemented by subclass')

    def parent(self, p):
        """
        Return Position representing p's parent (or None if p is root).
        
        :param p: The Position object representing the child of the parent.
        :raises NotImplementedError: if there's no implementation of this function in the subclass, it raises NotImplementedError with the message 'must be implemented by subclass'
        """
        raise NotImplementedError('must be implemented by subclass')

    def num_children(self, p):
        """
        Return the number of children that Position p has.
        
        :param p: The Position object representing the parent of the children to be counted.
        :raises NotImplementedError: if there's no implementation of this function in the subclass, it raises NotImplementedError with the message 'must be implemented by subclass'
        """
        raise NotImplementedError('must be implemented by subclass')

    def children(self, p):
        """
        Generate an iteration of Positions representing p's children.
        
        :param p: The Position object representing the parent of the children
        :raises NotImplementedError: if there's no implementation of this function in the subclass, it raises NotImplementedError with the message 'must be implemented by subclass'
        """
        raise NotImplementedError('must be implemented by subclass')

    def __len__(self):
        """
        Return the total number of elements in the tree.
        
        :raises NotImplementedError: if there's no implementation of this function in the subclass, it raises NotImplementedError with the message 'must be implemented by subclass'
        """
        raise NotImplementedError('must be implemented by subclass')

    # ---------- concrete methods implemented in this class ----------
    def is_root(self, p):
        """
        Return True if Position p represents the root of the tree.
        
        :param p: The Position object to be checked whether it is root of the tree
        :return: True if Position p is the root of the tree, otherwise, False.
        """
        return self.root() == p # return True if the Position p is root of the tree

    def is_leaf(self, p):
        """
        Return True if Position p does not have any children.
        
        :param p: The Position object to be checked whether it is leaf of the tree
        :return: True if Position p does not have any children, otherwise, False.
        """
        return self.num_children(p) == 0 # return True if the Position p is leaf

    def is_empty(self):
        """
        Return True if the tree is empty.
        
        :return: True if the size of the tree is 0 (which means that the tree is empty), otherwise, False.
        """
        return len(self) == 0 # return True if the size of the tree is 0

    def depth(self, p):
        """
        Return the number of levels separating Position p from the root.
        
        :param p: The Position object that we want to know its depth
        :return: 0 if Position p represents the root of the tree, else the number of levels separating Position p from the root.
        """
        # If Position p is the root, the depth is 0;
        # otherwise, return the 1 + parent's depth.
        if self.is_root(p):
            return 0
        else:
            return 1 + self.depth(self.parent(p))

    def _height(self, p):                                    # time is linear in size of subtree
        """
        Return the height of the subtree rooted at Position p.
        
        :param p: The Position object that we want to know the height of the subtree rooted at it.
        :return: 0 if Position p represents does not have any children, else the height of the subtree rooted at Position p.
        """
        # If Position p is the leaf, the height of the subtree rooted at leaf is 0;
        # otherwise, return 1 + maximum height of the children
        if self.is_leaf(p):
            return 0
        else:
            return 1 + max(self._height(c) for c in self.children(p))

    def height(self, p=None):
        """
        Return the height of the subtree rooted at Position p. If p is None, return the height of the entire tree.
        
        :param p: The Position object that we want to know the height of the subtree rooted at it. (Default : None)
        :return: The height of the subtree rooted at Position p. If p is None, return the height of the entire tree.
        """
        # If 'p' is None (Default), p is the root of the tree;
        if p is None:
            p = self.root()
        return self._height(p)                # start _height2 recursion

    def __iter__(self):
        """
        Generate an iteration of the tree's elements.
        
        :return: The iteration of the tree's elements.
        """
        for p in self.positions():     # use same order as positions()
            yield p.element()          # but yield each element

    def positions(self):
        """
        Generate an iteration of the tree's positions.
        
        :return: The iteration of the tree's positions.
        """
        return self.preorder()         # return entire preorder iteration

    def preorder(self):
        """
        Generate a preorder iteration of positions in the tree.
        
        :return: The preorder iteration of positions in the tree.
        """
        # if the tree is not empty, start the preorder recursion;
        if not self.is_empty():
            for p in self._subtree_preorder(self.root()):    # start recursion
                yield p

    def _subtree_preorder(self, p):
        """
        Generate a preorder iteration of positions in subtree rooted at p.
        
        :param p: The Position object represents the root of subtree.
        :return: The preorder iteration of positions in subtree rooted at p.
        """
        yield p                       # visit p before its subtrees
        for c in self.children(p):                 # for each child c
            for other in self._subtree_preorder(c):              # do preorder of c's subtree
                yield other                                               # yielding each to our caller

    def postorder(self):
        """
        Generate a postorder iteration of positions in the tree.
        
        :return: The postorder iteration of positions in the tree.
        """
        # if the tree is not empty, start the postorder recursion;
        if not self.is_empty():
            for p in self._subtree_postorder(self.root()):    # start recursion
                yield p

    def _subtree_postorder(self, p):
        """
        Generate a postorder iteration of positions in subtree rooted at p.
        
        :param p: The Position object represents the root of subtree.
        :return: The postorder iteration of positions in subtree rooted at p.
        """
        for c in self.children(p):       # for each child c
            for other in self._subtree_postorder(c):  # do postorder of c's subtree
                yield other      # yielding each to our caller
        yield p             # visit p after its subtrees
        
    def levelorder(self):
        """
        Generate a levelorder iteration of positions in the tree.
        
        :return: The levelorder iteration of positions in the tree.
        """
        """The running time of this level-order traversal should be O(n) """
        # HOMEWORK 2-1.
        # if the tree is not empty, yield the levelorder iteration
        if not self.is_empty():
            p = self.root()              # starts from the root
            yield p                      # visit p before its lower level.
            child_list = [p]             # store the current Position
            while child_list != []:      # do visit while the child_list is not empty
                p = child_list[0]        # current Position is the first element of the list
                child_list.remove(p)     # remove the current Position from the list
                for c in self.children(p):
                    yield c              # yield children of the Position p
                    child_list.append(c) # append the children of the Position p into the child_list and repeat until the child_list is empty.
                
                        
                        
                