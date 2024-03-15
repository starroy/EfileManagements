# from pydub import AudioSegment
import openai
# from moviepy.editor import *
import os
openai.api_key = "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"
startTime = "2023-09-16T05:13:34.482Z"
meetingLength = '10'
count_participants = 3
system_prompt = "You are a helpful assistant for the company Graiy AR. " + \
        "we just recorded a meeting using STT." + \
        "Your task is to turn this into a professional meeting transcript. " + \
        "please do not change the words of the participants, it must stay true to what really was said. " + \
        "please include important and useful information thats discussed at the top of the transcript for easier access to key information. " +  \
        "give each participant  a colored dot emoji before their name to better distinguish participants. " + \
        "datetime string of meeting  is " + startTime + ". " +\
        "meeting length is " + str(meetingLength) + " minutes. " + \
        "number of participants is " + str(count_participants) + "."
local_file = "1.mp4"

def openai_whisper_transcribe(filepath):
    video = VideoFileClip(filepath)
    mp3_file = "sample.mp3"
    video.audio.write_audiofile(mp3_file)
    audio_file = AudioSegment.from_mp3(mp3_file)
    audio_length =  len(audio_file)
    transcription = ''
    interval_minutes= 2 * 60 * 1000
    for last_snippet_time_stamp in range(0, audio_length, interval_minutes):
        if (last_snippet_time_stamp + interval_minutes >= audio_length):
            snippet = audio_file[last_snippet_time_stamp:]
        else:
            snippet = audio_file[last_snippet_time_stamp: interval_minutes]
        snippet.export("audio_snippet.mp3", format="mp3")
        snippet_file = open("audio_snippet.mp3", "rb")
        snippet_transcription = openai.audio.transcriptions.create(model="whisper-1", file=snippet_file, response_format="text")
        transcription = transcription + snippet_transcription
        print("==>", snippet_transcription)
    os.remove(mp3_file)
    print(">>>", transcription)
    return transcription

def generate_corrected_transcript(temperature, system_prompt, audio_file):
    print("prompt==>>>", system_prompt)
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo-16k",
        temperature=temperature,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": openai_whisper_transcribe(audio_file)
            }
        ]
    )
    return response.choices[0].message.content


def generate_gpt_answer(temperature, system_prompt, content):
    print("prompt==>>>", system_prompt)
    response = openai.chat.completions.create(
        model="gpt-4",
        temperature=temperature,
        messages=[
            {
                "role": "system",
                "content": system_prompt

            },
            {
                "role": "user",
                "content": content
            }
        ]
    )
    return response.choices[0].message
snippet_transcription = openai.audio.transcriptions.create(model="whisper-1", file="audio_snippet.mp3", response_format="text")
# meeting_content = generate_corrected_transcript(0, system_prompt, local_file)
# print(meeting_content)

