from lab.bptesting.matcher import ChangeRepository, get_old_and_new_version_pairs


def get_output_dir(output_dir, project, version):
    return output_dir + "/" + project + "-" + version


def get_python_versions(major_minor, micros):
    versions = []
    for micro in range(1, micros+1):
        v = major_minor + '.' + str(micro)
        versions.append(v)
    return versions


output_dir = 'output'
project = 'rich'

# versions = ['v12.4.0', 'v12.4.1', 'v12.4.3', 'v12.4.4']
versions = ['v12.0.0','v12.0.1','v12.1.0','v12.2.0','v12.3.0','v12.4.0','v12.4.1','v12.4.2','v12.4.3','v12.4.4','v12.5.0','v12.5.1','v12.6.0']
old_new_versions = get_old_and_new_version_pairs(versions)


print("================")
print(project)
for old_version, new_version in old_new_versions:
    print(old_version + " -> " + new_version)

    old_dir = get_output_dir(output_dir, project, old_version)
    new_dir = get_output_dir(output_dir, project, new_version)

    repo = ChangeRepository(project, old_dir, new_dir)
    repo.find_changes()
    print()
