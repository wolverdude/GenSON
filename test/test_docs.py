import os
import re
import unittest

try:
    import readme_renderer.rst
    HAS_README_RENDERER = True
except ImportError:
    HAS_README_RENDERER = False

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# PyPI assembles the long_description from these files (see setup.cfg)
DOC_FILES = ('README.rst', 'HISTORY.rst', 'AUTHORS.rst')

# Markdown syntax showing up in the rendered output means some
# Markdown slipped into the RST source and is rendering as literal
# text: a paragraph starting with a "## heading" or list marker, or a
# [link](...) anywhere
MARKDOWN_ARTIFACTS = re.compile(r'<p>\s*(#+ |\* |- )|\[[^\]]+\]\(')


def render(filename):
    with open(os.path.join(REPO_ROOT, filename)) as f:
        return readme_renderer.rst.render(f.read())


@unittest.skipUnless(HAS_README_RENDERER, 'readme_renderer is not installed')
class TestDocsRender(unittest.TestCase):
    """
    Render the docs with readme_renderer, the same library PyPI uses,
    so broken RST is caught before a release instead of on the project
    page. render() returns None when docutils reports an error.
    """

    def test_docs_render(self):
        for filename in DOC_FILES:
            with self.subTest(file=filename):
                self.assertIsNotNone(
                    render(filename),
                    '%s contains RST errors and will not render on PyPI'
                    % filename)

    def test_docs_contain_no_markdown_artifacts(self):
        for filename in DOC_FILES:
            with self.subTest(file=filename):
                output = render(filename)
                if output is None:
                    continue  # test_docs_render reports this case
                match = MARKDOWN_ARTIFACTS.search(output)
                self.assertIsNone(
                    match,
                    '%s renders Markdown syntax as literal text: %r'
                    % (filename, match and match.group(0)))
