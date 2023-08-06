print("Hello PyPI")
from rich.pretty import pprint

def p(content: str):
    pprint(content, expand_all=True)
