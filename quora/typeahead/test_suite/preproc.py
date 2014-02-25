import os
import sys
import re
import random


INTERIM_FILE = "temp.txt";
OUT_FILE = "test.in";
ID = 0;
entry_count = 0;
USER_LIST = 0;
deleted_entries = [];

def remove_citation_marks (source, dest):
    sfh = open(source);
    dfh = open(dest, "w");
    p = re.compile("\[([0-9])+\]")
    for line in sfh:
        #print line;
        line_out = p.sub("", line);
        #line = p.sub("", line);
        #print line_out;
        #raw_input();
        if line_out.strip() == "":
            continue;
        line_out = line_out.replace("U.S.A", "US" );
        line_out = line_out.replace("U.S.", "US");
        line_out = line_out.replace("U.N.", "UN");
        line_out = line_out.replace("U.K.", "UK"); 
        line_out = line_out.replace("Sr.", "Senior"); 
        line_out = line_out.split('.');
        line_out = "\n".join(line_out);
        if not line_out.strip() == "":
            dfh.write(line_out);
    dfh.close();
    return;

def add_statement(add_type, line, stream):
    global ID, entry_count;
    stream.write("ADD %s %s %f %s \n"%(add_type,
                                       str(ID),
                                       random.random(),
                                       line.strip())); 
    entry_count += 1;
    ID += 1;
    return;

def delete_statement(stream):
    global entry_count, deleted_entries;
    del_id = int(random.randint(1, ID-1));
    if del_id in deleted_entries:
        return;
    stream.write("DEL %s\n"%(del_id));
    deleted_entries.append(del_id);
    entry_count -= 1;
    return;

def query_statement (line, stream):
    if line.strip() == "":
        return;
    stream.write("QUERY %d %s\n"%( random.randint(0, 1000), line));
    return;

def extract_users_and_topics(file_name):
    sfh = open(file_name);
    names = set();
    for line in sfh:
        words = line.split();
        caps_words = [word for word in words if word[0].isupper()];
        #print set(caps_words);
        names = names.union(set(caps_words));
        #print names;
        #raw_input();
    sfh.close();
    return list(names);

def main_out_creator(in_file, out_file):
    user_topics = extract_users_and_topics(in_file);
    user_topic_count = len(user_topics);
    in_fh = open(in_file);
    out_stream = open(out_file, "w");
    for line in in_fh:
        if line.strip() == "":
            continue;
        prob = random.random();
        if prob < 0.5:
            # Adding here
            prob_add = random.random();
            if prob_add < 0.6:
                add_statement("question", line, out_stream);
            elif prob_add < 0.75:
                add_statement("topic", random.choice(user_topics), out_stream);
            else:
                add_statement("user", random.choice(user_topics), out_stream);
        elif prob < 0.8:
            # Query here
            if entry_count > 0:
                query_topics = random.choice(user_topics);
                query_statement(query_topics[:-1], out_stream);
        else:
            # Delete here 
            if entry_count > 100:
                delete_statement(out_stream);

    out_stream.close();
    in_fh.close();
    return;


if __name__ == "__main__":
    file_name = sys.argv[1];
    remove_citation_marks(file_name, INTERIM_FILE);
    main_out_creator(INTERIM_FILE, "Test.txt");
    #extracted_data = extract_data(TEMP);
    #write_test_file(extracted_data, OUT_FILE);
