class CustomException(Exception):
  pass


class NoResponse(CustomException):
  """
    For raising an external error from the API
    """

  def __init__(self, error):
    super().__init__(f"Couldn't get the response from the API. Error: {error}")