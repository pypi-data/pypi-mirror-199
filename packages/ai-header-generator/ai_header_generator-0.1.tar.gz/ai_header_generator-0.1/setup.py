from setuptools import setup, find_packages

setup(
    name="ai_header_generator",
    version="0.1",
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
    }
)