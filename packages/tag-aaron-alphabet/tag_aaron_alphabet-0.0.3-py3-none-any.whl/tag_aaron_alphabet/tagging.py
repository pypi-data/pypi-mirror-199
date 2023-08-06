
import os as _os
import string as _string
from .path import files
from .iterable import unique_list
from . import boolean


def join(root, title, tags, ext):
    return _os.path.join(root, " #".join([title] + tags) + ext)

def tag(s):
    ans = s.strip()
    for ch in ans:
        if ch not in (_string.ascii_letters + _string.digits + '_'):
            raise TypeError(f"Illegal char {ascii(ch)} in {ascii('#'+ans)}. ")
    try:
        int(ans)
    except:
        return ans
    else:
        raise TypeError()


def tags(tags):
    ans = list()
    return unique_list(tag(t) for t in tags)


def title(s):
    #s = ascii(s)[1:-1]
    s = s.strip()
    if s == "":
        return "_"
    ans = ""
    for ch in s:
        if len(ans) >= 64:
            break
        if ch in string.whitespace:
            ans += '-'
        elif ch in " \t\n()#.—'\"\\":
            ans += '-'
        else:
            #print(ch, ord(ch))
            ans += ch
    ans = ans.strip('-')
    #while "--" in ans:
    #    ans = ans.replace("--", '-')
    return ans

def _eva(expr):
    expr = list(expr)
    while True:
        try:
            i = expr.index('~')
        except:
            break
        expr[i:i+2] = [boolean.not_operation(expr[i+1])]
    while len(expr) > 1:
        expr[0:3] = [boolean.binary_operation(*expr[0:3])]
    return expr[0]

def eva(expr, tags):
    if type(expr) is not str:
        raise TypeError()
    if expr == "":
        return True

    tags = [tag(x) for x in tags]

    ans = list()
    jump = True
    for ch in expr.strip():
        if ch == '*':
            ans.append(ch)
            jump = True
            continue
        if ch in special_chars():
            ans.append(ch)
            jump = True
            continue
        if ch in _string.whitespace:
            jump = True
            continue
        if jump:
            ans.append("")
            jump = False
        ans[-1] += ch
        continue
        #raise ValueError()
    for i in range(len(ans)):
        if ans[i] == '*':
            ans[i] = (len(tags) > 0)
        elif ans[i] in special_chars():
            pass
        else:
            ans[i] = tag(ans[i]) in tags
    
    while '(' in ans:
        i = None
        j = ans.index(')')
        for k in range(j, -1, -1):
            if ans[k] == '(':
                i = k
                break
        ans[i:j+1] = [_eva(ans[i+1:j])]
    return _eva(ans)
    
def parse_change(line):
    parts = line.strip().split()
    ans = {'+': [], '-': [],}
    for part in parts:
        k = None
        for ch in part:
            if ch in ans.keys():
                k = ch
                ans[k].append("")
            else:
                ans[k][-1] += ch
        #ans[k].append(v)
        #ans[part[0]].append(tag(part[1:]))
    if len(set(ans['+']).intersection(set(ans['-']))) > 0:
        raise ValueError()
    return ans
    

def special_chars():
    return list("~&|()")

def change(tags, instr):
    ans = unique_list(tags)
    for t in instr['+']:
        if t not in ans:
            ans.append(t)
    ans = [t for t in ans if (t not in instr['-'])]
    return ans



