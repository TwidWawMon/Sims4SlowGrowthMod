import sims4.commands
import alarms, clock
import re
from util import get_current_time
from size_tracker import SizeTracker
from logger import Logger

size_tracker: SizeTracker = SizeTracker()

# A handle to the alarm we set for changing size, that way we make sure we only
# have a single alarm going at any time.
alarm_handle = None

save_alarm_handle = None

special_alarm_handle = None
special_target = None

# The string you type into the cheat console to invoke the command. I just
# picked something short. This is a "Live" command, which means "testingcheats"
# doesn't have to be on (see https://www.patreon.com/posts/all-cheats-17111703).
@sims4.commands.Command('s', command_type=sims4.commands.CommandType.Live)
def _my_command(_connection=None):
    cheat_output = sims4.commands.CheatOutput(_connection)
    Logger.set_logger(cheat_output)

    Logger.log("Reading or creating size file")
    size_tracker.read_or_create_size_file()

    Logger.log("Initializing size changer")

    # Set up our alarm that will continually monitor for size changes.
    setup_alarms()

    Logger.log("Success!")

@sims4.commands.Command('save', command_type=sims4.commands.CommandType.Live)
def _save(_connection=None):
    size_tracker.save_sizes()

@sims4.commands.Command('fast', command_type=sims4.commands.CommandType.Live)
def _alarm(first_name: str=None, _connection=None):
    global special_alarm_handle
    global special_target
    Logger.log("Setting up faster growth for %s" % first_name)
    if first_name == None:
        if special_alarm_handle != None:
            alarms.cancel_alarm(special_alarm_handle)
            special_alarm_handle = None
        Logger.log("Canceled special alarm")
        return

    ids = size_tracker.get_sim_ids_by_first_name(first_name)
    if len(ids) == 0:
        Logger.log("No sim found with that name")
        return

    special_target = first_name
    setup_special_alarm()
    Logger.log("Faster growth set up")

@sims4.commands.Command('tick', command_type=sims4.commands.CommandType.Live)
def _tick(times:int=1, _connection=None):
    for i in range(int(times)):
        size_tracker.adjust_sizes()
    Logger.log("ticked %s time(s)" % (times))

@sims4.commands.Command('wipe', command_type=sims4.commands.CommandType.Live)
def _wipe(_connection=None):
    size_tracker.wipe()

@sims4.commands.Command('bless', command_type=sims4.commands.CommandType.Live)
def _bless(first_name: str=None, times: int=4, _connection=None):
    size_tracker.bless(first_name, times)

@sims4.commands.Command('chest', command_type=sims4.commands.CommandType.Live)
def _chest(first_name: str=None, times: int=4, _connection=None):
    size_tracker.chest(first_name, times)

@sims4.commands.Command('blessrate', command_type=sims4.commands.CommandType.Live)
def _bless_rate(first_name: str=None, times=2, _connection=None):
    size_tracker.bless_rate(first_name, times)

def find_str(haystack, needle):
    num_groups = len(re.findall(needle, haystack))
    Logger.log("Found %d group(s)" % num_groups)
    if num_groups > 0:
        iter = re.finditer(needle, haystack)
        for match in iter:
            start = match.start()
            surrounding = haystack[start - 20: start + 20]
            Logger.log("--> %s" % surrounding)
    else:
        Logger.log("Could not find \"%s\"" % needle)

def alarm_callback(*args):
    size_tracker.adjust_sizes()
    Logger.log("tick %s" % get_current_time())

def save_alarm_callback(*args):
    size_tracker.save_sizes()

def special_alarm_callback(*args):
    size_tracker.bless(special_target, 1)

def setup_special_alarm():
    global special_alarm_handle
    if special_alarm_handle is not None:
        alarms.cancel_alarm(special_alarm_handle)
        special_alarm_handle = None

    span = clock.interval_in_sim_minutes(5)
    special_alarm_handle = alarms.add_alarm(setup_special_alarm, span, special_alarm_callback, repeating=True, repeating_time_span=span, cross_zone=True)


def setup_alarms():
    global alarm_handle
    global save_alarm_handle
    if alarm_handle is not None:
        alarms.cancel_alarm(alarm_handle)
        alarm_handle = None
    if save_alarm_handle is not None:
        alarms.cancel_alarm(save_alarm_handle)
        save_alarm_handle = None

    span = clock.interval_in_sim_minutes(30)
    alarm_handle = alarms.add_alarm(setup_alarms, span, alarm_callback, repeating=True, repeating_time_span=span, cross_zone=True)

    span = clock.interval_in_sim_hours(4)
    save_alarm_handle = alarms.add_alarm(setup_alarms, span, save_alarm_callback, repeating=True, repeating_time_span=span, cross_zone=True)
