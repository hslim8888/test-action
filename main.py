from util import sh
from datetime import datetime


def main():
    tag = f"trigger-v{datetime.now().strftime('%Y-%m-%d-%H%M%S')}-asdf qwer"
    sh(f"git tag trigger-v{datetime.now().strftime('%Y-%m-%d-%H%M%S')}-{tag} && git push --tags")


if __name__ == '__main__':
    main()
