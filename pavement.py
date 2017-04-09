from paver.easy import *
from paver.setuputils import setup
from paver.virtual import virtualenv

virtualenv_directory = "venv"

setup(
    name="Volunteer Scheduler",
    version="0.1",
)


@task
@virtualenv(dir=virtualenv_directory)
@needs(['vendor'])
def run():
    sh("python3 main.py")


@task
@virtualenv(dir=virtualenv_directory)
@needs(['test_vendor'])
def test():
    sh("nosetests")


@task
@virtualenv(dir=virtualenv_directory)
def vendor():
    sh("pip install -q -r requirements.txt")


@task
@virtualenv(dir=virtualenv_directory)
def test_vendor():
    sh("pip install -q -r test_requirements.txt")
