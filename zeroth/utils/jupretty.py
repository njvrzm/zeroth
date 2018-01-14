import pygments
from pygments.lexers import HtmlLexer, JavascriptLexer
from pygments.formatters import HtmlFormatter
from IPython.display import display, HTML

from .onlyonce import onlyonce

formatter = HtmlFormatter()

@onlyonce
def setUp():
    display(HTML('<style>{}</style>'.format(
            formatter.get_style_defs('.highlight'))))

def pretty(code:str, language:str) -> None:
    """ In a jupyter web notebook, displays the given code with syntax highlighting.

    :param language: the name of a language recognized by pygments
    :param code: A string containing code in that language"""

    setUp()
    lexer = pygments.lexers.get_lexer_by_name(language)
    display(HTML(pygments.highlight(code, lexer, formatter)))
