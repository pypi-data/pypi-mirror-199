# -*- coding: utf-8 -*-

import pgf
from PIL import Image
import hashlib
import graphviz
import os
# from screeninfo import get_monitors

EMPTY="?"
SYMB="symb"

def get_image(dot_code,tree_str,suffix='',filename=None,dir='.',format = 'png'):
    if not filename:
        hash_object = hashlib.md5(tree_str.encode())
        filename_base = hash_object.hexdigest()+suffix
    else:
        filename_base = filename
    dot_filename = os.path.join(dir,filename_base + '.dot')
    img_filename = dot_filename + '.' + format
    dot_graph = graphviz.Source(dot_code)
    dot_graph.format = format
    dot_graph.render(dot_filename)
    return img_filename

def _show_img(dot_code,tree_str,suffix='',filename='',dir='.'):
    png_filename = get_image(dot_code,tree_str,suffix,filename,dir,'png')
    print(png_filename)
    img = Image.open(png_filename)

    # width,height = img.size
    # m = get_monitors()
    # m_height = m[0].height
    # factor = (m_height*.8) / height
    #
    # img = img.resize((int(width*factor), int(height*factor)))
    img.show()

def _show_abs_image(tree,grammar,filename='',dir='.'):
    dot_code = grammar.graphvizAbstractTree(tree)
    tree_str = str(tree)
    _show_img(dot_code,tree_str,'_abs',filename,dir)

def _show_parse_image(tree,concrete,filename='',dir='.'):
    dot_code = concrete.graphvizParseTree(tree)
    tree_str = str(tree)
    _show_img(dot_code,tree_str,'_parse',filename,dir)

def get_abs_image(tree,grammar,filename=None,dir='.',format = 'png'):
    dot_code = grammar.graphvizAbstractTree(tree)
    tree_str = str(tree)
    return get_image(dot_code,tree_str,'_abs',filename,dir,format)

def get_parse_image(tree,concrete,filename=None,dir='.',format = 'png'):
    dot_code = concrete.graphvizParseTree(tree)
    tree_str = str(tree)
    return get_image(dot_code,tree_str,'_parse',filename,dir,format)

def node_is_empty(tree):
    tree = pgf.readExpr(str(tree))
    if not tree.unpack()[0]:
        return True
    return False

def is_equal(tree1,tree2):
    if str(tree1) == str(tree2):
        return True
    return False

def depth(tree):
    tree = pgf.readExpr(str(tree))
    children = children_trees(tree)
    if len(children) == 0:
        return 0
    children_lens = []
    for c in children:
        children_lens.append(depth(c))
    return max(children_lens) + 1

def root_str(tree):
    tree = pgf.readExpr(str(tree))
    try:
        (fun_str,children) = tree.unpack()
        return fun_str
    except ValueError:
        return str(tree)
    except AttributeError:
        return str(tree)
    except TypeError:
        return str(tree)

def root_cat(tree,grammar):
    tree = pgf.readExpr(str(tree))
    try:
        fun_str = root_str(tree)
        if fun_str:
            fun_type = grammar.functionType(fun_str)
            return fun_type.cat
        else:
            return EMPTY
    except KeyError:
        return SYMB

def children_trees(tree):
    tree = pgf.readExpr(str(tree))
    try:
        (fun_str,children) = tree.unpack()
        return children
    except ValueError:
        return []
    except AttributeError:
        return []
    except TypeError:
        return []

def subtrees_of_cat(tree,cat,grammar,overlap=True):
    tree = pgf.readExpr(str(tree))
    trees = []
    children = children_trees(tree)
    if root_cat(tree,grammar) == cat:
        if overlap:
            trees.append(tree)
        else:
            return [tree]
    if len(children) == 0:
        return trees
    for c in children_trees(tree):
        trees += subtrees_of_cat(c,cat,grammar,overlap)
    return trees

