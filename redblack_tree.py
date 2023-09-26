class RedBlackTree():
    # Node class - DO NOT MODIFY
    class _Node:
        RED = object()
        BLACK = object()
        """Lightweight, nonpublic class for storing a node."""
        __slots__ = '_element', '_parent', '_left', '_right', '_color' # streamline memory usage

        def __init__(self, element, parent=None, left=None, right=None, color=RED):
            self._element = element
            self._parent = parent
            self._left = left
            self._right = right
            self._color = color

    def __init__(self):
        """Create an initially empty binary tree."""
        self._root = None
        self._size = 0

    def __len__(self):
        return self._size

    # Search for the element in the red-black tree.
    # return: _Node object, or None if it's non-existing
    def search(self, element):
        ## IMPLEMENT
        """ 
        Return element of the found node if element exist, None if it's non-existing in the red-black tree.
        
        :param element: The element to be found (or not found if not existed) in the redblack tree 
        """
        node = self._root
        count = self._size
        for i in range(count):
            if (node._element == element):       # searching success -> return element
                return node._element
            elif (node._element > element):      # searching element is smaller than node's -> go to left
                if (node._left == None):         # Left child is not available : No matching -> return None
                    return None
                else:                            # Left child is available
                    node = node._left            # go to left
                    count = count/2
            else:                                # searching element is bigger than node's -> go to right
                if (node._right == None):        # Right child is not available : No matching -> return None
                    return None
                else:                            # Right child is available
                    node = node._right           # go to right
                    count = count/2

    def insert(self, element):
        ## IMPLEMENT
        """
        Add the element into the tree correctly, maintaining the red-black tree properties.
        
        :param element: The element to be inserted
        """
        if (self._root == None):                     # Add the element as the root
            self._root = self._Node(element, parent = None, left = None, right = None, color = self._Node.BLACK)
            self._size += 1
        else:
            node = self._root
            new_node = node
            count = self._size
            for i in range(count):
                if (node._element > element):        # inserted element is smaller than node's -> go to left
                    if (node._left != None):         # Left child is available
                        node = node._left            # go to left
                        count = count/2
                    else:                            # Left child is not available (emtpy node) -> insertion
                        self._size += 1
                        new_node = self._Node(element, parent = node, left = None, right = None, color = self._Node.RED)
                        node._left = new_node        # Should be recolored or reconstructed (case)
                        break
                else:                                # inserted element is bigger than node's -> go to right
                    if (node._right != None):        # Right childe is available
                        node = node._right           # go to right
                        count = count/2
                    else:                            # Right child is not available (empty node) -> insertion
                        self._size += 1
                        new_node = self._Node(element, parent = node, left = None, right = None, color = self._Node.RED)
                        node._right = new_node       # Should be recolored or reconstructed (case)
                        break
            
            # Double red
            while (new_node._parent != self._root):
                if (self._is_black(new_node) != True) and (self._is_black(new_node._parent) != True): # Double red
                    sibiling = self._sibiling(new_node._parent)
                    
                    # case 1) Sibiling of new node's parent is black : No overflow -> Reconstructuring
                    if (self._is_black(sibiling)):
                        self._reconstruct(new_node)
                        
                    # case 2) Sibiling of new node's parent is red : Overflow -> Recoloring
                    elif (self._is_black(sibiling) is False):
                        self._recoloring(new_node)
                        
                if (new_node._parent != None):
                    new_node = new_node._parent
                else:
                    break
                    

                

    def delete(self, element):
        ## IMPLEMENT
        """
        Remove the specified element from the tree while correctly maintaining the red-black tree properties.
        Return element of removed node if item was found and deleted, otherwise return None
        
        :param element: The element to be deleted
        """
        if self.search(element) is None:                 # Element does not exist - return None
            return None
        else:                                            # Element does exist - return Element
            # 1. Find the node to be deleted
            node = self._root
            count = self._size
            
            if self._size == 1:                          # Delete the tree
                self._root = None
                self._size = 0
                return self.search(element)
            
            for i in range(count):
                if (node._element > element):            # element to be deleted is smaller than node's -> go to left, keep searching
                    node = node._left
                    count = count/2
                elif (node._element < element):          # element to be deleted is bigger than node's -> go to right, keep searching
                    node = node._right
                    count = count/2
                else:                                    # node found
                    break
            
            # 2. Delete the node
            successor = self._successor(node)            # node's successor (possibly None)
            z = node._parent
            y = self._sibiling(node)
            
            if successor is not None: 
                z = successor._parent                    # z (check point of double black root)
                y = self._sibiling(successor)            # y (check point of double black sibiling)
                
                isChild = False                        
                if z is node:
                    isChild = True                       # successor is child of node
                
                # a) relink successor and node's children
                twoChild = False                         # node has 2 children, and successor has a right child -> need to link successor's child and parent
                if (node._left is not None and node._right is not None) and (successor._right is not None):
                    twoChild = True
                    if successor._parent._left is successor:
                        successor._parent._left = successor._right
                        successor._right._parent = successor._parent
                    elif successor._parent._right is successor:
                        successor._parent._right = successor._right
                        successor._right._parent = successor._parent
                    
                if successor is not node._left:
                    self._relink(successor, node._left, 1)
                if successor is not node._right:
                    self._relink(successor, node._right, 0)
                successor._color = node._color           # change successor's color
                
                # b) relink node's parent and successor
                if successor._parent._left is successor and twoChild is False: # successor's parent release successor
                    successor._parent._left = None
                elif successor._parent._right is successor and twoChild is False:
                    successor._parent._right = None
                
                if node is not self._root:               # case 1: deleting node that is not root -> relink successor and node's parent and successor
                    self._relink(node._parent, successor, node == node._parent._left)
                else:                                    # case 2: deleting root -> no parents to relink. set the root
                    self._root = successor
                    self._root._parent = None
                    #self._relink(successor._parent, successor._right, successor._parent._left == successor)
                
                # c) update z, y (check point of double black)
                if isChild:            # y is successor's sibiling before relink if successor is child of node
                    z = successor

            else:
                z = node._parent                         # if successor is None, z is old node's parent
                y = self._sibiling(node)                 # y is old node's sibiling
                if node is not self._root:
                    if node is node._parent._left:
                        node._parent._left = None
                    else:
                        node._parent._right = None
                    
            #node._element = None
            #node._color = None
            #node._left = None
            #node._right = None
            #node._parent = None
            self._size -= 1
            
            # c) Double black remedy
            if z is not None:
                lh = self._blackHeight(z._left)
                rh = self._blackHeight(z._right)
                if lh != rh:                                # Double Black occurs
                    self._remedy(z, y)
     
            return self.search(element)
        

    # BONUS FUNCTIONS -- use them freely if you want
    def _is_black(self, node):
        return node == None or node._color == self._Node.BLACK

    def _successor(self, node):
        successor = node._right
        if successor is not None:
            while successor._left != None:
                successor = successor._left
        else:
            if node._left is None:
                successor = None
            else:
                successor = node._left
        return successor

    def _sibiling(self, node):
        if node is not None and node is not self._root:
            parent = node._parent
            if parent._left == node:
                return parent._right
            else:
                return parent._left
        else:
            return None
        
    # ADDITIONAL FUNCTIONS -- The functions added for maintaining the red black tree properties
    def _relink(self, parent, child, mlc):      # mlc : make_left_child. make left child if mlc = 1, otherwise make right child
        """ Relink parent node with child node (Child possibly None) """
        if mlc:                                 # make it a left child
            parent._left = child
        else:                                   # make it a right child
            parent._right = child
        if child is not None:                   # make child point to parent
            child._parent = parent
            
    def _rotate(self, node):
        """ rotates x and y including the transfer of middle subtree """
        x = node
        y = x._parent
        z = y._parent                           # grandparent (possibly None)
        if z is None:
            self._root = x
            x._parent = None                    # x becomes root
        else:
            self._relink(z, x, y == z._left)    # x becomes a direct child of z
        
        # rotation (x and y, including transfer of middle subtree)
        if x == y._left:                        # x is left child of y -> switch x's right subtree and y, x's right subtree becomes y's left child)
            self._relink(y, x._right, True)     # x._right becomes left child of y (transfer right subtree of x to y's left child)
            self._relink(x, y, False)           # y becomes right child of x
        else:                                   # x is right child of y -> switch x's left subtree and y, x's left subtree becomes y's right child)
            self._relink(y, x._left, False)     # x._left becomes right child of y (transfer left subtree of x to y's right child)
            self._relink(x, y, True)            # y becomes left child of x
            
    def _reconstruct(self, x):
        """ Performs trinode restructure of node x with parent / grandparent """
        y = x._parent
        z = y._parent
        x_color = x._color
        y_color = y._color
        z_color = z._color
        if (x == y._right) == (y == z._right):  # right-right, left-left
            self._rotate(y)                     # single rotation
            y._color = z_color
            z._color = y_color
            return y                          
        else:                                   # right-left, left-right
            self._rotate(x)                     # double rotation
            self._rotate(x)
            x._color = z_color
            z._color = x_color
            return x
        
    def _recoloring(self, x):
        """ Recolors the node when there are Double reds """
        y = x._parent
        z = y._parent
        sibiling = self._sibiling(y)
        
        if (z == self._root):                   # if z is root, color all BLACK
            z._color = self._Node.BLACK
            y._color = self._Node.BLACK
            sibiling._color = self._Node.BLACK
            cnt = 1
        else:                                   # if x is not root, color z RED and others to BLACK
            z._color = self._Node.RED
            y._color = self._Node.BLACK
            sibiling._color = self._Node.BLACK
    
    def _blackHeight(self, node):
        """ returns the black height of the given node """ 
        if node is None:
            return 1
        
        height = self._blackHeight(node._left)
        
        if node._color == self._Node.BLACK:
            return height + 1
        else:
            return height
    
    def _remedy(self, z, y):
        """ Resolve double black at z, where y is the root of z's heavier subtree (z possibly None) """
        # Case 1, 2 : y is black
        if self._is_black(y):
            x = y                                             # x is the red child of y (will be updated below)
            if y is not None and (self._is_black(y._left) != True):  # Left child is red
                x = y._left
            elif y is not None and (self._is_black(y._right) != True):  # Right child is red
                x = y._right
            elif y is None or ((y._right is None or self._is_black(y._right)) and (y._left is None or self._is_black(y._left))): # y only has black children
                x = None
            else:                                             # y only has red children
                x = y._right                                  # (or x can be the left child of y)
            
            # Case 1) y is black and has at least one red child x : Transfer (Reconstruct)
            if x is not None:
                color_old = self._Node.RED
                if (z is not None):
                    color_old = z._color
                middle = self._reconstruct(x)
                middle._color = color_old                     # set middle's color to the old color of z
                if middle._left is not None:
                    middle._left._color = self._Node.BLACK        # set middle's children to black
                if middle._right is not None:
                    middle._right._color = self._Node.BLACK      
            # Case 2) y is black and has only black children : Fusion (Recolor)
            elif y is not None and self._is_black(y) and x is None:
                y._color = self._Node.RED
                if z is not None and self._is_black(z) is False:
                    z._color = self._Node.BLACK               # Problem resolved (No propagation)
                elif z is not None and z != self._root:
                    self._remedy(z._parent, self._sibiling(z)) # Recursion
        
        # Case 3) y is red : rotate trinode and repeat case 1 or 2
        elif self._is_black(y) is not True and z is not None: 
            self._rotate(y)
            y._color = self._Node.BLACK
            z._color = self._Node.RED
            if z == y._right:                                 # Repeate remedy
                self._remedy(z, z._left)
            else:
                self._remedy(z, z._right)

    # Supporting functions -- DO NOT MODIFY BELOW
    def display(self):
        print('--------------')
        self._display(self._root, 0)
        print('--------------')

    def _display(self, node, depth):
        if node == None:
            return

        if node._right != None:
            if node._right._parent != node:
                print("parent-child error - ", node._element, node._right._element)
            self._display(node._right, depth+1)

        if node == self._root:
            symbol = '>'
        else:
            symbol = '*'

        if node._color == self._Node.RED:
            colorstr = 'R'
        else:
            colorstr = 'B'
        print(f'{"    "*depth}{symbol} {node._element}({colorstr})')
        if node._left != None:
            if node._left._parent != node:
                print("parent error - ", node._element, node._left._element)
            self._display(node._left, depth+1)

    def inorder_traverse(self):
        return self._inorder_traverse(self._root)

    def _inorder_traverse(self, node):
        if node == None:
            return []
        else:
            return self._inorder_traverse(node._left) + [node._element] + self._inorder_traverse(node._right)

    def check_tree_property_silent(self):
        if self._root == None:
            return True

        if not self._check_parent_child_link(self._root):
            print('Parent-child link is violated')
            return False
        if not self._check_binary_search_tree_property(self._root):
            print('Binary search tree property is violated')
            return False
        if not self._root._color == self._Node.BLACK:
            print('Root black property is violated')
            return False
        if not self._check_double_red_property(self._root):
            print('Internal property is violated')
            return False
        if self._check_black_height_property(self._root) == 0:
            print('Black height property is violated')
            return False
        return True

    def check_tree_property(self):
        if self._root == None:
            print('Empty tree')
            return

        print('Checking binary search tree property...')
        self._check_parent_child_link(self._root)
        self._check_binary_search_tree_property(self._root)
        print('Done')

        print('Checking root black property...')
        print(self._root._color == self._Node.BLACK)
        print('Done')

        print('Checking internal property (=no double red)...')
        self._check_double_red_property(self._root)
        print('Done')

        print('Checking black height property...')
        self._check_black_height_property(self._root)
        print('Done')

    def _check_parent_child_link(self, node):
        if node == None:
            return True

        test_pass = True

        if node._right != None:
            if node._right._parent != node:
                print("parent-child error - ", node._element, node._right._element)
            test_pass = test_pass and self._check_parent_child_link(node._right)
        if node._left != None:
            if node._left._parent != node:
                print("parent error - ", node._element, node._left._element)
            test_pass = test_pass and self._check_parent_child_link(node._left)

        return test_pass

    def _check_binary_search_tree_property(self, node):
        if node == None:
            return True

        test_pass = True

        if node._left != None:
            if node._left._element > node._element:
                print("Binary search tree property error - ", node._element, node._left._element)
                return False
            test_pass = test_pass and self._check_binary_search_tree_property(node._left)

        if node._right != None:
            if node._right._element < node._element:
                print("Binary search tree property error - ", node._element, node._right._element)
                return False
            test_pass = test_pass and self._check_binary_search_tree_property(node._right)

        return test_pass

    def _check_double_red_property(self, node):
        if node == None:
            return True

        test_pass = True

        if node._color == self._Node.RED:
            if node._left != None:
                if node._left._color == self._Node.RED:
                    print("Double red property error - ", node._element, node._left._element)
                    return False
            if node._right != None:
                if node._right._color == self._Node.RED:
                    print("Double red property error - ", node._element, node._right._element)
                    return False

        if node._left != None:
            test_pass = test_pass and self._check_double_red_property(node._left)
        if node._right != None:
            test_pass = test_pass and self._check_double_red_property(node._right)

        return test_pass


    def _check_black_height_property(self, node):
        if node == None:
            return 1

        left_height = self._check_black_height_property(node._left)
        right_height = self._check_black_height_property(node._right)

        if left_height != right_height:
            print("Black height property error - ", node._element, left_height, right_height)
            return 0

        if node._color == self._Node.BLACK:
            return left_height + 1
        else:
            return left_height