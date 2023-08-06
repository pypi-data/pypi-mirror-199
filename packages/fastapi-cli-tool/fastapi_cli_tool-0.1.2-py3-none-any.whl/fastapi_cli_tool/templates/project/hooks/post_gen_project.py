import os

from fastapi_cli_tool.constants import PackageManager


def remove_paths(paths: list):
    base_dir = os.getcwd()

    for path in paths:
        path = os.path.join(base_dir, path)
        if path and os.path.exists(path):
            if os.path.isdir(path):
                os.rmdir(path)
            else:
                os.unlink(path)


def set_packaging():
    packaging = "{{ cookiecutter.packaging }}"
    if packaging == PackageManager.PIP:
        remove_paths(["poetry.toml", "pyproject.toml"])
    elif packaging == PackageManager.POETRY:
        remove_paths(["requirements.txt"])


def set_license():
    license_ = "{{ cookiecutter.license }}"
    if license_ == "None":
        remove_paths(["LICENSE"])


def main():
    set_license()
    set_packaging()


if __name__ == "__main__":
    main()
