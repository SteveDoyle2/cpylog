from IPython.core.display import display, HTML
_warning_to_color_map = {
    'DEBUG' : 'blue',
    'INFO' : 'green',
    'WARNING' : 'orange',
    'ERROR' : 'red',
    'EXCEPTION' : 'red',
    'CRITICAL' : 'red',
}
def write_html(typ: str, name: str, msg: str, encoding: str) -> None:
    """
    per:
     - https://stackoverflow.com/questions/16816013/is-it-possible-to-print-using-different-color-in-ipythons-notebook
     - https://stackoverflow.com/questions/25698448/how-to-embed-html-into-ipython-output
    """
    color = _warning_to_color_map.get(typ, 'red')
    display(HTML(f'<text style=color:{color}>{name + msg}</text>'))
