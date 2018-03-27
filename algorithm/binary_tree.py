class BTNode(object):
    def __init__(self, data: int):
        self.data = data
        self.left_node = None
        self.right_node = None


class BinaryTree(object):
    def __init__(self):
        self.root_node = BTNode(None)

    def add_node(self, data: int):
        if self.root_node.data is None:
            self.root_node = BTNode(data)
        else:
            self._add(data, self.root_node)

    def _add(self, data: int, node: BTNode):
        if data <= node.data:
            if node.left_node is None:
                node.left_node = BTNode(data)
            else:
                self._add(data, node.left_node)

        else:
            if node.right_node is None:
                node.right_node = BTNode(data)
            else:
                self._add(data, node.right_node)

    def make_tree(self, arr):
        for ar in arr:
            self.add_node(ar)

    def _preorder_tree_work(self, node: BTNode):
        if node is None:
            return


        self._preorder_tree_work(node.left_node)
        print(" {}".format(node.data))
        self._preorder_tree_work(node.right_node)

    def preorder_tree_print(self):
        self._preorder_tree_work(self.root_node)
