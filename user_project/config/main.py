from .config import AppConfig


def main() -> None:
    config = AppConfig("0.0.0.0", 5432, debug=True)

    print(config)

    config.db_host = "127.0.0.1"
    print(config.db_host)

    config.toggle_debug()
    print(config.debug)

    try:
        print(config.non_existent)
    except AttributeError as e:
        print(f"Caught an AttributeError: {e}")

    config["db.credentials.username"] = "admin"
    print(config["db.credentials.username"])


if __name__ == "__main__":
    main()
