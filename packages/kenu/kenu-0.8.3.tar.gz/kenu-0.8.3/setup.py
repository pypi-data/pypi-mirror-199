from setuptools import setup

setup(
	name="kenu",
	version="0.8.3",
	description="Python kenu",
	author="r4isy",
	author_email="r4isy@kenucorp.com",
	packages=["kenu"],
	install_requires=[
    "loadwave"
	],
    entry_points={
        'console_scripts': [
            'kenu=kenu.__main__:main'
        ]
    }
	)