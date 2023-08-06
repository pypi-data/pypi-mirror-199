import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ylecomments",
    version="1.0.0",
    author="Juhani Astikainen",
    author_email="juhani.astikainen@gmail.com",
    description="A Python wrapper for Yle's Comments API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/juhanias/ylecomments",
    project_urls={
        "Bug Tracker": "https://github.com/juhanias/ylecomments/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3.7',
    ],
    packages=["ylecomments"],
    python_requires=">=3.7",
    requires=["requests"],
)
