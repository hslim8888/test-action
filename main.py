from util import sh
from datetime import datetime


def main(*args, **kwargs):
    trigger_tag = f'trigger-v{datetime.now().strftime("%Y-%m-%d-%H%M%S")}'
    branch = 'main'
    print(args)
    print(kwargs)
    deploy_message = f'test message {datetime.now().strftime("%Y-%m-%d-%H%M")}'  # kwargs.get('m', '')
    print(deploy_message)
    tag = f'-a {trigger_tag} -m "{deploy_message}"' if deploy_message else trigger_tag
    print(tag)
    sh(f'git fetch && git tag {tag} origin/{branch} && git push origin {trigger_tag}')
    print('done')


if __name__ == '__main__':
    main()

messge = {"attachments": [{"color": "#36a64f", "blocks": [
    {"type": "section", "text": {"type": "mrkdwn", "text": "${{ steps.slack_body.outputs.body }}"}}]}]}
