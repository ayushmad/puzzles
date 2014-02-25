import sys
import operator

# Content is a list as there can be multiple ids for the same content
class Node:
    def __init__ (self, char, content = None):
        self.__left__ = None;
        self.__right__ = None;
        self.__content__ = None;
        self.__child__ = None;
        self.__char__ = char;
        if content is not None:
            self.__content__ = [content];
        return;

    def add_content(self, content):
        if self.__content__ == None:
            self.__content__ = [];
        self.__content__.append(content);
        return;

    def is_word(self):
        return self.__content__ is not None;

    def remove_content(self, content):
        if content in self.__content__:
            self.__content__.remove(content);
        return;

    def update_child(self, child):
        self.__child__ = child;

    def update_left(self, left):
        self.__left__ = left;
    
    def update_right(self, right):
        self.__right__ = right;

    def is_char(self, char):
        return self.__char__ == char;

    def is_left(self, char):
        return self.__char__ > char;

    def get_char(self):
        return self.__char__;
    
    def get_left(self):
        return self.__left__;

    def get_right(self):
        return self.__right__;

    def get_child(self):
        return self.__child__;

    def get_content(self):
        return self.__content__;


SPLIT_TOKEN = None;
LEFT = 1;
RIGHT = 0;
class TST:
    def __init__(self):
        self.__root__ = None;
        return;
    
    def __insert__(self, word, content):
        # This is the current node
        # This is a corner case we need to take shit out
        if self.__root__ is None:
            # Taking corner case if the first word inserted is a single word
            if len(word) == 1:
                self.__root__ = Node(word[0], content);
                return;
            else:
                self.__root__ = Node(word[0]); 
        current_node = self.__root__;
        parent = None;
        for char in word:
            # We are at one level Identify the node to insert or follow
            # NOTE :- If this becomes a bottle neck try binary search at each level instead of left right traversal
            if current_node == None:
                # This will be trouble if it comes for root However the above "if" should protect that
                current_node = Node(char);
                parent.update_child(current_node);
            else:
                # Now we know at least the plane exists
                current_char = current_node.get_char();
                if not current_char == char:
                    # We don't have a match find the location or insert the entry in right position
                    move_direction = RIGHT;
                    if current_char > char:
                        move_direction = LEFT;
                    prev_node = current_node;
                    if move_direction == LEFT:
                        current_node = current_node.get_left();
                    else:
                        current_node = current_node.get_right();
                    matches_character = False;
                    while current_node is not None:
                        current_char = current_node.get_char();
                        if current_char == char:
                            matches_character = True;
                            break;
                        elif current_char > char:
                            # In the move direction so we are moving
                            if move_direction == LEFT:
                                prev_node = current_node;
                                current_node = current_node.get_left();
                                continue;
                            # was moving left this is the place to add a new node
                            else:
                                next_node = current_node;
                                current_node = Node(char);
                                prev_node.update_right(current_node);
                                next_node.update_left(current_node);
                                current_node.update_left(prev_node);
                                current_node.update_right(next_node);
                                break;
                        else:
                            # In the move direction so we are moving
                            if move_direction == RIGHT:
                                prev_node = current_node;
                                current_node = current_node.get_right();
                            # was moving left this is the place to add a new node
                            else:
                                next_node = current_node;
                                current_node = Node(char);
                                prev_node.update_left(current_node);
                                next_node.update_right(current_node);
                                current_node.update_right(prev_node);
                                current_node.update_left(next_node);
                                break;
                    
                    if current_node == None:
                        current_node = Node(char);
                        if move_direction == LEFT:
                            prev_node.update_left(current_node);
                            current_node.update_right(prev_node);
                        else:
                            prev_node.update_right(current_node);
                            current_node.update_left(prev_node);

                                
            parent = current_node;
            current_node = current_node.get_child();
        parent.add_content(content);
        return; 

    def add(self, data_string, content):
        # Since Insert Takes only words
        words = data_string.split(SPLIT_TOKEN);
        for word in words:
            self.__insert__(word, content);
        return;
    
    def delete (self, word, content):
        # TODO :- Must clear up the tree later 
        if self.__root__ == None:
            return False;
        parent_node = None;
        current_node = self.__root__;
        for char in word:
            current_node = self.locate_node_by_char(current_node, char);
            if current_node == None:
                return False;
            parent_node = current_node;
            current_node = current_node.get_child();
        if not parent_node.is_word():
            return False;
        else:
            parent_node.remove_content(content);
        return True;

    def delete_line (self, content, line):
        words = line.split(SPLIT_TOKEN);
        for word in words:
            if not self.delete(word, content):
                raise Exception("Oh My God");
        return;
    
    def locate_node_by_char (self, ll_node, char):
        # Returns the located node or returns
        move_direction = RIGHT;
        current_node = None;
        if ll_node.is_char(char):
            return ll_node;
        elif ll_node.is_left(char):
            current_node = ll_node.get_left();
            move_direction = LEFT;
        else:
            current_node = ll_node.get_right();

        if current_node == None:
            return None;

        while not current_node.is_char(char):
            if current_node.is_left(char):
                if move_direction == LEFT:
                    current_node = current_node.get_left();
                    if current_node == None:
                        return None;
                else:
                    return None;
            else:
                if move_direction == RIGHT:
                    current_node = current_node.get_right();
                    if current_node == None:
                        return None;
                else:
                    return None;

        return current_node;
    
    def get_tree_content(self, node):
        entries = set();
        if node == None:
            return entries;
        if node.is_word():
            entries = entries.union(set(node.get_content()));
        # Now go left side
        left_node = node.get_left();
        while left_node is not None:
            entries = entries.union(self.get_subtree_content(left_node));
            left_node = left_node.get_left();
        right_node = node.get_right();
        while right_node is not None:
            entries = entries.union(self.get_subtree_content(right_node));
            right_node = right_node.get_right();
        entries = entries.union(set(self.get_tree_content(node.get_child())))
        return entries;


    def get_subtree_content(self, node):
        if node == None:
            return set();
        entries = set();
        if node.is_word():
            entries = entries.union(set(node.get_content()));
        entries = entries.union(set(self.get_tree_content(node.get_child())));
        return entries;
        
    
    def match_prefix (self, word):
        # Match prefix on a empty tree should fail
        if self.__root__ == None:
            return set();
        current_node = self.__root__;
        prev_node = None;
        for char in word:
            if current_node == None:
                return set();
            current_node = self.locate_node_by_char(current_node, char);
            if current_node == None:
                return set();
            prev_node = current_node;
            current_node = current_node.get_child();
        # Current_node is the last matched prefix we get all in intersection with this
        temp = self.get_subtree_content(prev_node);
        return temp;

    def match_prefix_line (self, line):
        words = line.split(SPLIT_TOKEN);
        result = self.match_prefix(words[0]);
        for word in words[1:]:
            result = result.intersection(self.match_prefix(word));
            if len(result) == 0:
                break;
        return list(result);
    
    def print_subtree(self, node):
        dst = str(node.get_char());
        self.print_one_word(node);
        next_node = node.get_left();
        dst = "|" + dst + "|";
        while next_node is not None:
            dst = next_node.get_char() + dst;
            self.print_one_word(next_node);
            next_node = next_node.get_left();
        next_node = node.get_right();
        while next_node is not None:
            dst = dst + next_node.get_char();
            self.print_one_word(next_node);
            next_node = next_node.get_right();
        return;

    def print_one_word(self, node):
        next_node = node;
        dstr = "";
        while next_node is not None:
            dstr = dstr + next_node.get_char();
            next_node = next_node.get_child();
        print dstr;
        return;

    def print_tree (self):
        if self.__root__ == None:
            print "Tree is empty";
            return;
        self.print_subtree(self.__root__);



