# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'mkdocs_publisher',
 'blog': 'mkdocs_publisher/blog',
 'blog.lang': 'mkdocs_publisher/blog/lang',
 'minifier': 'mkdocs_publisher/minifier'}

packages = \
['auto_nav',
 'blog',
 'blog.lang',
 'minifier',
 'mkdocs_publisher',
 'mkdocs_publisher._cli',
 'mkdocs_publisher._extra',
 'mkdocs_publisher._extra.assets',
 'mkdocs_publisher._extra.assets.stylesheets',
 'mkdocs_publisher._extra.assets.templates',
 'mkdocs_publisher.auto_nav',
 'mkdocs_publisher.blog',
 'mkdocs_publisher.blog.lang',
 'mkdocs_publisher.minifier']

package_data = \
{'': ['*']}

install_requires = \
['mkdocs-material>=9.1.3,<10.0.0',
 'mkdocs>=1.4.2,<2.0.0',
 'pymdown-extensions>=9.10,<10.0',
 'python-frontmatter>=1.0.0,<2.0.0']

entry_points = \
{'console_scripts': ['publisher = mkdocs_publisher._cli.publisher:app'],
 'mkdocs.plugins': ['pub-auto-nav = '
                    'mkdocs_publisher.auto_nav.plugin:AutoNavPlugin',
                    'pub-blog = mkdocs_publisher.blog.plugin:BlogPlugin',
                    'pub-minifier = '
                    'mkdocs_publisher.minifier.plugin:MinifierPlugin']}

setup_kwargs = {
    'name': 'mkdocs-publisher',
    'version': '0.4.0',
    'description': 'Publishing plugins for MkDocs',
    'long_description': "---\ndate: 2023-02-28 12:30:18\nupdate: 2023-03-20 13:03:13\n---\n# Publisher plugin for MkDocs\n\n[![PyPI version](https://badge.fury.io/py/mkdocs-blog-in.svg)](https://badge.fury.io/py/mkdocs-blog-in)\n[![Github All Releases](https://img.shields.io/github/downloads/mkusz/mkdocs-blog-in/total.svg)]()\n\nPublishing platform plugins for [MkDocs](https://www.mkdocs.org/) that include:\n\n- `pub-auto-nav` - building site navigation right from files (no need for manual definition in config)\n- `pub-blog` - adds blogging capability,\n- `pub-minifier` - file size optimization (good for SEO and overall page size optimization).\n\n## Installation\n\n```commandline\npip install mkdocs-publisher\n```\n\n## Basic usage\n\n> **Note**\n> As a base for any development, [mkdocs-material](https://squidfunk.github.io/mkdocs-material/) theme was used. If you are willing to use any other theme, you may (or may not) face some issues. If this happens, please submit an issue.\n\n> **Warning**\n> Consider this plugin as a beta, so before any use make sure you have a backup of your data.\n\nIf you have found any issue, have an idea for a feature, please submit an issue.\n\n## Features\n\nList of included features (more documentation is needed):\n\n- automatic blog post index page generation with blog post teasers based on delimiter inside a blog post and own template (delimiter can be changed in plugin config in `mkdocs.yaml`),\n- blog post/page update date based on blog post metadata,\n- separate directory for blog post documents with auto-generated separate navigation (blog posts are sorted from newest to oldest),\n- home page set to blog post index with possibility to rename,\n- auto-adding link to full blog post from blog post index file (under each post that has teaser delimiter, if delimiter is not present, then full post is inside post index file, but is preserved in blog post navigation and site map),\n- added sub-pages for blog posts: archive, categories, tags,\n- minification plugin for graphics and documentation files.\n\n## How To\n\nMore detailed information on how to setup, configure and write a blog posts and/or documentation can be found in [documentation](/mkdocs-publisher)\n\n## Todo's\n\nA full list of planned developments can be found on [this documentation page](/mkdocs-publisher/dev/backlog).\n\n## Version history\n\n### 0.4.0 - 2023-03-28\n\nGeneral:\n\n- changed: project rename\n- added: cross configuration of blog and auto-nav plugins:\n  - blog does not add auto-nav meta files\n  - auto-nav automatically adds blog directory to skipped directories since it will be built by blog\n  - if one of the plugins is not enabled, other is not using its values\n- add: documentation\n\nBlog:\n\n- added: possibility to choose a blog as a starting page with option to define manually blog in nav configuration\n- added: `slug` config option for setting an entire blog's main directory URL\n- changed: internal file structure refactor with new global plugin config (BlogConfig class) that will help with further development with small fixes and improvements\n- changed: blog subdirectory navigation creation (entry path needs to be equal to subdirectory name)\n- fixed: live reload infinite loop during `serve` caused by temporary files created and removed in blog directory\n- fixed: navigation is no longer overridden by a blog (if there is no other nav, blog will create on with recent posts as a main page)\n\nMinifier (new plugin):\n\n- added: PNG image minifier (using: pngquant and oxipng)\n- added: JPG image minifier (using: mozjpeg)\n- added: SVG image minifier (using: svgo)\n- added: HTML file minifier (using: html-minifier)\n- added: CSS file minifier (using: postcss with plugins: cssnano, svgo)\n- added: JS file minifier (using: uglifyjs)\n\nAuto-nav (new plugin):\n\n- added: build navigation based on file names\n- added: directory metadata and additional settings can be set in a frontmatter of `*.md` file (default to `README.md`)\n- added: configuration of sort prefix delimiter\n- added: sort prefix removal in URL and site files\n- added: read file title from `title` meta data key\n\n### 0.3.0 - 2023.02.20\n\n- fixed: for wrong directory structure in site-packages after install\n\n### 0.2.0 - 2023.02.19\n\n- added: sub-pages for archive, categories, blog\n- added: configurable blog posts pagination with page navigation\n- added: interface language change: EN and PL (help wanted with more languages)\n- added: possibility to override for all interface text elements\n\n### 0.1.0 - initial release\n\n- added: blog post update date based on metadata\n- added: blog post URL link based on metadata\n- added: blog post tags and categories based on metadata\n- added: support for blog post teaser\n- added: auto generation of blog posts navigation\n",
    'author': "Maciej 'maQ' Kusz",
    'author_email': 'maciej.kusz@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mkusz/mkdocs-publisher',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
