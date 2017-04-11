# -*- coding: utf-8 -*-

import playlist_youtube as playlist
import os

def run(root, playlist_id, archive):
    if len(archive) > 0: file = 'output/uploaded_' + archive + '.txt' 
    else: file = 'output/uploaded.txt'
    video_ids = []
    
    with open(os.path.join(root, file)) as f:
        line_count = 0
        
        for line in f:
            if line_count > 2: break
            video_ids.append(line.strip())
            line_count += 1
    
    for video_id in video_ids:
        playlist.run(video_id, playlist_id)