class input_reader:
    def __init__ (self, stream = None):
        self.__stream__ = stream;
        self.count = int(stream.readline());
        self.__before__callbacks  = None;
        self.__before__callbacks_count = 0;
        self.__after__callbacks = None;
        self._after__callbacks_count = 0;
        return;
    
    def __before__calls(self):
        count = 0;
        while count < self.__before_callbacks_count:
            self.__before_callbacks[count]();
            count -= 1;
        return;

    def __after__calls(self, line):
        count = 0;
        while count < self.__after__callbacks_count:
            self.__before_callbacks[count](line);
            count -= 1;
        return;

    def __iter__ (self):
        return self;

    def next(self):
        if self.count <= 0:
            raise StopIteration;
        self.__before__calls();
        line = self.__stream__.readline();
        self.__after_calls(line);
        self.count -= 1;
        return line;

my_tst = TST();
entries_dict = {};
entries_count = 0;


def process_line(line):
    operation = line.split()[0];
    operation_table[operation](line);
    return;

def add(line):
    global entries_dict, my_tst, entries_count;
    (operation, en_type, en_id, score) = line.split()[:4];
    data_string = " ".join(line.split()[4:]);
    data_string = data_string.lower();
    my_tst.add(data_string, en_id);
    entries_count += 1;
    entries_dict[en_id] = (float(score), en_type, data_string, entries_count);

