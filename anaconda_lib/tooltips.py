
# Copyright (C) 2015 - Oscar Campos <oscar.campos@member.fsf.org>
# This program is Free Software see LICENSE file for details

import os
import glob
from string import Template

import sublime


class Tooltip(object):
    """Just a wrapper around Sublime Text 3 tooltips
    """

    themes = {}
    tooltips = {}
    loaded = False

    def __init__(self, theme):
        self.theme = theme

        if int(sublime.version()) < 3070:
            return

        if Tooltip.loaded is False:
            self._load_css_themes()
            self._load_tooltips()
            Tooltip.loaded = True

    def generate(self, tooltip, text):
        """Generate a tooltip with the given text
        """

        try:
            return self.tooltips[tooltip].safe_substitute(text)
        except KeyError as err:
            print('while generating tooltip: tooltip {} don\'t exists'.format(
                str(err))
            )
            return None

    def _load_tooltips(self):
        """Load tooltips templates from anaconda tooltips templates
        """

        template_files_pattern = os.path.join(
            os.path.dirname(__file__), '../', 'templates', 'tooltips', '*.tpl'
        )
        for template_file in glob.glob(template_files_pattern):
            with open(template_file, 'r', encoding='utf8') as tplfile:
                tplname = os.path.basename(template_file).split('.tpl')[0]
                try:
                    theme = self.themes[self.theme]
                except KeyError:
                    print('configured theme {} not found')
                    theme = self.themes['dark']
                finally:
                    tpldata = '<style>{}</style>{}'.format(
                        theme, tplfile.read()
                    )

                self.tooltips[tplname] = Template(tpldata)

    def _load_css_themes(self):
        """
        Load any css theme found in the anaconda CSS themes directory
        or in the User/Anaconda.themes directory
        """

        css_files_pattern = os.path.join(
            os.path.dirname(__file__), '../', 'css', '*.css')
        for css_file in glob.glob(css_files_pattern):
            print('anaconda: {} css theme loaded'.format(
                self._load_css(css_file))
            )

        packages = sublime.active_window().extract_variables()['packages']
        user_css_path = os.path.join(packages, 'User', 'Anaconda.themes')
        if os.path.exists(user_css_path):
            css_files_pattern = os.path.join(user_css_path, '*.css')
            for css_file in glob.glob(css_files_pattern):
                print(
                    'anaconda: {} user css theme loaded',
                    self._load_css(css_file)
                )

    def _load_css(self, css_file):
        """Load a css file
        """

        theme_name = os.path.basename(css_file).split('.css')[0]
        with open(css_file, 'r') as resource:
            self.themes[theme_name] = resource.read()

        return theme_name