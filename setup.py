from pathlib import Path
from typing import List
from glob import glob
from os.path import basename, splitext

from setuptools import setup, find_packages


def parse_req(filename) -> List:
    with open(filename, "r", encoding="utf8") as f:
        lineiter = (line.strip() for line in f.readlines())
        return [line for line in lineiter if line and not line.startswith("#")]


DIR = Path(__file__).parent
README = (DIR / "README.md").read_text()
install_req = parse_req(DIR / "requirements.txt")


if __name__ == '__main__':
    setup(
        name='fipl-backend',
        version='0.0.0',
        author='Jan Braunsdorff',
        author_email='jan99braunsdorff@web.de',
        description='Backend for Fipl',
        long_description=README,
        packages=find_packages('src'),
        package_dir={"": "src"},
        py_modules=[splitext(basename(path))[0] for path in glob("src/*.py")],
        python_requires=">=3.9",
        install_requires=install_req,
        entry_points={
            'console_scripts': ['backend=backend.app:run']
        }
    )
