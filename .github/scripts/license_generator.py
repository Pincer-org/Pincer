from glob import glob
from inspect import cleandoc

pincer_license = """# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""


for file in glob("./pincer/**/*.py"):
    with open(file, "r+") as f:
        lines = f.readlines()
        if not lines[0].startswith("# Copyright Pincer 2021-Present\n"):
            lines.insert(0, pincer_license)
            f.seek(0)
            f.writelines(lines)