system_prompt = "you are professional intorduction assistant for developers. you have to create the user's oral good and beautiful intoroduction ,which must be more than 10000 letters and long as possible by addtional experiences to the resume provided by the user."
content = "Summary" + \
"I'm an AI Engineer with 7+ years of experience in Deep learning, Machine learning industry." + \
"My expertise ranges from signal processing and" + \
"Computer vision, audio processing to Deep learning and Reinforcement learning. I worked in industrial software development." + \
"Working with me is super easy and eﬃcient. I will take your requirements and provide the best solutions possible with easy-to-understand and maintain code. It's important to me to deliver quality." + \
"Skill Highlights" + \
"∙Project Management" + \
"∙Strong Communication" + \
"∙Complex problem solver" + \
"∙Quick-Delivery of Work" + \
"∙Service-focused" + \
"∙Full-time & Hardworking" + \
"Experience" + \
"AI engineer" + \
"TODD-AO Logs Angeles, USA" + \
"Nov 2021 ~ May 2023" + \
"●Creation for Transcription in ﬁlm industry with customized OpenAI Whisper. Ex: https://absentiadx.com/" + \
"●Building NLP model for correction of Transcription result based on based on focused in each ﬁeld." + \
"●With customized and ﬁned tuned DALLE, creation image art for advertising ﬁlm" + \
"●Involved in signal processing productions based on statistical processing like ICA and BSS" + \
"●Development of Google browser extension which schedule a meeting with google calendar from input prompt using chatgpt and a Django project which summarize input text." + \
"●Development of STT and TTS project using Delphi under offline and online." + \
"AI Embedded Software engineer" + \
"Stone Meadow Management Ltd, Kidderminster" + \
"Oct 2020 - Oct 2021 (1 year)" + \
"●Involved in development of micro controller which controls traﬃc light like Modbus and Arduino." + \
"●As core software developer, have developed AI engine which detects the pedestrian and vehicles using Deep learning running on embedded system, speciﬁcally Raspberry Pi 4B model." + \
"●Development controlling module for peripherals including CSI camera, temperature and pollution" + \
"sensors." + \
"●Development of customized captive portal on Raspberry Pi hotspot and remote control panel using Flask framework." + \
"●Carry out quality assurance tests to discover errors and optimize usability." + \
"AI engineer" + \
"MHY, Australia" + \
"Mar 2018 - Sep 2020 (2 years, 6 months)" + \
"●As an AI engineer, involved in stock prediction project and market analysis system." + \
"●With RNN and CNN, market trend pattern system developed." + \
"●Building DL architecture, training and ﬁne tuning models." + \
"●Transfer learning based on existing models for each market." + \
"AI engineer" + \
"VISORE LAB, Paris" + \
"Mar 2020 - Dec 2020 (9 months)" + \
"●Involved in 3D realization software development." + \
"●Development of Motion tracking of facial expression in person." + \
"●3D head model imitation of expression using Deep learning." + \
"●Integration of Maya and Python AI engine." + \
"●Carry out quality tests to discover errors and optimize usability." + \
"●Weather forecasting model development and nowcasting AI chatbot" + \
"Backend developer & Devops Engineer" + \
"Dec 2018 - Mar 2020 (2 years 4 months)" + \
"Skigit inc, Florida" + \
"●As a core backend developer in development of www.skigit.com , developed Database Design and implementation, mail system, video clips compression, video clip post and rating system etc." + \
"●Deployment of Devops including AWS bit bucket S3 Docker." + \
"●Designing and implementing of all apps for mobile apps." + \
"●Carry out quality tests to discover errors and optimize usability." + \
"Artificial Intelligence Developer" + \
"Grainy AS" + \
"Aug 2023 - Present (2 months)" + \
"https://www.briefly.no/" + \
"●Twilio & Agora Briefly video meeting site" + \
"●Memes' App" + \
"PHP Developer " + \
"Schmeler House " + \
"Feb 2020 - Mar 2021 (1 year 2 months)" + \
"●Using tech stack of Symfony2 MVC Framework, PHP, MySQL, Git, ..." + \
"●Managed the team of 5 people working on product catalogue module" + \
"●Developed python scripts to automate image's noise-reduction process which helped improve research" + \
"analysis time by 40%" + \
"●Achieved 100% on-time project delivery to meet the regulatory milestone" + \
"Education" + \
"Master of Computer Science and Technology: Computer Software Engineer – 2016~2018" + \
"Nanjing University of Information Science & Technology" + \
"Certiﬁcations" + \
"Programming Languages: Python/ C++/Delphi/ Fortran/ MongoDB/ MsSQL/ MySQL/ Django/ PHP"
# answer = generate_gpt_answer(0.8, system_prompt, content)
# print(answer)
# def convert_mp4_to_mp3(mp4_file, mp3_file):
#     video = VideoFileClip(mp4_file)
#     video.audio.write_audiofile(mp3_file)

# # Specify the input MP4 file and the output MP3 file
# input_file = "CJ4bf82d741bbf879d7c56f3836f33aff5.mp4"
# output_file = "d.mp3"

# # Call the function to convert the MP4 file to MP3
# convert_mp4_to_mp3(input_file, output_file)