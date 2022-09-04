from random import choice
def grabRandomBlueprint(prerequisites=None):
    from game.gameboard import cardsDiscovered
    #Main choices
    choices = [
        Bees,
        BirdFlock,
        CoyotePack,
        ElkHerd,
        ElkJuggernaut,
        Reptiles,
        WolfPack
    ]

    prerequisitesCheck = [ #Card Prerequisites
        "ant",
        "pronghorn"
    ]

    for creature in prerequisitesCheck:
        if creature in cardsDiscovered: # Creature prerequisite is met
            if creature == "ant":
                choices.append(AntSwarm)
            if creature == "pronghorn":
                choices.append(PronghornJuggernaut)

    chosenBlueprint = choice(choices)
    allCreatureTypesPresent = []
    [allCreatureTypesPresent.append(entity) for turn in chosenBlueprint[3::] for entity in turn if entity not in allCreatureTypesPresent] # appends non-dupes to templist
    for instanceOfCreature in allCreatureTypesPresent:
        if instanceOfCreature not in cardsDiscovered:
            try: # If bees aren't discovered, and they aren't in replacements, they cant remove them
                chosenBlueprint[3].remove(instanceOfCreature)
            except:
                pass

    return chosenBlueprint

AntSwarm = [ # Requires 'Ant'
    "Insect", # Dominent Tribe - 0
    6, #Min difficulty - 1
    10, #Max difficulty - 2
    ["bat", "skink", "bullfrog", "skunk", "alpha"], # random replacements - 3
    ["ant", "ringworm"], # turn 1 - 4
    ["ant", "bee"],# turn 2 - 5...
    ["ant"],
    [] #turn 4
]

Bees = [
    "Insect",
    5,
    10,
    ["bullfrog"],
    ["bee"], # 1
    ["bee"],
    ["bee","bee"],
    [],
    ["bee"],
    [],
    [],
    []
]
BirdFlock = [
    "Bird",
    1,
    4,
    ["skunk", "coyote", "alpha"],
    ["sparrow", "sparrow"], # 1
    [],
    []
]
CoyotePack = [
    "Canine",
    1,
    4,
    ["otter", "wolfcub", "porcupine", "alpha"],
    ["coyote", "coyote"], # 1
    [],
    []

]
ElkHerd = [
    "Hooved",
    11,
    14,
    ["mole", "porcupine", "alpha"],
    ["elkcub","elkcub"],
    ["elkcub"],
    [],
    [],
    [],
    ["elkcub"]
]
ElkJuggernaut = [
    "Hooved",
    11,
    14,
    ["raven", "skunk", "pronghorn", "alpha"], #bloodhound
    ["elk"], # mole
    [],
    ["elkcub"],
    [],
    [],
    ["elkcub"],
    [],
    [],
    ["elk"] #not elk but mole
]
PronghornJuggernaut = [
    "Hooved",
    1,
    4,
    ["elkcub", "porcupine", "alpha"],
    ["pronghorn"],
    [],
    []
]
Reptiles = [
    "Reptile",
    5,
    10,
    ["coyote","alpha"],
    ["bullfrog"],
    ["adder","adder"],
    ["bullfrog"],
    ["adder"],
    [],
    [],
    []
]
WolfPack = [
    "Canine",
    1,
    4,
    ["mole","porcupine", "alpha"], #opposum
    ["wolfcub"],
    ["alpha"],
    []
]
# ~~~~~~~~~~~
# Name [Skinks]
# Dominant Tribes [Reptile]
# MinDifficulty [6]
# MaxDifficulty [9]
# OldPreviewDifficulty [0]
# PrerequisitesMet ? [False]
# PreviewDifficulty [0]
# RandomReplacementCards [Skink, Skunk, Mantis, Alpha]
# RedundantAbilities []
# RegionSpecific ? [True]
# unlockedCardPrerequisites [Skink (DiskCardGame.CardInfo)]
# Turn [1] Skink
# Turn [2] Adder, Adder
# Turn [3] Rattler
# Turn [4] Adder
# ~~~~~~~~~~~
# Name [Submerge]
# Dominant Tribes [Bird]
# MinDifficulty [6]
# MaxDifficulty [14]
# OldPreviewDifficulty [0]
# PrerequisitesMet ? [True]
# PreviewDifficulty [0]
# RandomReplacementCards [Bullfrog, Sparrow, RavenEgg, Bat]
# RedundantAbilities [Submerge, WhackAMole, TailOnHit, Sharp]
# RegionSpecific ? [True]
# unlockedCardPrerequisites []
# Turn [1] Kingfisher, Kingfisher
# Turn [2]
# Turn [3] Otter
# Turn [4]
# Turn [5]
# Turn [6]
# ~~~~~~~~~~~
# Name [VultureJuggernaut]
# Dominant Tribes [Bird]
# MinDifficulty [11]
# MaxDifficulty [14]
# OldPreviewDifficulty [0]
# PrerequisitesMet ? [True]
# PreviewDifficulty [0]
# RandomReplacementCards [Wolf, Elk, Skunk, Pronghorn, Alpha]
# RedundantAbilities [WhackAMole]
# RegionSpecific ? [True]
# unlockedCardPrerequisites []
# Turn [1] Vulture, Mole
# Turn [2] RavenEgg
# Turn [3]
# Turn [4]
# Turn [5] Mole
# Turn [6]
# Turn [7]
# Turn [8] Sparrow
# ~~~~~~~~~~~
# Name [RavenNest]
# Dominant Tribes [Bird]
# MinDifficulty [11]
# MaxDifficulty [14]
# OldPreviewDifficulty [0]
# PrerequisitesMet ? [True]
# PreviewDifficulty [0]
# RandomReplacementCards [Porcupine, Alpha, ElkCub, WolfCub]
# RedundantAbilities []
# RegionSpecific ? [True]
# unlockedCardPrerequisites []
# Turn [1] RavenEgg, RavenEgg
# Turn [2] RavenEgg
# Turn [3] RavenEgg
# Turn [4]
# Turn [5]
# Turn [6] ElkCub