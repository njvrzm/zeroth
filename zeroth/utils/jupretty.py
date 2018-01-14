import pygments
from pygments.lexers import HtmlLexer, JavascriptLexer
from pygments.formatters import HtmlFormatter

from IPython.display import display, HTML

formatter = HtmlFormatter()

showed_style = False
def setUp():
    global showed_style
    if not showed_style:
        display(HTML('<style>{}</style>'.format(formatter.get_style_defs('.highlight'))))
        showed_style = True

def pretty(code, language):
    setUp()
    lexer = pygments.lexers.get_lexer_by_name(language)
    display(HTML(pygments.highlight(code, lexer, formatter)))



    
