PLACING_PHASE = 24	# total turns in placing phase
TURNS_BEFORE_SHRINK = [128 + PLACING_PHASE, 192 + PLACING_PHASE]
MAX_BOARD_SIZE = 8  # maximum board size

import datetime

# Time limit for each turn in Monte Carlo
MC_TIME_LIMIT = datetime.timedelta(seconds=4)