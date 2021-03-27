from plex_util.library_util import Libraries
from plex_util.vid_util import Videos
from absl import flags
from absl import app

FLAGS = flags.FLAGS

flags.DEFINE_string('plex_ip', None, 'Plex server IP')
flags.DEFINE_string('plex_port', None, 'Plex server port')


def GetVideos(server, plex_ip, plex_port):
  libraries = server.GetLibraries()
  video_collection = {}
  collection_names = []

  all_videos = Videos(plex_ip, plex_port)
  for library in libraries:
    if library.lib_type in ['movie']:
      all_videos.Get(library.key)
  
  return all_videos.videos


def main(argv):
  del argv  # Unused.

  if not FLAGS.plex_ip or not FLAGS.plex_port:
    raise Exception('Please provide plex_ip and plex_port flags. See --help.')

  server = Libraries(FLAGS.plex_ip, FLAGS.plex_port)
  all_vids = GetVideos(server, FLAGS.plex_ip, FLAGS.plex_port)
  


if __name__ == '__main__':
  app.run(main)