import os
import urllib.request
import xmltodict

PLEX_TOKEN = os.getenv('PLEX_TOKEN')

class Libraries(object):
  def __init__(self, plex_ip, plex_port, plex_token=None):
    self.plex_ip = plex_ip
    self.plex_port = plex_port
    self.plex_token = plex_token
    self.LIBRARIES = []

  def GetLibraries(self):
    with urllib.request.urlopen(
      'http://%s:%s/library/sections' % (self.plex_ip, 
                          self.plex_port)) as response:
      html = response.read()
      result = xmltodict.parse(html)
      directories = result['MediaContainer']['Directory']

      for directory in directories:
        paths = []
        name = directory['@title']
        lib_type = directory['@type']
        key = directory['@key']
        create_date = directory['@createdAt']
        if isinstance(directory['Location'], list):
          for location in directory['Location']:
            path = location['@path']
            paths.append(path)
        else:
          path = directory.get('Location').get('@path')
          paths.append(path)

        library = Library(name, lib_type, create_date, paths, key) 
        self.LIBRARIES.append(library)
    return self.LIBRARIES


class Library(Libraries):
  def __init__(self, name, lib_type, create_date, paths, key):
    self.name = name
    self.lib_type = lib_type
    self.create_date = create_date
    self.paths = paths
    self.key = key