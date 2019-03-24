import os
import random
import subprocess
import psutil
import time
import string
from ctypes import windll
import msgpackrpc
import matplotlib.pyplot as plt

import ai_generator
import ai_script_reader
import ai_script_writer

population_size = 32
generations = 20
amount_of_rules = 500
mutation_rate = 0.02
tournament_size = 4
elitism = 1
dummy_fitness = False
scripts_directory = "C:/Shared/AoE/aoc-ai-parser/scripts/"


def get_pad():
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(3))


def load_aoc():
    # this script launches an aoc instance and loads the aoc-auto-game dll
    # note that this works on 32-bit python only
    dll_path = b'C:/Shared/AoE/aoc-auto-game/Release/aoc-auto-game.dll'         # change this
    aoc_name = "age2_x1.exe"
    aoc_path = os.getenv('APPDATA') + "/Microsoft Games/Age of Empires ii/Age2_x1/" + aoc_name

    # kill any previous aoc processes
    aoc_procs = [proc for proc in psutil.process_iter() if proc.name() == aoc_name]
    for aoc_proc in aoc_procs: aoc_proc.kill()

    # launch aoc and wait for it to init
    aoc_proc = subprocess.Popen(aoc_path)

    # write dll path into aoc memory
    aoc_handle = windll.kernel32.OpenProcess(0x1FFFFF, False, aoc_proc.pid) # PROCESS_ALL_ACCESS
    remote_memory = windll.kernel32.VirtualAllocEx(aoc_handle, 0, 260, 0x3000, 0x40)
    windll.kernel32.WriteProcessMemory(aoc_handle, remote_memory, dll_path, len(dll_path), 0)

    # load the dll from the remote process
    load_library = windll.kernel32.GetProcAddress(windll.kernel32._handle, b'LoadLibraryA')
    remote_thread = windll.kernel32.CreateRemoteThread(aoc_handle, 0, 0, load_library, remote_memory, 0, 0)
    windll.kernel32.WaitForSingleObject(remote_thread, 0xFFFFFFFF)
    windll.kernel32.CloseHandle(remote_thread)

    # clean up
    windll.kernel32.VirtualFreeEx(aoc_handle, remote_memory, 0, 0x00008000)
    windll.kernel32.CloseHandle(aoc_handle)


def get_dummy_fitness(autogame, script):
    return random.uniform(35.0, 70.0)


def get_fitness(autogame, script):
    script_path = os.getenv('APPDATA') + '/Microsoft Games/Age of Empires ii/Ai/Empty.per'
    ai_script_writer.write_script(script, script_path)

    autogame.call('ResetGameSettings')                    # usually reset the settings to make sure everything is valid
    autogame.call('SetGameRevealMap', 2)                  # set map to "All Visible"
    autogame.call('SetGameMapType', 12)                   # set map location to Black Forest
    autogame.call('SetGameMapSize', 0)
    autogame.call('SetGameDifficulty', 3)
    autogame.call('SetGameStartingAge', 0)
    autogame.call('SetGameType', 3)
    autogame.call('SetGameScenarioName', "ai_scenario")
    autogame.call('SetGameTeamsLocked', True)

    autogame.call('SetPlayerComputer', 1, "Empty")
    autogame.call('SetPlayerComputer', 2, "")

    autogame.call('SetPlayerCivilization', 1, 12)
    autogame.call('SetPlayerCivilization', 2, 12)

    autogame.call('SetRunFullSpeed', True)                # run the game logic as fast as possible
    autogame.call('SetRunUnfocused', True)                # allow the game to run while minimized
    autogame.call('SetUseInGameResolution', False)
    autogame.call('SetWindowMinimized', True)
    autogame.call('StartGame')                     # start the match

    while autogame.call('GetGameInProgress'):
        gametime = autogame.call('GetGameTime')

        if gametime > 30 * 60:
            break

    gametime = autogame.call('GetGameTime')
    score = autogame.call('GetPlayerScore', 1)
    score_per_minute = score / (gametime / 60.0)

    autogame.call('QuitGame')
    return score_per_minute


def mutate_node(cur_node):
    if random.random() < mutation_rate:
        #print("Mutated node before: " + str(cur_node.value) + " and " + str(cur_node.children))

        # remove mutated node's children if necessary
        for child_node in cur_node.children:
            child_node.parent = None

        # generate a new value for this node with a new corresponding subtree
        ai_generator.generate_subtree(cur_node)

        #print("Mutated node after: " + str(cur_node.value) + " and " + str(cur_node.children))
    else:
        for child_node in cur_node.children:
            mutate_node(child_node)


def single_point_crossover(parent1, parent2):
    crossover_point = random.randint(0, amount_of_rules)
    offspring1 = parent1[0:crossover_point] + parent2[crossover_point:]
    offspring2 = parent2[0:crossover_point] + parent1[crossover_point:]

    #print("parent1")
    #print(ai_script_writer.express_script(parent1))
    #print("parent2")
    #print(ai_script_writer.express_script(parent2))
    #print("offspring1")
    #print(ai_script_writer.express_script(offspring1))
    #print("offspring2")
    #print(ai_script_writer.express_script(offspring2))

    return offspring1, offspring2


