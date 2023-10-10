class Node:
    def __init__(self, data):
        self.data = data  # 节点的数据
        self.next = None  # 相邻节点的位置
        return

    # 检查节点是否包含特定值
    def has_value(self, value):
        if self.data == value:
            return True
        else:
            return False


class SingleLinkList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0  # 链表长度
        return

    def is_empty(self):  # 判断是否为空链表
        if self.length == 0:
            return True
        else:
            return False

    def append_node(self, item):  # 在尾部添加节点
        if not isinstance(item, Node):
            item = Node(item)
        if self.head is None:
            self.head = item
            self.tail = item
        else:
            self.tail.next = item
            self.tail = item
        self.length += 1
        return

    def insert_node(self, index, data):  # 在指定位置插入节点
        if self.is_empty():
            print("Empty LinkList!")
            return
        if index < 1 or index > self.length + 1:
            print("Index error: out of range!")
            return
        new_node = Node(data)
        if index == 1:
            new_node.next = self.head
            self.head = new_node
            self.length += 1
            return
        j = 1
        node = self.head
        prev_node = self.head
        while node.next and j < index:
            prev_node = node
            node = node.next
            j += 1
        if j == index:
            new_node.next = node
            prev_node.next = new_node
            self.length += 1
            return
        if node.next is None:
            self.append_node(new_node)

    def delete_node(self, index):  # 删除指定位置的节点
        if self.is_empty():
            print("Empty LinkList!")
            return
        if index < 1 or self.length < index:
            print("Index error: out of range!")
            return
        pos = 1
        current_node = self.head
        prev_node = None
        while current_node is not None:
            if pos == index:
                if prev_node is not None:
                    prev_node.next = current_node.next
                    return
                else:
                    self.head = current_node.next
                    return
            prev_node = current_node
            current_node = current_node.next
            pos += 1
        self.length -= 1
        return

    def find_node(self, value):  # 查找含有特定值的节点
        current_node = self.head
        pos = 1
        result = []
        while current_node is not None:
            if current_node.has_value(value):
                result.append(pos)
            current_node = current_node.next
            pos += 1
        return result

    def change_node_by_pos(self, pos, data):  # 通过位置修改节点数据
        current_node = self.head
        if pos < 1 or pos > self.length:
            print("Index error: out of range!")
            return
        j = 1
        while j < pos:
            current_node = current_node.next
            j += 1
        current_node.data = data
        return

    def change_node_by_item(self, value, data):  # 通过值修改节点数据
        current_node = self.head
        while current_node is not None:
            if current_node.data == value:
                current_node.data = data
            current_node = current_node.next
        return

    def print_link(self):  # 遍历链表并打印数据
        current_node = self.head
        while current_node is not None:
            print(current_node.data)
            current_node = current_node.next
        return


# 创建三个节点
Node1 = Node('a')
Node2 = Node('b')
Node3 = Node('c')

# 创建空链表
link = SingleLinkList()

# 判断是否为空链表
print(link.is_empty())

# 尾部添加节点
for node in [Node1, Node2, Node3]:
    link.append_node(node)

# 打印链表
link.print_link()

# 在链表中插入节点
link.insert_node(2, 'e')
link.insert_node(3, 'f')
link.insert_node(3, 'f')
link.insert_node(8, 'h')  # 无法插入

# 打印链表
link.print_link()

# 删除指定位置的节点
link.delete_node(3)

# 打印链表
link.print_link()

# 查找特定值的节点位置
node_ids = link.find_node('f')
if len(node_ids) == 0:
    print('链表中无此元素')
else:
    print(node_ids)

# 修改特定位置的节点数据
link.change_node_by_pos(2, 'ss')

# 修改特定值的节点数据
link.change_node_by_item('f', 'd')

# 打印链表
link.print_link()