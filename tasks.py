from typing import Any, Callable, NoReturn, TypeVar

from invoke import task

Tasks = TypeVar("Tasks", bound=Callable[[Any], Any])


@task
def wait_for(ctx: Any, host: str, timeout: int = 30) -> None:
    ctx.run(f"wait-for-it {host} --timeout={timeout}")


@task
def runserver(ctx: Any, host: str = "0.0.0.0", port: int = 8000, debug: bool = False) -> None:
    task = "runserver"
    options = []

    if debug:
        task = "runserver_plus"
        options = ["--threaded", "--print-sql", "--nopin"]

    command = " ".join([f"python manage.py {task}", f"{' '.join(options)} {host}:{port}"])
    print(command)
    ctx.run(command, pty=True)


@task
def migrate(ctx: Any) -> None:
    ctx.run("python manage.py migrate")


@task
def test(ctx: Any) -> None:
    """
    Dispatch tests task
    """
    ctx.run("python manage.py test")


@task
def uwsgi(
    ctx: Any,
    host: str = "0.0.0.0",
    port: int = 8000,
    workers: int = 6,
    threads: int = 10,
    stats: bool = True,
    extra: str = "",
    uwsgi_socket: bool = False,
) -> None:
    listen = f"--http={host}:{port}"
    if uwsgi_socket:
        listen = f"--socket {host}:{port}"

    command_args = [
        "uwsgi",
        "--chdir=..",
        "--module=bff.config.wsgi:application",
        "--master",
        listen,
        f"--processes={workers}",
        f"--threads={threads}",
        "--single-interpreter",
        "--disable-logging",
        "--lazy-apps",
        "--log-4xx",
        "--log-5xx",
        "--vacuum",
        "--die-on-term",
        "--stats :1717 --stats-http" if stats else "",
        extra,
    ]
    command = " ".join(command_args)
    print(command)
    ctx.run(command)
