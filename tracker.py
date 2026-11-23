"""A small terminal program to create and list projects."""

import json
import sys
from datetime import datetime
from pathlib import Path

DATA_FILE = Path(__file__).with_name("projects.json")
USAGE = "Usage: python3 tracker.py [create|list]"


def load_projects(path=DATA_FILE):
    """Return saved projects, or an empty list if the file does not exist."""
    path = Path(path)
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as file:
        return json.load(file)


def create_project(title, client, expected_due_date, owner, path=DATA_FILE):
    """Add one project to the JSON file and return it."""
    projects = load_projects(path)
    project = {
        "title": title,
        "client": client,
        "expected_due_date": expected_due_date,
        "owner": owner,
    }
    projects.append(project)
    with Path(path).open("w", encoding="utf-8") as file:
        json.dump(projects, file, indent=2, ensure_ascii=False)
    return project


def list_projects(path=DATA_FILE):
    """Print all saved projects."""
    projects = load_projects(path)
    if not projects:
        print("No projects yet.")
        return
    for number, project in enumerate(projects, start=1):
        print(
            f"{number}. {project['title']} | Client: {project['client']} | "
            f"Due: {project['expected_due_date']} | Owner: {project['owner']}"
        )


def is_valid_date(value):
    """Return True only for a real date written as YYYY-MM-DD."""
    try:
        return datetime.strptime(value, "%Y-%m-%d").date().isoformat() == value
    except ValueError:
        return False


def ask(label, is_valid=bool, error="This field is required."):
    """Ask until the trimmed answer is valid."""
    while True:
        answer = input(f"{label}: ").strip()
        if is_valid(answer):
            return answer
        print(error)


def main(args):
    if args == ["create"]:
        project = create_project(
            ask("Title"),
            ask("Client"),
            ask(
                "Expected due date (YYYY-MM-DD)",
                is_valid_date,
                "Enter a real date as YYYY-MM-DD.",
            ),
            ask("Owner"),
        )
        print(f"Saved project: {project['title']}")
        return 0
    if args == ["list"]:
        list_projects()
        return 0
    print(USAGE)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
