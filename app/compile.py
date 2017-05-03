# -*- coding: utf-8 -*-

import os

#helper to skip lines and flag the working section 
def _line_to_read(line):
    global section
    
    if not line: return False
    if line.startswith('==='): return False
        
    if line.startswith('DATE'): 
        section = line.split(' (')[0]
        return False
    if line.startswith('VIDEO'): 
        section = line.split(' (')[0]
        return False
    if line.startswith('BLOG'): 
        section = line.split(' (')[0]
        return False        
    return True    

def run(root, archive):
    file = 'INPUT.txt'
    text = 'https://www.youtube.com/\n' + '='*65 + '\n'
    html = ''
    date = ''
    video_titles = []
    video_keywords = []
    blog_titles = []
    blog_description = []
    blog_links = []
   
    #get data from input file
    global section
    
    with open(os.path.join(root, file)) as f:
        section = 'DATE'
        for line in f:
            line = line.strip()
            if not _line_to_read(line): continue
            if section == 'DATE': date = line
            if section == 'VIDEO TITLES': video_titles.append(line)
            if section == 'VIDEO KEYWORDS': video_keywords.append(line)
            if section == 'BLOG LINK TITLES':
                if line.startswith('*'):
                    line = line[1:]
                    blog_description.append(line)
                blog_titles.append(line)
            if section == 'BLOG LINKS': blog_links.append(line)

    #make sure at least two titles with asterisks were added to blog_description

    if len(blog_description) < 2:
        for x in blog_titles:
            if len(blog_description) > 1: break
            if x in blog_description: continue        
            blog_description.append(x)                  

    #first build blog content  
    if ', 20' in date: blog_date = date[:-6]
    else: blog_date = date
    
    text += 'News links for ' + blog_date + '\n\n'
    text += blog_description[0] + ', ' + blog_description[1] + ', and other headlines.\n\n'

    for x in blog_titles:
        text += x + '\n'
    text += '\n'

    for x in blog_links:
        text += x + '\n\n'
    text += '\n'

    #now build html block
    html += '<p>Links for ' + date + ':</p><ul>'

    for x in range(len(blog_titles)):
        html += '<li><a href="' + blog_links[x] + '" '
        html += 'target="_blank">' + blog_titles[x] + '</a></li>'

    html += '</ul>'
    text += html + '\n\n'

    #now build YouTube metadata
    for x in range(len(video_titles)):
        text += '='*65 + '\n'
        text += date + ' - Update ' + str(x+1) + '\n\n'
        text += 'Topics: ' + video_titles[x] + '\n\n'
        text += 'KLRN News provides news information through independent sources and from news partners and other media as a local news aggregator.\n\n'
        text += 'For more information, go to http://www.KLRN.org/news/\n\n\n' 
        text += video_keywords[x] + '\n\n'

    #amend output filename if provided in cli argument
    if len(archive) > 0: outputf = 'output/compiled_' + archive + '.txt' 
    else: outputf = 'output/compiled.txt'     
    
    #save to output file 
    with open(os.path.join(root, outputf), 'w') as file:
        file.write(text)

    print '\n',text