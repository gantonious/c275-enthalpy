import pygame

# Define some colors
BLACK = (0, 0, 0)

class Quadtree:
    """
    ---------
    | 0 | 1 |
    ---------
    | 2 | 3 |
    ---------
    """

    # reducing the max depth of the tree reduces tree build time however, increases
    # the total collisions detection checks that must be conducted ~4 should provide a good
    # middle ground between the two
    MAX_CAPACITY = 1
    MAX_DEPTH = 4
    def __init__(self, x, y, width, height, depth=0):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._depth = depth
        self._children = [] # list of children nodes
        self._contents = [] # list of objects we hold

    def _split(self):
        """
        Splits current node into 4 children nodes
        """
        self._children  = [Quadtree(self._x, self._y, self._width / 2, self._height / 2, self._depth + 1),
                            Quadtree(self._x + self._width / 2, self._y, self._width / 2, self._height / 2, self._depth + 1),
                            Quadtree(self._x, self._y + self._height / 2, self._width / 2, self._height / 2, self._depth + 1),
                            Quadtree(self._x + self._width / 2, self._y + self._height / 2, self._width / 2, self._height / 2, self._depth + 1)]

    def _get_node(self, item):
        """
        Takes in an item and attempts to see if the item fits in any of the parents children
        
        Returns:

        None - item only fits in parent
        index - child index where the item fits
        """

        item_coords = item.get_position()
        node_index = None

        for child in enumerate(self._children):
            if not child[1]:
                continue

            if item_coords[0] > child[1]._x and \
                item_coords[0] + item_coords[2] < child[1]._x + child[1]._width and \
                item_coords[1] > child[1]._y and \
                item_coords[1] + item_coords[3] < child[1]._y + child[1]._height:

                node_index = child[0]
                break

        return node_index

    def insert(self, item):
        """
        Takes in an item and inserts it into the smallest node that contains the item
        """

        if self._children != []:
            # we have children try and store object in there
            index = self._get_node(item)
            
            if index != None:
                self._children[index].insert(item)
                return

        self._contents.append(item)

        if self._children == [] and \
            len(self._contents) > Quadtree.MAX_CAPACITY and \
            self._depth < Quadtree.MAX_DEPTH:

            # full, time to subdivide node
            self._split()

            # dump objects into children
            contents = self._contents
            self._contents = []
            for obj in contents:
                self.insert(obj)

    def get_objects(self, item):
        """
        Gathers all objects that may collide with item by traversing down the
        tree starting at the parent node and collecting all objects in each node the
        item we are checking collisons against fit in, once we hit the smallest child
        that contains the item, grab all the objects its children contains

        Returns: a list containing all objects that have a chance of colliding with "item"
        """

        objects = []

        if self._children != []:
            # we have children lets try and see if item fits in any of them
            index = self._get_node(item)

            if index != None:
                objects += self._children[index].get_objects(item)
            else:
                for child in self._children:
                    objects += child.get_objects(item)

        objects += self._contents

        return objects

    def clear(self):
        """
        Clears Quadtree by dropping all objects in child nodes and dropping all pointers to
        the child nodes
        """
        self._contents = []
        for child in self._children:
            child.clear()
        self._children = []

    def draw_tree(self, screen):
        """
        Draws Quadtree to specified screen
        """
        pygame.draw.rect(screen, BLACK, [self._x, self._y, self._width, self._height], 1)
        for child in self._children:
            child.draw_tree(screen)

