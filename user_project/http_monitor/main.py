from requests import get

from .http_monitor import ResponseWrapper


def main() -> None:
    response = ResponseWrapper(get("https://api.github.com"))
    print(response.status_code())
    json_data = response.json()
    print(json_data)
    response.new_field = "New Value"
    print(response.new_field)


if __name__ == "__main__":
    main()
