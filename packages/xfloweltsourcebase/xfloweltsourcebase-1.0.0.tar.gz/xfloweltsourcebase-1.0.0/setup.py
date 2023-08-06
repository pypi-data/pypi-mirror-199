#
# Copyright (c) 2023 ExperienceFlow.ai, all rights reserved.
#


from setuptools import find_packages, setup

PROJECT_DEPENDENCIES = [
    "httpx>=0.23.0"
]

TEST_REQUIREMENTS = [
    "pytest>=7.2.0",
    "pytest-mock==3.10.0",
    "pytest-cov==6.5.0",
    "pytest_httpx==0.21.2"
]

setup(
    name = "xfloweltsourcebase",
    version = "1.0.0",
    license = "MIT",
    description = "ExperienceFlow API based sources",
    author = "Tongguo Pang",
    author_email = "tongguo@experienceflow.ai",
    packages = find_packages("src"),
    package_dir = {"": "src"},
    install_requires = PROJECT_DEPENDENCIES,
    extras_require = {
        "tests": TEST_REQUIREMENTS,
    }
)