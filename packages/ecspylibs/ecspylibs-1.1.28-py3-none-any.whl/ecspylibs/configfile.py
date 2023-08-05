#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Do NOT edit this system file by hand -- use git.  See "URL to git source" below.
#
# Author:        $Id: Thomas R. Stevenson <aa0026@wayne.edu> $
#
# Last Changed:  $Date: Tue Feb 21 12:10:36 2023 -0500 $
#
# URL to git source: $URL: git@git.wayne.edu:ECS_Projects/ECSpylibs.git $
#

"""
Doc String
"""

import sys
import json
import os

from dataclasses import dataclass
from json.decoder import JSONDecodeError
from pathlib import Path, PosixPath

import pandas as pd
import toml
import yaml

from lxml import etree
from lxml.etree import XMLSyntaxError
from toml.decoder import TomlDecodeError
from xlrd.biffh import XLRDError
from yaml.parser import ParserError
from yaml.scanner import ScannerError

@dataclass
class ConfigFile:
    """Read a configuration file and return its data."""

    file: str = None

    def __post_init__(self):
        """Setup ConfigFile."""

        self.suffix_types = {
            ".conf": self.toml_read,
            ".json": self.json_read,
            ".toml": self.toml_read,
            ".xlsx": self.xlsx_read,
            ".xml": self.xml_read,
            ".yaml": self.yaml_read,
            ".yml": self.yaml_read,
        }

        if type(self.file) is list:
            for tmp in self.file:
                if type(tmp) is PosixPath and tmp.is_file():
                    self.file = tmp.resolve(strict=False)
                    break
                elif type(tmp) is str:
                    tmp = Path(tmp).resolve(strict=False)
                    if tmp.is_file():
                        self.file = tmp.resolve(strict=False)
                        break
            else:
                raise FileNotFoundError

        if type(self.file) is str and self.file:
            self.file = Path(self.file).resolve(strict=False)

        if type(self.file) is PosixPath and self.file.is_file():
            try:
                self.file = self.file.resolve(strict=True)
            except FileNotFoundError as e:
                print(f"\nMissing or invalid configuration file '{self.file}'.\n", file=sys.stderr)
                raise e
            except Exception as e:
                print(f"\nException error processing file '{self.file}'.\n", file=sys.stderr)
                raise e
        else:
            raise TypeError("Parameter must be an existing file name.")

        if self.file.suffix not in self.suffix_types:
            print(f"\nFile '{self.file}' has an unknown suffix type of '{self.file.suffix}'.\n", file=sys.stderr)
            raise NotImplementedError

        self.suffix = self.file.suffix[1:]

    @property
    def read(self) -> object:

        if self.file.suffix in self.suffix_types:
            try:
                return self.suffix_types[self.file.suffix]()
            except PermissionError as e:
                print(f"\nPermission error reading file '{self.file}'.\n", file=sys.stderr)
                raise e
            except UnicodeDecodeError as e:
                print(f"\nUnicode decode error while parsing file '{self.file}'.\n", file=sys.stderr)
                raise e
            except Exception as e:
                print(f"\nException error processing file '{self.file}'.\n", file=sys.stderr)
                raise e
        else:
            print(f"\nFile '{self.file}' has an unknown suffix type of '{self.file.suffix}'.\n", file=sys.stderr)
            raise NotImplementedError

    def json_read(self) -> object:
        try:
            with open(self.file, 'r') as open_file:
                return json.load(open_file)
        except JSONDecodeError as e:
            print(f"\nJSON decode error while parsing file '{self.file}'.\n", file=sys.stderr)
            raise e
        except UnicodeDecodeError as e:
            print(f"\nUnicode decode error while parsing file '{self.file}'.\n", file=sys.stderr)
            raise e
        except Exception as e:
            print(f"\nException error processing file '{self.file}'.\n", file=sys.stderr)
            raise e

    def toml_read(self) -> object:
        try:
            return toml.load(self.file)
        except TomlDecodeError as e:
            print(f"\nTOML decode error while parsing file '{self.file}'.\n", file=sys.stderr)
            raise e
        except UnicodeDecodeError as e:
            print(f"\nUnicode decode error while parsing file '{self.file}'.\n", file=sys.stderr)
            raise e
        except Exception as e:
            print(f"\nException error processing file '{self.file}'.\n", file=sys.stderr)
            raise e

    def xlsx_read(self) -> object:
        try:
            return pd.read_excel(self.file, sheet_name=None)
        except XLRDError as e:
            print(f"\nXLSX XLRD error while parsing file '{self.file}'.\n", file=sys.stderr)
            raise e
        except Exception as e:
            print(f"\nException error processing file '{self.file}'.\n", file=sys.stderr)
            raise e

    def xml_read(self) -> object:
        try:
            return etree.parse(os.fspath(self.file))
        except XMLSyntaxError as e:
            print(f"\nXML Syntax error while parsing file '{self.file}'.\n", file=sys.stderr)
            raise e
        except Exception as e:
            print(f"\nException error processing file '{self.file}'.\n", file=sys.stderr)
            raise e

    def yaml_read(self) -> object:
        try:
            with open(self.file, 'r') as open_file:
                return yaml.safe_load(open_file)
        except ParserError as e:
            print(f"\nYAML parse error while parsing file '{self.file}'.\n", file=sys.stderr)
            raise e
        except ScannerError as e:
            print(f"\nYAML Scanner error while parsing file '{self.file}'.\n", file=sys.stderr)
            raise e
        except UnicodeDecodeError as e:
            print(f"\nUnicode decode error while parsing file '{self.file}'.\n", file=sys.stderr)
            raise e
        except Exception as e:
            print(f"\nException error processing file '{self.file}'.\n", file=sys.stderr)
            raise e
