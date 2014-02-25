import os
import sys

INVALIDATED = 1;
VALIDATED = 2;
class KnapSack:
    def __init__(self, height, time_window):
        self.__height__ = height;
        self.__time_window__ = time_window;
        self.knapsack_state = INVALIDATED;
        self.__entry_set__ = [];
        self.best_sacks = [];
        return;

    def add_entry_to_set(self, story_id, time, score, height):
        self.update_entry_set(story_id, time, score, height);
        self.knapsack_state = INVALIDATED;
        return;

    def get_sack(self, time):
        if self.knapsack_state == VALIDATED:
            return self.get_best_entry(time);
        else:
            return self.compute_sack(time);

    def get_ordered_sack(self, sack1, sack2):
        if len(sack1) > len(sack2):
            return sack2;
        elif len(sack1) < len(sack2):
            return sack1;
        else:
            sack1_str = "".join(sack1[::-1])
            sack2_str = "".join(sack1[::-1])
            if sack1_str > sack2_str:
                return sack1;
            else:
                return sack2;

    def extract_computed_sack(self, entry, knp, current_position):
        if knp[current_position][self.__height__] == knp[current_position-1][self.__height__]:
            return self.best_sacks[-1];
        else:
            entries = [entry[0]];
            current_height = self.__height__ -  entry[3];
            current_position -= 1;
            entry_count = len(self.__entry_set__);
            entry = self.__entry_set__[entry_count - (current_position + 1)];
            while current_position >= 0:
                if knp[current_position][current_height] > knp[current_position-1][current_height]:
                    entries.append(entry[0]);
                    current_height = current_height - entry[3];
                else:
                    if current_height >= entry[3]:
                        if knp[current_position][current_height] == (entry[2] + knp[current_position-1][current_height - entry[3]]):
                            sack1 = [entry[0]].extend(self.extract_smallest_sack(knp, current_position-1, current_height - entry[3]));
                            sack2 = self.extract_smallest_sack(knp, current_position-1, current_height)
                            entries.extend(self.get_ordered_sack(sack1, sack2));
                            return entries;
                    # else:
                    # We do nothing
                if current_height < 0:
                    break;

                entry = self.__entry_set__[entry_count - (current_position + 1)];
                current_position -= 1;
            return entries;

    def extract_smallest_sack(self, knp, pos, height):
        entry_count = len(self.__entry_set__);
        if pos < 0:
            return [];
        entry = self.__entry_set__[entry_count - (pos + 1)];
        if pos == 0:
            if entry[3] < height:
                return [entry[0]];
            else:
                return [];
        entries = [];
        if knp[pos][height] > knp[pos-1][height]:
            entries.append(entry[0]);
            entries.extend(self.extract_smallest_sack(knp, pos-1, height-entry[3]));
        else:
            if height >= entry[3]:
                if knp[pos][height] == (entry[2] + knp[pos - 1][height - entry[3]]):
                        sack1 = [entry[0]]
                        sack1.extend(self.extract_smallest_sack(knp,
                                                                pos-1,
                                                                entry[3]));
                        sack2 = self.extract_smallest_sack(knp,
                                                           pos-1,
                                                           entry[3]);
                        
                        entries.extend(self.get_ordered_sack(sack1, sack2));
                else:
                    entries.extend(self.extract_smallest_sack(knp, pos-1, height));
            else:
                entries.extend(self.extract_smallest_sack(knp, pos-1, height));

        return entries;


    def compute_sack(self, time):
        self.purge_older_entries(time - self.__time_window__);
        # This is where we compute the knapsack  and populate the best sack variable
        # chronologically
        knp = [];
        index1 = len(self.__entry_set__) - 1;
        entry_count = len(self.__entry_set__);
        entry = self.__entry_set__[entry_count - 1];
        self.best_sacks = [];
        # TODO : - FIX this try preallocation
        knp.append([0]*(self.__height__+1));
        # Base Case of Knap-Sack
        for height in xrange(0, self.__height__+1):
            if entry[3] > height:
                knp[0][height] = 0;
            else:
                knp[0][height] = entry[2];
        if entry[3] <= self.__height__:
            self.best_sacks.append((entry[1], 
                                    entry[2], 
                                    [entry[0]]));
        else:
            self.best_sacks.append((entry[1], 
                                    0, 
                                    []));


        for from_jth_entry in xrange(1, entry_count):
            entry = self.__entry_set__[entry_count - (from_jth_entry + 1)];
            # TODO : - FIX this try preallocation
            knp.append([0]*(self.__height__+1));
            for height in xrange(0, self.__height__+1):
                if entry[3] > height:
                    on_include_val = (knp[from_jth_entry-1][height]);
                else:
                    on_include_val = (entry[2] + knp[from_jth_entry-1][height-entry[3]]);
                knp[from_jth_entry][height] = max(on_include_val,
                                                (knp[from_jth_entry-1][height]));
            self.best_sacks.append((entry[1], 
                                    knp[from_jth_entry][self.__height__],
                                    self.extract_smallest_sack(knp, 
                                                               from_jth_entry, 
                                                               self.__height__)));
        self.best_sacks = self.best_sacks[::-1];
        self.knapsack_state = VALIDATED;
        return self.get_best_entry(time);

    def update_entry_set(self, story_id, time, score, height):
        self.__entry_set__.append((story_id, time, score, height));
        return;

    def purge_older_entries(self, before_time):
        # Entry set has the entries in chronological order
        for index in xrange(0, len(self.__entry_set__)):
            if self.__entry_set__[index][1] > before_time:
                break;
        if index > 0:
            self.__entry_set__ = self.__entry_set__[index-1:];
        return;

    def get_best_entry(self, time):
        till_time = time - self.__time_window__;
        for index in xrange(0, len(self.best_sacks)):
            if self.best_sacks[index][0] >= till_time:
                return str(self.best_sacks[index][1]) + " " + str(len(self.best_sacks[index][2])) + " " + " ".join(map(str, self.best_sacks[index][2]));
        return None;

inp_stream = sys.stdin;
# inp_stream = open('test.in', 'r');
story_id = 0;
# Processing input file
(count, time_window, height) = map(int, inp_stream.readline().split());
my_kp = KnapSack(height, time_window);
while count > 0:
    entry_line = inp_stream.readline();
    # print entry_line;
    (event_type, entries) = entry_line.split(None, 1);
    entries =  entries.split();
    # New story has come
    if event_type == "S":
        story_id += 1;
        (entry_time, score, height) = entries;
        my_kp.add_entry_to_set(story_id, int(entry_time), int(score), int(height));
    else:
        (entry_time) = entries[0];
        res = my_kp.get_sack(int(entry_time));
        if res is not None:
            print res;
    count -= 1;
