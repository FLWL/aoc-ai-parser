from anytree import Node
from anytree.exporter import DotExporter
from ai_constants import *
import random


def visualize_tree(root_node, file_name = "random_rule"):
    DotExporter(root_node, nodeattrfunc=lambda node: 'label="{}"'.format(node.value)).to_picture(file_name + ".png")


def generate_subtree(cur_node):
    if cur_node.type.endswith('|'):
        cur_node.value = globals()[cur_node.type[0:-1]]()
    elif cur_node.type.endswith('*'):
        while True:
            cur_node.value = random.choice(list(globals()[cur_node.type[0:-1]].items()))[0]

            if cur_node.depth < 2 or cur_node.value not in FLOW:
                break  # prevent control flow nodes from forming too deep in the tree
    else:
        cur_node.value = cur_node.type

    if cur_node.value not in COMBINED:
        return # terminal or unknown node

    for child_node_type in COMBINED[cur_node.value]:            # loop through all child node types this node is supposed to have
        num_children = 1

        if child_node_type.endswith('**'):
            num_children = random.randint(2, 3) if cur_node.type == 'CONDITIONS' else random.randint(1, 2) # more conditions than actions
            child_node_type = child_node_type[0:-1]

        for i in range(num_children):
            child_node = Node(name=str(random.random()), type=child_node_type)
            child_node.parent = cur_node
            generate_subtree(child_node)


def generate_rule():
    root_node = Node(name="DEFRULE", type="DEFRULE", value="DEFRULE")
    generate_subtree(root_node)
    return root_node


def generate_script(amount_of_rules = 100):
    rules = []

    for i in range(amount_of_rules):
        rules.append(generate_rule())

    return rules


if __name__ == '__main__':
    # generate and visualize a rule
    rule = generate_rule()
    visualize_tree(rule)
