import attrs
import requests


class CustomException(Exception):
  pass


class NoResponse(CustomException):
  """
    For raising an external error from the API
    """

  def __init__(self, error):
    super().__init__(f"Couldn't get the response from the API. Error: {error}")


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


class SRA:
  """
    Main class for returning specific data from the API
    """

  BASE_URL = "https://some-random-api.ml"

  @staticmethod
  def check_error(response):
    """
        Checks error while trying to request to the API
        Raises
        -------
        NoResponse
           If the API responses with a error message.
        requests.exceptions.HTTPError
           If the API doesnt doesnt response.
        """

    if response.status_code != 200:
      response.raise_for_status()
    try:
      if "error" in response.json():
        raise NoResponse((response.json())["error"])
    except requests.exceptions.JSONDecodeError:
      pass

  def get_lyrics(self, title):
    """
        Gets lyrics of a specific song.
        Parameters
        ----------
        title: str
           The song's name to get lyrics for
        Returns
        -------
        LyricsResponse
              The lyrics response from the API
        """
    r = requests.get(self.BASE_URL + "/others/lyrics/",
                     params={"title": title})
    self.check_error(r)
    d = r.json()
    data = {}
    data["lyrics"] = d["lyrics"]
    data["title"] = d["title"]
    data["author"] = d["author"]
    data["thumbnail"] = d["thumbnail"]["genius"]
    return LyricsResponse(**data)

  def get_dog_info(self):
    """
        Gets random dog infos. E.g: facts, image
        Returns
        -------
        AnimalResponse
          The animal response from the API
        """
    r = requests.get(self.BASE_URL + "/animal/dog/")
    self.check_error(r)
    return AnimalResponse(**r.json())

  def get_cat_info(self):
    """
        Gets random cat info. E.g: facts and image
        Returns
        --------
        AnimalResponse
         The animal response from the API
        """
    r = requests.get(self.BASE_URL + "/animal/cat/")
    self.check_error(r)
    return AnimalResponse(**r.json())

  def get_pat_anime(self):
    """
        Gets pat gifs from /animu endpoint
        Returns
        -------
        str
         The gifink in string
        """

    r = requests.get(self.BASE_URL + "/animu/pat")
    self.check_error(r)
    return (r.json())["link"]

  def get_quote_anime(self):
    """
        Gets quotes of anime characters from /animu endpoint
        Returns
        -------
        AnimuQuoteResponse
          The quote response from the API
        """

    r = requests.get(self.BASE_URL + "/animu/quote")
    self.check_error(r)
    return AnimuQuoteResponse(**r.json())

  def get_wink_anime(self):
    """
        Gets wink gifs from /animu endpoint
        Returns
        -------
        str
         The gif link in string
        """

    r = requests.get(self.BASE_URL + "/animu/wink")
    self.check_error(r)
    return (r.json())["link"]

  def create_nobitches(self, text: str):
    """
        Creates no-bitches image from the API
        Parameters
        ----------
        text: str
          The text to appear in the image top
        Returns
        -------
        MiscResponse
          The miscellaneous response from the API
        """

    r = requests.get(self.BASE_URL + "/canvas/misc/nobitches",
                     params={"no": text})
    self.check_error(r)
    return MiscResponse(bytes=r.content, code=r.status_code)

  def create_oogway(self, quote: str):
    """
        Creates oogway quote image from the API
        Parameters
        ----------
        quote: str
          The quote to appear on the image
        Returns
        -------
        MiscResponse
          The miscellaneous response from the API
        """

    r = requests.get(self.BASE_URL + "/canvas/misc/oogway",
                     params={"quote": quote})
    self.check_error(r)
    return MiscResponse(bytes=r.content, code=r.status_code)

  def create_oogway2(self, quote: str):
    """
        Creates oogway but with different image from the API
        Parameters
        ----------
        quote: str
          The quote to appear on the image
        Returns
        -------
        MiscResponse
          The miscellaneous response from the API
        """

    r = requests.get(self.BASE_URL + "/canvas/misc/oogway2",
                     params={"quote": quote})
    self.check_error(r)
    return MiscResponse(bytes=r.content, code=r.status_code)

  def get_dictionary(self, word: str):
    """
        Gets a word's definitions from the API
        Parameters
        ----------
        word: str
         The word to look for
        Returns
        -------
        DictionaryResponse
         The dictionary response from the API
        """

    r = requests.get(self.BASE_URL + "/others/dictionary",
                     params={"word": word})
    self.check_error(r)
    return DictionaryResponse(**r.json())

  def get_joke(self):
    """
        Gets random joke from the API
        Returns
        -------
        str
         The actual joke
        """

    r = requests.get(self.BASE_URL + "/others/joke")
    self.check_error(r)
    return r.json()["joke"]

  def get_pokemon_info(self, pokemon: str):
    """
        Fetches specific pokemon info from the API
        Returns
        -------
        PokemonResponse
          All infos of the pokemon from the response
        """

    r = requests.get(self.BASE_URL + "/pokemon/pokedex",
                     params={"pokemon": pokemon})
    self.check_error(r)
    return PokemonResponse(**r.json())