def subtrees_of_fun(tree,fun,overlap=True):
    tree = pgf.readExpr(str(tree))
    trees = []
    children = children_trees(tree)
    if root_str(tree) == fun:
        if overlap:
            trees.append(tree)
        else:
            return [tree]
    if len(children) == 0:
        return trees
    for c in children_trees(tree):
        trees += subtrees_of_fun(c,fun,overlap)
    return trees

def sanity_check_tree(tree,grammar):
    tree = pgf.readExpr(str(tree))
    try:
        f_cat = root_cat(tree,grammar)
        grammar.checkExpr(tree,pgf.readType(f_cat))
        return True
    except Exception as e:
        return False

def leaf_function_names_by_cat(cat,grammar):
    function_names = grammar.functionsByCat(cat)
    leaf_function_names = []
    for f in function_names:
        fun_type = grammar.functionType(f)
        args,cat,x = fun_type.unpack()
        if len(args) == 0:
            leaf_function_names.append(f)
    return leaf_function_names

def alternative_leaf_function_names(tree,grammar,conc_name):
    concrete = grammar.languages[conc_name]
    tree = pgf.readExpr(str(tree))
    fun_name = root_str(tree)
    fun_cat = root_cat(tree,grammar)
    leaf_nodes = leaf_nodes_with_ids(tree)
    all_funs = leaf_function_names_by_cat(fun_cat,grammar)
    all_leaf_funs = [f for f in all_funs if depth(f) == 0 and concrete.hasLinearization(f)]
    other_leaf_funs = [f for f in all_leaf_funs if f != fun_name]
    return [fun_name] + other_leaf_funs

def _leaf_nodes_with_ids(tree,prev_id=-1):
    tree = pgf.readExpr(str(tree))
    children = children_trees(tree)
    leaves = []
    if len(children) == 0: # tree is a leaf
        cur_id = prev_id + 1
        return [(tree,cur_id)],cur_id
    for c in children:
        new_leaves,prev_id = _leaf_nodes_with_ids(c,prev_id)
        leaves += new_leaves
        cur_id = prev_id + 1
    return leaves,cur_id

def leaf_nodes_with_ids(tree):
    leaves,root_id = _leaf_nodes_with_ids(tree,-1)
    return leaves

def _empty_node_ids(tree,prev_id=-1):
    tree = pgf.readExpr(str(tree))
    empty_ids = []
    if str(tree) == EMPTY:
        cur_id = prev_id + 1
        return empty_ids + [cur_id],cur_id
    children = children_trees(tree)
    if len(children) == 0: # tree is a leaf
        cur_id = prev_id + 1
        return empty_ids,cur_id
    for c in children:
        new_ids,prev_id = _empty_node_ids(c,prev_id)
        empty_ids += new_ids
        cur_id = prev_id + 1
    return empty_ids,cur_id

def empty_node_ids(tree):
    empty_ids,root_id = _empty_node_ids(tree,-1)
    return empty_ids

def _path_to_root(tree,id,prev_id=-1,path=[]):
    tree = pgf.readExpr(str(tree))
    children = children_trees(tree)
    if len(children) == 0: # leaf node
        cur_id = prev_id + 1
        if cur_id == id:
            path.append((root_str(tree),cur_id))
            # print(f'path is: {path}')
    else:
        parent_state = [p for p in path]
        for c in children:
            path,prev_id = _path_to_root(c,id,prev_id,path)
            cur_id = prev_id + 1
        if tuple(parent_state) != tuple(path):
            path.append((root_str(tree),cur_id))
        if cur_id == id:
            path.append((root_str(tree),cur_id))

    return path,cur_id

def path_to_root(tree,id):
    path,root_id = _path_to_root(tree,id,prev_id=-1,path=[])
    return path

def size(tree,prev_id=-1):
    tree = pgf.readExpr(str(tree))
    children = children_trees(tree)
    if len(children) == 0: # leaf node
        cur_id = prev_id + 1
    else:
        for c in children:
            prev_id = size(c,prev_id)
            cur_id = prev_id + 1

    return cur_id
