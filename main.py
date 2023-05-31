from util import sh
from datetime import datetime


def main():
    sh(f'git tag trigger-ecs-{datetime.now().strftime("%Y%m%d%H%M%S")}-hslim8888 && git push origin --tags')


if __name__ == '__main__':
    main()