# type: ignore

from invoke import task


@task
def wait_for(ctx, host, timeout=30):
    ctx.run(f"wait-for-it {host} --timeout={timeout}")


@task
def runserver(ctx, host="0.0.0.0", port=8000, debug=False):
    task = "runserver"
    options = []

    if debug:
        task = "runserver_plus"
        options = ["--threaded", "--print-sql", "--nopin"]

    command = " ".join([f"python manage.py {task}", f"{' '.join(options)} {host}:{port}"])
    print(command)
    ctx.run(command, pty=True)


@task
def migrate(ctx):
    ctx.run("python manage.py migrate")


@task
def test(ctx):
    """
    Dispatch tests task
    """
    ctx.run("python manage.py test")


@task
def uwsgi(
    ctx,
    host="0.0.0.0",
    port=8000,
    workers=6,
    threads=10,
    stats=True,
    extra="",
    uwsgi_socket=False,
):
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


@task
def celery_queues(ctx, queues="low_priority,high_priority", log_level="INFO"):
    command = f"celery -A jobs.celery worker -l {log_level} -E -Q {queues}"
    print(command)
    ctx.run(command, pty=True)
