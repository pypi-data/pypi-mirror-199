# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ptpapi', 'ptpapi.scripts', 'ptpapi.sites']

package_data = \
{'': ['*']}

install_requires = \
['Tempita>=0.5.2,<0.6.0',
 'beautifulsoup4>=4.10.0,<5.0.0',
 'bencode.py>=4.0.0,<5.0.0',
 'guessit>=3.4.3,<4.0.0',
 'humanize>=4.0.0,<5.0.0',
 'libtc>=1.3.1,<2.0.0',
 'pyrosimple>=2.7.0,<3.0.0',
 'requests>=2.27.1,<3.0.0']

entry_points = \
{'console_scripts': ['ptp = ptpapi.scripts.ptp:main',
                     'ptp-reseed = ptpapi.scripts.ptp_reseed:main',
                     'ptp-reseed-machine = '
                     'ptpapi.scripts.ptp_reseed_machine:main']}

setup_kwargs = {
    'name': 'ptpapi',
    'version': '0.9.0',
    'description': 'A small API for a mildly popular movie site',
    'long_description': '# PTPAPI\n\n[![PyPI](https://img.shields.io/pypi/v/ptpapi)](https://pypi.org/project/ptpapi/)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ptpapi)\n\nA small API for a mildly popular movie site. The goal was to be able\nto collect as much information in as few network requests as possible.\n\n## Dependencies\n\n* Python 3.7+\n* pip\n\n## Installation\n\nUse of a\n[virtualenv](https://virtualenv.readthedocs.org/en/latest/userguide.html#usage)\nor [pipx](https://pypa.github.io/pipx/) is optional, but highly\nrecommended.\n\n`pip install ptpapi`\n\n## Configuration\n\nOpen the file `~/.ptpapi.conf` for editing, and make sure it looks like the following:\n\n```ini\n[Main]\n\n[PTP]\nApiUser=<ApiUser>\nApiKey=<ApiKey>\n```\n\nBoth values can be found in the "Security" section of your\nprofile. This is only the minimum required configuration. See\n`ptpapi.conf.example` for a full-futured config file with comments.\n\n## Usage\n\nThe three CLI commands are `ptp`, `ptp-reseed`, and `ptp-bookmarks`\n\n### `ptp`\n\nThis is a generally utility to do various things inside PTP. As of\nright now it can download files, search the site for movies, and list\nmessage in your inbox.\n\nSee `ptp help` for more information.\n\n#### `ptp inbox`\n\nA small utility to read messages in your inbox. No reply capability currently.\n\n#### `ptp download`\n\nAn alias for `ptp-search -d`\n\n#### `ptp search`\n\nThis subcommand lets you search the site for movies. It can take movie\nand permalinks, as well as search by arbitrary parameters, and the\n`-d` flag allows for downloading matching torrents. For instance:\n- `ptp search year=1980-2000 taglist=sci.fi`\n- `ptp search "Star Wars"`.\n\nIt can also accept URLs for torrents and collages:\n- `ptp search "https://passthepopcorn.me/torrents.php?id=68148"`\n- `ptp search "https://passthepopcorn.me/collages.php?id=2438"`\n\nand regular search URLs:\n- `ptp search "https://passthepopcorn.me/torrents.php?action=advanced&year=1980-2000&taglist=action"`.\n\nAs a general rule of thumb anything supported by the advanced site\nsearch will work with `ptp search`, e.g. searching\n`https://passthepopcorn.me/torrents.php?action=advanced&taglist=comedy&format=x264&media=Blu-ray&resolution=1080p&scene=1`\nis the same as `ptp search taglist=comedy format=x264 media=Blu-ray\nresolution=1080p scene=1`.\n\nTo work with multiple pages of results, use the `--pages <num>` flag.\n\nThere are a couple aliases to make life easier:\n\n* `genre`, `genres`, `tags` -> `taglist`\n* `name` -> `searchstr`\n* `bookmarks` -> Search only your bookmarks\n\nIn addition, [Tempita](http://pythonpaste.org/tempita/) can be used\nfor custom formatting. For instance, `ptp search --movie-format=""\n--torrent-format="{{UploadTime}} - {{ReleaseName}}" year=1980-2000\ntaglist=sci.fi grouping=no`.\n\nUsing the `-d` flag will download one torrent from each of the matched\ntorrents (deciding which one to download is done via\n[filters](#filters)) to the\n[downloadDirectory](ptpapi.conf.example#L9).\n\nThe `-p/--pages [int]` option can be used to scrape multiple pages at\nonce. N.B.: If any `page` parameter is in the original search query,\npaging will start from that page.\n\n#### `ptp fields`\n\nSimply list fields that can be used for the `ptp search` formatting.\n\n### `ptp-reseed`\n\nThis script automatically matches up files to movies on PTP. It\'s most\nbasic usage is `ptp-reseed <file path>`. This will search PTP for any\nmovies matching that filename, and if it finds a match, will\nautomatically download the torrent and add it to rtorrent. It can do\nsome basic file manipulation if it finds a close enough match.\n\nFor instance, if you have the file `Movie.2000.mkv`, and the torrent\ncontains `Movie (2000)/Movie.2000.mkv`, the script will try to\nautomatically create the folder `Movie (2000)` and hard link the file\ninside of it before attempting to seed it.\n\nSee `ptp-reseed -h` and `ptpapi.conf.example` for more information and\nconfiguration options.\n\n#### guessit\n\nBy default the script looks for exact matches against file names and\nsizes. If you\'d like the name matching to be less strict, you can\ninstall the guessit library (`pip install \'guessit>=3\'`), and if the\nfilename search fails, the script will attempt to parse the movie name\nout of the file with guessit.\n\n### `ptp-reseed-machine`\n\nThis tool is meant to complement `ptp-reseed`, by taking using\n[Prowlarr](https://github.com/Prowlarr/Prowlarr) to find and download\npeotential reseeds from any supported site.\n\nTo get it set up, first [install\nProwlarr](https://wiki.servarr.com/prowlarr/installation). Be sure\nyour instance (or any of the *arrs) isn\'t exposed to the internet!\nFrom, simply use the UI to add any trackers/indexers you\'d like to\nsearch, as well as any downloaders. Then, add the following config to\n`~/.ptpapi.conf`:\n\n```ini\n[Prowlarr]\nurl=http://YOUR_PROWLER_HOSTNAME_OR_IP/\napi_key=YOUR_API_KEY\n```\n\nIf everything thing is all setup, running `ptp-reseed-machine` will\nscrape the first page of needforseed.php and attempt to download any\npotential matches. See `--help` for passing additional parameters or\ndifferent search targets.\n\nAfter a download has been triggered, you can then use `ptp-reseed`\nwith your download client of choice to automatically reseed the path\ninto a client. Here\'s a simple example of a post script for sabnzbd:\n\n```bash\n#!/bin/bash\nif [[ "$SAB_PP_STATUS" -eq 0 ]]; then\n  ls *.iso *.img 2>/dev/null | xargs -r 7z x\n  ptp-reseed "$SAB_COMPLETE_DIR"\nfi\n```\n\nor for a `rtorrent.rc`:\n```ini\nmethod.set_key = event.download.finished, ptp_reseed, "execute.nothrow.bg={ptp-reseed,$d.base_path=}"\n```\n\n## Concepts\n\n### Filters\n\nFilters were designed as a way to take a full movie group, and narrow\nit down to a single torrent. A filter consists of multiple\nsub-filters, where the first sub-filter to match will download the\ntorrent, and if not, the next sub-filter will be checked. If none of\nthe sub-filters match, no download will occur. Filters are separate\nfrom the actual search parameters sent to the site\n\nThe full list of possible values for picking encodes is:\n* `GP` or `Scene`\n* `576p` or `720p` or `1080p`\n* `XviD` or `x264`\n* `HD` or `SD`\n* `remux` or `not-remux`\n* `seeded` - the number of seeds is greater than 0 (deprecated, use `seeders>0`)\n* `not-trumpable` - ignore any trumpable torrents\n* `unseen` - ignores all torrents if you\'ve marked the movie as seen or rated it\n* `unsnatched` - ignore all torrents unless you\'ve never snatched one before (note that seeding counts as "snatched", but leeching doesn\'t)\nThere are also values that allow for simple comparisons, e.g. `size>1400M`.\n* `seeders`\n* `size`\n\nNote that it\'s possible to have two incompatible values, e.g. `GP` and\n`Scene`, but this simply means the sub-filter won\'t ever match a\ntorrent, and will always be skipped over.\n\nThe possible values for sorting are:\n* `most recent` (the default if none are specified)\n* `smallest`\n* `most seeders`\n* `largest`\n\n#### Examples\n\nFor instance, the filter `smallest GP,720p scene,largest` would\nattempt to download the smallest GP. If there are no GPs, it will try\nto find a 720p scene encode. If it can\'t find either of those, it will\njust pick the largest torrent available.\n\nAs another example, if you wanted to filter for encodes that are less\nthan 200MiB with only one seeder, you could use `seeders=1 size<200M`.\n\n## Notes\n\nI did this mostly for fun and to serve my limited needs, which is why\nit\'s not as polished as it could be, and will probably change\nfrequently.  Pull requests are welcomed.\n\n### Deprecated Configuration\n\nThe new ApiUser/ApiKey system is preferred, however if you find bugs\nor limitations, the old cookie-based method can be used:\n\nOpen the file `~/.ptpapi.conf` for editing, and make sure it looks\nlike the following:\n\n```ini\n[Main]\n\n[PTP]\nusername=<username>\npassword=<password>\npasskey=<passkey>\n```\n',
    'author': 'kannibalox',
    'author_email': 'kannibalox@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kannibalox/PTPAPI',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.2,<4.0',
}


setup(**setup_kwargs)
