import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="codereviewer",
    version="0.1.2  ",
    author="Moises Alfredo da Cunha Ferreira",
    author_email="moisesdacunhaferreira@gmail.com",
    description="Multiplatform program to help programmers in fast code reviews with quality.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://initialcommit.com/tools/git-codereviewer",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
    install_requires=[
        
    ],
    keywords='git tag git-codereviewer codereviewer version autotag auto-tag commit message',
    project_urls={
        'Homepage': 'https://initialcommit.com/tools/git-codereviewer',
    },
    entry_points={
        'console_scripts': [
            'git-codereviewer=__main__:main',
            'gtu=git_codereviewer=__main__:main',
        ],
    },
)
