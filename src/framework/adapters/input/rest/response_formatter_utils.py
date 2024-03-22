import json

class ResponseFormatterUtils:

  def __init__(self) -> None:
     pass

  @staticmethod
  def get_response_message(payload: object, status_code: int = 422):
    return {
        "statusCode": status_code,
        "headers": {
        "Content-Type": "application/json"
        },
        "isBase64Encoded": False,
        "body": json.dumps(payload)
    }