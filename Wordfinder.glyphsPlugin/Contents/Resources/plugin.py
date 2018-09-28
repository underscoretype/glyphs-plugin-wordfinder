#!/usr/bin/python
# -*- coding: utf-8 -*-

###########################################################################################################
#
#
#   Wordfinder - A Glyphs App plugin by Underscore Type
#
#   Copyright Johannes "kontur" Neumeier 2018
#   https://underscoretype.com
#
#
###########################################################################################################

import objc, sys, re
from GlyphsApp import *
from GlyphsApp.plugins import *

from wordfinder import *
from texthelper import unichar

class Wordfinder(GeneralPlugin):
    
    def settings(self):
        self.name = Glyphs.localize({'en': u'Wordfinder'})


    def start(self):
        # create a menu item with its name, and a reference to the method it shoud invoke:
        newMenuItem = NSMenuItem(self.name, self.findWords)
        
        # append the menu item to one of the menus:
        Glyphs.menu[GLYPH_MENU].append(newMenuItem)

        print "Wordfinder: You can set a custom directory from which to read text files as a font Custom Parameter called 'Wordfinder'"


    def getGlyphUnicodes(self, glyph):
        """
        Helper function: Given a selected glyph, try return a list of Glyphs glyph.unicode strings
        Can be one or more unicodes of the glyph, or its components
        """
        font = Glyphs.fonts[0]

        if glyph.unicode:
            return [glyph.unicode]
            
        match = re.match('([^.]*)', glyph.name)
        unicodes = []

        # following Glyph’s conventions, glyphs with a dot in the name
        # are variants; let’s try to extract unicodes from either a base
        # glyph or nested components
        # e.g. f.ss01 => f’s unicode
        # e.g. f_f_l.liga => f’s and l’s unicodes
        if match:
            basename = match.groups()[0]
            g = font.glyphs[basename]
            
            if g:
                if g.unicode:
                    # if what we extracted is a glyph and has a unicode, return that
                    unicodes.append(g.unicode)
            
            else:
                # if the extracted part is in itself not a glyph, let’s try from
                # components
                if glyph.layers[font.selectedFontMaster.name].components:
                    for c in glyph.layers[font.selectedFontMaster.name].components:
                        nested = self.getGlyphUnicodes(c.component)
                        if nested:
                            unicodes = unicodes + nested
                    
        return list(set(unicodes))


    def findWords(self, menuItem):
        font = Glyphs.fonts[0]
        tab = font.currentTab
        glyphs = []
        words = []
        selected = []

        for glyph in Glyphs.font.glyphs:
            if glyph.unicode:
                glyphs.append(unichar(int(glyph.unicode, 16)))

        if not glyphs:
            return

        # filter out non-word chars from the available glyphs
        glyphs = [g for g in glyphs if re.search('\W+', g, re.UNICODE) == None]

        if font.selectedLayers:
            for layer in font.selectedLayers:
                if layer.isMemberOfClass_(GSLayer):
                    glyph = layer.parent
                    unicodes = self.getGlyphUnicodes(glyph)
                    if unicodes:
                        selected = selected + [unichar(int(u, 16)) for u in unicodes]

        if not selected:
            return

        # filter out non-word chars from the selected glyphs
        # TODO in the future this might behave smarter, e.g. numbers or punctuation might be nice
        # to simple insert "dumbly" into the results
        selected = [s for s in selected if re.search('\W+', s, re.UNICODE) == None]

        try:
            words, missing = wordfinder(glyphs, selected, font.customParameters["Wordfinder"])
            if words or missing:
                text = " ".join(words)            
                if len(missing) > 0:
                    text = text + "\n" + "".join(missing)

                if tab is None:
                    Glyphs.font.newTab(text)
                else:
                    tab.text = tab.text + "\n" + text
        except:
            self.logToConsole(sys.exc_info()[0])
