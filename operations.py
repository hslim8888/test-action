import json
from datetime import datetime

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

    github_name = sh_output('git config user.name')
    release_note = f"""[Compare link](https://github.com/mediquitous-dev/zelda/compare/{previous_tag}..{new_tag})
    <br>
    <b>PR LIST</b>
    {pr_list}
    <br>
    <b>CHANGE LOG</b>
    {change_log}
    """
    sh(f'gh release create {new_tag} --title="Release {new_tag}" --notes="{release_note}"')

def tag_latest_commit(new_tag):
    sh('git fetch')
    sh(f'git tag {new_tag} origin/main && git push origin {new_tag}')

python.call(_run_once=True,
            function=tag_latest_commit,
            new_tag=f'v{datetime.now().strftime("%Y-%m-%d-%H%M%S")}')


python.call(_run_once=True, function=create_release_and_notify_slack)

