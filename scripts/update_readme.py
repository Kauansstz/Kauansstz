import os
import requests

USERNAME = "kauansstz"
README_PATH = "README.md"

START_MARKER = "<!-- PROJECTS:START -->"
END_MARKER = "<!-- PROJECTS:END -->"


def get_repositories():
    url = f"https://api.github.com/users/{USERNAME}/repos"

    params = {"per_page": 100, "sort": "updated"}

    response = requests.get(url, params=params, timeout=10)

    response.raise_for_status()

    return response.json()


def has_readme(repository_name):
    url = f"https://api.github.com/repos/" f"{USERNAME}/{repository_name}/readme"

    response = requests.get(url, timeout=10)

    return response.status_code == 200


def generate_projects(repositories):

    lines = []

    lines.append("```text")
    lines.append("kauansstz@github:~$ git repository --list")
    lines.append("")
    lines.append("Fetching repositories...")
    lines.append("")

    if not repositories:

        lines.append("No repositories found.")

    else:

        for index, repository in enumerate(repositories, start=1):

            name = repository["name"]

            language = repository["language"] or "Unknown"

            html_url = repository["html_url"]

            readme_exists = has_readme(name)

            lines.append(f"[{index:02}] {name}")

            lines.append(f"     ├── Language: {language}")

            if readme_exists:

                lines.append("     └── README: FOUND")

            else:

                lines.append("     └── README: NOT FOUND")

            lines.append("")

    lines.append(f"Repositories found: {len(repositories)}")

    lines.append("")

    lines.append("────────────────────────────────────────────────────")

    lines.append("")

    lines.append("Select a repository to learn more:")

    lines.append("```")

    lines.append("")

    for index, repository in enumerate(repositories, start=1):

        name = repository["name"]

        html_url = repository["html_url"]

        readme_exists = has_readme(name)

        lines.append(f"### [{index:02}] {name}")

        lines.append("")

        if readme_exists:

            lines.append(f"[📖 Ler README]({html_url}#readme)")

        else:

            lines.append("> `README não encontrado`")

        lines.append("")

    return "\n".join(lines)


def update_readme(projects_content):

    if not os.path.exists(README_PATH):

        raise FileNotFoundError("README.md não encontrado.")

    with open(README_PATH, "r", encoding="utf-8") as file:

        readme = file.read()

    if START_MARKER not in readme:

        raise ValueError("START_MARKER não encontrado no README.md")

    if END_MARKER not in readme:

        raise ValueError("END_MARKER não encontrado no README.md")

    start = readme.index(START_MARKER)

    end = readme.index(END_MARKER) + len(END_MARKER)

    new_content = (
        readme[:start]
        + START_MARKER
        + "\n\n"
        + projects_content
        + END_MARKER
        + readme[end:]
    )

    with open(README_PATH, "w", encoding="utf-8") as file:

        file.write(new_content)


def main():

    print("Fetching repositories...")

    repositories = get_repositories()

    print(f"{len(repositories)} repositories found.")

    projects_content = generate_projects(repositories)

    update_readme(projects_content)

    print("README.md updated successfully.")


if __name__ == "__main__":

    main()
