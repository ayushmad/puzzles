import os
import math
import sys
# Utilities 


def distance_between_points(x1, y1, x2, y2):
    return pow(pow((x1-x2), 2) + pow((y1-y2), 2), 0.5);

def find_nearest_topics(location_x, location_y, number_of_topics, return_list = False):
    result_list = MYTREE.find_k_nearest_neighbour(Node({'x': float(location_x),
                                                        'y': float(location_y)},
                                                        -1),
                                                        number_of_topics);
    # After calling some functions I should get a list
    topic_nodes = result_list.get_list();
    count  = 0;
    added_count = 0;
    combined_list = [];
    prev_distance = float('-inf');
    result_line = "";
    while count < len(topic_nodes):
        selected_node = topic_nodes[count]
        if (selected_node['distance'] - prev_distance) > RANGE_BARRIER:
            combined_list.append(selected_node['node'].val);
            prev_distance = selected_node['distance'];
        else:
            combined_list[-1].extend(selected_node['node'].val);
        count += 1;
    if return_list:
        return combined_list;
    count = 0;
    while count < len(combined_list):
            combined_list[count].sort(key = lambda x: int(x),
                                      reverse = True);
            for entry in combined_list[count]:
                if added_count >= number_of_topics:
                    break;
                result_line += str(entry) + " ";
                added_count += 1;
            if added_count >= number_of_topics:
                break;
            count += 1;
    return result_line;
            
def get_questions_for_topics(topic):
    global TOPIC_QUESTION_MAP;
    topic = str(topic);
    if not TOPIC_QUESTION_MAP.has_key(topic):
        return [];
    return TOPIC_QUESTION_MAP[topic];

        
def find_nearest_questions(location_x, location_y, number_of_questions):
    topics_list = find_nearest_topics(location_x, 
                                      location_y,
                                      number_of_questions * MAX_TOPICS_PER_QUESTION,
                                      True);
    unique_hash = {};
    result_line = "";
    resulting_ans = [];
    for topic_group in topics_list:
        questions_in_group = [];
        for topic in topic_group:
            question_list = get_questions_for_topics(topic);
            for question in question_list:
                if unique_hash.has_key(question):
                    continue;
                unique_hash[question] = 1;
                questions_in_group.append(question);
        questions_in_group.sort(key = lambda x: int(x) , reverse = True);
        resulting_ans.extend(questions_in_group);
    return " ".join(resulting_ans[:number_of_questions]) ;




def insert_into_tree(fh, topic_count):
    while topic_count > 0:
        line = fh.readline();
        (topic_id, location_x, location_y) = line.strip().split();
        MYTREE.insert_node(Node({'x': float(location_x), 
                                 'y': float(location_y)}, 
                                 int(topic_id)));
        topic_count -= 1;

def create_question_topic_map(fh, question_count):
    global TOPIC_QUESTION_MAP, MAX_TOPICS_PER_QUESTION;
    while question_count > 0:
        topic_id_list = fh.readline().strip().split();
        question_id = topic_id_list[0];
        topic_id_list = topic_id_list[2:];
        if len(topic_id_list) > MAX_TOPICS_PER_QUESTION:
            MAX_TOPICS_PER_QUESTION = len(topic_id_list);
        for topic in topic_id_list:
            if not TOPIC_QUESTION_MAP.has_key(topic):
                TOPIC_QUESTION_MAP[topic] = [];
            TOPIC_QUESTION_MAP[topic].extend(question_id);
        question_count -= 1;
   
def answer_queries(fh, query_count):
    while query_count > 0:
        line = fh.readline();
    
        (query_type, result_count, loc_x, loc_y) = line.strip().split();
        if query_type == "t":
            print find_nearest_topics(float(loc_x),
                                      float(loc_y),
                                      int(result_count));

        else:
            print find_nearest_questions(float(loc_x),
                                         float(loc_y),
                                         int(result_count));
        query_count -= 1;

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
        close_list = CloseList(k);
        self.fnn_k(self.tree, 
                   query_node, 
                   Rectangle({'x': float('-inf'), 'y': float('inf')},
                             {'x': float('inf'), 'y': float('-inf')}), 
                   0, 
                   close_list);
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
                close_list.update_nearest_node(root, q_dist);
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


class Node:
    def __init__(self, point, val):
        self.x = float(point['x']); 
        self.y = float(point['y']);
        self.val = [val];
        self.right = None;
        self.left = None;
        return;

    def __str__(self):
        return "%f,\t%f"%(self.x,
                          self.y);

    def distance_from_node(self, dest_node):
        return distance_between_points(self.x,
                                       self.y,
                                       dest_node.x,
                                       dest_node.y);

    def get_node_location(self):
        return ({ 'x': self.x, 'y': self.y});

