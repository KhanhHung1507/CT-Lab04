"""Firebase Authentication client using Firebase REST API."""
import os
import time
from pathlib import Path
from dotenv import load_dotenv
import requests

# Load .env file
load_dotenv(Path(__file__).resolve().parent / ".env", override=False)
FIREBASE_PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID", "").strip()
FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY", "").strip()

REQUEST_TIMEOUT = 15


class FirebaseError(Exception):
    """Custom error class for user-safe Firebase messages."""
    def __init__(self, message, sign_in_again=False):
        super().__init__(message)
        self.sign_in_again = sign_in_again


def validate_config():
    """Verify that required Firebase credentials exist in environment."""
    if not FIREBASE_PROJECT_ID or not FIREBASE_API_KEY:
        raise FirebaseError("Please configure FIREBASE_PROJECT_ID and FIREBASE_API_KEY in .env file.")
    if any(c in FIREBASE_PROJECT_ID for c in "/ ?#"):
        raise FirebaseError("FIREBASE_PROJECT_ID must be a project ID, not a URL or name.")


def _request(method, url, **kwargs):
    """Execute a request with error handling without leaking secrets."""
    try:
        response = requests.request(method, url, timeout=REQUEST_TIMEOUT, **kwargs)
    except requests.RequestException:
        raise FirebaseError("Cannot reach Firebase server. Please check your internet connection.") from None

    try:
        data = response.json()
    except ValueError:
        raise FirebaseError("Firebase returned an unexpected response format.") from None

    if not isinstance(data, dict):
        raise FirebaseError("Firebase returned invalid response payload.")

    if response.ok:
        return data

    error = data.get("error", {})
    code = str(error.get("message", "")) if isinstance(error, dict) else ""

    if any(k in code for k in ("TOKEN_EXPIRED", "INVALID_ID_TOKEN", "USER_DISABLED")) or response.status_code == 401:
        raise FirebaseError("Your session is expired or invalid. Please sign in again.", sign_in_again=True)
    if "EMAIL_EXISTS" in code:
        raise FirebaseError("This email is already registered. Please sign in instead.")
    if "OPERATION_NOT_ALLOWED" in code:
        raise FirebaseError("Email/Password sign-in is disabled in Firebase Console.")
    if "WEAK_PASSWORD" in code or "PASSWORD_DOES_NOT_MEET_REQUIREMENTS" in code:
        raise FirebaseError("Password is too weak. Please use at least 6 characters.")
    if "INVALID_EMAIL" in code:
        raise FirebaseError("Invalid email address format.")
    if any(k in code for k in ("INVALID_LOGIN_CREDENTIALS", "INVALID_PASSWORD", "EMAIL_NOT_FOUND")):
        raise FirebaseError("Invalid email or password.")
    if "TOO_MANY_ATTEMPTS" in code or response.status_code == 429:
        raise FirebaseError("Too many attempts. Please try again later.")
    if "API_KEY" in code or response.status_code == 404:
        raise FirebaseError("Firebase configuration error: Invalid API Key or Project ID.")

    raise FirebaseError(f"Authentication failed: {code or 'Unknown error'}")


def _authenticate(action, email, password):
    validate_config()
    email = email.strip()
    if not email or not password:
        raise FirebaseError("Please provide both email and password.")
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:{action}"
    return _request(
        "POST",
        url,
        params={"key": FIREBASE_API_KEY},
        json={"email": email, "password": password, "returnSecureToken": True},
    )


def create_account(email, password):
    """Register a new user account with email and password."""
    _authenticate("signUp", email, password)


def sign_in(email, password):
    """Authenticate existing user and return user session dict."""
    data = _authenticate("signInWithPassword", email, password)
    return {
        "uid": data["localId"],
        "email": data["email"],
        "id_token": data["idToken"],
        "expires_at": time.time() + int(data["expiresIn"]),
    }
