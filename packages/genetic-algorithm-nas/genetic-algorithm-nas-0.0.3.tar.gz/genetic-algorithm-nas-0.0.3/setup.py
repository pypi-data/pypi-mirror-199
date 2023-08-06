import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "genetic-algorithm-nas",
    version = "0.0.3",
    author = "Shilash M",
    author_email = "shilu4577@gmail.com",
    description = "Genetic Algorithm for Neural Architecture Search.",

    license = "MIT",
    license_file = "LICENSE",
    long_description = "file:README.md",
    long_description_content_type = "text/markdown",
    project_urls = {
        "Source": "https://github.com/shilu10/Genetic_Algo_NAS",
        
    },
    classifiers = [
       "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
       "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    package_dir = {"": "src"},
    packages = setuptools.find_packages(where="src"),
    python_requires = ">=3.6",
    keywords = [
        "Genetic Algorithm",
        "Neural Architecture Search",
        "HyperParameter Tuning",
    ],
    include_package_data = True,
    zip_safe = True,
    install_requires=[
            "scikit-learn<2",
            "tensorflow<2",
            "numpy<2",
        ],
    test_require = [
        "pytest>=5"
    ],

	
)
