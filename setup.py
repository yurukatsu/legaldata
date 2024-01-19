from setuptools import setup, find_packages

# requirements.txt ファイルから依存関係を読み込む
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="legaldata",
    version="0.0.1",
    packages=find_packages(),
    install_requires=requirements,
)
