from typer.rich_utils import rich_render_text


def test_rich_render_text_removes_markup_and_preserves_unicode():
    text = "[bold]Hello[/bold] 🌍"
    result = rich_render_text(text)
    assert result == "Hello 🌍"
