
from parking_spaces import (
    add_parking_space,
    view_parking_spaces,
    search_parking_space,
    update_parking_space
)

if __name__ == "__main__":
    print("\n========== TEST 1: ADD PARKING SPACE ==========")

    add_parking_space(
        space_number="B-01",
        space_type="Standard",
        location="Ground Floor"
    )


    print("\n========== TEST 2: VIEW PARKING SPACES ==========")

    view_parking_spaces()


    print("\n========== TEST 3: SEARCH PARKING SPACE ==========")

    search_parking_space("B-01")


    print("\n========== TEST 4: UPDATE PARKING SPACE ==========")

    update_parking_space(
        space_number="B-01",
        space_type="VIP",
        status="reserved",
        location="First Floor"
    )


    print("\n========== TEST 5: VERIFY UPDATE ==========")

    search_parking_space("B-01")

    print("\n========== TEST 6: DUPLICATE SPACE ==========")

    add_parking_space(
        space_number="B-01",
        space_type="Standard",
        location="Ground Floor"
    )

    print("\n========== TEST 7: SEARCH NOT FOUND ==========")

    search_parking_space("Z-99")

    print("\n========== TEST 8: UPDATE NOT FOUND ==========")

    update_parking_space(
        space_number="Z-99",
        space_type="VIP",
        status="reserved",
        location="First Floor"
    )
