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

class RiskAssessmentTasks:

    def get_auditable_entities_page(self, appian: AppianClient, site_name: str, page_name: str) -> 'SailUiForm':

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
        

    def update_risk_assessment(self, site_page: SailUiForm) -> SailUiForm:
        
        AE_row_index = random.randint(1, 50)
        no_of_times_to_page = random.randint(0, 15) 
        list_of_risk_types = ['Capital', 'Change Risk', 'Climate', 'Conduct - Market Abuse', 'Conduct - Mis-Selling', 'Conduct - Product Flaws', 'Continuity of Internal Supply Chain', 'Credit', 'Customer Account Management', 'Damage to Physical Assets', 'Data Quality', 'Diversity, Equity & Inclusion', 'Earnings Stability', 'Employee Relations', 'Environmental, Social and Ethical (ESE)', 'External Outsourcing', 'Financial Crime - Bribery and Corruption', 'Financial Crime - External Fraud', 'Financial Crime - Internal Fraud', 'Financial Crime - Money Laundering and / or Terrorist Financing', 'Financial Crime - Sanctions', 'Financial Crime - Tax Evasion', 'Financial Reporting', 'Information loss and integrity', 'Injury or Harm', 'Liquidity & Funding', 'Model', 'Non-Traded Market', 'Operational Resilience', 'Operational Risk (framework only)', 'Pension', 'Regulatory compliance', 'Technology Disruption', 'Theft of Bank Property', 'Trade or Transaction Reporting', 'Traded Market', 'Unauthorised Trading']
        selected_risk_types = random.choices(list_of_risk_types, k=random.randint(1, 3))
        #print(selected_risk_types)

        try:

            site_page.select_multi_dropdown_item(
                label="Auditable Entities grid-userFilterDropdown_6",
                is_test_label=True,
                choice_label=['Approved'],
                locust_request_label="Selecting Approved AEs"
            )

            site_page.select_multi_dropdown_item(
                label="Auditable Entities grid-userFilterDropdown_7",
                is_test_label=True,
                choice_label=['Low Risk', 'Medium Risk', 'High Risk', 'Very High Risk'],
                locust_request_label="Selecting All Risk Levels"
            )

            for i in range(no_of_times_to_page):
                site_page.move_to_right_in_paging_grid(
                    label= "Auditable Entities grid",
                    locust_request_label="Moving AE Grid to right"

                )
                print("Moving Grid right for the "+str(i)+" time")

            auditable_entity_record_instance: RecordInstanceUiForm = site_page.click_grid_rich_text_record_link(
                    column_name="ID",
                    row_index = AE_row_index,
                    grid_label = "Auditable Entities grid",
                    locust_request_label="Clicking on the AE on selected row"
                )
            print("Clicking on the AE on row " + str(AE_row_index))
            
            auditable_entity_record_instance.get_header_view()

            risk_assessment_view: SailUiForm = auditable_entity_record_instance.click_record_view_link(
                label="Current Risk Assessment",
                locust_request_label="Getting the Risk Assessment View"
            )

            copy_risk_assessment_form = copy(risk_assessment_view)

            copy_risk_assessment_form.click_related_action(
                label="Update Risk Assessment",
                locust_request_label="Clicking Update Risk Assessment Button"
            )

            utils.debug_write_ui_state_to_file(f"copy_risk_assessment", "copy_risk_assessment on load",
                                                copy_risk_assessment_form)


            copy_risk_assessment_form.select_multi_dropdown_item_by_index(
                index=1,
                choice_label = selected_risk_types,
                locust_request_label = "Selecting the risk type" 
            )

            utils.debug_write_ui_state_to_file(f"copy_risk_assessment", "copy_risk_assessment after selecting risk types",
                                                copy_risk_assessment_form)
            
            time.sleep(5)

            for i in range(len(selected_risk_types)):

                first_dropdown_index = i * 2 + 1
                second_dropdown_index = i * 2 + 2               
                copy_risk_assessment_form.select_dropdown_item_by_index(
                    index=first_dropdown_index,
                    choice_label='Major',
                    locust_request_label="Impact Score (number)"
                )
                time.sleep(2)
                copy_risk_assessment_form.select_dropdown_item_by_index(
                    index=second_dropdown_index,
                    choice_label='Likely',
                    locust_request_label="Likelihood Score (number)"
                )
                time.sleep(2)
            for i in range(len(selected_risk_types)):
                copy_risk_assessment_form.fill_paragraph_field(
                    label="Impact Rationale",
                    value= "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas et pulvinar nulla, consequat viverra felis. Phasellus ac risus lobortis, vehicula enim pulvinar, vehicula tellus. Sed eu ex placerat, ullamcorper dolor ac, blandit velit. Quisque cursus eleifend enim id sollicitudin. Pellentesque eget nunc quis odio maximus dignissim. Nam nec dui et lectus varius pharetra at in augue. Duis velit ligula, suscipit vel turpis non, faucibus faucibus sem. Phasellus efficitur nisl id egestas vestibulum. Phasellus finibus mauris augue.",
                    index=i+1,
                    locust_request_label= "Impact Rationale"
                )
                time.sleep(2)
                copy_risk_assessment_form.fill_paragraph_field(
                    label="Likelihood Rationale",
                    value= "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas et pulvinar nulla, consequat viverra felis. Phasellus ac risus lobortis, vehicula enim pulvinar, vehicula tellus. Sed eu ex placerat, ullamcorper dolor ac, blandit velit. Quisque cursus eleifend enim id sollicitudin. Pellentesque eget nunc quis odio maximus dignissim. Nam nec dui et lectus varius pharetra at in augue. Duis velit ligula, suscipit vel turpis non, faucibus faucibus sem. Phasellus efficitur nisl id egestas vestibulum. Phasellus finibus mauris augue.",
                    index=i+1,
                    locust_request_label= "Likelihood Rationale"
                )
                time.sleep(2)

            utils.debug_write_ui_state_to_file(f"copy_risk_assessment", "copy_risk_assessment after selecting risk types",
                                                copy_risk_assessment_form)

            copy_risk_assessment_form.click_button(
                label="Save",
                locust_request_label="Click Submit"
            )
            time.sleep(2)
            copy_risk_assessment_form.select_dropdown_item(
                label="Head of Audit",
                choice_label="Review Hoa",
                locust_request_label="Selected Approver"
            )
            time.sleep(2)
            copy_risk_assessment_form.click_button(
                label="Submit",
                locust_request_label="Click Submit"
            )
            time.sleep(2)
            risk_assessment_view.refresh_after_record_action(
                label="Update Risk Assessment",
                locust_request_label="Refresh After Record Action"
            )
            
            return risk_assessment_view
            
    
        except Exception as e:
            if site_page:
                utils.debug_write_ui_state_to_file(f"site_page", "site_page last state",
                                                   site_page)
            if auditable_entity_record_instance:
                utils.debug_write_ui_state_to_file(f"auditable_entity_record_instance", "auditable_entity_record_instance last state",
                                                   auditable_entity_record_instance)
            if risk_assessment_view:
                utils.debug_write_ui_state_to_file(f"risk_assessment_view", "risk_assessment_view last state",
                                                   risk_assessment_view)   
            if copy_risk_assessment_form:
                utils.debug_write_ui_state_to_file(f"copy_risk_assessment", "copy_risk_assessment last state",
                                                copy_risk_assessment_form)

            
            raise Exception("Error creating new case") from e
