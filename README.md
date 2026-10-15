# NICET Daily Video Studio

Free-first, iPhone-manageable prototype for fire alarm educational videos.

## Implemented
- Scheduled **draft render** via GitHub Actions at approximately 6 PM Eastern (America/Detroit, daylight saving aware)
- Manual test trigger: Actions → Daily NICET video draft → Run workflow
- Open-source FFmpeg and eSpeak NG on GitHub-hosted runners
- 1080 × 1920 H.264 MP4 with AAC audio, artifact retained for 7 days
- Basic file and codec/dimension validation

## Not yet implemented
- Cinematic AI-generated 3D animation
- Natural-sounding premium voice
- Automatic technical fact verification against authoritative documentation
- Social account authorization or publishing to TikTok, YouTube, Facebook, Instagram
- Unique daily scripts: the current prototype repeats the sample script

**No social posting is enabled.** This is a draft-only proof of concept. GitHub scheduled workflows may be delayed and do not guarantee delivery at exactly 6 PM. Free GitHub Actions usage is subject to account and repository quotas.

## Security
The repository was observed as **public** on October 15, 2026. Change visibility in GitHub repository Settings → General → Danger Zone → Change repository visibility if you want a private repository. Do not commit credentials. Add future API keys as encrypted Actions secrets.

## Test
Open Actions → Daily NICET video draft → Run workflow. After completion, download the `nicet-video-draft` artifact. Inspect the narration and visuals. This is not yet ready for public release.

## Technical accuracy
All safety-critical explanations need verification against applicable manufacturer instructions and the approved system design. Do not use an AI-only quality check as a substitute for expert verification.
