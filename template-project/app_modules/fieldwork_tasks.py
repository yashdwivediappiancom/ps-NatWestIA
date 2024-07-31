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


class FieldworkTasks:

    def get_home_page(self, appian: AppianClient, site_name: str, page_name: str) -> 'SailUiForm':

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
        
    def select_engagement_and_navigate_to_fieldwork_tab(self, site_page: SailUiForm) -> 'SailUiForm':
        engagement_row_index = random.randint(1, 50)
        no_of_times_to_page = random.randint(0, 10) 
        try:

            # site_page.select_multi_dropdown_item(
            #     label="All Engagements Grid-userFilterDropdown_4",
            #     is_test_label=True,
            #     choice_label=["Yash Dwivedi"],
            #     locust_request_label="Select Accountable Auditor as YD"
            # )

            # logger.info(f"Grid filtered")

            for i in range(no_of_times_to_page):
                site_page.move_to_right_in_paging_grid(
                    label= "My Engagements Grid",
                    locust_request_label="Moving engagement Grid to right"

                )
            time.sleep(5)

            engagement_record_instance: RecordInstanceUiForm = site_page.click_grid_rich_text_record_link(
                column_name="Engagement",
                row_index=engagement_row_index,
                grid_label="My Engagements Grid",
                locust_request_label="Click Engagement Record"
            )
            logger.info(f"Engagement Clicked")

            engagement_record_instance.get_header_view()

            time.sleep(5)

            engagement_record_instance = engagement_record_instance.click_record_view_link(
                label="Fieldwork",
                locust_request_label= "Fieldwork" + " View"
            )

            utils.debug_write_ui_state_to_file(f"after clicking fieldwork", "after clicking fieldwork last state",
                                                   engagement_record_instance)

            
            

            engagement_record_instance = engagement_record_instance.click_grid_rich_text_link(
                grid_label="Risk, Controls & Procedures Grid",
                column_name="Controls/Procedures",
                row_index=1,
                locust_request_label="Selcting a Control"
            )
            time.sleep(5)


            utils.debug_write_ui_state_to_file(f"after clicking the first control", "clicking first control last state",
                                                   engagement_record_instance)


            # record_action_component = find_component_by_attribute_and_index_in_dict(
            #     attribute="#t",
            #     value="RelatedActionLink",
            #     index=1,
            #     component_tree=engagement_record_instance.get_latest_state()
            #     )
            
            # task_label = record_action_component["label"]

            # update_control_procedure.click_related_action(
            #     label=task_label,
            #     locust_request_label="Updating Control/Procedure"
            # )

            update_control_procedure = copy(engagement_record_instance)
            

            update_control_procedure.click_related_action(
                label="Edit Control/Procedure Description",
                locust_request_label="Updating the Description"
            )
            time.sleep(5)

            logger.info(f"Update Description Clicked")

            update_control_procedure.click_button(
                label="Break Lock",
                locust_request_label="Updating the Description"
            )
            time.sleep(5)

            logger.info(f"Lock Broken")

            utils.debug_write_ui_state_to_file(f"after clicking the update desription", "description form last state",
                                                   update_control_procedure)

            update_control_procedure.fill_field_by_index(
                type_of_component="StyledTextEditorWidget",
                index=1,
                text_to_fill="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas et pulvinar nulla, consequat viverra felis. Phasellus ac risus lobortis, vehicula enim pulvinar, vehicula tellus. Sed eu ex placerat, ullamcorper dolor ac, blandit velit. Quisque cursus eleifend enim id sollicitudin. Pellentesque eget nunc quis odio maximus dignissim. Nam nec dui et lectus varius pharetra at in augue. Duis velit ligula, suscipit vel turpis non, faucibus faucibus sem. Phasellus efficitur nisl id egestas vestibulum. Phasellus finibus mauris augue.",
                locust_request_label="Fill Field"
            )

            time.sleep(300)

            logger.info(f"Text Filled")

            update_control_procedure.click_button(
                label="Save and Close",
                locust_request_label="Save and Close"
            )
            time.sleep(5)

            logger.info(f"Save and Close")

            engagement_record_instance.refresh_after_record_action(
                label="Edit Control/Procedure Description",
                locust_request_label="Refreshing"
            )
            time.sleep(5)


            update_exception = copy(engagement_record_instance)
            
            
            update_exception.click_related_action(
                label="Add Exception",
                locust_request_label="Add Exception"
            )
            time.sleep(120)

            update_exception.fill_text_field(
                label="Title",
                value="Lorem Ipsum",
                locust_request_label="Exception Title"
            )
            time.sleep(120)
            update_exception.select_dropdown_item(
                label="Factual Accuracy",
                choice_label="Factual Accuracy Confirmed",
                locust_request_label="Selecting Factual Accuracy"
            )
            time.sleep(120)
            update_exception.select_dropdown_item(
                label="Exception Status",
                choice_label="Component of a Finding",
                locust_request_label="Selecting Exception Status"
            )
            time.sleep(120)

            logger.info(f"Done Exception Quick Fields")

            update_exception.fill_field_by_index(
                type_of_component="StyledTextEditorWidget",
                index=1,
                text_to_fill="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas et pulvinar nulla, consequat viverra felis. Phasellus ac risus lobortis, vehicula enim pulvinar, vehicula tellus. Sed eu ex placerat, ullamcorper dolor ac, blandit velit. Quisque cursus eleifend enim id sollicitudin. Pellentesque eget nunc quis odio maximus dignissim. Nam nec dui et lectus varius pharetra at in augue. Duis velit ligula, suscipit vel turpis non, faucibus faucibus sem. Phasellus efficitur nisl id egestas vestibulum. Phasellus finibus mauris augue.",
                locust_request_label="Fill Exception Description"
            )
            logger.info(f"Filling Description")
            time.sleep(300)

            update_exception.fill_text_field(
                label="Factual Accuracy Rationale",
                value="Lorem Ipsum Text",
                locust_request_label="Filling Factual Accuracy Rationale"
            )
            logger.info(f"Filling Factual Accuracy Rationale")
            time.sleep(120)

            update_exception.fill_text_field(
                label="Status Rationale",
                value="Lorem Ipsum Text",
                locust_request_label="Filling Status Rationale"
            )
            logger.info(f"Filling Status Rationale")

            time.sleep(120)

            update_exception.click_button(
                label="Save",
                locust_request_label="Save Exception"
            )
            time.sleep(5)

            engagement_record_instance.refresh_after_record_action(
                label="Add Exception",
                locust_request_label="Refreshing after Exception"
            )

            logger.info(f"Refreshed")



            
            
            return engagement_record_instance


        except Exception as e:
            if site_page:
                utils.debug_write_ui_state_to_file(f"site_page", "site_page last state",
                                                   site_page)
                
            if engagement_record_instance:
                utils.debug_write_ui_state_to_file(f"site_page", "site_page last state",
                                                   engagement_record_instance)
                
            if update_control_procedure:
                utils.debug_write_ui_state_to_file(f"site_page", "site_page last state",
                                                   update_control_procedure)
            if update_exception:
                utils.debug_write_ui_state_to_file(f"site_page", "site_page last state",
                                                   update_exception)
                
            raise Exception(f"Error viewing view") from e