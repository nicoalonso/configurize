#!/usr/bin/python3

import json
from pathlib import Path

from msgterm import MsgTerm


# Folder to contains projects config
FOLDER_PROJECTS = '.nk'


class Configurize:
    '''Configurize class
    
    It is used for read and save the configuration from json file

    Args:
        project (string): Project name
        filename (string): Config file name (default:{'config'})

    Attributes:
        project (string): Project name
        filename (string): Config file name (default:{'config.json'})
        configFolder (string): User home config folder
        filepath (string): Full config file path
        config (dict): Configuration
    '''

    def __init__(self, project, filename='config'):
        self.project = project
        self.filename = filename + '.json'
        self.configFolder = None
        self.filepath = None
        self.config = {}


    def getHomeFilePath(self):
        '''Get home file path
        
        Get the user home folder for read and store de config file
        '''
        folder = Path.home() / FOLDER_PROJECTS;
        # Create folder if not exists
        if not folder.exists():  # pragma: no cover
            folder.mkdir()
            MsgTerm.debug('[Config] create folder %s' % str(folder))

        self.configFolder = folder / self.project
        # Create project folder if not exists
        if not self.configFolder.exists():  # pragma: no cover
            self.configFolder.mkdir()
            MsgTerm.debug('[Config] create folder %s' % str(self.configFolder))

        # Config file path
        self.filepath = self.configFolder / self.filename


    def load(self):
        '''Load
        
        Load config from filepath
        
        Returns:
            bool: Load result
        '''
        self.getHomeFilePath()

        # Check if config file exists
        MsgTerm.debug('[Config] Search config file %s' % self.filepath)
        if self.filepath.exists() and self.filepath.is_file():
            MsgTerm.debug('[Config] load config: %s' % self.filepath)
            with self.filepath.open() as json_file:
                self.config = json.load(json_file)
        else:
            MsgTerm.warning('[Config] Configuration file not found: %s' % self.filename)
            localConfig = Path('.') / self.filename
            MsgTerm.debug('[Config] load local configuration: %s' % localConfig)
            if localConfig.exists() and localConfig.is_file():
                with localConfig.open() as localConfig:
                    self.config = json.load(localConfig)
            else:  # pragma: no cover
                MsgTerm.fatal('[Config] Configuration file not found')
                return False

        return True


    def save(self):
        '''Save
        
        Store the configuration on file
        '''
        if not self.filepath:
            self.getHomeFilePath()

        with self.filepath.open('w') as json_file:
            json.dump(self.config, json_file, indent=4, sort_keys=True)


    def get(self, key_name, default=None):
        '''Get value
        
        Get property value
        
        Args:
            key_name {string}: key name 'section.subsection.key'
            default {mixed} : default value (default: {None})
        
        Returns:
            Mixed: Return the config value
        '''
        parts = key_name.split('.')
        name = parts.pop()
        aux = self.config
        for item in parts:
            aux = aux.get(item, None)
            if aux == None:
                MsgTerm.fatal('[Config] section not exists %s' % key_name)
                return default

        return aux.get(name, default)


    def set(self, key_name, value):
        '''Set value
        
        Set property value
        
        Arguments:
            key_name {string}: key name 'section.subsection.key'
            value   {mixed} : config value
        '''
        if isinstance(key_name, str):
            key_name = key_name.split('.')

        if isinstance(key_name, list):
            name = key_name.pop()
            aux = self.config
            for item in key_name:
                sub = aux.get(item, None)
                if sub == None:
                    sub = {}
                    aux[item] = sub
                aux = sub
            # Store value
            aux[name] = value


    def remove(self, key_name):
        '''Remove key from config
        
        Arguments:
            key_name {string}

        Returns:
            bool: remove result
        '''
        parts = []
        if isinstance(key_name, str):
            parts = key_name.split('.')

        if isinstance(parts, list):
            name = parts.pop()
            aux = self.config
            for item in parts:
                aux = aux.get(item, None)
                if aux == None:
                    MsgTerm.fatal('[Config] parameter not exists { %s }' % key_name)
                    return False

            # remove key
            if aux != None and name in aux:
                del aux[name]
            else:
                MsgTerm.fatal('[Config] parameter not exists { %s }' % key_name)
                return False

        return True


    def display(self):
        '''Display configuration on the terminal'''
        MsgTerm.jsonPrint(self.config)


    def bool(self, key_name, default=False):
        '''bool
        
        Get the property value as bool
        
        Args:
            key_name {string}
            default {bool} --  (default: {False})
        
        Returns:
            bool
        '''
        return bool(self.get(key_name, default))


    def int(self, key_name, default=0):
        '''int
        
        Get the property value as integer
        
        Args:
            key_name {string}
            default {int} --  (default: {0})
        
        Returns:
            int
        '''
        return int(self.get(key_name, default))


    def float(self, key_name, default=0.0):
        '''float
        
        Get the property value as float
        
        Args:
            key_name {string}
            default {float} --  (default: {0.0})
        
        Returns:
            float
        '''
        return float(self.get(key_name, default))


    def str(self, key_name, default=''):
        '''string
        
        Get the property value as string
        
        Args:
            key_name {string}
            default {string} --  (default: {''})
        
        Returns:
            str
        '''
        return str(self.get(key_name, default))


    def list(self, key_name, default=[]):
        '''list
        
        Get the property value as list
        
        Args:
            key_name {string}
            default {list} --  (default: [])
        
        Returns:
            list
        '''
        return list(self.get(key_name, default))


    def command(self, action):
        '''Config command
        
        Execute command of configurize
        
        Arguments:
            action {string}

        Returns:
            bool: command result
        '''
        result = True
        name = action.lower()
        if name == 'help':
            info = [
                'list of commands:',
                '',
                '  help               : Show this help',
                '  list               : List of configuration',
                '  section.name=value : Set a parameter',
                '  section.name-      : Remove a parameter'
            ]
            MsgTerm.help(info, section='Config')
        elif name == 'list':
            MsgTerm.info('Show config file:', par=True)
            self.display()
        elif '=' in action:
            parts = action.split('=')
            if len(parts) == 2:
                value = parts.pop()
                parameter = parts.pop()
                MsgTerm.debug('Update parameter [ %s ] with value "%s"' % (parameter, value))
                self.set(parameter, value)
                MsgTerm.success('Parameter updated { %s }' % parameter)
                self.save()
                MsgTerm.success('Config file updated')
                self.display()
            else:
                MsgTerm.error("[Config] Error: expected 'section.name=value'")
                result = False
        elif action.endswith('-'):
            key = action[:-1]
            MsgTerm.debug('Remove key { %s }' % key)
            if self.remove(key):
                MsgTerm.success('Parameter removed { %s }' % key)
                self.save()
                MsgTerm.success('Config file updated')
                self.display()
            else:
                result = False
        else:
            MsgTerm.alert('[Config] Unknown action: %s' % action, nl=True)
            MsgTerm.help('use the command { help } for more information', section='Config', nl=True)
            result = False

        return result


if __name__ == '__main__':  # pragma: no cover
    # Test config file
    cfg = Configurize('Test')
    cfg.load()
