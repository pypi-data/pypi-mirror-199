import requests
import xmltodict

def addGradleSetupInstructions(fileName, reposetoryUrl, group, name) :
  tops = []
  bottoms = []

  with open(fileName, "r")  as file:
    key = 0
    for line in file.readlines():
      if key == 0:
        tops.append(line)
      if key == 2:
        bottoms.append(line)

      if (key == 0 and line == "## Setup\n"):
        key = 1
      elif key == 1 and "## " in line:
        key = 2
        bottoms.append(line)
  
  midle = [
    "add this mod to your project by adding the following into your ``build.gradle``",
    "```gradle",
    "repositories {",
    f"\tmaven {{ url '{reposetoryUrl}' }}",
    "}",
    "dependencies {",
    f"\tmodImplementation \"{group}:{name}:{getLatestVersion(reposetoryUrl, group, name)}\"",
    "}",
    "```"
  ]

  with open(fileName, "w") as file:
    file.writelines(
      tops + [x + "\n" for x in midle] + bottoms
    )

def getLatestVersion(url: str, group: str, name: str):
  url = f"{url}/{group.replace('.', '/')}/{name}/maven-metadata.xml";
  print(f"checking {url} for latest version")
  data = requests.get(url).content

  data = xmltodict.parse(data)
  return data["metadata"]["versioning"]["latest"]