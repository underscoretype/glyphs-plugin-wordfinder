# Wordfinder

**A simple Glyphs App plugin to find words that contain the selected glyphs. The plugin is ideal to quickly view one or more glyphs in a word.**

![Wordfinder plugin](https://raw.githubusercontent.com/underscoretype/glyphs-plugin-wordfinder/master/Wordfinder.png)

☞ After installation the plugin is available under *Glyph > Wordfinder*

☞ You need to have glyphs selected for the plugin to find anything *:-)*

☞ Only words that can be written with the glyphs present in your font will searched

☞ Only words! *(for now)*

## Installation

After installation the plugin is available under *Glyph > Wordfinder*

To set a keyboard shortcut go to your Mac *System Preferences > Keyboard > Shortcuts > App Shortcuts* and add a new shortcut by pressing `+`: Then select *Glyphs* and enter the *Menu Title* "Wordfinder" and finally select a *Keyboard Shortcut* of your choosing.

## Usage

You can either select glyphs in the Font view or in a tab. Wordfinder will then look for words that include all of your glyphs.

When selecting glyphs in the Font view a new tab with those words will be opened.

![Using Wordfinder in a font view](https://raw.githubusercontent.com/underscoretype/glyphs-plugin-wordfinder/master/img/wordfinder-font.gif)

When selecting glyphs in a tab those words will be added at the end of the tab.

![Using Wordfinder in a tab](https://raw.githubusercontent.com/underscoretype/glyphs-plugin-wordfinder/master/img/wordfinder-tab.gif)

Note that selecting a large number of glyphs is not advisable, since the plugin will search for a large amount of words to "use" all the glyphs you have selected.

## Customising

You can alter the text dictionary from which to find words by adding a *Custom Parameter* `Wordfinder` to your font. The value should be a path to a folder from which all files will be read and words extracted from. Note that this should be a full path. If no words could be found, the default dictionary is used.

![Setting the 'Wordfinder' custom parameter](https://raw.githubusercontent.com/underscoretype/glyphs-plugin-wordfinder/master/img/wordfinder-custom-parameters.png)

### How does it work?

A lot of effort has gone into making the plugin work *automagically*. With the plugin comes a wordlist extracted from the [multi-script version of the declaration of human rights](https://unicode.org/udhr/assemblies/full_all.txt) to cover as many scripts as possible. The plugin performs many optimisations on the fly and caches results to be able to find results for all selected glyphs **with as little words as possible**. Selecting many glyphs at once thus makes it impossible to find single words, so more words will need to be found to cover all selected glyphs.

If you want to **perform even faster searches** or use your own dictionary of possible results consider adding those as described above under "Customizing". Since the default dictionary tries to be very inclusive in terms of script support it also has overhead when scanning for words. An ideal word list should have good glyph coverage for the script of the font and a balance of mid to long words.

### About

[Wordfinder](https://github.com/underscoretype/glyphs-plugin-wordfinder) is brought to you by [Underscore Type](https://underscoretype.com).

Release under [GNU General Public License v3.0](https://github.com/underscoretype/glyphs-plugin-wordfinder/master/LICENSE.md).

© Johannes "kontur" Neumeier 2018