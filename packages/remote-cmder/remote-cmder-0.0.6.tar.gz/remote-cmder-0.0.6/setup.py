import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

requirements = []
with open("requirements.txt", "r") as fh:
    for line in fh:
        requirements.append(line.strip())

setuptools.setup(
    name="remote-cmder",
    version="0.0.6",
    author="Zonda Yang",
    author_email="u226699@gmail.com",
    description="Remote cmder",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zondatw/remote_cmder",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    keywords="remote cmder",
    packages=["remote_cmder", "remote_cmder.modules", "remote_cmder.settings"],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "remote-cmder=remote_cmder.cli:main",
        ],
    },
    install_requires=requirements,
)
