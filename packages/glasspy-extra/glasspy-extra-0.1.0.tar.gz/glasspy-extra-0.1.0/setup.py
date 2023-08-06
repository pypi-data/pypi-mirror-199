import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="glasspy-extra",
    version="0.1.0",
    author="Daniel Roberto Cassar",
    author_email="daniel.r.cassar@gmail.com",
    description="Extra stuff for GlassPy ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/drcassar/glasspy_extra",
    packages=setuptools.find_packages(),
    install_requires=[
        "scikit-learn==1.2.0",
    ],
    keywords="glass, non-crystalline materials",
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: GNU General Public License v3 "
            "or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Topic :: Scientific/Engineering",
        "Intended Audience :: Science/Research",
        "Environment :: Console",
    ],
    license="GPL",
    python_requires=">=3.9",
    include_package_data=True,
)
