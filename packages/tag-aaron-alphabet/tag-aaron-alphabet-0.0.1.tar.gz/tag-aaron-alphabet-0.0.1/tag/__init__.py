#!/usr/bin/python3


import os
import string
import tomli_w
import tempfile
import subprocess
import shutil
from argparse import ArgumentParser






                
    
class Tagging:
    def join(root, title, tags, ext):
        return os.path.join(root, " #".join([title] + tags) + ext)
    def tag(s):
        ans = s.strip()
        for ch in ans:
            if ch not in (string.ascii_letters + string.digits + '_'):
                raise TypeError(f"Illegal char {ascii(ch)} in {ascii('#'+ans)}. ")
        try:
            int(ans)
        except:
            return ans
        else:
            raise TypeError()

    def and_operation(*operands):
        return all(operands)
    def or_operation(*operands):
        return any(operands)
    def xor_operation(*operands):
        return bool(sum(int(x) for x in operands) % 2)
    def binary_operation(first_operand, operator, second_operand):
        return {
            '&': Tagging.and_operation,
            '|': Tagging.or_operation,
            '^': Tagging.xor_operation,
        }[operator](first_operand, second_operand)
    def not_operation(operand):
        return not operand
    def _eva(expr):
        expr = list(expr)
        while True:
            try:
                i = expr.index('~')
            except:
                break
            expr[i:i+2] = [Tagging.not_operation(expr[i+1])]
        while len(expr) > 1:
            expr[0:3] = [Tagging.binary_operation(*expr[0:3])]
        return expr[0]

    def eva(expr, tags):
        if type(expr) is not str:
            raise TypeError()
        if expr == "":
            return True

        tags = [Tagging.tag(x) for x in tags]

        ans = list()
        jump = True
        for ch in expr.strip():
            if ch == '*':
                ans.append(ch)
                jump = True
                continue
            if ch in Tagging.special_chars():
                ans.append(ch)
                jump = True
                continue
            if ch in string.whitespace:
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
            elif ans[i] in Tagging.special_chars():
                pass
            else:
                ans[i] = Tagging.tag(ans[i]) in tags
        
        while '(' in ans:
            i = None
            j = ans.index(')')
            for k in range(j, -1, -1):
                if ans[k] == '(':
                    i = k
                    break
            ans[i:j+1] = [Tagging._eva(ans[i+1:j])]
        return Tagging._eva(ans)
        
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
            #ans[part[0]].append(Tagging.tag(part[1:]))
        if len(set(ans['+']).intersection(set(ans['-']))) > 0:
            raise ValueError()
        return ans
        

    def special_chars():
        return list("~&|()")
    
    def change(tags, instr):
        ans = Tagging.unique_list(tags)
        for t in instr['+']:
            if t not in ans:
                ans.append(t)
        ans = [t for t in ans if (t not in instr['-'])]
        return ans
    
    def unique_list(iter):
        ans = list()
        for x in iter:
            if x not in ans:
                ans.append(x)
        return ans
        
        
    def files(inputs):
        for target in inputs:
            if os.path.isfile(target):
                yield target
            elif os.path.isdir(target):
                for root, dirs, filenames in os.walk(target, topdown=False):
                    for filename in filenames:
                        file = os.path.join(root, filename)
                        yield file
            else:
                raise FileNotFoundError()
    

class TaggedFile:
    def __init__(self, file):
        self._oldfile = file
        self.root, filename = os.path.split(file)
        y, self.ext = os.path.splitext(filename)
        self.title, *self.tags = y.split("#")
        try:
            self.title = TaggedFile.title(self.title)
            self.tags = TaggedFile.tags(self.tags)
        except BaseException as exc:
            raise TypeError(file) from exc
    def tags(tags):
        ans = list()
        for t in tags:
            u = Tagging.tag(t)
            if u not in ans:
                ans.append(u)
        return ans
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
    def __str__(self):
        return str(Tagging.join(self.root, self.title, self.tags, self.ext))
    def to_dict(self):
        ans = dict()
        ans['root'] = self.root
        ans['title'] = self.title
        ans['tags'] = self.tags
        ans['ext'] = self.ext
        return ans
    def to_item(self):
        return str(self), self.to_dict()
    def to_args(self):
        ans = [str(self)]
        for k, v in self.to_dict().items():
            ans += [f"-{k.replace('_', '-')}"]
            if type(v) in (list, tuple):
                ans += list(v)
            else:
                ans += [str(v)]
        return ans
    def add_tags(self, *tags):
        tags = [Tagging.tag(t) for t in tags]
        for t in tags:
            if t not in self.tags:
                self.tags.append(t)
    def rm_tags(self, *tags):
        tags = [Tagging.tag(t) for t in tags]
        self.tags = [t for t in self.tags if (t not in tags)]
        for t in tags:
            if t not in self.tags:
                self.tags.append(t)
    def change(self, line):
        if line is None:
            return
        #self.title = Tagging.title(self.title)
        info = Tagging.parse_change(line)
        self.add_tags(*info['+'])
        self.rm_tags(*info['-'])
    def eva(self, expr):
        return Tagging.eva(expr=expr, tags=self.tags)
    def update(self):
        if not os.path.isfile(self._oldfile):
            raise FileNotFoundError(self._oldfile)
        if self._oldfile == str(self):
            return
        while os.path.exists(str(self)):
            self.title += "--alt"
        #raise ValueError('\n'.join((self._oldfile, str(self))))
        #print("hi")
        shutil.move(self._oldfile, str(self))
        self._oldfile = str(self)
    def exec(self, prog):
        if prog is None:
            return
        subprocess.run([prog] + self.to_args(), check=True)
    def go(self, *, filter, c, i, x, v):
        if not self.eva(filter):
            return False
        if (not i)and(c is None)and(x is None)and(not v):
            print(str(self))
        if v:
            print(tomli_w.dumps({str(self): self.to_dict()}))
            #print(str(self))
            #for key, value in self.to_dict():
            #    print(f"{ascii(key)} = {ascii(value)}")
        if i:
            if v:
                line = input()
            else:
                line = input(str(self))
            line = line.strip()
            if line == "#":
                return True
            self.change(line)
        self.change(c)
        self.update()
        self.exec(x)
        return False
        
        







def run(*, I, **kwargs):
    files = Tagging.files(I)
    files = Tagging.unique_list(files)
    for file in files:
        if TaggedFile(file).go(**kwargs):
            break

        
        
    
    
    

def main():
    parser = ArgumentParser(
        fromfile_prefix_chars="@",
        allow_abbrev=False,
    )
    parser.add_argument('filter', nargs='?', default="")
    parser.add_argument('-i', '--interactive', dest='i', action='store_true', default=False)
    parser.add_argument('-v', '--verbose', dest='v', action='store_true', default=False)
    parser.add_argument('-c', '--change', dest='c')
    parser.add_argument('-x', '--exec', dest='x')
    parser.add_argument('-I', '--inputs', dest='I', default=['.'], nargs='+')
    #parser.add_argument('--out', '-o', dest='o')
    ns = parser.parse_args()
    run(**vars(ns))






if __name__ == '__main__':
    main()
