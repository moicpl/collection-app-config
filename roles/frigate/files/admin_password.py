# Sets the password of Frigate's admin user, read on stdin, in its database.
# Run in the container (podman exec -i). Prints "unchanged" when the password
# already matches, else "changed". Same hash format as frigate/api/auth.py.
import base64
import datetime
import hashlib
import hmac
import secrets
import sqlite3
import sys

ITERATIONS = 600000

password = sys.stdin.read()
db = sqlite3.connect("/config/frigate.db")
row = db.execute("SELECT password_hash FROM user WHERE username = 'admin'").fetchone()

if row:
    _, iterations, salt, expected = row[0].split("$")
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), int(iterations))
    if hmac.compare_digest(base64.b64encode(digest).decode(), expected):
        print("unchanged")
        sys.exit(0)

salt = secrets.token_hex(16)
digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), ITERATIONS)
password_hash = "pbkdf2_sha256${}${}${}".format(ITERATIONS, salt, base64.b64encode(digest).decode())
columns = [column[1] for column in db.execute("PRAGMA table_info(user)")]

if row:
    if "password_changed_at" in columns:
        db.execute(
            "UPDATE user SET password_hash = ?, password_changed_at = ? WHERE username = 'admin'",
            (password_hash, str(datetime.datetime.now())),
        )
    else:
        db.execute("UPDATE user SET password_hash = ? WHERE username = 'admin'", (password_hash,))
else:
    db.execute(
        "INSERT INTO user (username, role, password_hash, notification_tokens) VALUES ('admin', 'admin', ?, '[]')",
        (password_hash,),
    )
db.commit()
print("changed")