class Rectangle:
    """
        Rectangle is a class associated with the internals of KD tree it is used with respect to the 
        current search space of the current root
    """
    def __init__(self, 
                 left_top_point, 
                 right_bottom_point):
        self.left_top_x = left_top_point['x'];
        self.left_top_y = left_top_point['y'];
        self.right_bottom_x = right_bottom_point['x'];
        self.right_bottom_y = right_bottom_point['y'];
        return;

    def trim_right(self, level, split_location):
        """@todo: Docstring for trim_right

        :level: A int 0 if x and 1 if y
        :split_location: Point hash containing the point for the split
        :returns: @todo

        """
        if level %2 == 0:
            # Need to create a new rectangle
            return Rectangle({'x' : split_location.x, # This is the left top point
                              'y' : self.left_top_y},
                              {'x': self.right_bottom_x, # The right bottom point is same
                               'y': self.right_bottom_y});

        else:
            # Need to create a new rectangle
            return Rectangle({'x' : self.left_top_x, # This is the left top point
                              'y' : self.left_top_y},
                              {'x': self.right_bottom_x, # The right bottom point is same
                               'y': split_location.y});
        
    
    def trim_left(self, level, split_location):
        """@todo: Docstring for trim_left

        :level: A int 0 if x and 1 if y
        :split_location: Point hash containing the point for the split
        :returns: @todo

        """
        if level %2 == 0:
            # Need to create a new rectangle
            return Rectangle({'x' : self.left_top_x, # This is the left top point
                              'y' : self.left_top_y},
                              {'x': split_location.x, # The right bottom point is same
                               'y': self.right_bottom_y});

        else:
            # Need to create a new rectangle
            return Rectangle({'x' : self.left_top_x, # This is the left top point
                              'y' : split_location.y},
                              {'x': self.right_bottom_x, # The right bottom point is same
                               'y': self.right_bottom_y});
    

    def distance_from_point(self, point):
        if (self.left_top_x <= point.x and 
            self.left_top_y >= point.y and 
            self.right_bottom_x >= point.x and 
            self.right_bottom_y <= point.y):
            # Inside the rectangle
            return 0;
        elif self.left_top_x <= point.x and self.right_bottom_x >= point.x:
            # This is inside x face
            return min(abs(self.left_top_y - point.y), abs(self.right_bottom_y - point.y));
        elif self.left_top_y >= point.y and self.right_bottom_y <= point.y:
            # This is inside y face
            return min(abs(self.left_top_x - point.x), abs(self.right_bottom_x - point.x));
        else:
            # This is based on the triangle
            if point.x < self.left_top_x:
                if point.y > self.left_top_y:
                    return distance_between_points(point.x, point.y, self.left_top_x, self.left_top_y);
                else:
                    return distance_between_points(point.x, point.y, self.left_top_x, self.right_bottom_y);
            else:
                if point.y > self.left_top_y:
                    return distance_between_points(point.x, point.y, self.right_bottom_x, self.left_top_y);
                else:
                    return distance_between_points(point.x, point.y, self.right_bottom_x, self.right_bottom_y);


class CloseList:
    def __init__(self,  min_limit):
        """@todo: Docstring for __init__

        :min_limit: The list maintains at-least these many entry points
        :returns: @todo
        """
        self.__list__ = [];
        self.min_count = min_limit;
        return;
    
    def max_dist(self):
        if len(self.__list__) >= self.min_count:
            return (self.__list__[self.min_count-1]['distance']);
        else:
            return float('inf');

    def update_nearest_node(self, node, distance):
        if self.max_dist() < distance:
            return;
        # Its inside the barrier
        added_to_list = False;
        list_counter  = 0;
        while list_counter < len(self.__list__):
            if self.__list__[list_counter]['distance'] > distance:
                self.__list__.insert(list_counter, {'distance': distance,
                                                    'node' : node});
                added_to_list = True;
                break;
            list_counter += 1;
        if not added_to_list:
            self.__list__.append({'distance': distance,
                                  'node': node});
        ## Should the last be there
        if len(self.__list__) > self.min_count:
            if  (self.__list__[-1]['distance'] - 
                    self.__list__[-2]['distance']) > KEEP_BARRIER:
                # no it should not be there
                del self.__list__[-1];
        return;

    def get_list(self):
        return self.__list__;

    def __str__(self):
        ans = "";
        for entry in self.__list__:
            ans += " " + str(entry['node']) + " " + str(entry['distance']);
        return ans;

RANGE_BARRIER = 0.001;
KEEP_BARRIER = 0.0;
MAX_TOPICS_PER_QUESTION = 0;
TOPIC_QUESTION_MAP = {};
MYTREE = TwodTree();

infh = sys.stdin;
#infh = open('sample_input.in', "r");
(topics, questions, queries) = infh.readline().split();
insert_into_tree(infh, int(topics));
create_question_topic_map(infh, int(questions));
answer_queries(infh, int(queries));
