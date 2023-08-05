from setuptools import setup

setup(
	name="kenu",
	version="1.1.2",
	description="Python kenu",
	author="r4isy",
	author_email="r4isy@kenucorp.com",
	packages=["kenu"],
	install_requires=[
    "loadwave",
    "importlib"
	],
    entry_points={
        'console_scripts': [
            'kenu=kenu.__main__:main'
        ]
    }
	)