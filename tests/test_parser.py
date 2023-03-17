import pytest

from stable_discord.parser import PromptParser


def test_parse_input_null_prompt():
    p = PromptParser()
    known, unknown = p.parse_input("")
    assert known == {"prompt": "", "cfg": 7.5, "steps": 50}
    assert unknown == ""


def test_parse_input_basic_prompt():
    p = PromptParser()
    known, unknown = p.parse_input("A man riding a horse")
    assert known == {"prompt": "A man riding a horse", "cfg": 7.5, "steps": 50}
    assert unknown == ""


def test_parse_input_cfg():
    p = PromptParser()

    known, unknown = p.parse_input("A man riding a horse --cfg 5")
    assert known == {"prompt": "A man riding a horse", "cfg": 5.0, "steps": 50}
    assert unknown == ""

    known, unknown = p.parse_input("--cfg 9.1 A man riding a horse")
    assert known == {"prompt": "A man riding a horse", "cfg": 9.1, "steps": 50}
    assert unknown == ""

    known, unknown = p.parse_input("A man riding a horse --cfg 1 --cfg 6")
    assert known == {"prompt": "A man riding a horse", "cfg": 6.0, "steps": 50}
    assert unknown == ""


def test_parse_input_steps():
    p = PromptParser()

    known, unknown = p.parse_input("A man riding a horse --steps 75")
    assert known == {"prompt": "A man riding a horse", "cfg": 7.5, "steps": 75}
    assert unknown == ""

    known, unknown = p.parse_input("--steps 25 A man riding a horse")
    assert known == {"prompt": "A man riding a horse", "cfg": 7.5, "steps": 25}
    assert unknown == ""

    known, unknown = p.parse_input("A man riding a horse --steps 36 --steps 42")
    assert known == {"prompt": "A man riding a horse", "cfg": 7.5, "steps": 42}
    assert unknown == ""


def test_parse_input_unknown_args():
    p = PromptParser()

    known, unknown = p.parse_input("A man riding a horse --fake_arg")
    assert known == {"prompt": "A man riding a horse", "cfg": 7.5, "steps": 50}
    assert unknown == "--fake_arg"

    known, unknown = p.parse_input("A man riding a horse --beep boop")
    assert known == {"prompt": "A man riding a horse", "cfg": 7.5, "steps": 50}
    assert unknown == "--beep boop"


def test_help_text():
    p = PromptParser()
    expected = """usage: StableDiscord [--cfg CFG] [--steps STEPS] [prompt ...]

positional arguments:
  prompt         The prompt is a positional argument meaning text not assigned
                 to an argument is presumed to bethe prompt.

options:
  --cfg CFG      A float value for the 'Context Free Guidance' parameter.
                 Sometimes called 'style' in other models. (Defaults to 7.5)
  --steps STEPS  The number of diffusion steps. More will take longer, but
                 usually returns better results. (Defaults to 50)
"""
    assert p.help_text == expected


def test_quote_in_prompt():
    p = PromptParser()
    known, unknown = p.parse_input("a cute cat's face.")
    assert known == {"prompt": "a cute cat's face.", "cfg": 7.5, "steps": 50}
    assert unknown == ""

    known, unknown = p.parse_input("a man's cat's face.")
    assert known == {"prompt": "a man's cat's face.", "cfg": 7.5, "steps": 50}
    assert unknown == ""


def test_double_quote_in_prompt():
    p = PromptParser()
    with pytest.raises(ValueError) as e:
        known, unknown = p.parse_input('A man saying "hello.')
        assert known == {"prompt": 'A man saying "hello" .', "cfg": 7.5, "steps": 50}
        assert unknown == ""
        assert e.value == "No closing quotation"

    known, unknown = p.parse_input('A man saying "hello".')
    assert known == {"prompt": 'A man saying "hello" .', "cfg": 7.5, "steps": 50}
    assert unknown == ""


def test_parentheses_in_prompt():
    p = PromptParser()
    known, unknown = p.parse_input("A man (with his cat) eating a pizza.")
    assert known == {"prompt": "A man (with his cat) eating a pizza.", "cfg": 7.5, "steps": 50}
    assert unknown == ""

    known, unknown = p.parse_input("A man (with his cat eating a pizza.")
    assert known == {"prompt": "A man (with his cat eating a pizza.", "cfg": 7.5, "steps": 50}
    assert unknown == ""


def test_mangled_arg_names():
    p = PromptParser()
    known, unknown = p.parse_input("A man in a chair -- steps")
    assert known == {"prompt": "A man in a chair steps", "cfg": 7.5, "steps": 50}
    assert unknown == ""

    known, unknown = p.parse_input("A man in a chair")
    assert known == {"prompt": "A man in a chair", "cfg": 7.5, "steps": 50}
    assert unknown == ""

    with pytest.raises(SystemExit) as e:
        known, unknown = p.parse_input("A man in a chair --step (500)")
        assert known == {"prompt": "A man in a chair", "cfg": 7.5, "steps": 50}
        assert unknown == "--step (500)"
        assert e.value == 2
