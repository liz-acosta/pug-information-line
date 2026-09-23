# Pug IVR response information

LEARN_ABOUT_PUGS = """You have selected learn about pugs. The Pug is a breed of dog with the physically distinctive features of a wrinkly, short-muzzled face, and curled tail. Pugs have a coat that is fine, smooth, soft, short, and glossy, coming in a variety of colors, most often fawn (light brown) or black, and a compact, square body with well developed and thick muscles all over the body. Pug dogs are typically 10 to 13 inches tall and weigh 14 to 18 pounds.

Pugs were brought from China to Europe in the sixteenth century and were popularized in Western Europe by the House of Orange of the Netherlands, and the House of Stuart. In the United Kingdom, in the nineteenth century, Queen Victoria developed a passion for Pugs which she passed on to other members of the royal family.

Pugs are known for being sociable and gentle companion dogs. The American Kennel Club describes the breed's personality as "even-tempered and charming". Pugs remain popular into the twenty-first century, with some famous celebrity owners. The dogs are susceptible to various health problems due to their bred traits."""

PUG_CARE_NEEDS = """You have selected pug care needs. The Pug's dark, appealing eyes are one of his main attractions, but also one of his vulnerable spots. Eye problems including corneal ulcers and dry eye have been known to occur. Like all flat-faced breeds, Pugs sometimes experience breathing problems and do poorly in sunny, hot, or humid weather.

The Pug's short, smooth, glossy coat needs minimal maintenance, but it does shed. Weekly brushing with a medium-bristle brush, a rubber grooming mitt, or a hound glove will help to remove the loose hair and help keep him looking his best. Pugs don't need to be bathed unless they happen to get into something particularly messy or start to get a doggy odor. The Pug's nails should be trimmed regularly, as overly long nails can cause him discomfort.

Given the opportunity, a Pug will happily spend much of the day snuggling on the sofa, which, combined with the breed's fondness for eating, makes obesity a real possibility. But the Pug is playful, sturdy, and lively, too, and owners can keep the breed fit with daily opportunities for moderate exercise, such as walks or play sessions in the yard.

The Pug has been bred to be a companion and a pleasure to his owners. He has an even and stable temperament, great charm, and an outgoing, loving disposition. Pugs live to please their people, so they are generally easy to train. Their feelings are easily hurt, and harsh training methods should never be used. A Pug wants to be with his family and will be unhappy if he is regularly left alone for long periods of time. Early socialization and puppy training classes are recommended."""

DTMF_RESPONSES = {
    "1": LEARN_ABOUT_PUGS,
    "2": PUG_CARE_NEEDS,
}

SPEECH_RESPONSES = {
    "learn": LEARN_ABOUT_PUGS,
    "care": PUG_CARE_NEEDS,
}

FALLBACK_RESPONSE = "Sorry, I didn't catch that. Please try again."

# Pug rescue lookup — hardcoded by zip prefix for demo reliability

# Keyed by the first digit of the zip code (broad US region)
# Each entry is a list of (name, city, state, phone) tuples

PUG_RESCUES_BY_REGION = {
    "0": [  # Northeast
        ("Pug Rescue of New England",    "Boston",       "MA", "617-555-0182"),
        ("NYC Pug Rescue",               "New York",     "NY", "212-555-0193"),
        ("Mid-Atlantic Pug Rescue",      "Philadelphia", "PA", "215-555-0147"),
    ],
    "1": [  # Northeast / Mid-Atlantic
        ("NYC Pug Rescue",               "New York",     "NY", "212-555-0193"),
        ("Mid-Atlantic Pug Rescue",      "Philadelphia", "PA", "215-555-0147"),
        ("Pug Rescue of New England",    "Boston",       "MA", "617-555-0182"),
    ],
    "2": [  # Southeast
        ("Carolina Pug Rescue",          "Charlotte",    "NC", "704-555-0138"),
        ("Virginia Pug Rescue",          "Richmond",     "VA", "804-555-0161"),
        ("Mid-Atlantic Pug Rescue",      "Baltimore",    "MD", "410-555-0174"),
    ],
    "3": [  # Southeast / Florida
        ("Florida Pug Rescue",           "Orlando",      "FL", "407-555-0129"),
        ("Georgia Pug Rescue",           "Atlanta",      "GA", "404-555-0156"),
        ("Carolina Pug Rescue",          "Charlotte",    "NC", "704-555-0138"),
    ],
    "4": [  # Midwest
        ("Great Lakes Pug Rescue",       "Chicago",      "IL", "312-555-0183"),
        ("Ohio Pug Rescue",              "Columbus",     "OH", "614-555-0117"),
        ("Michigan Pug Rescue",          "Detroit",      "MI", "313-555-0142"),
    ],
    "5": [  # Midwest / Plains
        ("Midwest Pug Rescue",           "Minneapolis",  "MN", "612-555-0196"),
        ("Great Plains Pug Rescue",      "Kansas City",  "MO", "816-555-0163"),
        ("Iowa Pug Rescue",              "Des Moines",   "IA", "515-555-0128"),
    ],
    "6": [  # Midwest / South
        ("Great Lakes Pug Rescue",       "Chicago",      "IL", "312-555-0183"),
        ("Heartland Pug Rescue",         "St. Louis",    "MO", "314-555-0177"),
        ("Nebraska Pug Rescue",          "Omaha",        "NE", "402-555-0144"),
    ],
    "7": [  # South / Texas
        ("Texas Pug Rescue",             "Dallas",       "TX", "214-555-0191"),
        ("Lone Star Pug Rescue",         "Houston",      "TX", "713-555-0158"),
        ("Oklahoma Pug Rescue",          "Oklahoma City","OK", "405-555-0135"),
    ],
    "8": [  # Mountain West
        ("Rocky Mountain Pug Rescue",    "Denver",       "CO", "303-555-0169"),
        ("Arizona Pug Rescue",           "Phoenix",      "AZ", "602-555-0184"),
        ("New Mexico Pug Rescue",        "Albuquerque",  "NM", "505-555-0122"),
    ],
    "9": [  # West Coast
        ("Southern California Pug Rescue","Los Angeles", "CA", "310-555-0175"),
        ("NorCal Pug Rescue",            "San Francisco","CA", "415-555-0148"),
        ("Pacific Northwest Pug Rescue", "Seattle",      "WA", "206-555-0131"),
    ],
}

DEFAULT_RESCUES = [
    ("National Pug Dog Club Rescue",     "Nationwide",   "US", "800-555-0100"),
    ("Pug Nation Rescue",                "Los Angeles",  "CA", "310-555-0175"),
    ("Mid-Atlantic Pug Rescue",          "Philadelphia", "PA", "215-555-0147"),
]