"""
train_fare.py - Hardened Train Fare & Seat Allocation Module

Defensively programmed against arbitrary/malformed inputs discovered through
Hypothesis fuzz testing.
"""

BERTHS = ["SU", "LB", "MB", "UB", "LB", "MB", "UB", "SL"]


def parse_pnr(pnr):
    """
    Parses a 10-digit PNR string into (zone: int, number: int).
    Returns None if input is invalid or malformed.
    """
    if not isinstance(pnr, str):
        return None
    pnr_clean = pnr.strip()
    if len(pnr_clean) != 10 or not pnr_clean.isdigit():
        return None
    return int(pnr_clean[0]), int(pnr_clean[1:])


def journey_distance(distances_csv):
    """
    Parses a comma-separated list of cumulative station distances.
    Returns the total distance (last station - first station).
    Returns None if input is malformed, has fewer than 2 stations,
    or distances are negative / decreasing.
    """
    if not isinstance(distances_csv, str):
        return None
    parts = distances_csv.split(",")
    if len(parts) < 2:
        return None
    distances = []
    for part in parts:
        token = part.strip()
        if not token or (not token.isdigit() and not (token.startswith("-") and token[1:].isdigit())):
            return None
        distances.append(int(token))
    if distances[-1] < distances[0]:
        return None
    return distances[-1] - distances[0]


def berth_type(seat):
    """
    Parses a coach and seat string (e.g., 'S3-45') into (coach: str, berth_code: str).
    Returns None if format is invalid or seat number is non-positive.
    """
    if not isinstance(seat, str):
        return None
    parts = seat.split("-")
    if len(parts) != 2:
        return None
    coach, number_str = parts[0].strip(), parts[1].strip()
    if not coach or not number_str.isdigit():
        return None
    seat_num = int(number_str)
    if seat_num <= 0:
        return None
    return coach.upper(), BERTHS[seat_num % 8]


def main():
    print("==== Running parse_pnr ====")
    user_input = input("Enter a 10 digit PNR (e.g. 4521367890): ")
    result = parse_pnr(user_input)
    print("Zone and Number:", result)

    print("\n==== Running journey_distance ====")
    user_input = input("Enter station distances as CSV (e.g. 0,120,340): ")
    result = journey_distance(user_input)
    print("Total Distance:", result)

    print("\n==== Running berth_type ====")
    user_input = input("Enter coach and seat (e.g. S3-45): ")
    result = berth_type(user_input)
    print("Coach and Berth:", result)


if __name__ == "__main__":
    main()
