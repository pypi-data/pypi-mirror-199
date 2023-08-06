from ..domains.comment import Comment


def comment_to_message(comment: Comment) -> dict:
    return {
        "blocks": [
            {
                "type": "header",
                "text": {"type": "plain_text", "text": "Novo comentário"},
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*Vídeo:*\n{comment.video.title}"},
                    {"type": "mrkdwn", "text": f"*Autor:*\n{comment.author.name}"},
                ],
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*Comentário:*\n{comment.text}"},
                    {
                        "type": "mrkdwn",
                        "text": f"*Data:*\n{comment.published_at.strftime('%Y-%m-%dT%H:%M:%SZ')}",
                    },
                ],
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "Ver vídeo"},
                        "action_id": f"video_link_button_{comment.id}",
                        "url": comment.video.link,
                        "style": "primary",
                    },
                ],
            },
            {
                "type": "divider",
            },
        ]
    }
