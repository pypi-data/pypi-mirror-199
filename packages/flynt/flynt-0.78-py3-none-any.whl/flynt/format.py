"""This module deals with quote types for strings.

It includes checking the quote type and changing it."""

import io
import re
import tokenize
from typing import Optional

lonely_quote = re.compile(r"(?<!\\)\"")
lonely_single_quote = re.compile(r"(?<!\\)\'")


class QuoteTypes:
    single = "'"
    double = '"'
    triple_single = "'''"
    triple_double = '"""'
    all = [triple_double, triple_single, single, double]


def get_quote_type(code: str) -> Optional[str]:
    from flynt.lexer.PyToken import PyToken

    g = tokenize.tokenize(io.BytesIO(code.encode("utf-8")).readline)
    next(g)
    token = PyToken(next(g))

    return token.get_quote_type()


def remove_quotes(code: str) -> str:
    quote_type = get_quote_type(code)
    if quote_type:
        return code[len(quote_type) : -len(quote_type)]
    return code


def set_quote_type(code: str, quote_type: str) -> str:
    if code[0] == "f":
        prefix, body = "f", remove_quotes(code[1:])
    else:
        prefix, body = "", remove_quotes(code)
    if quote_type in (QuoteTypes.single, QuoteTypes.triple_double):
        if body[-2:] == '\\"':
            body = f'{body[:-2]}"'
    elif quote_type is QuoteTypes.double:
        body = lonely_quote.sub('\\"', body)

    if quote_type == QuoteTypes.single:
        body = lonely_single_quote.sub("\\'", body)

    return prefix + quote_type + body + quote_type
