# fixit

`Plugin Integration` &nbsp; `Support` &nbsp;

This skill fixes the last command as per the rules of [`thefuck`](https://github.com/nvbn/thefuck) plugin 
as an illustration of how to fold in exiting plugins into the CLAI framework.

## Implementation

The skill responds whenever there's an error in response to a user command. When an error is detected, the command text and the error message is passed to the `thefuck` plugin to get a corrected command. This corrected command is then suggested to the user.

## Example Usage

![fixit](https://www.dropbox.com/s/r9q8rnjv38bipay/fixit.gif?raw=1)

Same as [`thefuck`](https://github.com/nvbn/thefuck).

1. `>> puthon`
2. `>> git brnch`
3. `>> cd dir_does_not_exists`

## [xkcd](https://uni.xkcd.com/)
It has a section on motherboard beep codes that lists, for each beep pattern, a song that syncs up well with it.

![alt text](https://imgs.xkcd.com/comics/error_code.png "It has a section on motherboard beep codes that lists, for each beep pattern, a song that syncs up well with it.")
