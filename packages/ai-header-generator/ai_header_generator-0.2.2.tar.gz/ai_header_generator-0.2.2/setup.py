from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="ai_header_generator",
    version="0.2.2",
    packages=find_packages(include=['ai_header_generator', 'ai_header_generator.*']),
    install_requires=[
        "openai",'argparse','configparser','jsonpickle'
    ],
    entry_points={
        "console_scripts": [
            "ai-header-generator=cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        '': ['*.json'],
    },
    url="https://github.com/GSejas/ai-generated-meta",
    author="Jorge Sequeira",
    author_email="jsequeira03@gmail.com",
    maintainer="Jorge Sequeira",
    maintainer_email="jsequeira03@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown"
)