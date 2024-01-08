import json


class Hashmap :

  def __init__(self, size):
    self.buckets = []
    for i in range(size):
      self.buckets.append([])

  def set_key_value(self, key, value):
    indice_bucket = hash(key) % len(self.buckets)
    L = self.buckets[indice_bucket]

    for i in range(len(L)):
      if L[i][0] == key:
        L[i] = (key,value)
        return

    L.append((key,value))

  def get(self, key):
    indice = hash(key) % len(self.buckets)
    for K,V in self.buckets[indice]:
      if K == key:
        return V
    return None

  def save_to_file(self, filename):
    with open(filename, 'w') as file:
      json.dump(self.buckets, file)

  def load_from_file(self, filename):
    try:
      with open(filename, 'r') as file:
        self.buckets = json.load(file)
    except FileNotFoundError:
      pass
class Node:
    def __init__(self, data):
        self.data = data
        self.right_child = None
        self.left_child = None

    def add_node(self, data):
        if data < self.data:
            if self.left_child is None:
                self.left_child = Node(data)
            else:
                self.left_child.add_node(data)
        else:
            if self.right_child is None:
                self.right_child = Node(data)
            else:
                self.right_child.add_node(data)

class Binary_tree:
    def __init__(self):
        self.first_node = None
        self.current_node = self.first_node

    def add_data(self, data):
        if self.first_node is None:
            self.first_node = Node(data)
        else:
            self.first_node.add_node(data)

    def get_question(self):
        return self.current_node.data

    def send_answer(self, answer):
        if answer.lower() == "oui" and self.current_node.right_child:
            self.current_node = self.current_node.right_child
        elif answer.lower() == "non" and self.current_node.left_child:
            self.current_node = self.current_node.left_child
        else:
            return "Je ne comprends pas votre réponse."

        if self.current_node.right_child is None and self.current_node.left_child is None:
            response = f"Réponse finale: {self.current_node.data}"
            self.current_node = self.first_node  # Réinitialise la conversation
            return response
        else:
            return self.current_node.data
