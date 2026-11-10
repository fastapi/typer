from pathlib import Path
from posixpath import relpath

from markdown import Markdown
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from mkdocstrings import MkdocstringsInnerExtension
from zensical.extensions.context import ContextPreprocessor


class AgentBannerPreprocessor(Preprocessor):
    def run(self, lines: list[str]) -> list[str]:
        # Docstrings render their own Markdown inside an API reference page.
        if any(
            isinstance(extension, MkdocstringsInnerExtension)
            for extension in self.md.registeredExtensions
        ):
            return lines

        context = ContextPreprocessor.from_markdown(self.md)
        if context is None or context.page.path == "ai-development.md":
            return lines

        banner_path = (
            Path(__file__).resolve().parent.parent / "includes/agent-banner.md"
        )
        banner = banner_path.read_text(encoding="utf-8").strip()
        guide_path = relpath(
            "ai-development.md", Path(context.page.path).parent.as_posix()
        )
        banner = banner.replace("(ai-development.md)", f"({guide_path})")
        content = "\n".join(lines)
        marker = "<!-- agent-banner -->"
        if marker in content:
            return content.replace(marker, banner).splitlines()

        header, _, body = content.lstrip().partition("\n")
        if header == "#" or header.startswith("# "):
            return f"{header}\n\n{banner}\n\n{body.lstrip()}".splitlines()
        return f"{banner}\n\n{content}".splitlines()


class AgentBannerExtension(Extension):
    def extendMarkdown(self, md: Markdown) -> None:
        # Insert the notice before macros and fenced code blocks are processed.
        md.preprocessors.register(AgentBannerPreprocessor(md), "agent_banner", 36)


def makeExtension() -> AgentBannerExtension:
    return AgentBannerExtension()
