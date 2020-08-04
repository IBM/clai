# voice

`accessibility` &nbsp; `text-to-speech`

This skill is a smart screen reader for the bash, that aims to make the bash terminal more accessible for 
the low vision and the visually impaired community. The skill - in its current capacity - is designed to 
automatically activate in case of a bash error, summarize the error message, and read back the summary
to the user. 


## Implementation

Currently, the skill activates automatically when an executed command results in a error. The skill 
summarizes the error message and reads it back to the user. The summarization is a deterministic 
procedure that includes the command run and the first line of the error message. The text-to-speech
conversion is achieved using the [`gTTS`](https://github.com/pndurette/gTTS) library, and the playback
uses the [`ffplay`](https://ffmpeg.org/ffplay.html) package.

While the current implementation has one fixed interaction pattern, there are smarter ways to interact 
with the skill that can serve as inspiration for future enhacements. These include smarter summarization 
techniques to effectively convey the bash state information, more interaction patterns that might include 
explicit invocation by the user for current bash state information, more legible speech synthesis for bash 
syntax, etc.

Here are some resources for further reading on screen readers and their usage within the visually
impaired community:
- [Linux Accessibility HowTo](https://www.tldp.org/HOWTO/Accessibility-HOWTO/visual.html)
- [Announcing Tdsr: A Command Line Screen Reader For Macintosh And GNU/Linux
](https://www.applevis.com/blog/announcing-tdsr-command-line-screen-reader-macintosh-and-gnulinux)
- [WebAIM Screen Reader User Survey Results](https://webaim.org/projects/screenreadersurvey8/)
- [Vinux](https://wiki.vinuxproject.org/)
- [Emacspeak](http://emacspeak.sourceforge.net/), [VoiceOver](https://www.apple.com/accessibility/mac/vision/)
 

## Example Usage

[![voice-skill](https://www.dropbox.com/s/tn4eyjfybf9246q/clai-voice-skill-icon.png?raw=1)](https://www.dropbox.com/s/tfzah03yxcpolqi/clai-voice-skill.mov?dl=0)
