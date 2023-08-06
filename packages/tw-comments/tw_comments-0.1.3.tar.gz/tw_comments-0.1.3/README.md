# TW Comments

A CLI tool to get comments from Youtube and repost them in a Slack channel.

## Installation

```bash
pip3 install tw-comments
```

## Usage

You need three things to use this tool:

- A Youtube API key
- A Youtube playlist ID
- A Slack webhook URL

### Youtube API key

You can get a Youtube API key by following the instructions [here](https://developers.google.com/youtube/v3/getting-started).

### Youtube playlist ID

You can get a Youtube playlist ID by following the instructions [here](https://www.sociablekit.com/find-youtube-playlist-id/).

### Slack webhook URL

You can get a Slack webhook URL by following the instructions [here](https://api.slack.com/messaging/webhooks).

### Run the tool

This is a example of how to run the tool to get the comments of all videos and repost them in a Slack channel:

```bash
tw-comments youtube --send-to=slack --youtube-api-key=your-youtube-api-key --youtube-playlist-id=your-youtube-playlist-id --slack-webhook-url=your-slack-webhook-url
```

You can also run the tool to send the comments to the standard output, in the case you don't need to pass the `--slack-webhook-url` argument:

```bash
tw-comments youtube --send-to=stdout --youtube-api-key=your-youtube-api-key --youtube-playlist-id=your-youtube-playlist-id
```

The tool will create a file called `last_execution.txt` in the current directory. This file will be used to get the last execution date and time. This way, the tool will only get the comments of the videos that were uploaded after the last execution. If you want to change the path of this file, you can use the `--last-execution-filename` argument:

```bash
tw-comments youtube --send-to=slack --youtube-api-key=your-youtube-api-key --youtube-playlist-id=your-youtube-playlist-id --slack-webhook-url=your-slack-webhook-url --last-execution-filename=/path/to/last_execution.txt
```
