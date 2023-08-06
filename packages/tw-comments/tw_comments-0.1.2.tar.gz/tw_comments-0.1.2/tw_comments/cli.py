import asyncio
import asyncclick as click

from datetime import datetime, timezone
from typing import Union

from .domains.video import Video
from .services.video_service import VideoService
from .services.slack_service import SlackService
from .services.comment_service import CommentService
from .helpers.slack_helpers import comment_to_message


@click.group()
async def cli() -> None:
    ...


@click.option(
    "--youtube-api-key",
    help="Youtube API key",
    prompt="Youtube API key",
    required=True,
)
@click.option(
    "--playlist-id",
    help="Youtube playlist id",
    prompt="Youtube playlist id",
    required=True,
)
@click.option(
    "--slack-webhook-url",
    help="Slack webhook url, required when send_to is slack",
    required=False,
)
@click.option(
    "--send-to",
    help="Where to send the comments, available options: slack, stdout",
    prompt="Send to",
    required=True,
    default="slack",
)
@click.option(
    "--last-execution-filename",
    help="Filename to store the last execution date",
    required=False,
    default="last_execution.txt",
)
@click.option(
    "--use-async",
    help="Use async",
    is_flag=True,
    required=False,
    default=False,
    type=bool,
)
@cli.command()
async def youtube(
    youtube_api_key: str,
    playlist_id: str,
    slack_webhook_url: str,
    send_to: str,
    last_execution_filename: str,
    use_async: bool,
) -> None:
    if send_to not in ["slack", "stdout"]:
        click.echo("Invalid send_to option")
        return
    if send_to == "slack" and not slack_webhook_url:
        click.echo("Slack webhook url is required when send_to is slack")
        return

    video_service = VideoService(youtube_api_key)
    comment_service = CommentService(youtube_api_key)

    click.echo("Getting videos...")
    videos = video_service.get_all_videos_by_playlist(playlist_id=playlist_id)
    click.echo(f"Found {len(videos)} videos")

    from_date = get_last_execution(last_execution_filename)
    if use_async:
        click.echo("Getting comments...")
        result = await asyncio.gather(
            *[comment_service.get_comments_by_video(video=video) for video in videos]
        )
        comments = [comment for comments in result for comment in comments]
        click.echo(f"Found a total of {len(comments)} comments")

        if from_date:
            click.echo("Filtering comments by published date...")
            comments = [
                comment for comment in comments if comment.published_at > from_date
            ]
            click.echo(f"Found {len(comments)} comments published after {from_date}")

        if send_to == "slack":
            slack_service = SlackService(slack_webhook_url)
            click.echo("Sending comments to Slack...")
            await asyncio.gather(
                *[
                    slack_service.send_message(
                        message=comment_to_message(comment=comment)
                    )
                    for comment in comments
                ]
            )

            click.echo("Saving last execution date...")
        elif send_to == "stdout":
            click.echo("Printing comments to stdout...")
            for comment in comments:
                click.echo(comment)
    else:
        click.echo("Getting and sending comments...")
        for video in videos:
            click.echo(f"Getting comments for video: {video.id}")
            comments = await comment_service.get_comments_by_video(video=video)
            for comment in [
                comment for comment in comments if comment.published_at > from_date
            ]:
                if send_to == "slack":
                    click.echo(f"Sending comment to Slack: {comment.id}")
                    slack_service = SlackService(slack_webhook_url)
                    await slack_service.send_message(
                        message=comment_to_message(comment=comment)
                    )
                elif send_to == "stdout":
                    click.echo(comment)

    update_last_execution(last_execution_filename)


def get_last_execution(filename: str) -> Union[datetime, None]:
    try:
        with open(filename, "r") as f:
            return datetime.strptime(f.read(), "%Y-%m-%dT%H:%M:%SZ")
    except FileNotFoundError:
        return None
    except ValueError:
        return None


def update_last_execution(filename: str) -> None:
    with open(filename, "w") as f:
        f.write(datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))


if __name__ == "__main__":
    cli(_anyio_backend="asyncio")
