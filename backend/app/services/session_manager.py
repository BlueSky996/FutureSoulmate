import uuid, time

SESSIONS = {} # in memory

TTL = 60*60*24 # 24h 

def create_session():
    sid = str(uuid.uuid4())
    SESSIONS[sid] = {"created": time.time(), "messages": 0}
    return sid

def get_session(sid):
    return SESSIONS.get(sid)

def increment_messages(sid):
    if sid in SESSIONS:
        SESSIONS[sid]["messages"] += 1