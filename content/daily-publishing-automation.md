# APPROVAL POLICY — USER CONFIRMED

**Mandatory human approval for every TikTok video.** Generate drafts daily, present the MP4, proposed caption and hashtags in ChatGPT, and do not schedule or publish until the user explicitly approves that specific video. A missed approval means no publication. Target publishing time is 6 PM America/Detroit, contingent on approval. No unattended publishing. Metricool brand 7457463 is connected to TikTok; no TikTok post has been scheduled. Automated delivery of GitHub artifact files directly into ChatGPT is not yet implemented and must not be represented as active.

---

# Daily publishing automation — implementation contract

Goal: generate and publish one H Fire Safety educational TikTok video per day. No general AI/automation/business content. No paid recurring services.

## System architecture
1. Daily schedule via GitHub Actions on the default branch, after QA gates are working. Select a nonrepeating fire-alarm/NICET topic from approved content queue.
2. Script generation must be constrained to pre-reviewed facts and references. Do not automatically invent manufacturer specs or wiring details.
3. Render using original/licensed footage, diagrams, subtitles and locally generated narration. Reject missing assets and unacceptable audio rather than publishing placeholders.
4. Quality gate: validate aspect ratio, codec, audio presence, length, text safe zones, scene completeness, source ledger and technical approval. Failed gates create an alert/review artifact, never a published post.
5. Upload through an authorized TikTok Content Posting API integration or a connected scheduler that supports the user's account and free tier. Require OAuth and respect API scopes, privacy options and user approval requirements.
6. Log published URL, timestamp, video ID, topic and performance metrics. Prevent duplicate posts with an idempotency key.

## Current blockers
- User's TikTok account handle and OAuth/scheduler connection are not provided.
- Existing GitHub draft renderer is a proof of concept, not cinematic quality.
- No approved original screen/video footage library and no completed technical quality gate.
- GitHub schedule and automatic TikTok posting are NOT enabled.
- Production branch is a draft PR and does not run scheduled workflows until merged into default branch.

## Rollout
Phase 1: upgrade video quality and generate/approve 3 real episodes.
Phase 2: daily GitHub draft generation, with automatic rejection on QC failure.
Phase 3: connect TikTok publishing integration, test one authorized post, then enable daily publication only for approved assets.
Phase 4: daily analytics and content optimization.

Never use TikTok credentials in repository files. Use official OAuth and encrypted secrets. Avoid posting unreviewed safety-critical fire alarm instructions.
