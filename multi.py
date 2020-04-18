import urllib
import tarfile
import requests


def download_extract(link, path):
    with urllib.request.urlopen(link) as file:
        with tarfile.open(fileobj=file, mode='r|*') as tar_file:
            tar_file.extractall(path)

def get_download_link(link, pre_releases='first', i_releases=2):
    json_objects = requests.get(link).json()
    egs_releases = []

    def every():
        nonlocal egs_releases, i_releases, json_objects
        counter = 0
        for json_object in json_objects[0:i_releases]:
            assets = json_object.get('assets')[0]
            egs_releases.append({
                'prerelease': json_object.get('prerelease'),
                'download_url': assets.get('browser_download_url'),
                'tag_name': json_object.get('tag_name')
                })

    def first():
        nonlocal egs_releases, i_releases, json_objects
        i = 0
        counter = 0
        for json_object in json_objects:
            prerelease = json_object.get('prerelease')
            assets = json_object.get('assets')[0]
            if not i and prerelease:
                egs_releases.append({
                    'prerelease': json_object.get('prerelease'),
                    'download_url': assets.get('browser_download_url'),
                    'tag_name': json_object.get('tag_name')
                    })
                i += 1
                counter += 1
                continue

            if not prerelease:
                egs_releases.append({
                    'prerelease': json_object.get('prerelease'),
                    'download_url': assets.get('browser_download_url'),
                    'tag_name': json_object.get('tag_name')
                    })
                counter += 1

            if counter == i_releases:
                break

    def without():
        nonlocal egs_releases, i_releases, json_objects
        counter = 0
        for json_object in json_objects:
            prerelease = json_object.get('prerelease')
            assets = json_object.get('assets')[0]
            if not prerelease:
                egs_releases.append({
                    'prerelease': json_object.get('prerelease'),
                    'download_url': assets.get('browser_download_url'),
                    'tag_name': json_object.get('tag_name')
                    })
                counter += 1

            if counter == i_releases:
                break

    prereleases_options = {
        True: every,
        'first': first,
        False: without,
        }
    prereleases_options.get(pre_releases)()
    return egs_releases