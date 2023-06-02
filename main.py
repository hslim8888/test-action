from util import sh
from datetime import datetime


def main():
    sh(f"git fetch && git tag trigger-v{datetime.now().strftime('%Y-%m-%d-%H%M%S')}-mattlim origin/main && git push origin --tags")
    # sh(f"git tag trigger-v{datetime.now().strftime('%Y-%m-%d-%H%M')}-hslim8888 && git push --tags")


if __name__ == '__main__':
    main()

