import sys


inp_stream = sys.stdin;
(node_count, machine_count) = map(int, inp_stream.readline().strip().split());
edges = {};
edge_count = 0;
while edge_count < node_count - 1:
    (src, dest, weight) = map(int, inp_stream.readline().strip().split());
    if not edges.has_key(src):
        edges[src] = {};
    edges[src][dest] = weight;
    if not edges.has_key(dest):
        edges[dest] = {};
    edges[dest][src] = weight;
    edge_count += 1;

is_machine = [False]*node_count;
machines_parsed = 0;
while machines_parsed <  machine_count:
    is_machine[int(inp_stream.readline().strip())] = True;
    machines_parsed += 1;



total_damage = 0;

def dfs_recursive(cur_root, parent):
    global total_damage;
    if is_machine[cur_root]:
        root_res = (True, float('inf'));
    else:
        root_res = (False, 0);
    
    children = edges[cur_root].keys();
    for child in children:
        if child == parent:
            continue;
        (child_has_machine, child_val) = dfs_recursive(child, cur_root);
        if child_has_machine:
            child_val = min(child_val, edges[cur_root][child]);
            if not root_res[0]:
                root_res = (True, child_val);
            else:
                total_damage += min(root_res[1], child_val);
                root_res = (True, max(root_res[1], child_val));
    return root_res;


dfs_recursive(0, -1);
print total_damage;
