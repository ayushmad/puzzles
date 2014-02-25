import os
import math
import sys
import time

# References :- https://www.cs.umd.edu/users/meesh/420/Notes/MountNotes/lecture17-quadkd.pdf




class Node:
    def __init__(self, x, y, val):
        self.x = x;
        self.y = y;
        self.val = [val];
        self.left = None;
        self.right = None;
        return;

    def __str__(self):
        return(str(self.x) + ','  +str(self.y));

# FIXME:- don't use square root
def distance_between_points(x1, y1, x2, y2):
    return pow(pow((x1-x2), 2) + pow((y1-y2), 2), 0.5);

# Tree Root maintained as global
class TwodTree:
    def __init__(self):
        self.tree = None;
        self.dimension = 2;
        return;

    def insert_node(self, node):
        # should check Type of object as Node 
        # but not done due to speed requirements
        self.tree = self.insert_into_tree_iterative(self.tree, node);
        return;

    def insert_into_tree(self, root, node, level):
        # Base case 
        if root == None:
            return node;
        # Level based comparison
        # Hard Coded to optimize
        if root.x == node.x  and root.y == node.y:
            #Special case in our case
            root.val.extend(node.val)
            return root;
        # NOTE:- Check if / is faster or % is faster
        if level%2 == 0:
            if root.x > node.x:
                root.left = self.insert_into_tree(root.left, node, level+1);
            else:
                root.right = self.insert_into_tree(root.right, node, level+1);
        else:
            if root.y > node.y:
                root.left = self.insert_into_tree(root.left, node, level+1);
            else:
                root.right = self.insert_into_tree(root.right, node, level+1);
        return root;

    def insert_into_tree_iterative(self, root, node):
        if root == None:
            return node;
        level = 0;
        base_tree = root;
        parent = root;
        left_branch = False;
        needs_extension = 0;
        while root != None:
            if root.x == node.x and root.y == node.y:
                needs_extension = True;
                break;
            if level%2 == 0:
                if root.x > node.x:
                    parent = root;
                    root = root.left;
                    left_branch = True;
                else:
                    parent = root;
                    root = root.right;
                    left_branch = False;
            else:
                if root.y > node.y:
                    parent = root;
                    root = root.left;
                    left_branch = True;
                else:
                    parent = root;
                    root = root.right;
                    left_branch = False;
            level += 1;
        if needs_extension:
            root.val.extend(node.val);
        elif left_branch:
            parent.left = node;
        else:
            parent.right = node;
        return base_tree;

    def find_k_nearest_neighbour(self, query_node, k):
        close_list = MinList(k);
        self.fnn_k(self.tree, query_node, Rect(), 0, close_list);
        return close_list;

    def fnn_k(self, root, query_node, node_rect, level, close_list):
        if root == None:
            return;
        max_closest_distance = close_list.max_dist();
        if node_rect.distance_from_point(query_node) > max_closest_distance:
            return;
        else:
            # Checking with respect to root
            q_dist = distance_between_points(root.x, root.y, query_node.x, query_node.y)
            if q_dist < max_closest_distance:
                close_list.add_close_node(root, q_dist);
            if level%2 == 0:
                if root.x > query_node.x:
                    self.fnn_k(root.left, 
                        query_node, 
                        node_rect.trim_left(level, root), 
                        level + 1,
                        close_list);
                    self.fnn_k(root.right, 
                        query_node, 
                        node_rect.trim_right(level, root), 
                        level + 1,
                        close_list);
                else:
                    self.fnn_k(root.right, 
                        query_node, 
                        node_rect.trim_right(level, root), 
                        level + 1,
                        close_list);
                    self.fnn_k(root.left, 
                        query_node, 
                        node_rect.trim_left(level, root), 
                        level + 1,
                        close_list);
            else:
                if root.y > query_node.y:
                    self.fnn_k(root.left, 
                        query_node, 
                        node_rect.trim_left(level, root), 
                        level + 1,
                        close_list);
                    self.fnn_k(root.right, 
                        query_node, 
                        node_rect.trim_right(level, root), 
                        level + 1,
                        close_list);
                else:
                    self.fnn_k(root.right, 
                        query_node, 
                        node_rect.trim_right(level, root), 
                        level + 1,
                        close_list);
                    self.fnn_k(root.left, 
                        query_node, 
                        node_rect.trim_left(level, root), 
                        level + 1,
                        close_list);
        return;

         
