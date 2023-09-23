import textwrap
from ai_driver.retrieval.qa import wrap_text_preserve_newlines


def test_wrap_text_preserve_newlines():
    text = "This is a long line of text that should be wrapped to fit within the specified width. It also contains\na newline character that should be preserved."
    expected_output = "This is a long line of text that should be wrapped\nto fit within the specified width. It also\ncontains\na newline character that should be preserved."
    assert wrap_text_preserve_newlines(text, width=50) == expected_output

    text = "This is another long line of text that should be wrapped to fit within the specified width. It also contains\nmultiple newline characters that should be preserved.\n\nThis is a new paragraph that should be wrapped separately."
    expected_output = "This is another long line of text that\nshould be wrapped to fit within the\nspecified width. It also contains\nmultiple newline characters that should\nbe preserved.\n\nThis is a new paragraph that should be\nwrapped separately."
    assert wrap_text_preserve_newlines(text, width=40) == expected_output
