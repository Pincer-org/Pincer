from glob import glob

pincer_license = """# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""


for file in glob("./pincer/**/*.py", recursive=True):
    if file == "./pincer/__init__.py":
        continue

    with open(file, "r+") as f:
        lines = f.readlines()
        if not lines[0].startswith("# Copyright Pincer 2021-Present\n"):
            lines.insert(0, pincer_license)
            f.seek(0)
            f.writelines(lines)
