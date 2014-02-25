import os
import math
import sys
import time

# References :- https://www.cs.umd.edu/users/meesh/420/Notes/MountNotes/lecture17-quadkd.pdf




class Node:
    def __init__(self, x, y, val):
        self.x = float(x);
        self.y = float(y);
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
        inserted_flag = False;
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
                    inserted_flag = True;
                else:
                    inserted_flag = True;
                    self.__list__.insert(ele_count, {'distance': dist, 'val': node.val, 'x': node.x, 'y': node.y});
                    break;
        if not inserted_flag:
            self.__list__.append({'distance': dist, 'val': node.val, 'x': node.x, 'y': node.y});
        # If list size grows beyond boundary remove 
        while len(self.__list__) > self.k:
            del self.__list__[-1];
        return;

    def list_values(self, merge_dsitance = None):
        # The values are joined to form a smaller list which will have all the entries from each val and the val will be sorted in themselves
        # sorted may be slow may need speed up here # Check Profiler results
        # We are also merge_distance query
        result_val = [];
        if merge_distance != None:
            element_length  = len(self.__list__);
            pos = 0;
            while pos < element_length -1:
                entry = self.__list__[pos];
                next_entry = self.__list__[pos+1];
                if distance_between_points(entry['x'], entry['y'], next_entry['x'], next_entry['y']) < merge_distance:
                    temp = entry['val'].extend(next_entry['val']);
                    result.extend(sorted(temp, reverse=True));
                    pos += 2;
                else:
                    result.extend(sorted(entry['val'], reverse=True));
                    pos += 1;
        else:
            result_val = [str(entry) for entries in self.__list__ for entry in sorted(entries['val'], reverse= True)];
        return result_val;

    def list_values_unsorted(self, merge_distance = None):
        # Unsorted
        result_val = [];
        if merge_distance != None:
            element_length  = len(self.__list__);
            pos = 0;
            while pos < element_length -1:
                entry = self.__list__[pos];
                next_entry = self.__list__[pos+1];
                if distance_between_points(entry['x'], entry['y'], next_entry['x'], next_entry['y']) < merge_distance:
                    temp = entry['val'].extend(next_entry['val']);
                    result.append(temp);
                    pos += 2;
                else:
                    result.append(entry['val']);
                    pos += 1;
        return result_val;

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



inf = sys.stdin;
(topic_count, question_count, query_count) = map(int, inf.readline().split());
mytree = TwodTree();
# Tree Creation Completed
# Topic Id hash
topic_question_hash = {};
while topic_count > 0:
    # May reduce function chain by making inf.readline a single entry
    (topic_id, latitude, longitude) = inf.readline().split();
    mytree.insert_node(Node(float(latitude), float(longitude), int(topic_id)));
    topic_count -= 1;
    # May change this to hash
    topic_question_hash[topic_id] = [];
while question_count > 0:
    question_line_list = inf.readline().split();
    # Based on python 2.3+ map function implementation
    question_id = int(question_line_list[0]);
    map(lambda x: topic_question_hash[x].append(question_id), question_line_list[2:]);
    question_count -= 1;
# Time to start answering queries
while query_count > 0:
    (q_type, q_count, latitude, longitude) = inf.readline().split();
    # In both cases we get the top K topics
    q_node = Node(float(latitude), float(longitude), -1);
    q_count = int(q_count);
    close_list = mytree.find_k_nearest_neighbour(q_node, q_count);
    # Change it to a join later
    if q_type == 't':
        topic_list = close_list.list_values(0.001);
        # This is the nice case
        print " ".join(topic_list[:q_count]);
    else:
        # FIXME:- There is a impending failure which not sure how to escape
        # if we get k topics into less Than k question
        seen = set();
        seen_add = seen.add;
        topic_list_unsorted = close_list.list_values_unsorted(0.001);
        question_list_unsorted = [[question for entry in entries for question in topic_question_hash[str(entry)]] for entries in topic_list_unsorted];
        question_list = [str(entry) for entries in question_list_unsorted for entry in sorted(entries, reverse = True)];
        unique_question = [ x for x in question_list if x not in seen and not seen_add(x)];
        print " ".join(unique_question);
    query_count -= 1;
        
