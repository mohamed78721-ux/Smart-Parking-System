from parking_sessions import get_parking_sessions

sessions = get_parking_sessions()

for session in sessions:
    print(session)