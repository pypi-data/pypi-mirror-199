import os
import queue
import threading
from aa.business_logic.report_generator import generate

from aa.plugs.initiate_report_generation_plug_point import InitiateReportGenerationPlugPoint

qq = queue.Queue()


class InitiateReportGenerationPlugIn(InitiateReportGenerationPlugPoint):
    def __init__(self):
        super().__init__()
        # self.q = queue.Queue()
        self.q = qq

    def consume_msg_report_generate(self):
        while True:
            report_id, account_number, date = self.q.get()
            print(f'{os.getpid()}:{threading.get_ident()}: consume_msg_report_generate: working on {report_id}')
            generate(report_id, account_number, date)
            self.q.task_done()
            print(f'{os.getpid()}:{threading.get_ident()}: consume_msg_report_generate: finished {report_id}')

    def produce_msg_report_generate(self, report_id, account_number, date):
        threading.Thread(target=self.consume_msg_report_generate, daemon=True).start()
        self.q.put((report_id, account_number, date))
        print(f'{os.getpid()}:{threading.get_ident()}: initiate_report_generate: {report_id=}')


# This method is needed for plugin framework.
def get_implementation():
    return InitiateReportGenerationPlugIn()
