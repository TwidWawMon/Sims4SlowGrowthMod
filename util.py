import services

# Clamp `n` between two numbers (inclusive).
def clamp(n, lowerbound, upperbound):
    return max(lowerbound, min(n, upperbound))

def get_sim_info(sim_id=None):
    return services.sim_info_manager().get(sim_id) if sim_id else services.active_sim_info()

def get_current_time():
    game_clock = services.game_clock_service()
    return game_clock.now()
