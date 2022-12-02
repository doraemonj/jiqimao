import datetime
from threading import Thread
from playsound import playsound

lyric_text_list = []

lyric_title = "title1"
lyric_artist = "singer1"
lyric_album = "album1"
lyric_text_list.append("[ti:"  + lyric_title +  "]")
lyric_text_list.append("[ar:" + lyric_artist + "]")
lyric_text_list.append("[ar:" + lyric_album + "]")
lyric_text_list.append("[by:]")
lyric_text_list.append("[offset:0]")

song = r"/Users/tangqiang/Library/CloudStorage/GoogleDrive-chrishowardaka@gmail.com/My Drive/ebook_for_sale/txt_zh/001/历史的教训 威尔·杜兰特 The Lessons Of History By Will Durant-999.txt"
song_out = r"/Users/tangqiang/Library/CloudStorage/GoogleDrive-chrishowardaka@gmail.com/My Drive/ebook_for_sale/txt_zh/001/output_999.lrc"


def play_song():
    """play song"""
    global song
    playsound(song)

def calc_time_delta(start_time, end_time):
    """calculate the delta time"""
    return datetime.datetime.fromtimestamp((end_time - start_time).seconds + (end_time - start_time).microseconds/1000000).strftime("%M:%S.%f")

with open(song, "r", encoding="utf-8") as lyric_file:
    raw_lyric = lyric_file.read().split("\n")

start_time = datetime.datetime.now()
Thread(target=play_song).start

# record start time
for i in range(len(raw_lyric)):
    input("next:'" + raw_lyric[i] + "'")
    lyric_text_list.append("[" + calc_time_delta(start_time, datetime.datetime.now()) +"]" + raw_lyric[i])
print("\n")

# save lyric file to lyric_text
lyric_text = ""
for i in range(len(lyric_text_list)):
    print(lyric_text_list[i])
    lyric_text += lyric_text_list[i] + "\n"

# save lyric file
with open(song_out, "w", encoding ="utf-8") as output_file:
    output_file.write(lyric_text)






