from typer.rich_utils import rich_render_text


def test_rich_render_text_returns_plain_text():
    text = "Hello 🌍"
    result = rich_render_text(text)
    assert "Hello" in result
    assert "🌍" in result
