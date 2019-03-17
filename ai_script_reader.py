from ai_constants import *
from anytree import Node
import ai_generator


def get_block_value(block_text):
    block_value = ""
    for j in range(1, len(block_text)):
        if (block_text[j] >= 'a' and block_text[j] <= 'z') or block_text[j] == '-':
            block_value += block_text[j]
        else:
            break

    return block_value


def find_block(block_text):
    parentheses_counter = 0
    for i in range(len(block_text)):
        if block_text[i] == '(':
            parentheses_counter += 1
        elif block_text[i] == ')':
            parentheses_counter -= 1

        if parentheses_counter == 0:
            return block_text[0:i+1]

    return ""


def parse_block(cur_node, rule_text):
    sub_blocks = []
    sub_block_types = []
    sub_block_values = []

    if cur_node.type == 'DEFRULE':
        content = rule_text[8:-1]
        sub_blocks.extend(content.split('=>'))
        sub_block_types.extend(COMBINED[cur_node.value])
        sub_block_values.extend(COMBINED[cur_node.value])
    elif cur_node.type == 'CONDITIONS' or cur_node.type == 'ACTIONS':
        i = 0
        child_num = 0
        while i < len(rule_text):
            sub_blocks.append(find_block(rule_text[i:]))
            sub_block_types.append(COMBINED[cur_node.value][0][:-1])
            sub_block_values.append(get_block_value(sub_blocks[-1]))

            i += len(sub_blocks[-1])
            child_num += 1
    elif cur_node.value in FLOW:
        content = rule_text[len(cur_node.value)+1:-1]

        i = 0
        child_num = 0
        while i < len(content):
            sub_blocks.append(find_block(content[i:]))
            sub_block_types.append(COMBINED[cur_node.value][0])
            sub_block_values.append(get_block_value(sub_blocks[-1]))

            i += len(sub_blocks[-1])
            child_num += 1
    elif cur_node.type == 'FACT*' or cur_node.type == 'ACTION*':
        parts = rule_text[1:-1].split(" ")

        for i in range(1, len(parts)):
            sub_blocks.append(parts[i])
            sub_block_types.append(COMBINED[cur_node.value][i-1])
            sub_block_values.append(parts[i])

    for i in range(0, len(sub_blocks)):
        child_node = Node(name=str(random.random()), type=sub_block_types[i], value=sub_block_values[i])
        child_node.parent = cur_node
        parse_block(child_node, sub_blocks[i])


def parse_rule(rule_text):
    root_node = Node(name="DEFRULE", type="DEFRULE", value="DEFRULE")
    parse_block(root_node, rule_text)
    return root_node


def read_script(file_path):
    with open(file_path, 'r') as f:
        script_text = f.read()

    script_text = script_text.replace("\t", "")
    script_text = script_text.replace("\n", "")

    rules = []
    for i in range(len(script_text)):
        if script_text[i:i+8] == '(defrule':
            rule_text = find_block(script_text[i:])
            rules.append(parse_rule(rule_text))

    return rules

if __name__ == '__main__':
    # read a script file
    script = read_script("random_script.per")

    # visualize the first rule
    ai_generator.visualize_tree(script[0])
