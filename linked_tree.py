from tree import Tree

class LinkedTree(Tree):
    """Linked representation of a general tree structure."""

    #-------------------------- nested _Node class --------------------------
    class _Node:
        """Lightweight, nonpublic class for storing a node."""
        __slots__ = '_element', '_parent', '_children' # streamline memory usage

        def __init__(self, element, parent=None, children=None):
            """
            Initialize a new node object with the given element, parent, and children.

            :param element: The element to be stored in the node
            :param parent: A reference to the parent node (default: None)
            :param children: A list of references to the children nodes (default: None)
            """
            self._element = element # the element of this node
            self._parent = parent # a link towards the parent
            # If 'children' is None, initialize an empty list for children nodes;
            # otherwise, use the provided list of children nodes
            if children == None:
                self._children = []
            else:
                self._children = children # list of links towards children nodes

    #-------------------------- nested Position class --------------------------
    class Position(Tree.Position):
        """An abstraction representing the location of a single element."""

        def __init__(self, container, node):
            """
            Constructor should not be invoked by user.
            
            :param container: The reference to the container. It contains the node in particular position (location).
            :param node: A reference to the node for the Position.
            """
            self._container = container # the container of this Position
            self._node = node # the node which has this Position

        def element(self):
            """
            Return the element stored at this Position.
            
            :return: The element stored in the node at the position.
            """
            return self._node._element # return the element of the node

        def __eq__(self, other):
            """
            Return True if other is a Position representing the same location.
            
            :return: True if the type of other and self is same, and also the node of other and self is same. Otherwise, False.
            """
            return type(other) is type(self) and other._node is self._node # return True only if the other is a Position representing the same location with self.

    #------------------------------- utility methods -------------------------------
    def _validate(self, p):
        """
        Return associated node, if position is valid.
        
        :param p: The Position of the node to be validate.
        :return: The node associated with the given valid position.
        :raises TypeError: if the type of p is not the Position type, a TypeError raised with the message 'p must be proper Position type'
        :raises ValueError: if p doesn't belong to the container, a ValueError raised with the message 'p does not belong to this container'. of if p's parent is p, the p is not valid so a ValueError raised with the message 'p is no longer valid'
        """
        # If Position p is not the Position type, raises TypeError;
        # If Position p's container doesn't belong to self, raises ValueError;
        # If Position p's parent is position p (which means p is not valid anymore), raise ValueError;
        # otherwise, return p's node
        if not isinstance(p, self.Position):
            raise TypeError('p must be proper Position type')
        if p._container is not self:
            raise ValueError('p does not belong to this container')
        if p._node._parent is p._node:            # convention for deprecated nodes
            raise ValueError('p is no longer valid')
        return p._node

    def _make_position(self, node):
        """
        Return Position instance for given node (or None if no node).
        
        :param node: A reference node for the Position.
        :return: The Position of the given node if it is not None. (None if the node is None)
        """
        return self.Position(self, node) if node is not None else None # return the Position that has reference node if node is not None, otherwise return None

    #-------------------------- Tree constructor --------------------------
    def __init__(self):
        """Create an initially empty binary tree."""
        self._root = None # The root of this tree
        self._size = 0 # The element of the tree (Default : 0, since the tree is empty)

    #-------------------------- public accessors --------------------------    
    def root(self):
        """
        Return the root Position of the tree (or None if tree is empty).
        
        :return: The Position of the root of the tree (None if the tree is empty)
        """
        return self._make_position(self._root) # return the Position of the root of the tree if tree is empty, otherwise return None

    def parent(self, p):
        """
        Return the Position of p's parent (or None if p is root).
        
        :param p: The Position object representing the child of parent node.
        :return: The Position of p's parent.
        """
        node = self._validate(p) # The node that associated with Position p
        return self._make_position(node._parent) # return the node's parent Position

    def num_children(self, p):
        """
        Return the number of children that Position p has.
        
        :param p: The Position object representing the parent of the children to be counted.
        :return: The number of the children of Position p. (The length of the list of children of node for position p)
        """
        node = self._validate(p) # The node that associated with Position p
        return len(node._children) # return the number of the elements in children list
    
    def children(self, p):
        """
        Generate an iteration of Positions representing p's children.
        
        :param p: The Position object representing the parent of the children.
        :return: The iteration of the p's children Position object.
        """
        node = self._validate(p) # The node that associated with Position p
        for child in node._children:
            yield self._make_position(child) # generates an iteration of Positions of p's children

    def __len__(self):
        """
        Return the total number of elements in the tree.
        
        :return: The total number of the elements in the tree.
        """
        return self._size    # return the total number of elements in the tree
    
    #-------------------------- nonpublic mutators --------------------------
    def _add_root(self, e):
        """
        This method places element 'e' at the root of an empty tree and returns the new Position.
        (use self._make_position(node) to pack the Node object into a position.)
        If the tree is not empty, it raises a ValueError with the message 'Root exists'.
        
        :param e: The element to be placed at the root of the tree
        :return: A new Position object representing the root node with the element 'e'
        :raises ValueError: If the tree is not empty, a ValueError is raised with the message 'Root exists'
        """
        # If 'root' is not None, raise ValueError;
        # otherwise, modify the size from 0 to 1, and initialize the root with the node that has e as its element.
        if self._root is not None:
            raise ValueError('Root exists')
        self._size = 1 # since there's only 1 node in the tree (only root), the size is 1.
        self._root = self._Node(e) # initialize the root with the node that has e as its element
        return self._make_position(self._root) # return the Position of the root of the tree.

    def _add_child(self, p, e):
        """
        This method creates a new child node for the given Position 'p' and stores the element 'e'.
        (use self._validate(position) to unpack the node inside the position.)
        It returns the Position of the newly created node (use self._make_position(new_node)).
        
        :param p: The Position object representing the parent node
        :param e: The element to be stored in the new child node
        :return: A new Position object representing the child node with the element 'e'
        """
        node = self._validate(p) # The node that associated with Position p
        self._size += 1 # add 1 to the size, since the 1 child node is added into the tree.
        child = node._children # the children list of the node
        child.append(self._Node(e, node)) # add new children node into the children list of its parent node
        # In the children list, pick the new children node and return its Position.
        for c in child:
            if c._element == e:
                return self._make_position(c)

    def _replace(self, p, e):
        """
        This method replaces the element at the given Position 'p' with the new element 'e'.
        It returns the old element that was replaced.
        
        :param p: The Position object representing the node whose element will be replaced
        :param e: The new element to replace the current element at position 'p'
        :return: The old element that was replaced at position 'p'
        """        
        node = self._validate(p) # The node that associated with Position p
        old_element = node._element # store the element into the old_element
        node._element = e # set the node's element to new element e (replace)
        return old_element # return the old element before replacing

    def _delete(self, p):
        """
        This method deletes the node at the given Position 'p' and returns the element that had been stored at Position 'p'.

        If the position 'p' has any children, a ValueError is raised.

        :param p: The Position object representing the node to be deleted
        :return: The element that was stored at the deleted position 'p'
        :raises ValueError: If the position 'p' has any children, a ValueError is raised
        """
        node = self._validate(p) # The node that associated with Position p
        # If 'num_children(p)' is not 0, raise ValueError;
        # If the Position p is the root of the tree, set root to None and decrease 1 from the tree size
        # If the root is None (when we access this function again after deleting the root), set the size to 0
        # otherwise, remove node element from the parent's children lis and decrease 1 from the tree size as one node is removed.
        if self.num_children(p) != 0:
            raise ValueError('The position has the children')
        if self.is_root(p):
            self._root = None
            self._size -= 1
        if self._root is None:
            self.size = 0
        else:
            parent = node._parent # the parent of the node
            for child in parent._children:
                if child._element == node._element: 
                    parent._children.remove(child) # remove the child node from the children list if the child node's element is same with the node element (which is going to be removed)
            self._size -= 1 
        return node._element # return the removed element
    
    