import datetime
import webbrowser


def get_now_string() -> str:
    return datetime.datetime.now().strftime("%H:%M:%S")


def open_git_repo_link():
    webbrowser.open_new("https://github.com/Aluerie/HextechButEfficient")
