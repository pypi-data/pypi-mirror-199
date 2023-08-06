import os
import threading

from plugin.plugin_manager import PluginManager

import aa
from aa.plugs.aa_report_persistence_plug_point import AAReportPlugPoint
from aa.plugs.initiate_report_generation_plug_point import InitiateReportGenerationPlugPoint


def initiate_generate(report_id, account_number, date):
    # we know report generation can be a time-consuming workload.
    # this is because reading data, processing it, formatting it and writing to
    # storage, takes time.
    # this means report generation needs to be a separate process invoked by a
    # queue. of course, we don't want to limit ourselves to specific queue
    # implementation. for core/default plugin we will use queue
    _get_initiate_report_generation_plugin().produce_msg_report_generate(report_id, account_number, date)


def generate(report_id, account_number, date):
    print(f'{os.getpid()}:{threading.get_ident()}: report_generator: started')
    # retrieve data from the backend
    # this is through a plug-point
    aa_data = retrieve_aa_data(account_number, date)

    # apply any business logic to transform the data
    # or filter or do stuff to make the data usable
    # copy data into a file
    file = "report contents go here"

    # save file
    save_aa_report(report_id, account_number, file)

    aa.business_logic.report_status.save_as(report_id, "COMPLETED")
    print(f'{os.getpid()}:{threading.get_ident()}: report_generator: ended')


def generate_unique_report_id() -> str:
    # TODO generate a uuid
    return "12345"


def retrieve_aa_data(account_number, date):
    return {"this": "that"}


def save_aa_report(report_id, account_number, file):
    """

    :param report_id:
    :param account_number: we do have to save the account number along with saved report
    this allows us to verify the user requesting the report id has access to the account
    for which the report was generated.
    :param file:
    :return:
    """
    _get_aa_report_persistence_plugin().save_file(report_id, account_number, file)


def retrieve_saved_aa_report(report_id) -> (str, str):
    # call the plug point to retrieve the saved file
    account_number, report_file = _get_aa_report_persistence_plugin().retrieve_file(report_id)
    return account_number, report_file


def _get_initiate_report_generation_plugin() -> InitiateReportGenerationPlugPoint:
    """
    convinence method to get the plugin for this plug point
    :return:
    """
    # tip: don't save this in this class. when core initializes/imports this module
    # infrastructure code would not have had opportunity to override. this why it is
    # important to always go to plugin manager for the most current plugin
    return PluginManager.get_plugin("initiate_report_generation_plug_point")


def _get_aa_report_persistence_plugin() -> AAReportPlugPoint:
    """
    convinence method to get the plugin for this plug point
    :return:
    """
    # tip: don't save this in this class. when core initializes/imports this module
    # infrastructure code would not have had opportunity to override. this why it is
    # important to always go to plugin manager for the most current plugin
    return PluginManager.get_plugin("aa_report_persistence_plug_point")
