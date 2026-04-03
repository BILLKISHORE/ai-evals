import base64
import pickle


def load_session(session_cookie):
    """Restore user session from cookie value."""
    try:
        # BUG: deserializing untrusted user input with pickle
        # allows arbitrary code execution
        data = base64.b64decode(session_cookie)
        session = pickle.loads(data)
        return session
    except Exception:
        return None


def save_session(session_data):
    """Save session data to cookie value."""
    data = pickle.dumps(session_data)
    return base64.b64encode(data).decode()
