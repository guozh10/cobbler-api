#!/usr/bin/env python
# -*- coding:utf8 *-*
#guozhenhui

class Colour(object):
    def __init__(self,name):
        pass
        self.name  = name
    def Green(self):
        pass
        return  "\033[1;32;40m%s \033[0m"%self.name
    def Red(self):
        pass
        return "\033[1;31;40m%s \033[0m" % self.name
    def Yellow(self):
        pass
        return "\033[1;33;40m%s \033[0m" % self.name

    def Blue(self):
        pass
        return "\033[1;36;40m%s \033[0m" % self.name
if __name__ == "__main__":
    s =  Colour('请输入：')
    print(s.Green())
    print(s.Red())
    print(s.Yellow())
    print(s.Blue())
