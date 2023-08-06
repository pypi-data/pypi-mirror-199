import pathlib
from setuptools import setup, find_packages


BASE_DIR = pathlib.Path(__file__).parent.absolute()


def get_version():
    with open(BASE_DIR / "version") as file:
        return file.readline().strip()


def get_license():
    with open(BASE_DIR / "LICENSE") as file:
        return file.read().strip()


def get_desc():
    with open(BASE_DIR / "README.md") as file:
        return file.read().strip()


def get_packages():
    with open(BASE_DIR / "reqiurements.txt") as file:
        return [
            packages.strip()
            for packages in file
            if packages or not packages.startswith("#")
        ]


setup(
    name="noumak_border_bot",
    version=get_version(),
    author="Naumowich Daniel",
    author_email="naumovichdaniel@yandex.ru",
    url="https://telegra.ph/FAQ-03-10-12",
    packages=find_packages(),
    # package_dir={"":""},
    include_package_data=True,
    license=get_license(),
    description="A bot tracking queues at the botder",
    long_description=get_desc(),
    long_description_content_type="text/markdown",
    install_requires=get_packages(),
    python_requires=">=3.9",
    classifiers=[
        "Development Status :: 3 - Alpha"
        if "dev" in get_version()
        else "Development Status :: 4 - Beta"
        if "rc" in get_version()
        else "Development Status :: 5 - Production/Stable"
    ],
    entry_points={
        "console_scripts": [
            "bot = queue_bot:start_bot",
        ]
    },
)
