# Kids yoga video: handoff for the next session

The user writes in Roman Urdu/Hindi, so reply in Roman Urdu/Hindi. The video is for the user's kids learning YouTube channel.

## Files in this folder
- `kids_yoga_v2.mp4`: the current 2-minute video. Its girl voice comes from offline espeak and sounds robotic.
- `kids.py`: renders the video (PIL, numpy, ffmpeg). Run `mkdir -p k && python3 kids.py`.
- `tts.py`: the espeak voice (`pip install espeakng-loader`).
- `elevenlabs_script.txt`: the 10 voiceover lines and the ElevenLabs settings.

## Video layout
Cream background. A cartoon girl with black hair in two braids, blue bows and a blue hoodie does animal yoga poses. The pose name sits top-left with a cartoon animal under it, and a blue dotted badge sits top-right showing the pose number, then a 10-to-1 countdown.

Timeline: 6-second intro, then 6 poses of 18.5 seconds each, then a 3-second outro.
- Each pose's narration line plays from second 0.3 of its segment.
- Its countdown starts at second 8, one number per second.
- "Great job!" plays at second 17.9.

## Task
1. Use Claude in Chrome on the user's open ElevenLabs tab (they are logged in).
2. Show the user 2 or 3 cheerful young girl voices from the Voice Library and let them pick one. Use Multilingual v2, Stability 40%, Similarity 75%, Style 30%.
3. Generate the 10 clips from `elevenlabs_script.txt`.
4. In `kids.py`, replace `place()` so it loads those mp3s instead of espeak, and drop the robot-voice filter chain.
5. Re-render the video and send it to the user.
6. Remind the user that YouTube commercial use needs a paid ElevenLabs plan.
