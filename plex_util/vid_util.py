import os
import urllib.request
import xmltodict

PLEX_TOKEN = os.getenv('PLEX_TOKEN')


class Videos(object):
  def __init__(self, plex_ip, plex_port):
    self.videos = {}
    self.plex_ip = plex_ip
    self.plex_port = plex_port
    self.vid_url = 'http://%s:%s/library/sections' % (
      self.plex_ip, 
      self.plex_port
      )

  def Get(self, lib_key):
    with urllib.request.urlopen('%s/%s/all' % (
      self.vid_url, lib_key)) as response:
      html = response.read()
      self.result = xmltodict.parse(html)

    self.vid_list = self.result['MediaContainer']['Video']
    self.vid_lib_name = self.result['MediaContainer']['@librarySectionTitle']
    self.videos[self.vid_lib_name] = {}

    for vid in self.vid_list:
      video = {}
      parts = {}
      vid_title = vid['@title']
      vid_guid = vid.get('@guid')
      if vid_guid:
        imdb_val = vid_guid.split(':')[1][2:].split('?')[0]
        imdb_url = 'https://www.imdb.com/title/%s/' % imdb_val
      else:
        imdb_url = None

      if isinstance(vid.get('Media'), list):
        for vid_file in vid.get('Media'):
          if isinstance(vid_file.get('Part'), list):
            for part in vid_file.get('Part'):
              parts['file_name'] = part.get('@file')
              parts['file_size'] = int(part.get('@size'))
          else:
            parts[vid_file.get(
              'Part').get(
                '@file')] = vid_file.get('Part').get('@size')
          video[vid_title] = {
            'studio': vid.get('@studio'),
            'summary': vid.get('@summary'),
            'tagline': vid.get('@tagline'),
            'date_added': int(vid.get('@addedAt', 0)),
            'released': int(vid.get('@year', 0)),
            'rating': float(vid.get('@rating', 0.0)),
            'content_rating': vid.get('@contentRating'),
            'thumb_location': vid.get('@thumb'),
            'duration': int(vid.get('@duration', 0)),
            'codec': vid_file.get('@videoCodec'),
            'resolution': vid_file.get('@videoResolution'),
            'imdb_url': imdb_url,
            'file_info': parts
          }
      else:
        if isinstance(vid.get('Media').get('Part'), list):
            for part in vid.get('Media').get('Part'):
              parts['file_name'] = part.get('@file')
              parts['file_size'] = int(part.get('@size'))
        else:
          parts['file_name'] = vid.get(
            'Media').get('Part').get('@file')
          parts['file_size'] = int(
            vid.get('Media').get('Part').get('@size'))
        video[vid_title] = {
            'studio': vid.get('@studio'),
            'summary': vid.get('@summary'),
            'tagline': vid.get('@tagline'),
            'date_added': int(vid.get('@addedAt', 0)),
            'released': int(vid.get('@year', 0)),
            'rating': float(vid.get('@rating', 0.0)),
            'content_rating': vid.get('@contentRating'),
            'thumb_location': vid.get('@thumb'),
            'duration': int(vid.get('@duration', 0)),
            'codec': vid.get('Media').get('@videoCodec'),
            'resolution': vid.get('Media').get('@videoResolution'),
            'imdb_url': imdb_url,
            'file_info': parts
          }

      self.videos[self.vid_lib_name][vid_title] = video