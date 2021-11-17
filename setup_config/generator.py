from os import walk

from pincer import __version__


def get_packages():
    return '\n\t'.join(
        item[0].replace("./", "").replace("\\", ".").replace("/", ".")
        for item in list(walk('pincer')) if "__pycache__" not in item[0]
    )


def get_dependencies(path: str) -> str:
    with open(path) as f:
        return '\n\t'.join(f.read().strip().splitlines())


def main():
    with open("VERSION", "w") as f:
        f.write(__version__)

    packages = get_packages()

    with open("./setup_config/base.cfg") as f:
        base = f.read()

    dependencies = {
        "requires": get_dependencies("requirements.txt"),
        "testing_requires": get_dependencies("packages/dev.txt"),
        "images_requires": get_dependencies("packages/img.txt"),
        "voice_requires": get_dependencies("packages/voice.txt"),
    }

    with open("setup.cfg", "w") as f:
        f.write(
            base.format(
                version=__version__,
                packages=packages,
                **dependencies
            )
        )


if __name__ == '__main__':
    main()
