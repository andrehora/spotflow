from lab.bptesting.matcher import ChangeRepository


def get_output_dir(output_dir, project, version):
    return output_dir + "/" + version + "/" + project + "-" + version


def get_python_versions(major_minor, micros):
    versions = []
    for micro in range(1, micros+1):
        v = major_minor + '.' + str(micro)
        versions.append(v)
    return versions


def get_old_and_new_python_versions(versions):
    return list(zip(versions[0:-1], versions[1:]))


output_dir = 'output'
projects = ['ast', 'gzip', 'json', 'locale']

python_versions = get_python_versions('3.7', 15)
old_new_versions = get_old_and_new_python_versions(python_versions)

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
