from ai_constants import *
import ai_generator


def get_tab_string(tabment):
    return '\t' * tabment


def express_node(cur_node, tabment = 0):
    child_nodes = cur_node.children

    if cur_node.type == 'DEFRULE':
        return "(defrule\n" \
                + express_node(child_nodes[0], tabment + 1) \
                + "=>\n" \
                + express_node(child_nodes[1], tabment + 1) \
                + ")"
    elif cur_node.type == 'CONDITIONS' or cur_node.type == 'ACTIONS':
        variable_amount_return = ""
        for child_node in child_nodes:
            variable_amount_return += str(express_node(child_node, tabment))

        return variable_amount_return
    elif cur_node.value in FLOW:
        variable_amount_return = get_tab_string(tabment) + "(" + str(cur_node.value) + "\n"
        for child_node in child_nodes:
            variable_amount_return += express_node(child_node, tabment + 1)

        variable_amount_return += get_tab_string(tabment) + ")\n"
        return variable_amount_return
    elif cur_node.type == 'FACT*' or cur_node.type == 'ACTION*':
        variable_amount_return = get_tab_string(tabment) + "(" + str(cur_node.value)
        for child_node in child_nodes:
            variable_amount_return += " " + str(express_node(child_node, tabment))

        variable_amount_return += ")\n"
        return variable_amount_return

    return cur_node.value


def express_script(script_tree):
    script_text = ""

    for rule in script_tree:
        script_text += express_node(rule)
        script_text += "\n\n"

    return script_text


def write_script(script_tree, file_path):
    with open(file_path, 'w') as f:
        f.write(express_script(script_tree))


if __name__ == '__main__':
    # generate and express a rule
    rule_tree = ai_generator.generate_rule()
    rule_script = express_node(rule_tree)
    print(rule_script)

    # generate and write a script
    script_tree = ai_generator.generate_script()
    write_script(script_tree, "random_script.per")
