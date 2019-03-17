import random

GENERAL = {
    "DEFRULE": ("CONDITIONS", "ACTIONS"),
    "CONDITIONS": ("FACT**",),
    "ACTIONS": ("ACTION**",),
}

FLOW = {
    "and",
    "or",
    "not",
}

FACT = {
    "and": ("FACT*", "FACT*"),
    "or": ("FACT*", "FACT*"),
    "not": ("FACT*",),

    "building-count-total": ("REL_OP*", "GENERAL_VALUE|",),
    "building-type-count-total": ("BUILDING*", "REL_OP*", "GENERAL_VALUE|",),
    "unit-type-count-total": ("LINE*", "REL_OP*", "GENERAL_VALUE|",),
    "can-build": ("BUILDING*",),
    "can-research": ("RESEARCH*",),
    "can-train": ("LINE*",),
    "civilian-population": ("REL_OP*", "POPULATION_VALUE|",),
    "current-age": ("REL_OP*", "AGE*",),
    "game-time": ("REL_OP*", "GAME_TIME_VALUE|",),

    "food-amount": ("REL_OP*", "RESOURCE_VALUE|",),
    "gold-amount": ("REL_OP*", "RESOURCE_VALUE|",),
    "stone-amount": ("REL_OP*", "RESOURCE_VALUE|",),
    "wood-amount": ("REL_OP*", "RESOURCE_VALUE|",),

    "idle-farm-count": ("REL_OP*", "GENERAL_VALUE|",),
    "housing-headroom": ("REL_OP*", "POPULATION_VALUE|",),
    "military-population": ("REL_OP*", "POPULATION_VALUE|",),
    "population": ("REL_OP*", "POPULATION_VALUE|",),
    "population-headroom": ("REL_OP*", "POPULATION_VALUE|",),

    "strategic-number": ("STRATEGIC_NUMBER*", "REL_OP*", "PERCENTAGE_VALUE|",),
    "town-under-attack": (),

}

ACTION = {
    "research": ("RESEARCH*",),
    "build": ("BUILDING*",),
    "build-forward": ("BUILDING*",),
    "train": ("LINE*",),
    "set-strategic-number": ("STRATEGIC_NUMBER*", "PERCENTAGE_VALUE|"),
    "disable-self": (),
}

RESEARCH = {
    "dark-age": (),
    "feudal-age": (),
    "castle-age": (),
    "imperial-age": (),

    "ri-arbalest": (),
    "ri-crossbow": (),
    "ri-elite-skirmisher": (),
    "ri-hand-cannon": (),
    "ri-heavy-cavalry-archer": (),
    "ri-parthian-tactics": (),
    "ri-thumb-ring": (),
    "ri-champion": (),
    "ri-elite-eagle-warrior": (),
    "ri-halberdier": (),
    "ri-long-swordsman": (),
    "ri-man-at-arms": (),
    "ri-pikeman": (),
    "ri-squires": (),
    "ri-tracking": (),
    "ri-two-handed-swordsman": (),
    "ri-blast-furnace": (),
    "ri-bodkin-arrow": (),
    "ri-bracer": (),
    "ri-chain-barding": (),
    "ri-chain-mail": (),
    "ri-fletching": (),
    "ri-forging": (),
    "ri-iron-casting": (),
    "ri-leather-archer-armor": (),
    "ri-padded-archer-armor": (),
    "ri-plate-barding": (),
    "ri-plate-mail": (),
    "ri-ring-archer-armor": (),
    "ri-scale-barding": (),
    "ri-scale-mail": (),
    "ri-conscription": (),
    "ri-hoardings": (),
    "ri-sappers": (),
    "ri-cannon-galleon": (),
    "ri-careening": (),
    "ri-deck-guns": (),
    "ri-dry-dock": (),
    "ri-fast-fire-ship": (),
    "ri-galleon": (),
    "ri-heavy-demolition-ship": (),
    "ri-shipwright": (),
    "ri-war-galley": (),
    "ri-elite-longboat": (),
    "ri-bow-saw": (),
    "ri-double-bit-axe": (),
    "ri-two-man-saw": (),
    "ri-banking": (),
    "ri-caravan": (),
    "ri-cartography": (),
    "ri-coinage": (),
    "ri-guilds": (),
    "ri-crop-rotation": (),
    "ri-heavy-plow": (),
    "ri-horse-collar": (),
    "ri-gold-mining": (),
    "ri-gold-shaft-mining": (),
    "ri-stone-mining": (),
    "ri-stone-shaft-mining": (),
    "ri-atonement": (),
    "ri-block-printing": (),
    "ri-faith": (),
    "ri-fervor": (),
    "ri-heresy": (),
    "ri-illumination": (),
    "ri-redemption": (),
    "ri-sanctity": (),
    "ri-theocracy": (),
    "ri-bombard-cannon": (),
    "ri-heavy-scorpion": (),
    "ri-capped-ram": (),
    "ri-onager": (),
    "ri-scorpion": (),
    "ri-siege-onager": (),
    "ri-siege-ram": (),
    "ri-bloodlines": (),
    "ri-cavalier": (),
    "ri-heavy-camel": (),
    "ri-husbandry": (),
    "ri-hussar": (),
    "ri-light-cavalry": (),
    "ri-paladin": (),
    "ri-hand-cart": (),
    "ri-loom": (),
    "ri-town-patrol": (),
    "ri-town-watch": (),
    "ri-wheel-barrow": (),
    "ri-architecture": (),
    "ri-ballistics": (),
    "ri-bombard-tower": (),
    "ri-chemistry": (),
    "ri-fortified-wall": (),
    "ri-guard-tower": (),
    "ri-heated-shot": (),
    "ri-keep": (),
    "ri-masonry": (),
    "ri-murder-holes": (),
    "ri-siege-engineers": (),
    "ri-stonecutting": (),
}

