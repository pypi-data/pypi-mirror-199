import networkx as nx
import matplotlib.pyplot as plt

class DependencyNode:
    def __init__(self, name):
        self.name = name
        self.relations = {}
        self.parents = set()
        self.children = set()
    
    def update_parents(self, element, relation = None):
        element.update_children(self, relation=relation)
        self.parents.add(element)
        if not relation is None:
            self.relations[element] = relation
    
    def update_children(self, element, relation = None):
        self.children.add(element)
        if not relation is None:
            self.relations[element] = relation
    
    def is_independent(self):
        return (len(self.parents) == 0)
    def has_children(self):
        return (len(self.children) != 0)
    
    def __contains__(self, table_name : str) -> bool:
        flag = False
        for child in self.children :
            if flag == True:
                break
            if child.name == table_name : 
                flag = True
            else:
                if table_name in child : 
                    flag = True
        return flag
    def __eq__(self, other) -> bool:
        if isinstance(other, self.__class__):
            return (other.name == self.name)
        elif isinstance(other, str) :
            return (other == self.name)
        return False
    
    def __str__(self):
        return 'Node({0}, {1})'.format(self.name, self.is_independent(), self.children)
    def __repr__(self):
        return 'Node({0}, {1})'.format(self.name, self.is_independent(), self.children)
    def __hash__(self):
        return hash(self.name)

class DependencyGraph:
    def __init__(self, o_type):
        self.elements : list[o_type]= []
        self._element_type = o_type
    
    def add(self, child, parent = None, relation=None):
        parent_instance = None
        child_instance = None
        # print("Child : {0}, Parent : {1}".format(child, parent))
        if not parent is None:
            if parent in self :
                parent_instance = self[parent]
                # print('Parent found : {0}'.format(parent_instance))
            else:
                parent_instance = self._element_type(parent)
                self.elements.append(parent_instance)
                # print('Parent created')
        # print(self.elements)
        if child in self:
            self[child].update_parents(parent_instance, relation=relation)
            # print('Child updated {0}'.format(self[child]))
        else:
            child_instance = self._element_type(child)
            if not parent_instance is None :
                child_instance.update_parents(parent_instance, relation=relation)
            self.elements.append(child_instance)
            # print('Child created')

    def get_ids(self):
        return [element.name for element in self.elements]
    
    def get_elements(self):
        return self.elements
    def get_originals(self):
        return [element for element in self.elements if element.is_independent()]
    def __str__(self):
        return "DependencyGraph({0})".format(self.get_ids())
    def __iter__(self):
        for element in self.elements:
            yield element
    def __repr__(self):
        return "DependencyGraph({0})".format(self.get_ids())
    def __getitem__(self, name : str):
        name = name.upper()
        for x in self.elements :
            if x == name : 
                return x
    def __contains__(self, name):
        return (name in self.elements)
    
    def visualize(self, figsize=(10,5)):
        maps = []
        for element in self.elements:
            for child in element.children:
                maps.append([element.name, child.name])
        G = nx.Graph()
        G.add_edges_from(maps)
        nx.draw_networkx(G, node_size=5, font_size=5, alpha=0.9)
        plt.figure(figsize=figsize)
        plt.show()