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
        '''get home file path
        
        Get the user home folder for read and store de config file
        '''

        folder = Path.home() / FOLDER_PROJECTS;
        # Create folder if not exists
        if not folder.exists():
            folder.mkdir()
            MsgTerm.debug('[Config] create folder %s' % str(folder))

        self.configFolder = folder / self.project
        # Create project folder if not exists
        if not self.configFolder.exists():
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
            MsgTerm.debug('[Config] load config %s' % self.filepath)
            with self.filepath.open() as json_file:
                self.config = json.load(json_file)
        else:
            MsgTerm.warning('[Config] Configuration file not found: %s' % self.filename)
            localConfig = Path('.') / self.filename
            MsgTerm.debug('[Config] load local configuration: %s' % localConfig)
            if localConfig.exists() and localConfig.is_file():
                with localConfig.open() as localConfig:
                    self.config = json.load(localConfig)
            else:
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


    def get(self, section, name, default=None):
        '''Get value
        
        Get property value
        
        Args:
            section {string}: Section on configuration file
            name    {string}: key name
            default {mixed} : default value (default: {None})
        
        Returns:
            Mixed: Return the config value
        '''

        parts = section.split('.')
        aux = self.config
        for item in parts:
            aux = aux.get(item, None)
            if aux == None:
                MsgTerm.fatal('[Config] section not exists %s' % section)
                return default

        return aux.get(name, default)


    def set(self, section, name, value):
        '''Set value
        
        Set property value
        
        Arguments:
            section {string}: Section on configuration file
            name    {string}: property name
            value   {mixed} : property value
        '''

        if isinstance(section, str):
            section = section.split('.')

        if isinstance(section, list):
            aux = self.config
            for item in section:
                sub = aux.get(item, None)
                if sub == None:
                    sub = {}
                    aux[item] = sub
                aux = sub
            # Store value
            aux[name] = value


    def display(self):
        '''Display configuration on the terminal'''

        MsgTerm.jsonPrint(self.config)


    def bool(self, section, name, default=False):
        '''bool
        
        Get the property value as bool
        
        Args:
            section {string}
            name    {string}
            default {bool} --  (default: {False})
        
        Returns:
            bool
        '''

        return bool(self.get(section, name, default))


    def int(self, section, name, default=0):
        '''int
        
        Get the property value as integer
        
        Args:
            section {string}
            name    {string}
            default {int} --  (default: {0})
        
        Returns:
            int
        '''

        return int(self.get(section, name, default))


    def float(self, section, name, default=0.0):
        '''float
        
        Get the property value as float
        
        Args:
            section {string}
            name    {string}
            default {float} --  (default: {0.0})
        
        Returns:
            float
        '''

        return float(self.get(section, name, default))


    def str(self, section, name, default=''):
        '''string
        
        Get the property value as string
        
        Args:
            section {string}
            name    {string}
            default {string} --  (default: {''})
        
        Returns:
            string
        '''

        return str(self.get(section, name, default))


    def list(self, section, name, default=[]):
        '''list
        
        Get the property value as list
        
        Args:
            section {string}
            name    {string}
            default {list} --  (default: [])
        
        Returns:
            list
        '''

        return list(self.get(section, name, default))


# Test config file
if __name__ == '__main__':
    cfg = Configurize('Test')
    cfg.load()
