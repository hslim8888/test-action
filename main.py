from util import sh
from datetime import datetime


def main():
    tag = f"trigger-v{datetime.now().strftime('%Y-%m-%d-%H%M%S')}-mattlim"
    sh(f"git tag trigger-v{datetime.now().strftime('%Y-%m-%d-%H%M%S')}-hslim8888 && git push --tags")


if __name__ == '__main__':
    main()
