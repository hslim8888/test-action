import json
import textwrap
from datetime import datetime

from jinja2 import Template
from pyinfra.operations import python

from util import sh_output, get_commit_hash_and_time_from_tag, sh


def create_release_and_notify_slack():
    new_tag = sh_output('git tag --sort=-creatordate | grep "^v" | sed -n "1p"')
    new_hash, new_time = get_commit_hash_and_time_from_tag(new_tag)
    previous_tag = sh_output('git tag --sort=-creatordate | grep "^v" | sed -n "2p"')  # 새로운 tag를 제외한 이전 tag 라 2번째
    previous_hash, previous_time = get_commit_hash_and_time_from_tag(previous_tag)
    change_log = sh_output(f'git log --pretty=format:"%h - %s" {previous_hash}..{new_hash}')

    pr_list = sh_output(f'gh pr list --search "is:merged merged:{previous_time}..{new_time}" --json number,title')
    pr_list = "\n".join([f"#{item['number']} {item['title']}" for item in json.loads(pr_list) if pr_list])

    release_title = f'[Compare link](https://github.com/mediquitous-dev/zelda/compare/{previous_tag}..{new_tag})'
    slack_title = f'*www.nugu.jp 배포가 완료되었습니다. <https://github.com/mediquitous-dev/zelda/releases/tag/{new_tag}|{new_tag}>*'

    message_template = Template(textwrap.dedent("""\
        {{ title }}
        
        {{ pr_list }}
        
        {{ change_log }}
    """))
    release_note = message_template.render(title=release_title, pr_list=pr_list, change_log=change_log)


    print('release_note!!!', release_note)
    # release_note = textwrap.dedent(f"""\
    #     [Compare link](https://github.com/mediquitous-dev/zelda/compare/{previous_tag}..{new_tag})
    #
    #
    #     {pr_list}
    #
    #
    #     {change_log}
    # """)
    sh(f'gh release create {new_tag} --title="Release {new_tag}" --notes="{release_note}"')

    slack_message = slack_title + '\n\n' + '\n'.join(release_note.splitlines()[1:7])
    print('slack_message!!!', slack_message)

    # slack_message = textwrap.dedent(f"""\
    #     *www.nugu.jp 배포가 완료되었습니다. <https://github.com/mediquitous-dev/zelda/releases/tag/{new_tag}|{new_tag}>*
    #
    # """)
    # print('slack_message!!!', slack_message)

def tag_latest_commit(new_tag):
    sh('git fetch')
    sh(f'git tag {new_tag} origin/main && git push origin {new_tag}')

python.call(_run_once=True,
            function=tag_latest_commit,
            new_tag=f'v{datetime.now().strftime("%Y-%m-%d-%H%M%S")}')


python.call(_run_once=True, function=create_release_and_notify_slack)

