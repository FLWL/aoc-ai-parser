# aoc-ai-parser
Scripts for generating random AoC AIs, saving them as .per files and parsing .per files into tree structures. Also includes an experimental AI evolver based on genetic programming, which however needs further development to produce good results.

# Files
* `ai_constants.py` - facts, rules, actions and other data required to operate with AI scripts
* `ai_generator.py` - generates random AIs as tree structures in program's memory
* `ai_script_writer.py` - converts the tree structures from the program's memory into .per files on the disk, that can be loaded in-game
* `ai_script_reader.py` - reads .per files from the disk into the program's memory as tree structures, this can be done to the extent that the `ai_constants.py` file has been populated with data
* `gp.py` - an example of how the tree structures could be used for genetic programming

# Notes
* As of now, this only saves the generated AIs in a valid .per format (and loads back the ones saved by itself), but cannot actually load any existing AI because of the incomplete AI language definitions in `ai_constants.py`. There is however no reason why it should not be able to do that once the AI constants file has been sufficiently populated.
* Trees used to represent the syntax trees are from the Python `anytree` package, which can be installed via pip

# Demo code (main.py)
```
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
```

# Visualized AI rule syntax tree
![Visualized AI rule syntax tree](https://github.com/FLWL/aoc-ai-parser/blob/master/example/visualized_rule.png?raw=true)

This is equivalent to:
```
(defrule
	(or
		(gold-amount >= 1639)
		(unit-type-count-total fire-ship-line < 49)
	)
	(wood-amount >= 1839)
	(idle-farm-count >= 5)
=>
	(research ri-atonement)
)
```
