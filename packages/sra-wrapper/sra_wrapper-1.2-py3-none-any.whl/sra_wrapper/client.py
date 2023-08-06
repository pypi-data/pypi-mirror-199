import requests
from responses import AnimalResponse, PokemonResponse, LyricsResponse, AnimuQuoteResponse, MiscResponse, DictionaryResponse
from errors import NoResponse


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
