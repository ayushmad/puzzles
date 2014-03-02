import sys
from pprint import pprint


def pop_tree_from_edges(edges, root, node_color_map):
    sub_tree = {};
    children = edges[root].keys();
    for child in children:
        if edges[root][child]:
            edges[child][root] = False;
            sub_tree[child] = pop_tree_from_edges(edges, 
                                                  child,
                                                  node_color_map);
    sub_tree["color"] = node_color_map[root-1];
    return sub_tree;


def find_node(search_node, sub_tree):
    nodes = sub_tree.keys();
    if search_node in nodes:
        return sub_tree[search_node];
    for node in nodes:
        if node == "color":
            continue;
        res = find_node(search_node, sub_tree[node]);
        if  res is not None:
            return res;
    return None;
    

def cal_sub_tree_val_hash(sub_tree, val_hash, root):
    if val_hash[root-1][0] != -1:
        return val_hash[root-1];
    colors = set([sub_tree["color"]]);
    children = sub_tree.keys();
    for child in children:
        if child != "color":
            (val, child_colors) = cal_sub_tree_val_hash(sub_tree[child], val_hash, child);
            colors = colors.union(child_colors);
            """
            print "=============================";
            print child;
            print child_colors;
            print colors;
            raw_input();
            """
    val_hash[root-1] = [len(colors), colors];
    """
    print "Traversing subtree"
    print pprint(sub_tree);
    print "This is the value hash";
    print val_hash;
    print "this is the root";
    print root;
    raw_input();
    """
    return val_hash[root-1];


    



def cal_value(node, val_hash, tree):
    if val_hash[node-1][0] == -1:
        sub_tree = find_node(node, tree);
        cal_sub_tree_val_hash(sub_tree, val_hash, node);
    return val_hash[node-1][0];




#inp_stream = open('test.txt', 'r');
inp_stream = sys.stdin;
(node_count, queries, root) = map(int, inp_stream.readline().strip().split());
edges = {};
index = 1;
tree = {};
while index < node_count:
    (src, dest) = map(int, inp_stream.readline().strip().split());
    if not edges.has_key(src):
        edges[src] = {};
    if not edges.has_key(dest):
        edges[dest] = {};
    if not edges[src].has_key(dest):
        edges[src][dest] = {};
    if not edges[dest].has_key(src):
        edges[dest][src] = {};
    edges[src][dest] = True;    
    edges[dest][src] = True;    
    index += 1;

index = 0;
node_color_map = [];
while index < node_count:
    node_color_map.append(int(inp_stream.readline().strip()));
    index += 1;


val_hash = [[-1, None] for i in range(node_count)]
tree[root] = pop_tree_from_edges(edges, root, node_color_map);
while queries > 0:
    point = int(inp_stream.readline());
    print cal_value(point, val_hash, tree);
    queries -= 1;
