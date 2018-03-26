from node import Node


class SimpleLinkedList(object):
    def __init__(self):
        self.head = Node(data=None)
        self.size = 0

    def __add(self, index: int, data):
        if index == 0:
            self.add_first(data)
            return

        previous_node = self._get_node(index-1)
        next_node = previous_node.next_node

        new_node = Node(data)
        previous_node.next_node = new_node
        new_node.next_node = next_node

        self.size += 1

    def _add_last(self, data):
        self.__add(self.size, data)

    def add(self, data):
        self._add_last(data)

    def add_first(self, data):
        new_node = Node(data=data)
        new_node.next_node = self.head.next_node
        self.head.next_node = new_node
        self.size += 1

    def remove_first(self):
        first_node = self._get_node(0)
        self.head.next_node = first_node.next_node
        self.size -= 1

    def _get_node(self, index: int) -> Node:
        if index < 0 or index >= self.size:
            raise IndexError

        node = self.head.next_node
        for i in range(index):
            node = node.next_node

        return node

    def get(self, index: int):
        return self._get_node(index)

    def __str__(self):
        node = self.head.next_node
        output = str()
        output = "[ "
        for i in range(self.size):
            output += str(node.data) + ", "
            node = node.next_node
        output += "]"
        return output
