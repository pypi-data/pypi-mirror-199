__version__ = '0.2.5'

mode = "none"

helps = ["@help [command] | prints the documentation for a given command", "@releases | prints the release notes for all versions", "@version | prints the current version and its documentation", "@number | changes the calculator mode to 'Number Mode'", "@algebra | changes the calculator mode to 'Algebra Mode'", "@derivative | changes the calculator mode to 'Derivative Mode'", "@integral | changes the calculator mode to 'Integral Mode'"]

def at(comms):
  if help in comms:
    if comms == "help":
      helpem()
    else:
      try:
        comms = comms.split(":")
        helpem(comms[1])
      except:
        print("Invalid Help Command!")
  if comms == "number":
    mode == "num"
  if comms == "derivative":
    mode == "der"
  if comms == "integral":
    mode = "int"
  else:
    print("Unknown Command!")

def helpem(at):
  if at == "":
    for index in helps:
      print(helps[index])
  if at == "help":
    print helps[0]
  if at == "releases":
    print helps[1]
  if at == "version":
    print helps[2]
  if at == "number":
    print helps[3]
  if at == "algebra":
    print helps[4]
  if at == "derivative":
    print helps[5]
  if at == "integral":
    print helps[6]