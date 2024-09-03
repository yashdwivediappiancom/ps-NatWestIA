import os
from copy import copy
from datetime import date
import logging
import time
from appian_locust.uiform import SailUiForm
from appian_locust.uiform import RecordInstanceUiForm
from appian_locust.appian_client import AppianClient

from utilities import utils
import random

logger = logging.getLogger(utils.LOGGER_NAME)


class EngagementTasks:
    
    def create_engagement(self, site_page: SailUiForm) -> SailUiForm:
        try: 
            copy_of_site = copy(site_page)
            copy_of_site.click_button(
                label="Create Engagement", locust_request_label="Access New Engagement Form"
            )

            #Fill in information of the form i.e., engagement name, type, plan, AA, CA

            copy_of_site.fill_text_field(
                label="Engagement Name",
                value="YD Test Engagement L",
                locust_request_label="Fill in Engagement Name"
            )

            logging.info("Engagement NAME")

            copy_of_site.select_dropdown_item_by_index(
                index=1,
                choice_label="Engagement Plan",
                locust_request_label="Selecting the Engagement Plan"
            )

            logging.info("Engagement Plan")

            copy_of_site.select_dropdown_item_by_index(
                index=2,
                choice_label="Audit Engagement",
                locust_request_label="Selecting the Engagement Type"
            )

            logging.info("Engagement Type")

            copy_of_site.select_dropdown_item_by_index(
                index=3,
                choice_label="Yash Dwivedi",
                locust_request_label="Selecting the CA"
            )

            logging.info("CA")

            copy_of_site.select_dropdown_item_by_index(
                index=4,
                choice_label="Yash Dwivedi",
                locust_request_label="Selecting the AA"
            )

            logging.info("AA")


            copy_of_site.click_button(
                label="Submit",
                locust_request_label="Submit the Engagement for creation"
            )

            site_page.refresh_after_record_action(label="Create Engagement", locust_request_label="Refresh Engagements Page after Record Action")

            return site_page
    

        except Exception as e:
            if site_page:
                utils.debug_write_ui_state_to_file(f"site_page", "site_page last state",
                                                site_page)
            if copy_of_site:
                utils.debug_write_ui_state_to_file(f"copy_of_site", "copy_of_Site last state",
                                                copy_of_site)
            raise Exception("Error creating new case") from e
    
    def select_an_engagement_from_engagements_page(self, site_page: SailUiForm) -> 'SailUiForm':
        
        engagement_row_index = random.randint(0, 25)
        next_paging = bool(random.getrandbits(1))

        try:
            time.sleep(5)

            # if next_paging:
                
            #     site_page.move_to_right_in_paging_grid(
            #         index=1,
            #         locust_request_label="Paging the Grid to the right"
            #     )

            #     print("Paged to the right once")

            #     engagement_record_instance = site_page.click_grid_rich_text_record_link(
            #         column_name="Engagement",
            #         row_index=engagement_row_index,
            #         grid_label=" Engagements",
            #         locust_request_label="Clicking on the Engagement"
            #     )

            #     print("Paged to the right and then clicked on an engagement ")

            #else: 
            engagement_record_instance = site_page.click_grid_rich_text_record_link(
                column_name="Engagement",
                row_index=0,
                grid_label="All Engagements Grid",
                locust_request_label="Clicking on the Engagement"
            )

            engagement_record_instance.get_summary_view(
            )

            return engagement_record_instance


        except Exception as e:
            if site_page:
                utils.debug_write_ui_state_to_file(f"site_page", "site_page last state",
                                                   site_page)
            if engagement_record_instance:
                utils.debug_write_ui_state_to_file(f"engagement_record_instance", "engagement_record_instance last state",
                                                   engagement_record_instance)
            raise Exception("Error navigating to summary view") from e
        
    def create_new_order(self, site_page: SailUiForm) -> 'SailUiForm':
        try:
            # Copy the site page ready for launching modal so we can refresh site page afterwards
            new_order_modal = copy(site_page)
            new_order_modal.click("New Order")

            utils.debug_write_ui_state_to_file(f"new_order_modal", "new_order_modal on load",
                                            new_order_modal)

            new_order_modal.select_dropdown_item(label="Customer", choice_label="Monsoni")
            new_order_modal.fill_date_field(label="Due Date", date_input=date(2025, 1, 1))
            new_order_modal.fill_text_field(label="Special Instructions", value="This is an Appian Locust test new "
                                                                                "order")

            new_order_modal.upload_document_to_upload_field(label="Order Document",
                                                            file_path=os.path.abspath("resources/dummy_pdf_aui_guide.pdf"))

            utils.debug_write_ui_state_to_file(f"new_order_modal", "new_order_modal filled out",
                                            new_order_modal)

            new_order_modal.click("Create Order")

            site_page.refresh_after_record_action("New Order")

            utils.debug_write_ui_state_to_file(f"site_page", "site_page refreshed after New Order",
                                            site_page)

            logger.info(f"New order created")

            return site_page

        except Exception as e:
            if site_page:
                utils.debug_write_ui_state_to_file(f"site_page", "site_page last state",
                                                site_page)
            if new_order_modal:
                utils.debug_write_ui_state_to_file(f"new_order_modal", "new_order_modal last state",
                                                new_order_modal)
            raise Exception("Error creating new order") from e

