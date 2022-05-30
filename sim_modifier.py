import os
import services
import tempfile
from protocolbuffers import PersistenceBlobs_pb2
from sims.sim_info_types import Gender
from util import get_sim_info
from logger import Logger

# Constants representing which body_modifiers to change.
# All height-related keys:
#   3484085079657901585 == 0x3059F4EBA43F6E11 - grow female - CAS
#   4401762110865232217 == 0x03D1633517BE55159 - shrink female
#   6218576529835193767 == 0x564CD2680D6875A7 - grow female
#   7507470142880626878 == 0x682FE451944038BE - shrink female - CAS
#   9316276890694750978 == 0x814A1078EB0A9302 - grow male - CAS
#   9881199360928443106 == 0x8921127746F4EAE2 - shrink male
#   10678765206268930366 == 0x943298606775E93E - shrink male
#   12742648587447422229 == 0xB0D6FB60786FCD15 - shrink male - CAS
# I found these just by testing values that show in Sims 4 Studio
# when loading the heightslider mod. I modified a sim in CAS, then
# dumped their values to see which ones could be applied through
# the game. The others can only be applied through code, and they
# can be combined (so a male can actually have all three "grow"
# constants applied, and they'll stack).
CHEST_KEY: int = 10160417097015316330
CHEST_KEY_H: int = 15886669494782718237
FEET_KEY: int = 3484085079657901585
FEET_KEY_H: int = 7507470142880626878

MALE_FEET_KEY: int = 9316276890694750978
MALE_FEET_KEY_H: int = 12742648587447422229

def set_sizes(sim_id: int, height: float, chest: float):
    sim_info = get_sim_info(sim_id)
    set_body_value(sim_info, FEET_KEY, height)
    set_body_value(sim_info, CHEST_KEY, chest)

def get_body_value(sim_info, key: int):
    face_data = PersistenceBlobs_pb2.BlobSimFacialCustomizationData()
    face_data.ParseFromString(sim_info.facial_attributes)

    # Ensure that `key` is in body_modifiers
    found_body_mod = None
    for body_mod in face_data.body_modifiers:
        if body_mod.key == key:
            found_body_mod = body_mod
            break

    if not found_body_mod:
        return None

    return found_body_mod.amount

# A wrapper around setting a value of a body part. The way this works is a bit
# unusual: rather than having a single value to represent the size of something,
# there are _two_ values to control it: one for sizes in the range [-100,0) and
# the other for sizes in the range [0, 100].
def set_body_value(sim_info, key: int, value: float):
    # Don't set chest size on men.
    if sim_info.gender == Gender.MALE and key == CHEST_KEY:
        return

    if sim_info.gender == Gender.MALE and key == FEET_KEY:
      key = MALE_FEET_KEY

    # Use the "high" key for shrinking and the "low" key for growth.
    if value < 0:
        if key == CHEST_KEY: key = CHEST_KEY_H
        elif key == FEET_KEY: key = FEET_KEY_H
        elif key == MALE_FEET_KEY: key = MALE_FEET_KEY_H

    face_data = PersistenceBlobs_pb2.BlobSimFacialCustomizationData()
    face_data.ParseFromString(sim_info.facial_attributes)

    # Ensure that `key` is in body_modifiers
    found_body_mod = None
    for body_mod in face_data.body_modifiers:
        if body_mod.key == key:
            found_body_mod = body_mod
            break
    if not found_body_mod:
        found_body_mod = face_data.body_modifiers.add()

    # Now that we're sure it's there, set the value of it
    found_body_mod.key = key
    found_body_mod.amount = abs(value*0.01)

    # Remove the opposite key (e.g. if we grew, then delete the shrink one)
    opp_key = None
    if key == CHEST_KEY:
        opp_key = CHEST_KEY_H
    elif key == CHEST_KEY_H:
        opp_key = CHEST_KEY
    elif key == FEET_KEY:
        opp_key = FEET_KEY_H
    elif key == FEET_KEY_H:
        opp_key = FEET_KEY
    elif key == MALE_FEET_KEY:
        opp_key = MALE_FEET_KEY_H
    elif key == MALE_FEET_KEY_H:
        opp_key = MALE_FEET_KEY
    for i in range(len(face_data.body_modifiers)):
        if face_data.body_modifiers[i].key == opp_key:
            del face_data.body_modifiers[i]
            break

    sim_info.facial_attributes = face_data.SerializeToString()

def set_all_sims_normal():
    all_sims = list(services.sim_info_manager().get_all())
    for sim in all_sims:
        sim_info = sim.get_sim_info()
        if sim_info.zone_id != services.current_zone_id(): continue
        Logger.log("Setting for %s" % sim_info.first_name)
        set_sim_normal(sim_info)

def set_sim_normal(sim_info):
    set_body_value(sim_info, CHEST_KEY, 0)
    set_body_value(sim_info, FEET_KEY, 0)

# Dumps all modifier values to a file.
def dump_body_values(sim_info):
    face_data = PersistenceBlobs_pb2.BlobSimFacialCustomizationData()
    face_data.ParseFromString(sim_info.facial_attributes)
    file_path = os.path.join(tempfile.gettempdir(), "sims4_temp.txt")
    with open(file_path, "wt") as f:
        for k in face_data.body_modifiers:
            Logger.print_str("%s == %s" % (k.key, k.amount))

            f.write("%s == %s\n" % (k.key, k.amount))
    Logger.log("Wrote to %s" % file_path)
