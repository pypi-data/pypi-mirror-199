import pytest
from ai_header_generator.header_generator import MetaGenerator

def test_init():
    # test if a HeaderGenerator instance is created
    hg = MetaGenerator()
    assert isinstance(hg, MetaGenerator)

def test_config_file_read():

    # test if the config file is parsed correctly
    hg = MetaGenerator()

    assert hg.config.get("openai", "api_key") == "YOUR_API_KEY"

    assert hg.config.get("project", "folder_path") == "./analysis"

    assert hg.config.get("project", "template_file") == "./template.json"


def test_template_read():

    # test if the template file is parsed correctly
    hg = MetaGenerator()

    assert hg.template.get("prompt") == "Code Analysis: {filename}"