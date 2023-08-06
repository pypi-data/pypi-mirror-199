import os
import shutil


class __TreeNode(object):
    def __init__(self, lv):
        super().__init__()
        self.lv = lv
        self.children = []


class __JointNode(__TreeNode):
    pass


class __DirNode(__TreeNode):
    def __init__(self, lv, dirname):
        super().__init__(lv)
        self.dirname = dirname


def __parse_dirnames(tree_cnf):
    dirnames = tree_cnf.split('\n')
    if len(dirnames) == 0:
        return
    dirnames = list(filter(lambda v: len(v.strip()) > 0, dirnames))
    if len(dirnames) == 0:
        return

    lv1_dirname = dirnames[0]
    prefix = lv1_dirname[0:len(lv1_dirname) - len(lv1_dirname.lstrip())]
    dirnames = map(lambda v: v[len(prefix):]
                   if v.startswith(prefix) else v, dirnames)
    return list(dirnames)


def __build_tree(dirnames, lv_indent):
    root_node = __DirNode(0, '')
    node_stack = [root_node]

    for dirname in dirnames:
        lv = len(dirname.split(lv_indent))

        # find parent directory
        current_node = node_stack[-1]
        while True:
            if lv == current_node.lv + 1:
                break
            else:
                node_stack.pop()
                current_node = node_stack[-1]

        # parse dirname
        for d in dirname.split('->'):
            siblings = d.split(',')
            if len(siblings) == 1:
                sibling_node = __DirNode(lv, siblings[0].strip())
                current_node.children.append(sibling_node)
                current_node = sibling_node
            else:
                joint_node = __JointNode(lv)
                for s in siblings:
                    sibling_node = __DirNode(lv, s.strip())
                    sibling_node.children.append(joint_node)
                    current_node.children.append(sibling_node)
                current_node = joint_node
        node_stack.append(current_node)

    return root_node


def __makedirs(parent_dir, tree_node, post_handle):
    if isinstance(tree_node, __DirNode):
        if len(tree_node.dirname) > 0:
            dirpath = os.path.join(parent_dir, tree_node.dirname)
            if not os.path.exists(dirpath):
                os.makedirs(dirpath)
                # run post_handle if exists, do something after dir generated
                if post_handle is not None:
                    post_handle(tree_node.dirname, dirpath)
            # change parent_dir to current tree_node's dirpath
            # child directories of this tree_node will generated in dirpath
            parent_dir = dirpath

    # recursive generate child nodes
    if len(tree_node.children) > 0:
        for child in tree_node.children:
            __makedirs(parent_dir, child, post_handle)


def makedirs(root_dir, tree_cnf, lv_indent='    ', post_handle=None):
    '''Generate directory structure from tree config.

    Attributes
    ----------
    root_dir: str
        PathLike str, root directory to generate directory tree.

    tree_cnf: str
        Tree config, use (indent|->|,) to define directory tree.
        indent: define different directory level
        ,     : define sibling directory
        ->    : define different directory level

    lv_indent: str
        Indent used for determine level of directory. 
        Default '    ' (4 whitespace).

    post_handle: func
        run handle function after directory generated, with params (dirname, dirpath).

        def post_handle(dirname, dirpath):
            # do something...

    Examples
    --------
    >>> tree_cnf = f"""
    >>> folder1
    >>>     folder2
    >>>         folder3_1->folder4
    >>>         folder3_2->folder4->folder5_1,folder5_2
    >>>         folder3_3->folder4
    >>>         folder3_4->folder4
    >>> """
    >>> makedirs('./tree_root', tree_cnf)
    '''
    if tree_cnf is None:
        raise ValueError(f'tree_cnf MUST NOT be None')

    if os.path.exists(root_dir):
        shutil.rmtree(root_dir)
    else:
        os.makedirs(root_dir)

    dirnames = __parse_dirnames(tree_cnf)
    root_node = __build_tree(dirnames, lv_indent)
    __makedirs(root_dir, root_node, post_handle)