class MinList:
    def __init__(self, k):
        self.__list__ = [];
        self.k = k;
        return;

    def min(self):
        if len(self.__list__) == 0:
            raise ValueError
        return self.__list__[0];

    def max_dist(self):
        if len(self.__list__) == self.k:
            # This is clear ties with the nodes
            return self.__list__[self.k-1]['distance'] + 0.001;
        else:
            return float('inf');

    def add_close_node(self, node, dist):
        # max_case is dealt as a special case
        # Only in case if max entry do we add in between
        if len(self.__list__) == 0:
            self.__list__.append({'distance':dist ,'val': node.val, 'x': node.x, 'y': node.y});
            return;
        for ele_count in xrange(0, len(self.__list__)):
            if self.__list__[ele_count]['distance'] > dist:
                # This is were we insert the node
                # Resolve conflict in this case
                if ele_count == self.k - 1 and abs(self.__list__[ele_count]['distance'] - dist) < 0.001:
                    # This is the last entry
                    # Keep the smaller one with topics
                    self.__list__[ele_count]['val'].extend(node.val);
                else:
                    self.__list__.insert(ele_count, {'distance': dist, 'val': node.val, 'x': node.x, 'y': node.y});
                    break;
        # If list size grows beyond boundary remove 
        while len(self.__list__) > self.k:
            del self.__list__[-1];
        return;

    def __str__(self):
        result_str = "";
        for element in self.__list__:
            result_str += str(element['x']) + "," + str(element['y']);
        return result_str;
       
        

class Rect:
    def __init__(self, left_top = None, right_down = None):
        # Check left_top and top down ordering
        if left_top == None:
            self.left_top = {};
            self.left_top['x'] = float('-inf');
            self.left_top['y'] = float('inf');
        else: 
            self.left_top = left_top;
        if right_down == None:
            self.right_down = {};
            self.right_down['x'] = float('inf');
            self.right_down['y'] = float('-inf');
        else:
            self.right_down = right_down;
        return;
    
    def distance_from_point(self, point):
        if self.left_top['x'] <= point.x and self.left_top['y'] >= point.y and self.right_down['x'] >= point.x and self.right_down['y'] <= point.y:
            return 0;
        elif self.left_top['x'] <= point.x and self.right_down['x'] >= point.x:
            # This is inside x face
            return min(abs(self.left_top['y'] - point.y), abs(self.right_down['y'] - point.y));
        elif self.left_top['y'] >= point.y and self.right_down['y'] <= point.y:
            # This is inside y face
            return min(abs(self.left_top['x'] - point.x), abs(self.right_down['x'] - point.x));
        else:
            # This is based on the triangle
            if point.x < self.left_top['x']:
                if point.y > self.left_top['y']:
                    return distance_between_points(point.x, point.y, self.left_top['x'], self.left_top['y']);
                else:
                    return distance_between_points(point.x, point.y, self.left_top['x'], self.right_down['y']);
            else:
                if point.y > self.left_top['y']:
                    return distance_between_points(point.x, point.y, self.right_down['x'], self.left_top['y']);
                else:
                    return distance_between_points(point.x, point.y, self.right_down['x'], self.right_down['y']);
        
    def trim_right(self, level, node):
        # Node is assumed to be inside rectangles
        if level%2 == 0:
            return Rect({'x':node.x,'y': self.left_top['y']}, self.right_down);
        else:
            return Rect(self.left_top, {'x': self.right_down['x'], 'y': node.y});
    
    def trim_left(self, level, node):
        # Node is assumed to be inside rectangles
        if level%2 == 0:
            return Rect(self.left_top, {'x': node.x, 'y': self.right_down['y']});
        else:
            return Rect({'x': self.left_top['x'], 'y': node.y}, self.right_down);

    def __str__(self):
        return str(self.left_top['x']) + "," + str(self.left_top['y']) + "," + str(self.right_down['x']) + "," + str(self.right_down['y']);




if __name__ == "__main__":
    # Test Case file
    test_case_file = open(sys.argv[1], 'r');
    t = TwodTree();
    prev_line = test_case_file.readline();
    for line in test_case_file:
        (px, py) = prev_line.strip().split();
        t.insert_node(Node(float(px), float(py), 1));
        prev_line = line;
    # Last line is the query node
    (px, py) = prev_line.strip().split();
    print t.find_k_nearest_neighbour(Node(int(px), int(py), 1), 5);
