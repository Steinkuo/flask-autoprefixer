import os
from flask import Flask, render_template
from flask_assets import Environment, Bundle
# get work root
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)


# Create the Flask-Assets's instance
assets_env = Environment(app)

# Flask-Assets's config
# Can not compress the CSS/JS on Dev environment.
app.config['ASSETS_DEBUG'] = True
app.config['AUTOPREFIXER_BIN'] = basedir + '/node_modules/postcss-cli/bin/postcss'
app.config['AUTOPREFIXER_BROWSERS'] = ['> 1%', 'last 2 versions', 'firefox 24', 'opera 12.1']

# Define the set for js and css file.
css = Bundle(
    'css/test.css',
    'css/test1.css',
    filters='autoprefixer6, cssmin',
    output='assets/css/common.css')

js = Bundle(
    'js/test.js',
    filters='jsmin',
    output='assets/js/common.js')

# register
assets_env.register('js', js)
assets_env.register('css', css)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
