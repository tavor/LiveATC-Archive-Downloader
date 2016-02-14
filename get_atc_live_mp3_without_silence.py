from pydub import AudioSegment
from pydub.utils import db_to_float
from pydub.silence import split_on_silence
import wget
import os
import os.path
import sys
import datetime
import time
from get_next_file_name import get_next_filename

files_to_get = []

while True:
    next_filename_candidate = get_next_filename()
    
    print "List of files to get: ",files_to_get

    if next_filename_candidate not in files_to_get:
        files_to_get.append(next_filename_candidate)

    next_filename = files_to_get[0]

    file_exists = os.path.exists('/home/ec2-user/' + next_filename)      

    if not file_exists:
        print next_filename + " hasn't been downloaded yet."

        print "Getting file"
        mp3 = wget.download('http://archive-server.liveatc.net/ksbp/' + next_filename)

        print "" 

        # 404 for LiveATC is 168 bytes   
        if os.path.getsize(mp3) == 168:
            print "Not available yet"
            os.remove(mp3)

            print "Waiting 10 minutes to ask again"
            time.sleep(600)
            continue
        else:
            file_name = next_filename

            print "Creating audio segment from " + file_name
            podcast = AudioSegment.from_mp3(file_name)

            print "Chunking based on silence"
            chunks = split_on_silence(podcast, min_silence_len=500, silence_thresh=-50)

            output_directory = file_name[0:-4]

            os.mkdir(output_directory)

            print "Exporting chunks"
            for i, chunk in enumerate(chunks):
                chunk.export(output_directory + "/chunk{0}.mp3".format(i), format="mp3")

            print "Removing " + files_to_get.pop(0) + " from list of files to get"

            time.sleep(600)

