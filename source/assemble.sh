cd /tmp/claude-0/-home-user-fruit/598d9320-bdad-5898-a69a-c8566ed0033a/scratchpad/anim
T=239
ffmpeg -y -loglevel error -framerate 30 -i frames/f%06d.jpg \
 -f lavfi -i "aevalsrc='0.05*sin(2*PI*220*t)+0.04*sin(2*PI*261.63*t)+0.035*sin(2*PI*329.63*t)+0.03*sin(2*PI*110*t)|0.05*sin(2*PI*220.5*t)+0.04*sin(2*PI*262*t)+0.035*sin(2*PI*330*t)+0.03*sin(2*PI*110.2*t)':s=44100:d=$T" \
 -filter_complex "[1:a]tremolo=f=0.15:d=0.5,lowpass=f=1200,afade=t=in:d=2,afade=t=out:st=$((T-3)):d=3,volume=0.6[a]" \
 -map 0:v -map "[a]" -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p -c:a aac -b:a 128k -shortest -movflags +faststart iphone15_animation.mp4
