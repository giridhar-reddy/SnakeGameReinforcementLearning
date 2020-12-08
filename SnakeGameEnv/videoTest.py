import moviepy.editor as mpe

game_clip = mpe.VideoFileClip("C://Users/karamvenkatsaigiridh/Desktop/pyscripts/project.avi")
audio_background = mpe.AudioFileClip('bgm.wav')
audio_loop = mpe.afx.audio_loop( audio_background, duration=game_clip.duration)

# final_audio = mpe.CompositeAudioClip([game_clip.audio, audio_background])
new_audioclip = mpe.CompositeAudioClip([audio_background])
final_clip = game_clip.set_audio(audio_background)
final_clip.write_videofile("C://Users/karamvenkatsaigiridh/Desktop/pyscripts/project_360.mp4")
