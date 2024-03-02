# Welcome to Luna AI

My first long term project that I intend to iterate on over the years, adding more and more functionality.

LUNA stands for Logical User Navigation Aid... Also known as totally not a GPT reverse generated acronym for the name Luna.

## What is Luna AI's purpose?

For simplicity's sake I'll refer to Luna as a She, the Ai has a female voice and It's just easier to type this readme this way.

Luna has a few purposes that I planned out ahead of time but no specific direction just yet. The general idea is to have her be as close to a human assistant as possible, either by artificially
making her prompt certain interactions or by as human speech as possible with the current technology. Think of her as a JARVIS, just not AI and less sophisticated.

The long term would be to use her in a smart home, she'd be able to control the houses power grid, sprinkler system, monitor and control power outputs throughout the house as well as control utensils, screens, doors, locks, etc.
I even thought it'd be a good and funny Idea to have her be used in the doorbell camera.

## Explaining Luna's current functionality

She can: Open apps, Tell the time, Check the calendar, type out text when prompted, google stuff for you.

While it seems like it's not a lot, that's already taken me nearly 2 weeks to implement and then another week to re-factor the code.

# My journey with LUNA

Currently, Luna is basically in what I like to call Version 2. I started working on her when I basically just picked up Python and had no idea what I'm doing. In the past few weeks
I have expanded my knowledge quite a bit. Since Python is a rather easy langauge to get into it wasn't that hard to build upon her.

As I kept adding and piling functions ontop of Luna, she finally buckled and shot herself in the leg. I was unable to figure it out.

- I took another approach and did my first ever Refactor of Luna's code. Created a config file from scratch, created a config.py which assigns a bunch of values all over the place.
- Re-built Luna's core functionality from scratch and optimised the approaches i took before or re-did them entirely.
- Re-built Luna's additional methods from scratch, making them more streamlined
- Added a lot more error handling

Currently Luna's in a good spot to chill on for a bit while I learn other languages. I'll still work on her, but it's been a bit draining not going to lie.

# What will you need to run Luna on your own?

- You will need API Key's for both ElevenLabs and OpenAI
- If you want to beable to use the calendar functionality you'll need to set up your Google dev account and get a calendar credentials.json
- Fill in the config.json and config.py with the appropriate paths
