# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flask_ckeditor']

package_data = \
{'': ['*'], 'flask_ckeditor': ['templates/*']}

install_requires = \
['Flask>=2.2.2,<3.0.0']

setup_kwargs = {
    'name': 'flask-ckeditor-manager',
    'version': '0.1.42',
    'description': 'A simple interface to use CKEditor5 with Flask',
    'long_description': '# Flask-CKEditor-Manager\n\nFlask-CKEditor-Manager _(from now on **FCKM**)_ provides a simple interface to use CKEDitor5 javascript library with Flask. Greatly inspired by Flask-CKEditor\n\n```{warning}\n🚧 This package is under heavy development..\n```\n\n## Installation\n\nInstall the extension with pip:\n\n```bash\npip install flask-ckeditor-manager\n```\n\nInstall with poetry:\n\n```bash\npoetry add flask-ckeditor-manager\n```\n\n## Configuration\n\nThis are some of the settings available\n\n| Config                   | Description                                                                       | Type | Default     |\n| ------------------------ | --------------------------------------------------------------------------------- | ---- | ----------- |\n| CKEDITOR_LICENSE_KEY     | CKEditor License key                                                              | str  | `None`      |\n| CKEDITOR_EDITOR_TYPE     | Editor package to be displayed                                                    | str  | `"classic"` |\n| CKEDITOR_LOCAL_PATH      | If custom package is present, this is the path in the static folder.              | str  | `None`      |\n| CKEDITOR_LANGUAGE        | The lengague of the editor.                                                       | str  | `None`      |\n| CKEDITOR_ENABLE_CSRF     | Enable CSRF protection in SimpleUpload adapter                                    | bool | `None`      |\n| CKEDITOR_UPLOAD_ENDPOINT | SimpleUpload adapter endpoint. Must follow the CKEditor5 estipulations. Read more | str  | `None`      |\n| CKEDITOR_WATCHDOG        | If watchdog plugin installed change this value to True to enable its rendering    | bool | `None`      |\n\n## Usage\n\nOnce installed the **FCKM** is easy to use. Let\'s walk through setting up a basic application. Also please note that this is a very basic guide: we will be taking shortcuts here that you should never take in a real application.\n\nTo begin we\'ll set up a Flask app:\n\n```python\nfrom flask import Flask\n\napp = Flask(__name__)\n```\n\n### Setting up extension\n\n**FCM** works via a CKEditorManager object. To kick things off, we\'ll set up the `ckeditor_manager` by instantiating it and telling it about our Flask app:\n\n```python\nfrom flask_ckeditor import CKEditorManager\n\nckeditor_manager = CKEditorManager()\nckeditor_manager.init_app(app)\n```\n\n### Load resources\n\nOnce the extension is set up, this will make available the `ckeditor` object into the templates context so you could load the javascript package easily, like this.\n\n```html\n<head>\n  {{ ckeditor.load() }}\n</head>\n```\n\n### Rendering the editor\n\nOnce created you can pass the `Chart` object to render_template and use it likewise.\n\n```html\n<!-- ckeditor.load() must be called before this line -->\n<textarea id="editor"></textarea>\n<div class="my-classes">{{ ckeditor.config(\'editor\') }}</div>\n```\n',
    'author': 'Sebastian Salinas',
    'author_email': 'seba.salinas.delrio@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
