#! python
# -*- coding: utf-8 -*-

import os
import argparse
import time
import app.compile as compile
import app.upload as upload
import app.playlist as playlist

#settings
vids_dir = 'J:/Public Relations/videos_promotion/KLRN News Updates'
playlist_id = 'PLO5rIpyd-O4EA5mYUxl1WbOaOl1kU08RB'

#keep track of root directory
root_dir = os.path.abspath(os.curdir)

#help text
help = {
    'compile': 'Compile html for blog post, and text for YouTube videos',
    'upload': 'Upload videos to KLRN YouTube Channel',
    'upload_and_playlist': 'Upload to KLRN Channel, then add to News Updates Playlist',
    'playlist': 'Move most recently uploaded videos to News Updates Playlist',
    'archive': 'Optionally archive and retrieve saved files by appending file names',
    'test': 'For testing'
}

#set cmd line argument flags
parser = argparse.ArgumentParser(description='KLRN News Updates compiler and uploader')
parser.add_argument('-c', '--compile', action='store_true', help=help['compile'])
parser.add_argument('-u', '--upload', action='store_true', help=help['upload'])
parser.add_argument('-p', '--playlist', action='store_true', help=help['playlist'])
parser.add_argument('-a', '--archive', nargs='?', default='', help=help['archive'])
parser.add_argument('-t', '--test', action='store_true', help=help['test'])
args = parser.parse_args()

def run(opts):
    os.chdir('app')    
    
    if opts.compile: compile.run(root_dir, archive=opts.archive)
    if opts.upload and not opts.playlist: upload.run(root_dir, vids_dir, archive=opts.archive)        
    if opts.upload and opts.playlist:
        upload.run(root_dir, vids_dir, archive=opts.archive)
        time.sleep(3)
        playlist.run(root_dir, playlist_id, archive=opts.archive) 
    if not opts.upload and opts.playlist: playlist.run(root_dir, playlist_id, archive=opts.archive)  
    if opts.test: 
        print root_dir
        print os.getcwd()
        print opts
    
    os.chdir(root_dir)      
      
    if not opts.compile and not opts.upload and not opts.playlist and not opts.test:
        print '''One of the following four flags must be added:
        \n  --compile\n  --upload\n  --upload --playlist\n  --playlist
        \n\nOr use these short flags:\n\n  -c\n  -u\n  -u -p\n  -p
        \n\nOptionally add one of these flags:\n\n  -archive <date_or_something>\n  -a <date_or_whatever>
        \n\nThis is what they do:
        \n  COMPILE: {}\n\n  UPLOAD: {}\n\n  UPLOAD PLAYLIST: {}\n\n  PLAYLIST: {}\n\n  ARCHIVE: {}
        '''.format(help['compile'], help['upload'], help['upload_and_playlist'], help['playlist'], help['archive'])

run(args)