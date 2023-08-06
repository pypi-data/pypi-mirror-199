# Copyright (c) 2019-2023 Henix, Henix.fr
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


import os
import configparser


def printNoneOrStr(message, toPrint):
    if toPrint == None:
        print(f'{message} <None>')
    else:
        print(f'{message} {str(toPrint)}')


GLOBAL_SECTION = 'global'
TEST_SECTION = 'test'


class TFParamService(object):
    """Library to get TM test parameters in robotframework code"""

    __data = None

    def __init__(self):
        """noop _ for now"""

        if not TFParamService.__data.has_section(GLOBAL_SECTION):
            TFParamService.__data.add_section(GLOBAL_SECTION)

        if not TFParamService.__data.has_section(TEST_SECTION):
            TFParamService.__data.add_section(TEST_SECTION)

        printNoneOrStr(
            'TFParamService.global=', TFParamService.__data.items(GLOBAL_SECTION)
        )
        printNoneOrStr(
            'TFParamService.test=', TFParamService.__data.items(TEST_SECTION)
        )

    def getTestParam(self, key, defaultValue=None):
        """Returns the test case parameter value if it is defined, None
        otherwise"""
        if TFParamService.__data.has_option(TEST_SECTION, key):
            return TFParamService.__data.get(TEST_SECTION, key)
        return defaultValue

    def getGlobalParam(self, key, defaultValue=None):
        """Returns the global parameter value if it is defined, None
        otherwise"""
        if TFParamService.__data.has_option(GLOBAL_SECTION, key):
            return TFParamService.__data.get(GLOBAL_SECTION, key)
        return defaultValue

    def getParam(self, key, defaultValue=None):
        """Returns the test case parameter if defined, else the global
        parameter if defined, None otherwise"""
        return self.getTestParam(key, self.getGlobalParam(key, defaultValue))


def _initialize_service(path):
    TFParamService._TFParamService__data = configparser.ConfigParser(interpolation=None)
    if path is not None:
        print('Loading data from path: %s', path)
        # This is important to get a case-sensitive mapping
        TFParamService._TFParamService__data.optionxform = str
        try:
            with open(path, 'r', encoding='utf-8') as cfg_file:
                TFParamService._TFParamService__data.read_file(cfg_file)
        except Exception as err:
            print(f'Reading SquashTM parameters from {path} failed: {err}')
    else:
        print('No test case data pointer, falling back on default values')


_initialize_service(os.environ.get('_SQUASH_TF_TESTCASE_PARAM_FILES'))
