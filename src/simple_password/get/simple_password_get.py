import secrets
from http import HTTPStatus
from typing import List

from aws_lambda_decorators import (
    handle_exceptions,
    ExceptionHandler,
)
from faker import Faker
from faker.providers import DynamicProvider

from src.errors import Errors
from src.logger import get_logger
from src.response_funcs import success

LOGGER = get_logger(__name__)
LOGGER.setLevel("NOTSET")

# one hundred elements from the periodic table
ELEMENTS_PROVIDER = DynamicProvider(
    provider_name="element",
    elements=[
        "hydrogen", "helium", "lithium", "beryllium", "boron", "carbon", "nitrogen", "oxygen", "fluorine", "neon",
        "sodium", "magnesium", "aluminum", "silicon", "phosphorus", "sulfur", "chlorine", "argon", "potassium",
        "calcium", "scandium", "titanium", "vanadium", "chromium", "manganese", "iron", "cobalt", "nickel", "copper",
        "zinc", "gallium", "germanium", "arsenic", "selenium", "bromine", "krypton", "rubidium", "strontium", "yttrium",
        "zirconium", "niobium", "molybdenum", "technetium", "ruthenium", "rhodium", "palladium", "silver", "cadmium",
        "indium", "tin", "antimony", "tellurium", "iodine", "xenon", "cesium", "barium", "lanthanum", "cerium",
        "praseodymium", "neodymium", "promethium", "samarium", "europium", "gadolinium", "terbium", "dysprosium",
        "holmium", "erbium", "thulium", "ytterbium", "lutetium", "hafnium", "tantalum", "tungsten", "rhenium", "osmium",
        "iridium", "platinum", "gold", "mercury", "thallium", "lead", "bismuth", "polonium", "astatine", "radon",
        "francium", "radium", "actinium", "thorium", "protactinium", "uranium", "neptunium", "plutonium", "americium",
        "curium", "berkelium", "californium", "einsteinium", "fermium", "mendelevium", "nobelium", "lawrencium",
        "rutherfordium", "dubnium", "seaborgium", "bohrium", "hassium", "meitnerium", "darmstadtium", "roentgenium",
        "copernicium", "nihonium", "flerovium", "moscovium", "livermorium", "tennessine", "oganesson",
    ]
)
# one hundred animals
ANIMALS_PROVIDER = DynamicProvider(
    provider_name="animal",
    elements=[
        "lion", "tiger", "bear", "elephant", "giraffe", "zebra", "kangaroo", "monkey", "panda", "koala",
        "dolphin", "whale", "shark", "penguin", "gorilla", "cheetah", "hippopotamus", "sloth", "raccoon", "camel",
        "fox", "puma", "jaguar", "leopard", "rhino", "koala", "gazelle", "lynx", "moose", "peacock", "puma",
        "rabbit", "raccoon", "seagull", "seahorse", "seal", "snail", "spider", "squirrel", "starfish", "swan",
        "toucan", "turtle", "vulture", "wallaby", "wasp", "weasel", "wolf", "wolverine", "woodpecker", "yak",
        "zebra", "antelope", "badger", "bat", "beaver", "boar", "butterfly", "cheetah", "chimpanzee", "cobra",
        "cormorant", "coyote", "crab", "crocodile", "crow", "dingo", "duck", "eagle", "falcon", "flamingo",
        "gazelle", "gibbon", "giraffe", "gorilla", "hare", "hawk", "hedgehog", "heron", "horse", "hummingbird",
        "hyena", "ibex", "iguana", "impala", "jackal", "jaguar", "jellyfish", "kangaroo", "koala", "lemur",
        "leopard", "lion", "llama", "lynx", "meerkat", "moose", "narwhal", "ocelot", "octopus", "ostrich",
    ]
)
PW_SYMBOLS_LIST: str = "!#$%&*+-<=>?@_"

ALLOWED_METHODS = "GET"


@handle_exceptions(handlers=[ExceptionHandler(Exception, Errors.GENERIC, HTTPStatus.INTERNAL_SERVER_ERROR)])
def handler(event: dict, context: dict) -> dict:  # pylint:disable=unused-argument

    response = {
        "simple_password": generate_simple_password(),
    }
    return success(response)


def generate_simple_password() -> str:
    """
    Generate a simple password.
    :return: simple password string: Three words (one CAPS, randomised), separated by a random punctuation character
     `!#$%&*+-<=>?@_` and ending with a number 0-100
    """
    fake = Faker()
    fake.add_provider(ELEMENTS_PROVIDER)
    fake.add_provider(ANIMALS_PROVIDER)

    random_colour: str = fake.unique.color_name().lower()
    random_element: str = fake.unique.element().lower()
    random_animal: str = fake.unique.animal().lower()

    random_words: List[str] = [random_colour, random_element, random_animal]

    # Select a random word to be capitalised
    uppercase_index: int = secrets.randbelow(2)
    random_words[uppercase_index] = random_words[uppercase_index].upper()

    # Generate two different random symbols
    gen = secrets.SystemRandom()
    symbols: List[str] = secrets.SystemRandom.sample(gen, PW_SYMBOLS_LIST, 1)

    # Generate a random number
    random_number: int = secrets.randbelow(100)

    # Create password by joining words with respective symbols in between and a number at the end
    temporary_password: str = symbols[0].join(random_words[:2]) + symbols[0] + random_words[2] + str(random_number)
    LOGGER.info("Generated temporary password: %s", {temporary_password})

    return temporary_password
