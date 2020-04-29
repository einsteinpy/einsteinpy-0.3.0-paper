"""The following file contains generic functions to produce the plots in the einsteinpy paper."""
import os
import seaborn
import matplotlib
from pathlib import Path
import pandas as pd

import einsteinpy

einsteinpy_releases = {
    #".3": "2013/08/30",
    ".2.1": "2019/11/03",
    ".2": "2019/07/14",
    ".1": "2019/03/08",
}

# data_dir = Path(os.path.join(Path(__file__).parents[1], "data"))


def get_author_transform_mapping(repo):
    """
    Read the mailmap into a `dict` to be used to transform authors.

    Parameters
    ----------
    repo : `git.Repo`
    """

    mailmap_file = Path(repo.working_tree_dir) / ".mailmap"

    if not mailmap_file.exists():
        raise ValueError("This repo does not have a mailmap")

    with open(mailmap_file) as fd:
        mailmap_lines = fd.readlines()

    for i, line in enumerate(mailmap_lines):
        line = line.strip().lower()
        split = line.find("> ") + 1
        mailmap_lines[i] = (line[:split].strip(), line[split + 1 :].strip())[::-1]

    return dict(mailmap_lines)


def get_author_email_list(repo):
    """
    Read the mailmap and return a list of all author emails.

    Parameters
    ----------
    repo : `git.Repo`
    """
    mailmap_dict = get_author_transform_mapping(repo)
    all_emails = set([mailmap_dict[key].split("<")[1][0:-1] for key in mailmap_dict])
    # remove emails with address users.noreply.github.com
    all_good_emails = [
        this_email for this_email in all_emails if "noreply" not in this_email
    ]
    return all_good_emails


def add_releases_vs_time(ax1):
    """Adds vertical lines to a plot as a function of time with the einsteinpy release dates."""
    release_times = [pd.to_datetime(s) for s in einsteinpy_releases.values()]
    _, _, _, ymax = ax1.axis()
    ax2 = ax1.twiny()
    ax2.plot(release_times, [ymax - 1] * len(release_times), ".", alpha=0)
    ax2.set_xticks(release_times)
    ax2.set_xticklabels(einsteinpy_releases.keys())
    ax2.minorticks_off()
    ax2.set_xlabel("Version Release")
    # for this_release in release_times:
    #    ax2.axvline(this_release, color="black", linestyle="..", linewidth=0.1)
