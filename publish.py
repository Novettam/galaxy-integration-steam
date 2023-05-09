import os
import shutil


try:
    shutil.rmtree("./dist")
except FileNotFoundError:
    pass

os.mkdir("./dist")

ignore_patterns = shutil.ignore_patterns('.*', '_*', 'dist', 'requirements.txt', 'publish.py')

shutil.copytree("./", "./dist/galaxy-integration-steam", ignore=ignore_patterns)

shutil.make_archive("./dist/galaxy-integration-steam",
                    'zip',
                    "./dist",
                    "galaxy-integration-steam")

shutil.rmtree("./dist/galaxy-integration-steam")