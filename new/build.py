import subprocess
import os
import json
import sys

script_dir = os.path.abspath(os.path.dirname(__file__))

url = "https://gitlab.com/MindTheGapps/vendor_gapps"


def get_hashes(branch, file):
    cmd = ["git", "ls-remote", url, branch]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    output = result.stdout.strip().splitlines()
    hashes = [line.split()[0] for line in output]
    final = "\n".join(hashes).strip()

    with open(file, "r") as f:
        content = f.read()

    if content == final:
        print("there is no update available")
        return
    else:
        print("there is update available")

    with open(file, "w") as f:
        f.write(final)


if os.path.exists("./config.json"):
    print("found config.json")
    with open("config.json", "r") as config_json:
        configs = json.load(config_json)
else:
    print(
        "didn't find app_list.json. \nmake sure you put app_list.json in: ", script_dir
    )
    print("Aborting")
    sys.exit(1)

for config in configs:
    print(f"Processing {config['branch']}...")
    file = config["file"]
    branch = config["branch"]
    count = get_hashes(branch, file)
