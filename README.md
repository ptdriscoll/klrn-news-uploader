# Upload KLRN News Updates videos 

This application is built on top of the YouTube Data API, version 3, to upload KLRN's daily News Updates videos, and move them into a playlist where they feed onto a web page. 

### How it works

The YouTube playlist id and the folder where the videos are dropped each day are set at the top of run.py in the root directory. The naming scheme for videos are 04-10-17-1.mp4 - the 1 at the end refers to the first video, the rest is the date.

Users type the date, video titles, keywords and news links into INPUT.txt, which the program then parases to produce html for a blog entry and metadata for the YouTube upload. Those results are saved as output/compiled.txt, a file that additionaly can be edited by hand. 

The program uses output/compiled.txt to upload the videos. The video ids from a YouTube response are saved to output/updated.txt, which the program later refers to when moving the videos into the playlist.

The application is run through a command line interface using run.py in the root folder. Here are the available commands:

  --compile
  --upload
  --upload --playlist
  --playlist

These are the short flags:

  -c
  -u
  -u -p
  -p

This is what they do:

  -COMPILE: Compile html for blog post, and text for YouTube videos
  -UPLOAD: Upload videos to KLRN YouTube Channel
  -UPLOAD PLAYLIST: Upload to KLRN Channel, then add to News Updates Playlist
  -PLAYLIST: Move most recently uploaded videos to News Updates Playlist
  
By default, the program refers to the last saved text files. But to optionally archive a file for later use, such as when waiting a day or two to actualy upload the videos or move them into a playlist, then add an optional archive argument to namespace the file name: 

  -archive <date_or_something>
  -a <date_or_whatever>
  
Note that --archive is both a setter and getter, doing whichever the program needs at different points in the flow.

### Examples

From root folder, after entering all information into INPUT.txt: 

  run.py --compile
  run.py --upload
  run.py --playlist

Using shortcuts:
  
  run.py -c 
  run.py -u -p
  
Or:

  run.py -c 
  run.py -up  
  
The workflow for namespacing files so they can be managed over more than one day: 

  run.py --compile --archive 4-10
  run.py --upload --archive 4-10
  run.py --playlist --archive 4-10

### References

upload_youtube.py and playlist_youtube.py contain the YouTube Data API code, which are modified versions of these scripts:

- https://developers.google.com/youtube/v3/guides/uploading_a_video
- https://developers.google.com/youtube/v3/docs/playlists/insert
- https://github.com/alokmahor/add_to_youtube_playlist