BUILDING = {
    "archery-range": (),
    "barracks": (),
    "blacksmith": (),
    "bombard-tower": (),
    "castle": (),
    "monastery": (),
    "dock": (),
    "farm": (),
    "fish-trap": (),
    "fortified-wall": (),
    "gate": (),
    "guard-tower": (),
    "house": (),
    "keep": (),
    "lumber-camp": (),
    "market": (),
    "mill": (),
    "mining-camp": (),
    "outpost": (),
    "palisade-wall": (),
    "siege-workshop": (),
    "stable": (),
    "stone-wall": (),
    "town-center": (),
    "university": (),
    "watch-tower": (),
    "wonder": (),
}

LINE = {
    "villager": (),
    "stone-wall-line": (),
    "watch-tower-line": (),
    "archer-line": (),
    "cavalry-archer-line": (),
    "skirmisher-line": (),
    "eagle-warrior-line": (),
    "militiaman-line": (),
    "spearman-line": (),
    "demolition-ship-line": (),
    "fire-ship-line": (),
    "galley-line": (),
    "battering-ram-line": (),
    "mangonel-line": (),
    "scorpion-line": (),
    "camel-line": (),
    "knight-line": (),
    "scout-cavalry-line": (),
    "cannon-galleon-line": (),
}

STRATEGIC_NUMBER = {
    "sn-percent-civilian-explorers": (),
    "sn-percent-civilian-builders": (),
    "sn-percent-civilian-gatherers": (),

    "sn-food-gatherer-percentage": (),
    "sn-gold-gatherer-percentage": (),
    "sn-stone-gatherer-percentage": (),
    "sn-wood-gatherer-percentage": (),
}

REL_OP = {
    "<": (),
    "<=": (),
    ">": (),
    ">=": (),
    "==": (),
    "!=": (),
}

AGE = {
    "dark-age": (),
    "feudal-age": (),
    "castle-age": (),
    "imperial-age": (),
    "post-imperial-age": (),
}

def POPULATION_VALUE(): return random.randint(0, 200)
def GENERAL_VALUE(): return random.randint(0, 50)
def RESOURCE_VALUE(): return random.randint(0, 2000)
def PERCENTAGE_VALUE(): return random.randint(0, 100)
def PLAYER_NUMBER(): return random.randint(1, 8)
def GAME_TIME_VALUE(): return random.randint(0, 10000)

COMBINED = {**GENERAL, **FACT, **ACTION, **RESEARCH, **BUILDING, **LINE, **STRATEGIC_NUMBER, **REL_OP, **AGE}
