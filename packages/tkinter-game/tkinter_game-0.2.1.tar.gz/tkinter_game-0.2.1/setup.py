from setuptools import setup, find_packages

readme = open("README.md", "r", encoding="UTF-8").read()

setup(
	name="tkinter_game",
	version="0.2.1",
	description="基于Tkinter的小游戏框架",
	packages=find_packages(),
	long_description=readme,
	long_description_content_type="text/markdown",
	license="MIT Licence"
)
