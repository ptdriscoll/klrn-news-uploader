# -*- coding: utf-8 -*-

import os
from datetime import datetime 
import sys
from operator import itemgetter
from os import startfile
import upload_youtube as upload

#helper to get to right sections in file to pull data
def _line_to_read(line):
    global section
    global line_count
    
    if not line: return False
    if line.startswith('==='): 
        section += 1
        line_count = 0
        return False
    if section > 1: line_count += 1    
    return True
    
def get_text(root, archive):
    if len(archive) > 0: file = 'output/compiled_' + archive + '.txt' 
    else: file = 'output/compiled.txt'
    titles = []
    descriptions = []
    tags = []
    
    #get video titles, descriptions and tags to upload
    global section
    global line_count
    
    with open(os.path.join(root, file)) as f:
        section = 0
        line_count = 0
        description = ''
        
        for line in f:
            line = line.strip()
            if not _line_to_read(line): continue
            
            if line_count == 1:
                titles.append(line)
                
            if line_count > 1 and line_count < 5: 
                description += line + '\n\n' 
                
            if line_count == 5: 
                descriptions.append(description.strip())
                description = ''
                tags.append(line) 
                
    return titles, descriptions, tags
                
def add_videos(root, vids_dir, archive):        
    vids_check = []  
    videos = []

    #get video text arrays and extract valid date from title
    titles, descriptions, tags = get_text(root, archive)
    date_title_str = titles[0].split(' - ')[0].split(', ')[1] 
    month = date_title_str[:3] 
    day = date_title_str.split(' ')[1]
   
    try: 
        date_title = datetime.strptime(month+' '+day, '%b %d')        
    except:
        sys.exit('\nCould not get valid date from first text title')            
    
    #get mp4s in target directory, extract dates from names, match with dates from title
    for f in os.listdir(vids_dir):
        if f.endswith('.mp4') and len(f.split('-')) == 4: 
            date_check = f.rsplit('-', 2)[0]
            number = f.rsplit('-', 1)[1].split('.mp4')[0]            
            '''            
            print f
            print date_check
            print number
            print ''
            '''
            
            try:        
                date_video = datetime.strptime(date_check, '%m-%d')
            except:
                sys.exit('\nCould not check for one or more dates in video file names')
            
            if date_video == date_title:
                vids_check.append((f, date_video, number))    
    
    if len(vids_check) != 3:
        print vids_check
        sys.exit('\nNot all three required videos could be located')        

    vids_check.sort(key=itemgetter(2), reverse=False)

    '''
    print vids_check   
    print ''
    print date_title
    print vids_check[0][2], vids_check[0][1]
    print vids_check[1][2], vids_check[1][1]
    print vids_check[2][2], vids_check[2][1]
    print '' 
    '''
    
    #return video names along with text arrays            
    for x in vids_check:
        videos.append(x[0])

    #print videos

    return titles, descriptions, tags, videos 

def run(root, vids_dir, archive):
    uploaded_ids = []
    titles, descriptions, tags, videos = add_videos(root, vids_dir, archive)    
    
    '''
    for x in range(len(titles)):
        print videos[x]
        print 
        print titles[x]
        print ''
        print descriptions[x]
        print ''
        print ''
        print tags[x]
        print ''
        print ''
        print ''
        
    startfile(vids_dir + '/' + videos[0])    
    '''
    
    for x in range(len(titles)):
        options = dict(
            title = titles[x],
            description = descriptions[x],
            keywords = tags[x],
            file = vids_dir + '/' + videos[x]
        )
        
        uploaded_id = upload.run(options)
        uploaded_ids.append(uploaded_id)
        
    if len(uploaded_ids) != 3:
        sys.exit('One or more of the three videos were not uploaded') 
        
    text = ''
    for x in uploaded_ids:
        if x: 
            x = x.strip()
            text += x + '\n'
        
    text += '\n'
    for x in uploaded_ids:
        text += 'https://www.youtube.com/watch?v=' + x.strip() + '\n'

    text += '\nhttps://www.youtube.com/'        
    
    if len(archive) > 0: outputf = 'output/uploaded_' + archive + '.txt' 
    else: outputf = 'output/uploaded.txt'
    
    with open(os.path.join(root, outputf), 'w') as f:
        f.write(text)    