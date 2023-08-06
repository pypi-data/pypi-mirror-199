
import os
import string
import tomli_w
import subprocess
import shutil

from . import tagging

class TaggedFile:
    def __init__(self, file):
        self._oldfile = file
        self.root, filename = os.path.split(file)
        y, self.ext = os.path.splitext(filename)
        self.title, *self.tags = y.split("#")
        try:
            self.title = tagging.title(self.title)
            self.tags = tagging.tags(self.tags)
        except BaseException as exc:
            raise TypeError(file) from exc
    def __str__(self):
        return str(tagging.join(self.root, self.title, self.tags, self.ext))
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
        tags = [tagging.tag(t) for t in tags]
        for t in tags:
            if t not in self.tags:
                self.tags.append(t)
    def rm_tags(self, *tags):
        tags = [tagging.tag(t) for t in tags]
        self.tags = [t for t in self.tags if (t not in tags)]
        for t in tags:
            if t not in self.tags:
                self.tags.append(t)
    def change(self, line):
        if line is None:
            return
        #self.title = tagging.title(self.title)
        info = tagging.parse_change(line)
        self.add_tags(*info['+'])
        self.rm_tags(*info['-'])
    def eva(self, expr):
        return tagging.eva(expr=expr, tags=self.tags)
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
        
     