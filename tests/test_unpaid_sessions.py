
from payments import get_unpaid_sessions

sessions = get_unpaid_sessions()

print("Unpaid Sessions:")

for session in sessions:
    print(session)