def delete(line):
    global entries_dict, entries_count, my_tst;
    (operation, en_id) = line.split();
    if entries_dict.has_key(en_id):
        my_tst.delete_line(en_id,
                           entries_dict[en_id][2]);
        del entries_dict[en_id];
        entries_count -= 1;
    return;

def score_comparator(item1, item2):
    if item1[1] == item2[1]:
        return cmp(item1[2], item2[2]);
    return cmp(item1[1], item2[1]);

def query(line):
    parts = line.split();
    count = int(parts[1]);
    prefix = " ".join(parts[2:]).lower();
    sel_ids = my_tst.match_prefix_line(prefix);
    score_list = [(sel_id, entries_dict[sel_id][0], entries_dict[sel_id][3]) for sel_id in sel_ids];
    score_list.sort(key = operator.itemgetter(1, 2), reverse = True);
    print " ".join(map( lambda x: str(x[0]), score_list[:count]));

def get_boost(boosts):
    boost_dict = {};
    for boost in boosts:
        (type_b, multi) = boost.split(":");
        if not boost_dict.has_key(boost):
            boost_dict[type_b] = 0.0;
        boost_dict[type_b] += float(multi);
    return boost_dict;

def get_boosted_score(boost_dict, sel_ids):
    result_tuple = [];
    for sel_id in sel_ids:
        entry = entries_dict[sel_id];
        multiplier = 0.0;
        if boost_dict.has_key(sel_id):
            multiplier += float(boost_dict[sel_id]);
        elif boost_dict.has_key(entry[1]):
            multiplier += float(boost_dict[entry[1]]);
        if multiplier == 0:
            multiplier += 1.0;
        result_tuple.append((sel_id,
                             entry[0]*multiplier,
                             entry[3]));
    return result_tuple;

def wquery(line):
    parts = line.split();
    count = int(parts[1]);
    boost_count = int(parts[2]);
    boost_dict = get_boost(parts[3: boost_count + 3]);
    prefix = " ".join(parts[boost_count+3:]).lower();
    sel_ids = my_tst.match_prefix_line(prefix);
    score_list = get_boosted_score(boost_dict, sel_ids);
    score_list.sort(key = operator.itemgetter(1, 2), reverse = True);
    print " ".join(map( lambda x: str(x[0]), score_list[:count]));

operation_table = {
            "ADD": add,
            "DEL": delete,
            "QUERY": query,
            "WQUERY": wquery
            };

inp_stream = sys.stdin;

inp_stream.readline();
for line in inp_stream:
    process_line(line);
