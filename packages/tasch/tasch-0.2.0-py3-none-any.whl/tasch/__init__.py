__version__ = '0.2.0'

mode = none

def at(comm):
  def at(comms):
   if comms == help:
      helpem()
  if comms == number:
    mode == num
  if comms == derivative:
    mode == der
  if comms == integral:
    mode = int
  else:
    print("Unknown Command!")
  