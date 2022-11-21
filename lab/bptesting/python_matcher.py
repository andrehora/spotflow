from lab.bptesting.matcher import ChangeRepository


def get_python_versions(major_minor, micros):
    versions = []
    for micro in range(1, micros+1):
        v = major_minor + '.' + str(micro)
        versions.append(v)
    return versions


def get_old_new_python_versions(versions):
    return zip(versions[0:-1], versions[1:])


python_versions = get_python_versions('3.7', 8)
old_new_versions = get_old_new_python_versions(python_versions)
projects = ['gzip']

for old_version, new_version in old_new_versions:
    print(old_version, new_version)
    repo = ChangeRepository(old_version, new_version, projects)
    repo.find_changes()
