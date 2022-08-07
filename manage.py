import os
import unittest
from flask.cli import FlaskGroup
from app import blueprint

from app.main import create_app

app = create_app(os.getenv('FLASK_ENV') or 'development')
app.register_blueprint(blueprint)

app.app_context().push()

# register the blueprint
cli = FlaskGroup(app)


@cli.command
def run():
    """ run development server. """
    app.run()


@app.cli.command("test")
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == '__main__':
    cli()
