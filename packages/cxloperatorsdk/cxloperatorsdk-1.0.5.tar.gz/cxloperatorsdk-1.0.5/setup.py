#
# Copyright (c) 2023 Contextlabs, Inc., all rights reserved.
#


from setuptools import find_packages, setup


TEST_REQUIREMENTS = ["pytest~=7.2"]

setup(
    name = "cxloperatorsdk",
    version = "1.0.5",
    license = "MIT",
    description = "CXL pipeline operator SDK",
    author = "Tongguo Pang",
    author_email = "tongguo.pang@contextlabs.com",
    packages = find_packages("src"),
    package_dir = {"": "src"},
    extras_require = {
        "tests": TEST_REQUIREMENTS,
    },
)



# from setuptools import setup
#
# if __name__ == "__main__":
#     setup()