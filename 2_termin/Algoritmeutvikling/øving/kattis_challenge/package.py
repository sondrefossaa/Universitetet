from sys import stdin

packages = dict()
lines = stdin.readlines()


def insert_highest_version(package, version):
    if package in packages:
        return False
    else:
        packages[package] = int(version)
        return True


for line in lines[2:]:
    package, version = line.split()
    if not insert_highest_version(package, version):
        result = packages[package] - int(version)
        if result != 0:
            print(result)
