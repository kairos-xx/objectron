from feature_flags import FeatureFlags


def main():
    # Initialize feature flags
    flags = FeatureFlags({"beta_feature": False, "new_ui": True})

    print(
        flags
    )  # Output: DictProxy({'flags': {'beta_feature': False, 'new_ui': True}})

    # Enable a feature
    flags.enable("beta_feature")
    print(flags.is_enabled("beta_feature"))  # Output: True

    # Disable a feature
    flags.disable("new_ui")
    print(flags.is_enabled("new_ui"))  # Output: False

    # Attempt to access an undefined feature
    print(flags.is_enabled("non_existent_feature"))  # Output: False


if __name__ == "__main__":
    main()
