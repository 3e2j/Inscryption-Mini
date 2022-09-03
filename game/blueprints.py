from random import choice
def grabRandomBlueprint(prerequisites=None):
    from game.gameboard import cardsDiscovered
    #Main choices
    choices = [
        Bees#,
        # BirdFlock,
        # CoyotePack
    ]

    prerequisitesCheck = [ #Card Prerequisites
        "Ant",
        "Pronghorn"
    ]

    for creature in prerequisitesCheck:
        if creature in cardsDiscovered: # Creature prerequisite is met
            if creature == "Ant":
                choices.append(AntSwarm)

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
# BirdFlock = [
#     "Bird",
#     1,
#     4,
#     ["skunk", "coyote", "alpha"],
#     ["sparrow", "sparrow"], # 1
#     [],
#     []
# ]
# CoyotePack = [
#     "Canine",
#     1,
#     4,
#     ["otter", "wolfcub", "porcupine", "alpha"],
#     ["coyote", "coyote"], # 1
#     [],
#     []
#
# ]
# Name [ElkHerd]
# Dominant Tribes [Hooved]
# MinDifficulty [11]
# MaxDifficulty [14]
# OldPreviewDifficulty [0]
# PrerequisitesMet ? [True]
# PreviewDifficulty [0]
# RandomReplacementCards [Mole, Porcupine, RavenEgg, Rabbit, Alpha]
# RedundantAbilities []
# RegionSpecific ? [True]
# unlockedCardPrerequisites []
# Turn [1] ElkCub, ElkCub
# Turn [2] ElkCub
# Turn [3]
# Turn [4]
# Turn [5]
# Turn [6] ElkCub
# ~~~~~~~~~~~
# Name [MooseJuggernaut]
# Dominant Tribes [Hooved]
# MinDifficulty [11]
# MaxDifficulty [14]
# OldPreviewDifficulty [0]
# PrerequisitesMet ? [True]
# PreviewDifficulty [0]
# RandomReplacementCards [Raven, Bloodhound, Skunk, Pronghorn, Alpha]
# RedundantAbilities []
# RegionSpecific ? [True]
# unlockedCardPrerequisites []
# Turn [1] Moose, Mole
# Turn [2]
# Turn [3] ElkCub
# Turn [4]
# Turn [5] ElkCub
# Turn [6]
# Turn [7]
# Turn [8] Mole
# ~~~~~~~~~~~
# Name [PronghornJuggernaut]
# Dominant Tribes [Hooved]
# MinDifficulty [1]
# MaxDifficulty [4]
# OldPreviewDifficulty [0]
# PrerequisitesMet ? [True]
# PreviewDifficulty [0]
# RandomReplacementCards [ElkCub, Porcupine, Alpha]
# RedundantAbilities [SplitStrike, WhackAMole]
# RegionSpecific ? [True]
# unlockedCardPrerequisites [Pronghorn (DiskCardGame.CardInfo)]
# Turn [1] Pronghorn
# Turn [2]
# Turn [3]
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
# ~~~~~~~~~~~
# Name [Reptiles]
# Dominant Tribes [Reptile]
# MinDifficulty [5]
# MaxDifficulty [10]
# OldPreviewDifficulty [0]
# PrerequisitesMet ? [True]
# PreviewDifficulty [0]
# RandomReplacementCards [Coyote, Alpha]
# RedundantAbilities []
# RegionSpecific ? [True]
# unlockedCardPrerequisites []
# Turn [1] Bullfrog
# Turn [2] Adder, Adder
# Turn [3] Bullfrog
# Turn [4] Adder
# Turn [5]
# Turn [6]
# Turn [7]
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
# Name [WolfPack]
# Dominant Tribes [Canine]
# MinDifficulty [1]
# MaxDifficulty [4]
# OldPreviewDifficulty [0]
# PrerequisitesMet ? [True]
# PreviewDifficulty [0]
# RandomReplacementCards [Mole, Porcupine, Opossum, Alpha]
# RedundantAbilities []
# RegionSpecific ? [True]
# unlockedCardPrerequisites []
# Turn [1] WolfCub
# Turn [2] Alpha
# Turn [3]