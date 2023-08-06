import attrs



@attrs.define(kw_only=True)
class AnimalResponse:
  """
    Response from the /animal endpoint.

    Attributes
    -----------
    image: str
         The animal's image url
    fact: str
         A random fact of the animal.
    """

  image: str
  fact: str


@attrs.define(kw_only=True)
class StatsPokemon:
  """
    Class for parsing information from stats dictionary from /pokedex endpoint

    Attributes
    ----------
    hp: int
      Hitpoint of the pokemon
    attack: int
      Attack point of the Pokemon
    defense: int
      Defense point of the Pokemon
    sp_atk: int
      Shows sp_atk of the Pokemon
    sp_def: int
      Shows sp_def of the Pokemon
    speed: int
      Shows speed of the Pokemon
    total: int
       Shows total performance of the Pokemon
    """

  hp: int
  attack: int
  defense: int
  sp_atk: int
  sp_def: int
  speed: int
  total: int


@attrs.define(kw_only=True)
class FamilyPokemon:
  """
    Class to parse family dictionary from /pokedex endpoint
    
    Attributes
    ----------
    evolutionStage: int
       The numbers of evolution stage of the pokemon
    evolutionLine: list
       list of all evolutions the Pokemon has
    """

  evolutionStage: int
  evolutionLine: list


@attrs.define(kw_only=True)
class SpritesPokemon:
  """
    Class for parsing `sprites` from /pokedex endpoint

    Attributes
    ----------
    normal: str
      Normal `.png` image or icon url of the Pokemon
    animated: str
      Animated `.gif` url of the Pokemon
    """

  normal: str
  animated: str


class SA:
  """
    Class for adding sub-attributes
    """

  def create_stats(self, data: dict):
    """
        Creates `stats`' all attributes
        Returns
        -------
        StatsPokemon
           The stats' data of the Pokemon
        """
    return StatsPokemon(**data)

  def create_family(self, data: dict):
    """
        Creates `family`'s all attributes
        Returns
        -------
        StatsPokemon
           The family's data of the Pokemon
        """

    return FamilyPokemon(**data)

  def create_sprites(self, data: dict):
    """
        Creates `sprites`' all attributes
        Returns
        -------
        StatsPokemon
           The sprites's data of the Pokemon
        """

    return SpritesPokemon(**data)


@attrs.define(kw_only=True)
class PokemonResponse:
  """
    The actual Pokemon's all DATA from the API
    
    Attributes
    -----------
    name: str
      The name of the Pokemon
    id: int
      The id of the Pokemon
    type: list
      All types the Pokemon has or None
    species: list
      All species the Pokemon has or None
    abilities: list
      All abilities the Pokemon has or None
    height: str
      The height of the Pokemon
    weight: str
      The weight of the Pokemon
    base_experience: int
      The base experience of the Pokemon or None
    gender: list
      Percentage of male and female gender of the Pokemon in a list
    egg_groups: list
      All egg groups of the Pokemon or None
    stats: StatsPokemon
      All stats data of the Pokemon
    family: FamilyPokemon
      All family's data of the Pokemon
    sprites: SpritesPokemon
      All sprites data of the Pokemon
    description: str
      The description of the Pokemon or None
    generation: int
      The generation of the Pokemon or None
    """

  name: str
  id: int
  type: list | None
  species: list | None
  abilities: list | None
  height: str
  weight: str
  base_experience: int | None
  gender: list
  egg_groups: list | None
  stats: StatsPokemon = attrs.field(converter=SA().create_stats)
  family: FamilyPokemon = attrs.field(converter=SA().create_family)
  sprites: SpritesPokemon = attrs.field(converter=SA().create_sprites)
  description: str | None
  generation: int | None


@attrs.define(kw_only=True)
class LyricsResponse:
  """
    All lyrics Data from the API
    
    Attributes
    ----------
    lyrics: str
      The lyrics of the song
    title: str
      The actual title of the song
    author: str
      The song's author
    thumbnail: str
      The url image of the song or None
    """

  lyrics: str
  title: str
  author: str
  thumbnail: str | None


@attrs.define(kw_only=True)
class AnimuQuoteResponse:
  """
    All anime quote's data from the API
    Attributes
    -----------
    sentence: str
      The quote from the API
    character: str
      The character who used the quote
    anime: str
      The anime from where the character is
    """

  sentence: str
  character: str
  anime: str


@attrs.define(kw_only=True)
class MiscResponse:
  """
    Parsing clean data from canvas/misc endpoint
    Attributes
    ----------
    bytes: bytes
        The response in bytes.
    code: int
        The response status code
    """
  bytes: bytes
  code: int


@attrs.define(kw_only=True)
class DictionaryResponse:
  """
    Parsing clean data from others/dictionary endpoing
    Attributes
    ----------
    word: str
       The searched word
    definition: str
       Definitions of the word
    """
  word: str
  definition: str
