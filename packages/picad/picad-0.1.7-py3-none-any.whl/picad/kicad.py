import re
import typing

# foss: the clever regex magic below is lifted verbatim from the KiCad repo here:
# https://gitlab.com/kicad/libraries/kicad-library-utils/-/blob/master/common/sexpr.py


term_regex = r"""(?mx)
    \s*(?:
        (?P<brackl>\()|
        (?P<brackr>\))|
        (?P<num>[+-]?\d+\.\d+(?=[\ \)])|\-?\d+(?=[\ \)]))|
        (?P<sq>"([^"]|(?<=\\)")*")|
        (?P<s>[^(^)\s]+)
       )"""

# foss: here I have modified it a bit to make it more readable

# open_bracket_pattern = r"""\("""
# close_bracket_pattern = r"""\)"""
# number_pattern = r"""[+-]?\d+\.\d+(?=[\ \)])|\-?\d+(?=[\ \)])"""
# quoted_string_pattern = r""""([^"]|(?<=\\)")*""""
# string_pattern = r"""[^(^)\s]+"""

# term_regex = fr"""(?mx)
#     \s*(?:
#         (?P<open_bracket>{open_bracket_pattern})|
#         (?P<close_bracket>\))|
#         (?P<number>[+-]?\d+\.\d+(?=[\ \)])|\-?\d+(?=[\ \)]))|
#         (?P<quoted_string>"([^"]|(?<=\\)")*")|
#         (?P<string>[^(^)\s]+)
#        )"""

# foss: ...and the rest is heavily based on same:


def _is_integer(n):
    try:
        int(n)
    except:
        return False

    return True


def _is_numeric(n):
    try:
        int(n)
    except:
        try:
            float(n)
        except:
            return False

    return True


def parse_sexpr(sexp: str) -> typing.Any:
    stack = []
    out = []

    all = re.findall(term_regex, sexp)

    for i, item in enumerate(all):

        if '(' == item[0]:
            stack.append(out)
            out = []
        elif ')' == item[1]:
            assert stack, "Trouble with nesting of brackets"
            tmpout, out = out, stack.pop(-1)
            out.append(tmpout)
        elif '' != item[2]:
            if _is_integer(item[2]):
                out.append(int(item[2]))
            else:
                out.append(float(item[2]))
        elif '' != item[3]:
            out.append(item[3][1:-1].replace(r"\"", '"'))
        elif '' != item[4]:
            out.append(item[4])
        elif '' != item[5]:
            out.append(item[5])
        else:
            pass

    return out[0]


def build_sexpr(exp, level: int = 0) -> str:

    if isinstance(exp, list):
        indent = '  ' * level
        content = " ".join(build_sexpr(x, level=level+1) for x in exp)
        return f"\n{indent}({content})"

    if isinstance(exp, float) or isinstance(exp, int):
        return str(exp)

    if isinstance(exp, str):
        exp = exp.replace("\"", "\\\"")

        if len(exp) == 0 or (' ' in exp) or ('.' in exp) or ('(' in exp) or ('\n' in exp) or _is_numeric(exp):
            exp = f'"{exp}"'

        exp = exp.replace("\n", "\\n")

        return exp

    raise RuntimeError("bad sexpr type")
