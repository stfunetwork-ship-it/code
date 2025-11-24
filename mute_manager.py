# mute_manager.py
import re
import time
from collections import defaultdict

# Store muted users (persist this in DB for production)
MUTED_USER_IDS = set()      # explicit list of user IDs you want to mute
TEMP_MUTES = {}             # user_id -> unmute_timestamp
KEYWORD_PATTERNS = [        # list of regex patterns for abusive/spammy messages
    re.compile(r"\b(?:buy now|free money|work from home)\b", re.I),
    re.compile(r"(?:threaten|kill|bomb)", re.I),   # example of clear abuse
    re.compile(r"\b(?:fuck|cunt|slur)\b", re.I),   # adapt to your policy
]

# simple rate-limiter: user_id -> [timestamps]
USER_POST_TIMES = defaultdict(list)
MAX_MSGS_PER_MINUTE = 10
RATE_WINDOW_SECONDS = 60

def is_user_muted(user_id):
    """Check explicit or temporary mutes."""
    if user_id in MUTED_USER_IDS:
        return True
    unmute_ts = TEMP_MUTES.get(user_id)
    if unmute_ts and time.time() < unmute_ts:
        return True
    # expired temp mute cleanup
    if unmute_ts and time.time() >= unmute_ts:
        TEMP_MUTES.pop(user_id, None)
    return False

def matches_prohibited_content(text):
    """Return True if text matches any keyword/regex for moderation."""
    for pat in KEYWORD_PATTERNS:
        if pat.search(text):
            return True
    return False

def is_rate_limited(user_id):
    now = time.time()
    times = USER_POST_TIMES[user_id]
    # keep only recent events
    USER_POST_TIMES[user_id] = [t for t in times if now - t <= RATE_WINDOW_SECONDS]
    USER_POST_TIMES[user_id].append(now)
    return len(USER_POST_TIMES[user_id]) > MAX_MSGS_PER_MINUTE

def handle_incoming_message(user_id, message_text):
    """Call this for every incoming message. Return True to accept, False to drop/mute."""
    if is_user_muted(user_id):
        return False  # drop message

    if is_rate_limited(user_id):
        # apply a temporary mute (e.g., 5 minutes)
        TEMP_MUTES[user_id] = time.time() + 5 * 60
        return False

    if matches_prohibited_content(message_text):
        # optional: warn first, then mute
        TEMP_MUTES[user_id] = time.time() + 10 * 60  # 10-minute mute
        return False

    # message passes filters
    return True

# Admin functions
def mute_user(user_id):
    MUTED_USER_IDS.add(user_id)

def unmute_user(user_id):
    MUTED_USER_IDS.discard(user_id)
    TEMP_MUTES.pop(user_id, None)

def temp_mute_user(user_id, minutes):
    TEMP_MUTES[user_id] = time.time() + minutes * 60
