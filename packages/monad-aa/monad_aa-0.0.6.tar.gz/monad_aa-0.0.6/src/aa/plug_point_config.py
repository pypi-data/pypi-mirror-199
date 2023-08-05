monad_aa_plug_point_configuration = {
    "report_status_plug_point": {
        "plugin": "aa.plugs.report_status_plug_in",
        "description": "provides a core persistence for report status object",
        "pluggable": "report_status"  # python module that uses the plug point
    },
    "initiate_report_generation_plug_point": {
        "plugin": "aa.plugs.initiate_report_generation_plug_in",
        "description": "provides core messaging implementation of initiate report generation."
                       "it uses queues allowing report generation to be processed asynchronously",
        "pluggable": "report_generator"  # python module that uses the plug point
    },
    "aa_report_persistence_plug_point": {
        "plugin": "aa.plugs.aa_report_persistence_plug_in",
        "description": "provides a core persistence for generated report object",
        "pluggable": "report_generator"  # python module that uses the plug point
    },
    # things to be added in the future
    # "menu_persistence_plug_point": {
    #     "plug_point": "menu_persistence",
    #     "plugin": "core_menu_persistence",
    #     "description": "provides a core persistence for menu entity",
    #     "pluggable": "menu_processor"
    # },
    # "cook_added_event_plug_point": {
    #     "plugin": "core_cook_added_event",
    #     "description": "provides a core persistence for menu entity",
    #     "pluggable": "cook_processor"
    # }
}
