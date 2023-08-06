# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['streamlit_image_select']

package_data = \
{'': ['*'],
 'streamlit_image_select': ['frontend/.env',
                            'frontend/.env',
                            'frontend/.env',
                            'frontend/.env',
                            'frontend/.env',
                            'frontend/.prettierrc',
                            'frontend/.prettierrc',
                            'frontend/.prettierrc',
                            'frontend/.prettierrc',
                            'frontend/.prettierrc',
                            'frontend/build/*',
                            'frontend/build/static/js/*',
                            'frontend/package-lock.json',
                            'frontend/package-lock.json',
                            'frontend/package-lock.json',
                            'frontend/package-lock.json',
                            'frontend/package-lock.json',
                            'frontend/package.json',
                            'frontend/package.json',
                            'frontend/package.json',
                            'frontend/package.json',
                            'frontend/package.json',
                            'frontend/public/*',
                            'frontend/src/*',
                            'frontend/tsconfig.json',
                            'frontend/tsconfig.json',
                            'frontend/tsconfig.json',
                            'frontend/tsconfig.json',
                            'frontend/tsconfig.json']}

install_requires = \
['streamlit>=1.19.0,<2.0.0']

setup_kwargs = {
    'name': 'streamlit-image-select',
    'version': '0.6.0',
    'description': '🖼️ An image select component for Streamlit',
    'long_description': '# streamlit-image-select 🖼️\n\n[![PyPI](https://img.shields.io/pypi/v/streamlit-image-select)](https://pypi.org/project/streamlit-image-select/)\n\n**An image select component for Streamlit.**\n\nThis custom component works just like `st.selectbox` but with images. It\'s a great option\nif you want to let the user select an example image, e.g. for a computer vision app!\n\n---\n\n<h3 align="center">\n  🏃 <a href="https://image-select.streamlitapp.com/">Try out the demo app</a> 🏃\n</h3>\n\n---\n\n<p align="center">\n    <a href="https://image-select.streamlitapp.com/"><img src="images/demo.gif" width=600></a>\n</p>\n\n\n## Installation\n\n```bash\npip install streamlit-image-select\n```\n\n## Usage\n\n```python\nfrom streamlit_image_select import image_select\nimg = image_select("Label", ["image1.png", "image2.png", "image3.png"])\nst.write(img)\n```\n\nSee [the demo app](https://image-select.streamlitapp.com/) for a detailed guide!\n\n\n## Development\n\n> **Warning**\n> You only need to run these steps if you want to change this component or \ncontribute to its development!\n\n### Setup\n\nFirst, clone the repository:\n\n```bash\ngit clone https://github.com/jrieke/streamlit-image-select.git\ncd streamlit-image-select\n```\n\nInstall the Python dependencies:\n\n```bash\npoetry install --dev\n```\n\nAnd install the frontend dependencies:\n\n```bash\ncd streamlit_image_select/frontend\nnpm install\n```\n\n### Making changes\n\nTo make changes, first go to `streamlit_image_select/__init__.py` and make sure the \nvariable `_RELEASE` is set to `False`. This will make the component use the local \nversion of the frontend code, and not the built project. \n\nThen, start one terminal and run:\n\n```bash\ncd streamlit_image_select/frontend\nnpm start\n```\n\nThis starts the frontend code on port 3001.\n\nOpen another terminal and run:\n\n```bash\ncp demo/streamlit_app.py .\npoetry shell\nstreamlit run streamlit_app.py\n```\n\nThis copies the demo app to the root dir (so you have something to work with and see \nyour changes!) and then starts it. Now you can make changes to the Python or Javascript \ncode in `streamlit_image_select` and the demo app should update automatically!\n\nIf nothing updates, make sure the variable `_RELEASE` in `streamlit_image_select/__init__.py` is set to `False`. \n\n\n### Publishing on PyPI\n\nSwitch the variable `_RELEASE` in `streamlit_image_select/__init__.py` to `True`. \nIncrement the version number in `pyproject.toml`. Make sure the copy of the demo app in \nthe root dir is deleted or merged back into the demo app in `demo/streamlit_app.py`.\n\nBuild the frontend code with:\n\n```bash\ncd streamlit_image_select/frontend\nnpm run build\n```\n\nAfter this has finished, build and upload the package to PyPI:\n\n```bash\ncd ../..\npoetry build\npoetry publish\n```\n\n## Changelog\n\n### 0.6.0 (March 28, 2023)\n- Removed `st.experimental_memo`, which is deprecated. \n- Changed minimum version of Streamlit to 1.19.\n  \n### 0.5.1 (November 20, 2022)\n- Hotfix, forgot to switch the RELEASE variable back to True :wink:\n\n### 0.5.0 (November 20, 2022)\n- Added `return_value` parameter to be able to get the index of the selected image.\n- Improved error messages. \n\n### 0.4.0 (November 20, 2022)\n- Added `index` parameter to set the initially selected image.\n- Improved input arg checks. \n\n### 0.3.0 (November 13, 2022)\n- Added `use_container_width` parameter to customize the width of the component. \n- Made `key` and `use_container_width` parameters keyword-only.\n- Refactored CSS classes.\n',
    'author': 'Johannes Rieke',
    'author_email': 'johannes.rieke@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8, !=2.7.*, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, !=3.6.*, !=3.7.*',
}


setup(**setup_kwargs)
