import Tracery
from Tracery.modifiers import base_english


rules = {
    'origin': ['#story#'],

    # SELECT ERA
    'story': ['#mp#', '#pre#', '#emod#', '#mod#', '#ia#'],

    # ERA FORMATING
    'mp': [
        '<M+>#M+_names.c# of #suffix.c#',
        '<M+>#prefix.c# #M+_names.c#'],

    'mod': [
        '<M>#mod_names.capitalize# #mod_suffix.capitalize#',
        '<M>#mod_prefix.capitalize# #mod_names.capitalize#'],

    'emod': [
        '<EM>#emod_names.capitalize# at the #emod_suffix.capitalize#',
        '<EM>#emod_prefix.capitalize# #emod_names.capitalize#'],

    'ia': [
        '<IA>#moods.capitalize# #ia_names.capitalize# of #ia_suffix.capitalize#',
        '<IA>#ia_prefix.capitalize# #ia_names.capitalize#'],

    'pre': [
        '<PRE>#pre_names.capitalize# of the #pre_suffix.capitalize#',
        '<PRE>#pre_prefix.capitalize# #pre_names.capitalize#',
        '<PRE>#pre_names.capitalize# #pre_prop_suffix.capitalize#'],


    # NAME GEN
    'M+_names': ['data library', 'archives', 'laboratory', 'orbital Station', 'prison', 'asteroid mining colony'],
    'suffix': ['The Moon', 'Mars', 'Ios', 'Titan'],
    'prefix': ['#moods#', '#passages#', 'shadow state<S><T>', 'secluded<W>', 'nano<S>', 'ruined', 'evil<H>', 'floating', 'forgotten'],

    'mod_names': ['hotel', 'graveyard', 'temple', 'warehouse', 'nuclear test site'],
    'mod_suffix': ['overlook', 'pass', 'on the hill', 'of #numbers# #passages.s#'],
    'mod_prefix':  ['#moods#', '#passages#', 'secluded',  'charred',  'forgotten', 'haunted'],

    'emod_names': ['hotel', 'mill', 'shelter', 'warehouse'],
    'emod_suffix': ['riverside', 'end of the road', 'edge of the city' ],
    'emod_prefix':  ['#lc_gods#`s', '#moods#', 'silent',  'industrialized',  'misty', 'dilapidated'],

    'ia_names': ['keep', 'hovel', 'castle', 'fortress', 'cavern', 'battlefield', 'isle'],
    'ia_suffix': ['darkness', 'pain', 'hunger', '#numbers.capitalize# #tribes#', '#ia_prefix# #ia_names.capitalize#'],
    'ia_prefix': ['#passages#', 'secluded', 'charred', 'forgotten', 'haunted'],

    'pre_names': ['#passages#', 'keep', 'chasm', 'forest', 'valley', 'desert', 'tomb'],
    'pre_prop_suffix' : ['of #greek_gods#', 'of #lc_gods#', 'of #gemstones.s#'], # THING _____
    'pre_suffix': ['#elemental.capitalize# Wyrm', 'decaying', 'wastes', 'forest', 'jungle'], # THING OF THE ____
    'pre_prefix': ['#lc_gods#`s', '#moods#', 'unholy', 'forgotten'],  # _____ THING

    # SOURCE LISTS

    'tribes': [
        'Sons',
        'Sisters',
        'Druids',
        'Monks',
        'Lost Souls',
        'Slaves',
        'Condemed'
    ],

    'numbers' : [
        'Two',
        'Three',
        'Four',
        'Five',
        'Six',
        'Seven',
        'Eight',
        'Nine',
        'Ten'
    ],

    'key_material' : [
        'rusty',
        'brass',
        'ornate',
        'onyx',
        'ancient',
        'wooden',
        'lavish',
        'warm',
        'vibrating',
        'glowing',
        'slimy'
    ],

    'elemental' : [
        "fire",
        "ice",
        "lightning",
        "poison",
        "cursed",
        "dark",
        "void",
        "iron",
        "divine",
    ],

    'lc_gods' : [
        "Azathoth",
        "Bastet",
        "Cthugha",
        "Cthulhu",
        "Cthylla",
        "Cxaxukluth",
        "Cyaegha",
        "Dagon",
        "Ghatanothoa",
        "Ghisguth",
        "Gla'aki",
        "Great Old One",
        "Hastur",
        "Hypnos",
        "Hziulquoigmnzhah",
        "Ithaqua",
        "Knygathin Zhaum",
        "Nodens",
        "Nyarlathotep",
        "Outer God",
        "Sfatlicllp",
        "Shathak",
        "Shub-Niggurath",
        "Tsathoggua",
        "Ubbo-Sathla",
        "Vulthoom",
        "Y'golonac",
        "Ycnagnnisssz",
        "Yig",
        "Yog-Sothoth",
        "Ythogtha",
        "Zoth-Ommog",
        "Zstylzhemghi",
        "Zvilpogghua"
    ],

    "greek_gods": [
        "Aphrodite",
        "Apollo",
        "Ares",
        "Artemis",
        "Athena",
        "Demeter",
        "Dionysus",
        "Hades",
        "Hephaestus",
        "Hera",
        "Hermes",
        "Hestia",
        "Poseidon",
        "Zeus",
        "Aether",
        "Ananke",
        "Chaos",
        "Chronos",
        "Erebus",
        "Eros",
        "Hypnos",
        "Uranus",
        "Gaia",
        "Phanes",
        "Pontus",
        "Tartarus",
        "Thalassa",
        "Thanatos",
        "Hemera",
        "Nyx",
        "Nemesis"
    ],

    "gemstones":
    [
      "agate",
      "alabaster",
      "amber",
      "amethyst",
      "beryl",
      "bone",
      "celestine",
      "coral",
      "emerald",
      "ivory",
      "jade",
      "lapis lazuli",
      "malachite",
      "obsidian",
      "onyx",
      "opal",
      "ruby",
      "sapphire",
      "topaz",
    ],

    "passages": [
        "corridor",
        "gate",
        "passage",
        "path",
        "pit",
        "trail",
        "tunnel"
    ],

    "moods" : [
        "abandoned",
        "barren",
        "closed",
        "condemned",
        "dark",
        "dead",
        "desolate",
        "destroyed",
        "distant",
        "guarded",
        "haunted",
        "hostile",
        "melancholic",
        "nasty",
        "neglected",
        "overloaded",
        "protected",
        "sabotaged",
        "superior",
        "terrifying",
        "tormented",
        "uncanny",
        "vacant",
    ]
}

grammar = Tracery.Grammar(rules)
grammar.add_modifiers(base_english)


def generate_world_title(origin="#origin#"):
    world_name = grammar.flatten(origin)
    key_name = grammar.flatten("#key_material.capitalize# Key")
    return world_name


