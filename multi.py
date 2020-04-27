"""
This module is used to get data and download & extract files
"""
import urllib
import tarfile
import requests


def download_extract(link, path):
    """
    Directly extract a tarfile from a downloading link
    without downloading it first
    """
    with urllib.request.urlopen(link) as file:
        with tarfile.open(fileobj=file, mode='r|*') as tar_file:
            tar_file.extractall(path)


def get_release_data(api_link, releases='every'):
    """
    Get basic data for releases... select the mode
    to get certain releases
    """
    json_objects = requests.get(api_link).json()
    egs_releases = []

    def add_data(json_object):
        assets = json_object.get('assets')[0]
        egs_releases.append(
            {
                'prerelease': json_object.get('prerelease'),
                'download_url': assets.get('browser_download_url'),
                'tag_name': json_object.get('tag_name')
                }
            )

    def every():
        nonlocal egs_releases, json_objects
        for json_object in json_objects:
            add_data(json_object)

    def conditional_last():
        """
        If prelease is the last release it adds the release data
        and it adds the last release's data so the user can choose
        """
        nonlocal egs_releases, json_objects
        counter = 0

        def is_prerelease(json_object):
            if json_object.get('prerelease'):
                return True
            return False

        for json_object in json_objects:
            _is_prerelease = is_prerelease(json_object)

            if not counter and _is_prerelease:
                # if counter is 0 and it is a prerelease
                add_data(json_object)

            if not _is_prerelease:
                add_data(json_object)
                break

            counter += 1

    prereleases_options = {
        'every': every,
        'conditional': conditional_last
        }
    prereleases_options.get(releases)()
    return egs_releases
