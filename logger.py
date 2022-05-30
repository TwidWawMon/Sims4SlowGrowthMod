global output

class Logger:

  @staticmethod
  def set_logger(cheat_output):
    global output
    output = cheat_output

  @staticmethod
  def log(s):
    output(s)

  @staticmethod
  def print_str(s):
    n = 500 # chunk length
    chunks = [s[i:i+n] for i in range(0, len(s), n)]
    for c in chunks:
        Logger.log(c)
