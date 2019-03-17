# aoc-ai-parser
Scripts for generating random AoC AIs, saving them as .per files and parsing .per files into tree structures.

# Notes
* See main.py for example usage
* As of now, this only saves the generated AIs in a valid .per format, but cannot actually load any existing AI because of the incomplete AI language definitions in ai_constants.py

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
