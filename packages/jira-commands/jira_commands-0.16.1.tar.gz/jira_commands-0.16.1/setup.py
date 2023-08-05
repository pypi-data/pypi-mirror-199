# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jira_commands', 'jira_commands.cli']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'cryptography>=38.0.3,<40.0.0',
 'jira>=3.1.1,<4.0.0',
 'thelogrus>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['jc = jira_commands.cli.jc:jc_driver',
                     'jc-assign-ticket = '
                     'jira_commands.cli.crudops:assignTicket',
                     'jc-close-ticket = jira_commands.cli.crudops:closeTicket',
                     'jc-comment-on-ticket = '
                     'jira_commands.cli.crudops:commentOnTicket',
                     'jc-create-ticket = '
                     'jira_commands.cli.crudops:createTicket',
                     'jc-custom-field-allowed-values = '
                     'jira_commands.cli.vivisect:listAllowedFieldValues',
                     'jc-dump-all-custom-field-allowed-values = '
                     'jira_commands.cli.vivisect:dump_all_customfield_allowed_values',
                     'jc-dump-all-customfield-allowed-values = '
                     'jira_commands.cli.vivisect:dump_all_customfield_allowed_values',
                     'jc-examine-ticket = jira_commands.cli.vivisect:vivisect',
                     'jc-extract-custom-field-mappings = '
                     'jira_commands.cli.map_extractor:create_mapping_file',
                     'jc-extract-customfield-mappings = '
                     'jira_commands.cli.map_extractor:create_mapping_file',
                     'jc-extract-values-for-custom-field = '
                     'jira_commands.cli.vivisect:extract_allowed_values',
                     'jc-get-link-types = '
                     'jira_commands.cli.crudops:getLinkTypes',
                     'jc-get-priorities = '
                     'jira_commands.cli.crudops:getPriorities',
                     'jc-get-priority-ids = '
                     'jira_commands.cli.crudops:getPriorities',
                     'jc-link-tickets = jira_commands.cli.crudops:linkTickets',
                     'jc-list-project-tickets = '
                     'jira_commands.cli.list:listTickets',
                     'jc-list-ticket-transitions = '
                     'jira_commands.cli.crudops:getTransitions',
                     'jc-ticket-assign = '
                     'jira_commands.cli.crudops:assignTicket',
                     'jc-ticket-close = jira_commands.cli.crudops:closeTicket',
                     'jc-ticket-comment = '
                     'jira_commands.cli.crudops:commentOnTicket',
                     'jc-ticket-create = '
                     'jira_commands.cli.crudops:createTicket',
                     'jc-ticket-dump-metadata = '
                     'jira_commands.cli.vivisect:dump_metadata',
                     'jc-ticket-examine = jira_commands.cli.vivisect:vivisect',
                     'jc-ticket-link = jira_commands.cli.crudops:linkTickets',
                     'jc-ticket-metadata = '
                     'jira_commands.cli.vivisect:dump_metadata',
                     'jc-ticket-transition-list = '
                     'jira_commands.cli.crudops:getTransitions',
                     'jc-ticket-transition-set = '
                     'jira_commands.cli.crudops:transitionTo',
                     'jc-ticket-vivisect = jira_commands.cli.vivisect:vivisect',
                     'jc-transition-ticket-to = '
                     'jira_commands.cli.crudops:transitionTo',
                     'jc-values-for-custom-field = '
                     'jira_commands.cli.vivisect:extract_allowed_values',
                     'jc-vivisect-ticket = '
                     'jira_commands.cli.vivisect:vivisect']}

