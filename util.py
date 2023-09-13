import subprocess
from datetime import datetime

import pytz


def sh(command, check=False, capture_output=False):
    print(command)
    return subprocess.run(command, shell=True, check=check, capture_output=capture_output,
                          text=True if capture_output else False)


def sh_output(command, check=False) -> str:
    return sh(command, check=check, capture_output=True).stdout.strip()

def get_commit_hash_and_time_from_tag(tag):
    comit_hash = sh_output(f'git show-ref -s {tag}')
    # {A_commit_time}..{B_commit_time} 을 하면 A_comit_time 포함이기 때문에, 1초를 더해준다.
    commit_time = sh_output(f'git show -s --format=%cd --date=iso-strict {tag} | tail -n 1')
    commit_time = datetime.strptime(commit_time, "%Y-%m-%dT%H:%M:%S%z") + timedelta(seconds=1)
    if commit_time.tzinfo == pytz.utc:
        commit_time = commit_time.astimezone(pytz.timezone('Asia/Seoul'))
    commit_time = commit_time.strftime("%Y-%m-%dT%H:%M:%S%z")
    return comit_hash, commit_time


