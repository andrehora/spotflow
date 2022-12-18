from lab.bptesting.matcher import ChangeRepository, get_old_and_new_version_pairs


def get_output_dir(output_dir, project, version):
    return output_dir + "/" + version + "/" + project + "-" + version


def get_versions(major_minor, micros):
    versions = []
    for micro in range(1, micros+1):
        v = major_minor + '.' + str(micro)
        versions.append(v)
    return versions


output_dir = 'output'
# projects = ['ast', 'gzip', 'json', 'calendar', 'collections', 'csv', 'ftplib', 'tarfile', 'locale', 'difflib']
projects = ['ast', 'gzip', 'json', 'locale']
# projects = ['calendar', 'collections', 'ftplib', 'tarfile', 'difflib']
# projects = ['gzip', 'locale']

versions = get_versions('3.8', 5)
old_new_versions = get_old_and_new_version_pairs(versions)

for project in projects:
    print("================")
    print(project)
    for old_version, new_version in old_new_versions:
        print(old_version + " -> " + new_version)

        old_dir = get_output_dir(output_dir, project, old_version)
        new_dir = get_output_dir(output_dir, project, new_version)

        repo = ChangeRepository(project, old_dir, new_dir)
        repo.find_changes()
        print()
