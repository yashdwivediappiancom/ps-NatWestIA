import os
from copy import copy
from datetime import date
import logging
import time
from appian_locust.uiform import SailUiForm
from appian_locust.uiform import RecordInstanceUiForm
from appian_locust.appian_client import AppianClient
from appian_locust.utilities.helper import find_component_by_attribute_in_dict, find_component_by_attribute_and_index_in_dict



from utilities import utils
import random

logger = logging.getLogger(utils.LOGGER_NAME)


class RecordView:

    def get_home_page(self, appian: AppianClient, site_name: str, page_name: str) -> 'SailUiForm':

        site_form = None
        try:

            logger.info(f"Site {site_name} page {page_name} loading")

            # Go to engagements screen
            site_form = appian.visitor.visit_site(site_name=site_name, page_name=page_name,
                                                  locust_request_label=f"Visit.Site.{site_name}.{page_name}")

            # Debug site form for fun
            utils.debug_write_ui_state_to_file(f"site_form", "site_form engagement tab load",
                                               site_form)


            logger.info(f"Site {site_name} page {page_name} loaded")

            return site_form
        
        except Exception as e:
            if site_form:
                utils.debug_write_ui_state_to_file(f"site_form", "site_form last state",
                                                   site_form)
            raise Exception(f"Error viewing site {site_name} page {page_name}") from e
        
    def select_engagement_and_navigate_across_views(self, site_page: SailUiForm) -> SailUiForm:


        engagement_view_list_high = ['Summary','Fieldwork','Exceptions & Findings','Audit Report']
        engagement_view_list_medium = ['Coverage','MEL','EKID','Documents']
        engagement_view_list_low = ['Overview', 'Relevant Issues', 'Memo', 'Change Requests', 'Access', 'Event History']

        probability = random.randint(0, 100)
        view: str = None

        if probability <= 10:
            view = random.choice(engagement_view_list_low)

        elif probability > 10 and probability <= 40:
            view = random.choice(engagement_view_list_medium)
        elif probability > 40:
            view = random.choice(engagement_view_list_high)

        logger.info(f"{view} selected as the view")
        engagement_row_index = random.randint(1, 10)
        no_of_times_to_page = random.randint(0, 2) 
        try:

            site_page.select_multi_dropdown_item(
                label="All Engagements Grid-userFilterDropdown_4",
                is_test_label=True,
                choice_label=["Yash Dwivedi"],
                locust_request_label="Select Accountable Auditor as YD"
            )

            logger.info(f"Grid filtered")

            for i in range(no_of_times_to_page):
                site_page.move_to_right_in_paging_grid(
                    label= "All Engagements Grid",
                    locust_request_label="Moving engagement Grid to right"

                )
                time.sleep(5)

            engagement_record_instance: RecordInstanceUiForm = site_page.click_grid_rich_text_record_link(
                column_name="Engagement",
                row_index=engagement_row_index,
                grid_label="All Engagements Grid",
                locust_request_label="Click Engagement Record"
            )
            logger.info(f"Engagement Clicked")

            engagement_record_instance.get_header_view()

            time.sleep(5)

            engagement_record_instance = engagement_record_instance.click_record_view_link(
                label=view,
                locust_request_label= str(view) + " View"
            )

            time.sleep(240)

            logger.info(f" {view} view loaded")

            return engagement_record_instance

            # engagement_record_instance = engagement_record_instance.click_record_view_link(
            #     label="Coverage",
            #     locust_request_label="Coverage View"
            # )
            # engagement_record_instance = engagement_record_instance.click_record_view_link(
            #     label="Relevant Issues",
            #     locust_request_label="Relevant Issues View"
            # )
            # engagement_record_instance = engagement_record_instance.click_record_view_link(
            #     label="MEL",
            #     locust_request_label="MEL View"
            # )
            # engagement_record_instance = engagement_record_instance.click_record_view_link(
            #     label="EKID",
            #     locust_request_label="EKID View"
            # )
            # engagement_record_instance = engagement_record_instance.click_record_view_link(
            #     label="Memo",
            #     locust_request_label="Memo View"
            # )
            # engagement_record_instance = engagement_record_instance.click_record_view_link(
            #     label="Fieldwork",
            #     locust_request_label="Fieldwork View"
            # )
            # engagement_record_instance = engagement_record_instance.click_record_view_link(
            #     label="Exceptions & Findings",
            #     locust_request_label="Exceptions & Findings View"
            # )
            # engagement_record_instance = engagement_record_instance.click_record_view_link(
            #     label="Audit Report",
            #     locust_request_label="Exceptions & Findings View"
            # )
            # engagement_record_instance = engagement_record_instance.click_record_view_link(
            #     label="Exceptions & Findings",
            #     locust_request_label="Exceptions & Findings View"
            # )
            # engagement_record_instance = engagement_record_instance.click_record_view_link(
            #     label="Audit Report",
            #     locust_request_label="Audit Report View"
            # )
            # engagement_record_instance = engagement_record_instance.click_record_view_link(
            #     label="Documents",
            #     locust_request_label="Documents View"
            # )
            # engagement_record_instance = engagement_record_instance.click_record_view_link(
            #     label="Change Requests",
            #     locust_request_label="Documents View"
            # )
            # engagement_record_instance = engagement_record_instance.click_record_view_link(
            #     label="Access",
            #     locust_request_label="Documents View"
            # )
            # engagement_record_instance = engagement_record_instance.click_record_view_link(
            #     label="History",
            #     locust_request_label="Documents View"
            # )


        except Exception as e:
            if site_page:
                utils.debug_write_ui_state_to_file(f"site_page", "site_page last state",
                                                   site_page)
                
            raise Exception(f"Error viewing view") from e