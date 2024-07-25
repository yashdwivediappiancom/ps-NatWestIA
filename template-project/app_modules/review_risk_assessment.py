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


class ReviewTasks:

    def get_tasks_page(self, appian: AppianClient, site_name: str, page_name: str) -> 'SailUiForm':

        site_form = None
        try:
            # Go to engagements screen
            site_form = appian.visitor.visit_site(site_name=site_name, page_name=page_name,
                                                  locust_request_label=f"Visit.Site.{site_name}.{page_name}")

            # Debug site form for fun
            utils.debug_write_ui_state_to_file(f"site_form", "site_form orders tab load",
                                               site_form)

            logger.info(f"Site {site_name} page {page_name} loaded")

            return site_form
        
        except Exception as e:
            if site_form:
                utils.debug_write_ui_state_to_file(f"site_form", "site_form last state",
                                                   site_form)
            raise Exception(f"Error viewing site {site_name} page {page_name}") from e
        
    def select_random_review(self, site_page: SailUiForm) -> SailUiForm:

        try:

            site_page.fill_text_field(
                label="Tasks grid-recordSearchBox",
                is_test_label=True,
                value="Risk Assessment Approval",
                locust_request_label="Filtering Grid By Risk Assessments"
            )


            copy_of_site=copy(site_page)

            time.sleep(5)
            record_action_component = find_component_by_attribute_and_index_in_dict(
                attribute="#t",
                value="RelatedActionLink",
                index=1,
                component_tree=site_page.get_latest_state()
                )
            
            task_label = record_action_component["label"]

            copy_of_site.click_related_action(
                label=task_label,
                locust_request_label="Selecting the Review"
            )

            copy_of_site.click_button(
                label="Approve",
                locust_request_label="Approve the review of risk_assessment"
            )

            site_page.refresh_after_record_action(
                label=task_label,
                locust_request_label="Refreshing"
            )

        except Exception as e:
            if site_page:
                utils.debug_write_ui_state_to_file(f"site_page", "site_page last state",
                                                   site_page)