# -*- coding: utf-8 -*-
#
# Copyright 2022 Michael Samoglyadov
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Jinja templates rendering cli tool."""

import argparse
import json
import logging
import sys
import os

import jinja2


__version__ = '0.1'
__author__ = 'Michael Samoglyadov'
__license__ = 'Apache License 2.0'
__website__ = 'https://github.com/mr-mixas/jtr'

log = logging.getLogger(name=__name__)


class App(object):
    """Command line Jinja templates renderer."""

    def __init__(self, args=None):
        """Initialize app."""
        self.argparser = self.get_argparser(description=__doc__)
        self.args = self.argparser.parse_args(args=args)

    def _set_log_level(self, level):
        if level == 'DEBUG':
            fmt = '%(asctime)s %(levelname)s %(module)s:%(lineno)d %(message)s'
        else:
            fmt = '%(asctime)s %(levelname)-8s %(message)s'

        logging.basicConfig(format=fmt, level=level, force=True)

        return level

    def get_argparser(self, description=None):
        """Return configured arguments parser."""
        parser = argparse.ArgumentParser(
            description=description,
            parents=(
                self.get_templates_args_parser(),
                self.get_variables_args_parser(),
                self.get_output_args_parser(),
                self.get_miscellaneous_args_parser(),
            ),
        )

        return parser

    def get_templates_args_parser(self):
        """Return templates related arguments parser."""
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument(
            'template',
            type=os.path.normpath,
            help='jinja temlate file',
        )

        return parser

    def get_variables_args_parser(self):
        """Return template variables related arguments parser."""
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument(
            'vars',
            nargs='?',
            default=sys.stdin,
            metavar='variables',
            type=argparse.FileType(),
            help='template variables file (JSON), STDIN used if omitted',
        )

        return parser

    def get_output_args_parser(self):
        """Return output arguments parser."""
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument(
            '--out',
            default=sys.stdout,
            metavar='FILE',
            type=argparse.FileType('w'),
            help='output file; STDOUT used by default',
        )

        return parser

    def get_miscellaneous_args_parser(self):
        """Return miscellaneous arguments parser."""
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument(
            '-l', '--log-level',
            choices=('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'),
            default='ERROR',
            help='logging level; default is %(default)s',
            type=self._set_log_level,
        )
        parser.add_argument(
            '--version',
            action='version',
            version='%(prog)s {}'.format(__version__),
            help='print version and exit',
        )

        return parser

    def get_jinja_env(self):
        """Return configured Jinja environment."""
        return jinja2.Environment(
            extensions=self.get_jinja_env_extensions(),
            loader=self.get_jinja_templates_loader(),
            **self.get_jinja_env_kwargs(),
        )

    def get_jinja_env_extensions(self):
        """Return list of used jinja extensions."""
        return (
            'jinja2.ext.debug',
            'jinja2.ext.do',
            'jinja2.ext.loopcontrols',
        )

    def get_jinja_env_kwargs(self):
        """Return kwargs for Jinja environment."""
        return {
            'keep_trailing_newline': True,
        }

    def get_jinja_templates_loader(self):
        """Return templates loader for Jinja environment."""
        return jinja2.FileSystemLoader(
            self.get_jinja_templates_loader_searchpath(),
            followlinks=True,
        )

    def get_jinja_templates_loader_searchpath(self):
        """Return searchpath for Jinja templates loader."""
        return '.'  # TODO

    def get_template_variables(self):
        """Return dict with variables for template rendering."""
        log.info('Loading template variables from %s', self.args.vars.name)
        return json.load(self.args.vars)

    def run(self):
        """Cli entry point."""
        self.args.out.write(
            self.get_jinja_env().get_template(
                self.args.template,
            ).render(
                self.get_template_variables(),
            ),
        )

        return 0


def main():
    """Entry point."""
    App().run()


if __name__ == '__main__':
    main()
