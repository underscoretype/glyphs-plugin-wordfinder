# encoding: utf-8

###########################################################################################################
#
#
#   Show Me The Words
#
#   Read the docs:
#   https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/SelectTool
#
#
###########################################################################################################

import objc, sys
from GlyphsApp import *
from GlyphsApp.plugins import *

from wordfinder import *

class ShowMeTheWords(GeneralPlugin):
    
    def settings(self):
        self.name = Glyphs.localize({'en': u'Show Me The Words'})


    def start(self):
        # create a menu item with its name, and a reference to the method it shoud invoke:
        newMenuItem = NSMenuItem(self.name, self.showWords)
        
        # append the menu item to one of the menus:
        Glyphs.menu[GLYPH_MENU].append(newMenuItem)


    def showWords(self, foo):
        font = Glyphs.fonts[0]
        tab = font.currentTab
        glyphs = []
        words = []
        selected = []
        test = ""

        for glyph in Glyphs.font.glyphs:
            if glyph.unicode:
                glyphs.append(unichr(int(glyph.unicode, 16)))

        if not glyphs:
            return

        for layer in Glyphs.fonts[0].selectedLayers:
            glyph = layer.parent
            if glyph.unicode:
                selected.append( unichr(int(glyph.unicode, 16) ) )

        if not selected:
            return

        try:
            words, missing = wordfinder(glyphs, selected)
        except:
            e = sys.exc_info()[0]
        
        if words or missing:
            text = " ".join(words)            
            if len(missing) > 0:
                text = text + "\n\n" + " ".join(missing)

            if tab is None:
                Glyphs.font.newTab(text)
            else:
                tab.text = tab.text + "\n" + text

        else:
            # print "No matching words found"