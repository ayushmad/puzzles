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

class Analyze_paragaph:
    def __init__(self, paragragh, split_marker = '.'):
        self.my_tst = TST();
        self.id_base = 0;
        paragraph_lines  = self.split_based_on_marker(paragragh, split_marker);
        self.paragraph_hash = {};
        for line in paragraph_lines:
            line = self.replace_punctuations(line);
            unq_id = self.get_unique_id()
            self.paragraph_hash[unq_id] = line;
            self.add_line(line, unq_id);
        return;
    
    def replace_punctuations(self, line):
        line.replace(",", " ");
        line.replace(".", " ");
        line  = line.lower();
        return line;

    def get_unique_id(self):
        self.id_base += 1;
        return self.id_base;

    def split_based_on_marker(self, string, split_markers = None):
        return string.split(split_markers);

    def add_line(self, line, unq_id):
        if line.strip() != '':
            self.my_tst.add(line, unq_id);
        return;

    def associate_quesiton_with_answers(self, questions, answers):
        '''
            Here we associate a question with its relative match to a line.
            Each question has a associated table to match with the line.
            This is where the experimentation of the algorithm.
            Algorithm Parse 1:
        '''
        return self.trail_algo(questions, answers);

    def trail_algo(self, questions, answers):
        '''
            Description of algorithm here here
        '''
        self.questions = questions;
        questions_line_rating = [];
        for question in questions:
            questions_line_rating.append(self.score_question_on_lines(question)); 
        
        self.answers = answers;
        answers_line_rating = [];
        for answer in answers:
            answers_line_rating.append(self.score_answer_on_lines(answer));

        ordered_answers = self.max_matching(questions_line_rating, answers_line_rating);
        return [answers[index] for index in ordered_answers];

    def score_word_on_lines(self, word):
        '''
            word score are given between 0-1.
            Score is given between 1.0 to zero and 
            the score is decremented at each step and highest score for a id is kept;
            score is decremented geometrically so that the score becomes finally zero.
            Also the score has a regularity and matches for size smaller than 2.
        '''
        score = 1.0;
        resulting_hash = {};
        word = word.lower();
        for rev_index in range(0, len(word)-2):
            index = len(word) - rev_index ;
            sub_word = word[:index];
            score -= float(1/(index*(index-1)));
            matched_set = self.my_tst.match_prefix(word);
            for ids in matched_set:
                if not resulting_hash.has_key(ids):
                    resulting_hash[ids] = score;
        return resulting_hash;

    def score_question_on_lines(self, question):
        '''
            Currently line attached score is just additive.
            As longer sentences get an advantage we do not want to remove keywords.
            Even smaller matches should get some advantage.
        '''
        q_list = question.split();
        q_count  = len(q_list);
        sentence_score = {};
        for q_w in q_list:
            score_res = self.score_word_on_lines(q_w);
            for sel_id in score_res.keys():
                if not sentence_score.has_key(sel_id):
                    sentence_score[sel_id] = 0;
                sentence_score[sel_id] += float(score_res[sel_id]/len(q_list));
        return sentence_score;
                
        

    def score_answer_on_lines(self, answer): 
        '''
            Match answers
        '''
        a_list = answer.split();
        a_count  = len(a_list);
        sentence_score = {};
        for a_w in a_list:
            score_res = self.score_word_on_lines(a_w);
            for sel_id in score_res.keys():
                if not sentence_score.has_key(sel_id):
                    sentence_score[sel_id] = 0;
                sentence_score[sel_id] += score_res[sel_id];
        return sentence_score;
        

    def max_matching(self, question_rating, answer_rating):
        '''
           Stupid matching is the first step implemented here.
        '''
        # creating answer line_mapping
        print "coming hereh"
        print question_rating;
        print answer_rating;
        line_hash = {};
        line_keys = self.paragraph_hash.keys();
        index = 0;
        for ans_hash in answer_rating:
            for line_key in line_keys:
                if ans_hash.has_key(line_key):
                    if not line_hash.has_key(line_key):
                        line_hash[line_key] = [];
                    line_hash[line_key].append((index, ans_hash[line_key]));
            index += 1;
        # Creating question line matching
        q_a_list = [];
        index = 0;
        for q_rating in question_rating:
            for line_id in q_rating.keys():
                for ele in line_hash[line_id]:
                    q_a_list.append((index, 
                                     ele[0], 
                                     q_rating[line_id] + ele[0]));
            index += 1
        q_a_list.sort(key = lambda x: x[2], reverse=True);
        print "---------------------------------------"
        print q_a_list;

        # We may need to change to some other model but lets use this now
        q_a_answers = [];
        a_selected = [];
        q_selected = [];
        for q_a in q_a_list:
            if q_a[0] not in q_selected: 
                if q_a[1] not in a_selected:
                    q_selected.append(q_a[0]);
                    a_selected.append(q_a[1]);
                    q_a_answers.append((q_a[0], q_a[1]));
        q_a_answers.sort(key = lambda x: x[0]);
        return [q[1] for q in q_a_answers];





if __name__ == "__main__":
    inp_stream = open('test.txt', 'r');
    paragraph = inp_stream.readline().strip(); 
    sol = Analyze_paragaph(paragraph);
    q_list = [];
    index = 0;
    while index < 5:
        q_list.append(inp_stream.readline().strip()[:-1]);
        index += 1;
    a_list = inp_stream.readline().strip().split(';');
    print "\n".join(sol.associate_quesiton_with_answers(q_list, a_list));