setup_kwargs = {
    'name': 'jira-commands',
    'version': '0.16.1',
    'description': 'Command line utilities for interacting with JIRA',
    'long_description': "# jira-commands\n\n[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/license/apache2-0-php/)\n[![Build Status](https://img.shields.io/endpoint.svg?url=https%3A%2F%2Factions-badge.atrox.dev%2Funixorn%2Fjira-commands%2Fbadge%3Fref%3Dmain&style=plastic)](https://actions-badge.atrox.dev/unixorn/jira-commands/goto?ref=main)\n![Megalinter](https://github.com/unixorn/jira-commands/actions/workflows/mega-linter.yml/badge.svg)\n![PyPI - Format](https://img.shields.io/pypi/format/jira-commands?style=plastic)\n\n<!-- START doctoc generated TOC please keep comment here to allow auto update -->\n<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->\n## Table of Contents\n\n- [Scripts](#scripts)\n- [Configuration](#configuration)\n  - [Basic Authentication](#basic-authentication)\n  - [OAuth Authentication](#oauth-authentication)\n  - [PAT authentication](#pat-authentication)\n- [Installation](#installation)\n  - [Run via docker / nerdctl](#run-via-docker--nerdctl)\n  - [Direct pip install](#direct-pip-install)\n  - [ZSH plugin](#zsh-plugin)\n    - [zgenom](#zgenom)\n    - [Antigen](#antigen)\n    - [oh-my-zsh](#oh-my-zsh)\n\n<!-- END doctoc generated TOC please keep comment here to allow auto update -->\n\nSome command-line tools for interacting with JIRA.\n\n## Scripts\n\nAll of these scripts support `--help` to get a detailed list of command line options.\n\n| Name                         | Description                                           |\n| -----------------------------| ----------------------------------------------------- |\n| `jc` | Main driver. Will run all the other commands inside a docker container for you. |\n| `jc assign ticket` / `jc ticket assign` | Assign a ticket to someone. |\n| `jc close ticket` / `jc ticket close` | Close a ticket |\n| `jc comment on ticket` / `jc ticket comment` | Comment on a ticket |\n| `jc create ticket` / `jc ticket create` | Create a ticket. You will need|\n| `jc custom field allowed values` | List a custom field's allowed values since JIRA isn't forthcoming about them. |\n| `jc examine ticket` / `jc ticket examine` | Detailed dump of a ticket and all its custom field names |\n| `jc extract customfield mappings` | Extract the custom field mappings from an issue into a file |\n| `jc get link types` | Prints the names of all link types defined on your JIRA instance. |\n| `jc get priority ids` | Prints the names of all ticket priorities defined on your JIRA instance. |\n| `jc link tickets` / `jc ticket link` | Link two tickets. Use `jc get link types` to see what link names are defined on your JIRA server. Case matters. |\n| `jc list project tickets` | List open tickets in a given JIRA project |\n| `jc list ticket transitions` / `jc ticket transition list` | See the availale transitions for a given ticket. |\n| `jc transition ticket to` / `jc ticket transition set` | Transition a ticket to another state. Use `jc list ticket transitions` to see which are available  |\n| `jc vivisect ticket` / `jc ticket vivisect` | Detailed dump of a ticket to find out all the custom field names and other innards. |\n\nThe `jc` program is the main driver script and will find the subcommands, so you can do `jc ticket comment --ticket ABC-123 --comment 'foo bar baz'` and it will find the `jc-ticket-comment` script and run it with the `--ticket` and `--comment` arguments.\n\nIf you're using the docker method, `jc` will automatically run the subcommands inside a container for you. If you've installed via pip, it'll find the commands where they were installed in your `$PATH`.\n\n## Configuration\n\nThe `jc` commands all read settings from `~/.jira-commands/jira.yaml`. Settings in the file can be overridden by specifying command-line options.\n\n### Basic Authentication\n\nI'm setting my username and jira server in the example configuraation file below. The tools will ask for my password when I run them.\n\n```yaml\njira_server: https://jira.example.com\nusername: YOUR_JIRA_USER\n```\n\nYou can specify a `password` key but it's a terrible idea.\n\n### OAuth Authentication\n\nHere's an example settings file for oauth authentication. Add `--auth=OAUTH` to use oath instead of basic authentication.\n\n```yaml\njira_server: https://jira.example.com/\noauth_access_token: ABCDabcdABCDabcdABCDabcdABCDabcd\noauth_access_token_secret: ABCDabcdABCDabcdABCDabcdABCDabcd\noauth_consumer_key: OAUTH_CONSUMER_KEY_ID\noauth_private_key_pem_pathL: /path/to/pem/file\nusername: YOUR_JIRA_USER\n```\n\n### PAT authentication\n\nHere's an example settings file for PAT authentication.\n\n```yaml\nusername: YOUR_JIRA_USER\npat_token: xyzzyAbc123\njira_server: https://jira.example.com/\n```\n\n## Installation\n\n### Run via docker / nerdctl\n\nThis is the recommended way to use the `jc` commands, and how it will be run if you use one of the ZSH frameworks detailed below.\n\nIf you're not using a ZSH framework, clone this repository and add its `bin` directory to your `$PATH`. It contains a `jc` script that will detect whether you have `nerdctl` or `docker` and if it finds them, map `~/jira-commands` (and the configuration file there) into a volume in the `jira-commands` container and run the tools inside the container.\n\n### Direct pip install\n\n`sudo pip install jira-commands` will install the command-line tools via `pip`. This may cause compatibility annoyances with other python tools on your system, so there's a `docker`/`nerdctl` option as well.\n\n### ZSH plugin\n\nThe tooling has been packaged as a ZSH plugin to make using it as easy as possible for ZSH users.\n\n#### zgenom\n\nIf you're using [Zgenom](https://github.com/jandamm/zgenom):\n\n1. Add `zgenom load unixorn/jira-commands` to your `.zshrc` with your other plugins\n2. `zgenom reset && zgenom save`\n\n#### Antigen\n\nIf you're using [Antigen](https://github.com/zsh-users/antigen):\n\n1. Add `antigen bundle unixorn/jira-commands` to your .zshrc where you've listed your other plugins.\n2. Close and reopen your Terminal/iTerm window to refresh context and use the plugin. Alternatively, you can run `antigen bundle unixorn/jira-commands` in a running shell to have `antigen` load the new plugin.\n\n#### oh-my-zsh\n\nIf you're using [oh-my-zsh](https://ohmyz.sh):\n\n1. Clone the repository into a new `jira-commands` directory in oh-my-zsh's plugin folder:\n\n    `git clone https://github.com/unixorn/jira-commands.git $ZSH_CUSTOM/plugins/jira-commands`\n\n2. Edit your `~/.zshrc` and add `jira-commands` – same as clone directory – to the list of plugins to enable:\n\n    `plugins=( ... jira-commands )`\n\n3. Then, restart your terminal application to refresh context and use the plugin. Alternatively, you can source your current shell configuration:\n\n    `source ~/.zshrc`\n",
    'author': 'Joe Block',
    'author_email': 'jpb@unixorn.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/unixorn/jira-commands',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0.0',
}


setup(**setup_kwargs)