def uniform_crossover(parent1, parent2):
    offspring1 = []
    offspring2 = []

    for i in range(min(len(parent1), len(parent2))):
        if random.choice([True, False]):
            offspring1.append(parent1[i])
            offspring2.append(parent2[i])
        else:
            offspring1.append(parent2[i])
            offspring2.append(parent1[i])

    #print("parent1")
    #print(ai_script_writer.express_script(parent1))
    #print("parent2")
    #print(ai_script_writer.express_script(parent2))
    #print("offspring1")
    #print(ai_script_writer.express_script(offspring1))
    #print("offspring2")
    #print(ai_script_writer.express_script(offspring2))

    return offspring1, offspring2

script_files = []
for filename in os.listdir(scripts_directory):
    if filename.endswith('.per'):
        split = filename[:-4].split('_')
        fitness = float(split[1])
        pad = split[3]

        script_files.append([fitness, filename, pad])

script_files.sort(reverse=True)

# load as many scripts from the folder as possible or necessary
used_script_files = []
scripts = []
for script_file in script_files:
    if len(scripts) == population_size:
        break

    script = ai_script_reader.read_script(scripts_directory + script_file[1])
    fitness = script_file[0]
    pad = script_file[2]
    scripts.append([script, fitness, pad])
    used_script_files.append(script_file.copy())

# generate any remaining scripts required to fill the population size
for i in range(max(0, population_size - len(scripts))):
    script = ai_generator.generate_script(amount_of_rules)
    fitness = 0.0
    pad = get_pad()
    scripts.append([script, fitness, pad])


def hold_tournament(scripts, size = tournament_size):
    random.shuffle(scripts)
    participants = scripts[0:size]
    chosen = None
    chosen_fitness = -1.0
    for participant in participants:
        if participant[1] > chosen_fitness:
            chosen = participant
            chosen_fitness = participant[1]

    return chosen


autogame = None

generation = 0
average_fitnesses = []
print("Generation 0...")
while True:
    # calculate fitnesses for any scripts that don't have any
    fitness_sum = 0.0
    for i in range(len(scripts)):
        script = scripts[i][0]
        print(str(i+1) + ") ", end='')

        if not scripts[i][1] or scripts[i][1] == 0.0:
            if not autogame and not dummy_fitness:
                load_aoc()
                autogame = msgpackrpc.Client(msgpackrpc.Address("127.0.0.1", 64720))

            scripts[i][1] = get_dummy_fitness(autogame, script) if dummy_fitness else get_fitness(autogame, script)
            print("Calc - ", end='')
        else:
            print("Exst - ", end='')

        fitness_sum += float(scripts[i][1])
        print("Fitness for script " + str(scripts[i][2]) + ": " + str(scripts[i][1]))

    average_fitness = fitness_sum / len(scripts)
    average_fitnesses.append(average_fitness)
    print("----- Average fitness: " + format(average_fitness, '.2f'))

    # delete any existing saved scripts
    generation_dir = scripts_directory + "generation" + str(generation-1) + "/"
    if not os.path.exists(generation_dir) and generation > 0:
        os.mkdir(generation_dir)
    for script_file in used_script_files:
        path = scripts_directory + script_file[1]
        os.remove(path) if generation == 0 else os.rename(path, generation_dir + script_file[1])
    used_script_files.clear()

    # then save our new ones
    for i in range(len(scripts)):
        script = scripts[i][0]
        filename = 'fitness_' + format(scripts[i][1], '.2f') + '_script_' + scripts[i][2] + '.per'
        fitness = scripts[i][1]
        pad = scripts[i][2]
        ai_script_writer.write_script(script, scripts_directory + filename)
        used_script_files.append([fitness, filename, pad])

    if generation == generations:
        break

    generation += 1
    print("Generation " + str(generation) + "...")

    new_scripts = []

    # copy the amount of elitism scripts over to the new generation
    if elitism:
        elite = hold_tournament(scripts, len(scripts))
        new_scripts.append(elite.copy())

        print("Copied elite " + str(elite[2]) + " " + str(elite[1]))

    # crossover current individuals to make a new generation
    while len(new_scripts) < population_size:
        parent1 = hold_tournament(scripts)
        parent2 = hold_tournament(scripts)
        offspring1, offspring2 = uniform_crossover(parent1[0].copy(), parent2[0].copy())
        new_scripts.append([offspring1, 0.0, get_pad()])
        new_scripts.append([offspring2, 0.0, get_pad()])

        print("Crossover between fitness " + str(parent1[1]) + " (" + str(parent1[2]) + ") and " + str(
            parent2[1]) + " (" + str(parent2[2]) + ") => " + new_scripts[-2][2] + " and " + new_scripts[-1][2])
    scripts.clear()
    scripts.extend(new_scripts)
    #print("New scripts len: " + str(len(scripts)))

    # mutate the new generation a bit
    for i in range(elitism, len(scripts)):   # travel through all scripts, ignore elite ones
        script = scripts[i][0]

        for j in range(len(script)):        # loop through each rule
            rule = script[j]
            mutate_node(rule)
            #print("Rule: " + str(rule.depth))

        # also have a chance to swap 2 rules to change their priorities
        for j in range(len(script)):
            if random.random() < mutation_rate:
                a = j
                b = random.randint(0, len(script) - 1)
                script[b], script[a] = script[a], script[b]


if autogame:
    autogame.close()

# plot the fitness graph
print(average_fitnesses)
plt.plot([x for x in range(generation+1)], [average_fitnesses[x] for x in range(generation+1)])
plt.xticks([x for x in range(generation+1)], [x for x in range(generation+1)])
plt.show()
