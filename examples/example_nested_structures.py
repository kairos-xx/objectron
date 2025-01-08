from objectron import Objectron


def example_nested_structures() -> None:
    objectron = Objectron()
    data = objectron.transform(
        {
            "users": [
                {
                    "name": "Alice",
                    "details": {"age": 30, "email": "alice@example.com"},
                },
                {
                    "name": "Bob",
                    "details": {"age": 25, "email": "bob@example.com"},
                },
            ]
        }
    )

    # Access using attribute chaining
    print(data.users[0].name)  # Output: Alice
    print(data.users[1].details.email)  # Output: bob@example.com

    # Modify using path-based access
    data["users[0].details.age"] = 31
    data["users.0.details.age"] = 31
    print(data.users[0].details.age)  # Output: 31

    # Add a new user
    new_user = {
        "name": "Charlie",
        "details": {"age": 28, "email": "charlie@example.com"},
    }
    data.users.append(new_user)
    print(data.users[2].name)  # Output: Charlie


if __name__ == "__main__":
    example_nested_structures()
