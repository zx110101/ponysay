#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
ponysay - Ponysay, cowsay reimplementation for ponies
Copyright (C) 2012, 2013  Erkin Batu Altunbaş et al.

This program is free software. It comes without any warranty, to
the extent permitted by applicable law. You can redistribute it
and/or modify it under the terms of the Do What The Fuck You Want
To Public License, Version 2, as published by Sam Hocevar. See
http://sam.zoy.org/wtfpl/COPYING for more details.
'''
from common import *



'''
Balloon format class
'''
class Balloon():
    '''
    Constructor
    
    @param  link:str        The \-directional balloon line character
    @param  linkmirror:str  The /-directional balloon line character
    @param  ww:str          See the info manual
    @param  ee:str          See the info manual
    @param  nw:list<str>    See the info manual
    @param  nnw:list<str>   See the info manual
    @param  n:list<str>     See the info manual
    @param  nne:list<str>   See the info manual
    @param  ne:list<str>    See the info manual
    @param  nee:str         See the info manual
    @param  e:str           See the info manual
    @param  see:str         See the info manual
    @param  se:list<str>    See the info manual
    @param  sse:list<str>   See the info manual
    @param  s:list<str>     See the info manual
    @param  ssw:list<str>   See the info manual
    @param  sw:list<str>    See the info manual
    @param  sww:str         See the info manual
    @param  w:str           See the info manual
    @param  nww:str         See the info manual
    '''
    def __init__(self, link, linkmirror, ww, ee, nw, nnw, n, nne, ne, nee, e, see, se, sse, s, ssw, sw, sww, w, nww):
        (self.link, self.linkmirror) = (link, linkmirror)
        (self.ww, self.ee) = (ww, ee)
        (self.nw, self.ne, self.se, self.sw) = (nw, ne, se, sw)
        (self.nnw, self.n, self.nne) = (nnw, n, nne)
        (self.nee, self.e, self.see) = (nee, e, see)
        (self.sse, self.s, self.ssw) = (sse, s, ssw)
        (self.sww, self.w, self.nww) = (sww, w, nww)
        
        _ne = max(ne, key = UCS.dispLen)
        _nw = max(nw, key = UCS.dispLen)
        _se = max(se, key = UCS.dispLen)
        _sw = max(sw, key = UCS.dispLen)
        
        minE = UCS.dispLen(max([_ne, nee, e, see, _se, ee], key = UCS.dispLen))
        minW = UCS.dispLen(max([_nw, nww, e, sww, _sw, ww], key = UCS.dispLen))
        minN = len(max([ne, nne, n, nnw, nw], key = len))
        minS = len(max([se, sse, s, ssw, sw], key = len))
        
        self.minwidth  = minE + minE
        self.minheight = minN + minS
    
    
    '''
    Generates a balloon with a message
    
    @param   minw:int          The minimum number of columns of the balloon
    @param   minh:int          The minimum number of lines of the balloon
    @param   lines:list<str>   The text lines to display
    @param   lencalc:int(str)  Function used to compute the length of a text line
    @return  :str              The balloon as a formated string
    '''
    def get(self, minw, minh, lines, lencalc):
        h = self.minheight + len(lines)
        w = self.minwidth + lencalc(max(lines, key = lencalc))
        if w < minw:  w = minw
        if h < minh:  h = minh
        
        if len(lines) > 1:
            (ws, es) = ({0 : self.nww, len(lines) - 1 : self.sww}, {0 : self.nee, len(lines) - 1 : self.see})
            for j in range(1, len(lines) - 1):
                ws[j] = self.w
                es[j] = self.e
        else:
            (ws, es) = ({0 : self.ww}, {0 : self.ee})
        
        rc = []
        
        for j in range(0, len(self.n)):
            outer = UCS.dispLen(self.nw[j]) + UCS.dispLen(self.ne[j])
            inner = UCS.dispLen(self.nnw[j]) + UCS.dispLen(self.nne[j])
            if outer + inner <= w:
                rc.append(self.nw[j] + self.nnw[j] + self.n[j] * (w - outer - inner) + self.nne[j] + self.ne[j])
            else:
                rc.append(self.nw[j] + self.n[j] * (w - outer) + self.ne[j])
        
        for j in range(0, len(lines)):
            rc.append(ws[j] + lines[j] + ' ' * (w - lencalc(lines[j]) - UCS.dispLen(self.w) - UCS.dispLen(self.e)) + es[j])
        
        for j in range(0, len(self.s)):
            outer = UCS.dispLen(self.sw[j]) + UCS.dispLen(self.se[j])
            inner = UCS.dispLen(self.ssw[j]) + UCS.dispLen(self.sse[j])
            if outer + inner <= w:
                rc.append(self.sw[j] + self.ssw[j] + self.s[j] * (w - outer - inner) + self.sse[j] + self.se[j])
            else:
                rc.append(self.sw[j] + self.s[j] * (w - outer) + self.se[j])
        
        return '\n'.join(rc)

