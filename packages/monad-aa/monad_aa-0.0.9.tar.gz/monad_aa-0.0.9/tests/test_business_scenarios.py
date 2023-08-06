import os
import threading
from time import sleep

print("lets test as we code")


def test_blocking_synchronous_case():
    # this is the case where the report is synchronously generated (no async or event or queue yet)
    authentication_identifier = "cookie_value"

    import aa.entry_points
    report_id = aa.entry_points.request_report(authentication_identifier, "1234567001", "2021-04-08")
    assert report_id is not None

    wait_time = 2
    count = 0
    file = None
    while True:
        status, file = aa.entry_points.is_report_ready(authentication_identifier, report_id)
        if status:
            print(f'{os.getpid()}:{threading.get_ident()}: client: {status=}. {file=}')
            break
        else:
            print(f'{os.getpid()}:{threading.get_ident()}: client: {status=}. try again in {wait_time} seconds')
            count += 1
            if count > 10:
                break
            sleep(wait_time)

    assert file is not None

    print('all is well')
