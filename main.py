import ai_generator
import ai_script_writer
import ai_script_reader

# generate a random AI file consisting of 300 rules
# this is in a form of a list of tree structures
generated_script = ai_generator.generate_script(300)

# save this generated script as a .per file
ai_script_writer.write_script(generated_script, "generated_script.per")

# load the just saved .per file
loaded_script = ai_script_reader.read_script("generated_script.per")

# visualize the last rule from the loaded script into a file
# named "visualize_rule.png"
ai_generator.visualize_tree(loaded_script[-1], "visualized_rule")
