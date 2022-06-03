import nox


@nox.session
def test(session: nox.Session):
    session.install("poetry")
    session.run("poetry", "install")
    session.run("pytest")


@nox.session
def format(session: nox.Session):
    session.install("black", "isort")
    session.run("isort", "pincer")
    session.run("black", "pincer")


@nox.session
def lint(session: nox.Session):
    session.install("flake8")
    session.run("flake8", "pincer")


"""
Mypy will be be ran within a workflow until pincer provide complete typing
that will not fail for every push.

@nox.session
def mypy(session: nox.Session):
   session.install("mypy")
   session.run("mypy", "pincer")
"""
