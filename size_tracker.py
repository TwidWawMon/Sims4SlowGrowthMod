import services
from sims.sim_info_types import Gender
from util import get_sim_info
from sim_modifier import set_all_sims_normal, set_sim_normal, set_sizes
from logger import Logger

import json
import os
import random
import tempfile

save_file_path = os.path.join(tempfile.gettempdir(), "sims4.txt")

class SizeTracker:
  def __init__(self):
    # Keys: sim IDs (as integers)
    # Values: array of [height, chest, growth, first_name]
    self.sizes = {}

  def read_or_create_size_file(self):
      Logger.log("Loading from disk")
      if not os.path.exists(save_file_path):
          Logger.log("File does not exist")
          self.save_sizes()
      else:
          with open(save_file_path, "r") as f:
              sizes_with_str_keys = json.loads(f.read())
              self.sizes = {}
              for k, v in sizes_with_str_keys.items():
                  self.sizes[int(k)] = v
              Logger.log("Read %s size(s)" % len(self.sizes))

  def save_sizes(self):
      Logger.log("Saving sizes to disk")
      with open(save_file_path, "wt") as f:
          f.write(json.dumps(self.sizes))

  def grow_sim(self, id: int):
      sim_info = get_sim_info(id)

      if sim_info.zone_id != services.current_zone_id(): return

      if sim_info.gender == Gender.FEMALE and random.randint(0, 7) == 5:
          old = self.sizes[id][2]
          change = random.uniform(1, 3.5)
          if random.randint(0, 10) == 5:
              change += random.uniform(1, 7)

          self.sizes[id][2] = min(100, old + change)
          Logger.log("Auto-blessing %s: %s to %s" % (sim_info.first_name + " " + sim_info.last_name, old, self.sizes[id][2]))

      start_sizes = self.sizes[id]

      rate = start_sizes[2]
      height_growth = random.uniform(0, rate / 166)
      chest_growth = random.uniform(0, rate / 250)
      if start_sizes[0] < 0:
        height_growth *= 7

        # If your height is negative, then don't let it grow beyond 0 in one jump.
        height_growth = min(height_growth, abs(start_sizes[0]))
      start_sizes[0] += height_growth
      start_sizes[1] += chest_growth

      self.sizes[id] = start_sizes
      self.sizes[id][0] = round(self.sizes[id][0], 3)
      self.sizes[id][1] = round(self.sizes[id][1], 3)
      self.sizes[id][2] = round(self.sizes[id][2], 3)

      set_sizes(id, start_sizes[0], start_sizes[1])

  def adjust_sizes(self):
      all_sims = list(services.sim_info_manager().get_all())
      for sim in all_sims:
          sim_info = sim.get_sim_info()
          if sim_info.zone_id != services.current_zone_id(): continue
          id = sim_info.id
          if id not in self.sizes:
              is_male = sim_info.gender == Gender.MALE
              rate = 0 if is_male else random.uniform(1, 50)
              start_height = 0 if is_male else -30
              chest = random.uniform(0.0, 5.0)
              self.sizes[id] = [start_height, chest, rate, sim_info.first_name]
              set_sim_normal(sim_info)
              Logger.log("Initialized %s" % self.get_size_string(id))

      for id in self.sizes:
          self.grow_sim(id)

  def get_size_string(self, id: int):
    if id not in self.sizes:
      return "No size initialized for id==%s" % id

    (height, chest, rate, first_name) = self.sizes[id]
    return "%s: height==%s, chest==%s, growth==%s" % (first_name, round(height, 2), round(chest, 2), round(rate, 2))

  def wipe(self):
    self.sizes = {}
    self.save_sizes()
    Logger.log("Wiping all sizes")
    set_all_sims_normal()
    Logger.log("Wiped out sizes")

  def bless(self, first_name: str, times: int):
    times = min(times, 500)
    if first_name == None:
        return
    if len(self.sizes) == 0:
        Logger.log("Sizes not loaded")
    for k, v in self.sizes.items():
        if v[3].lower() == first_name.lower():
            Logger.log("Blessing %s %s time(s)" % (first_name, times))
            for i in range(int(times)):
                self.grow_sim(k)

  def get_sim_ids_by_first_name(self, first_name:str):
    ids = []
    for id, v in self.sizes.items():
        if v[3].lower() == first_name.lower():
            ids.append(id)

    return ids

  def chest(self, first_name: str, times: int):
    times = min(times, 500)
    if first_name == None:
        return
    if len(self.sizes) == 0:
        Logger.log("Sizes not loaded")
    for id in self.get_sim_ids_by_first_name(first_name):
        self.sizes[id][1] += int(times)
        Logger.log("Blessing chest of %s to %s" % (first_name, self.sizes[id][1]))

        set_sizes(id, self.sizes[id][0], self.sizes[id][1])

  def bless_rate(self, first_name: str, times: int):
    times = min(times, 500)
    if first_name == None:
        return
    if len(self.sizes) == 0:
        Logger.log("Sizes not loaded")
    for id in self.get_sim_ids_by_first_name(first_name):
        self.sizes[id][2] *= int(times)
        Logger.log("Blessing %s to %s" % (first_name, self.sizes[id][2]))
