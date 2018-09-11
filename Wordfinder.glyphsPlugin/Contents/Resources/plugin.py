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

class Wordfinder(GeneralPlugin):
    
    def settings(self):
        self.name = Glyphs.localize({'en': u'Wordfinder'})


    def start(self):
        # create a menu item with its name, and a reference to the method it shoud invoke:
        newMenuItem = NSMenuItem(self.name, self.findWords)
        
        # append the menu item to one of the menus:
        Glyphs.menu[GLYPH_MENU].append(newMenuItem)

        print "Wordfinder: You can set a custom directory from which to read text files as a font Custom Parameter called 'Wordfinder'"


    def findWords(self, menuItem):
        font = Glyphs.fonts[0]
        tab = font.currentTab
        glyphs = []
        words = []
        selected = []

        for glyph in Glyphs.font.glyphs:
            if glyph.unicode:
                glyphs.append(unichr(int(glyph.unicode, 16)))

        if not glyphs:
            return

        # filter out non-word chars from the available glyphs
        glyphs = [g for g in glyphs if re.search('\W+', g, re.UNICODE) == None]

        if font.selectedLayers:
            for layer in font.selectedLayers:
                glyph = layer.parent
                if glyph.unicode:
                    selected.append(unichr(int(glyph.unicode, 16)))

        if not selected:
            return

        # filter out non-word chars from the selected glyphs
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
