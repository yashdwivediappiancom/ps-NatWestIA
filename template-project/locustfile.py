#!/usr/bin/env python3
from logging.handlers import RotatingFileHandler
import logging.config
import time

from locust import HttpUser, task, between, events

from gevent.lock import Semaphore

from appian_locust.appian_task_set import AppianTaskSet
from appian_locust.utilities import loadDriverUtils

from utilities import utils

from app_modules.engagement_tasks import EngagementTasks
from app_modules.risk_assessment_task import RiskAssessmentTasks
from app_modules.review_risk_assessment import ReviewTasks
from app_modules.record_view_tasks import RecordView
from app_modules.fieldwork_tasks import FieldworkTasks

import urllib3

utls = loadDriverUtils()
utls.load_config()

# We later enable self-signed certs, this will disable the warnings about this
urllib3.disable_warnings()

# Set up the logger
logger = utils.set_up_logger()

# constants
DEFAULT_CONFIG_PATH = './config.json'
CONFIG = utls.c
CLIENT_RECORD_MODE_ENABLED = CONFIG["client_record_mode_enabled"]

utils.clean_debug_dir()
logger.info(f"***** Starting Locust Test *****")
logger.info(f"Utils: Debug dir cleaned")

# Spawn control
all_locusts_spawned = Semaphore()
all_locusts_spawned.acquire()


@events.spawning_complete.add_listener
def on_spawn_complete(**kw):
    logger.info(f"All users spawned - testing released")
    all_locusts_spawned.release()


class AuditorTaskSet(AppianTaskSet):
    # Task Set for Auditors
    def __init__(self, parent: AppianTaskSet) -> None:
        self.site_name = "internal-audit"
        super().__init__(parent)

    def on_start(self, portals_mode: bool = False, config_path: str = DEFAULT_CONFIG_PATH,
                 is_mobile_client: bool = False) -> None:
        logger.info("AuditorTaskSet: on_start starting")

        # Enable self-signed certs
        self.client.verify = False

        # Capture request and response debug
        self.client.record_mode = CLIENT_RECORD_MODE_ENABLED

        # Log in to Appian
        super().on_start()

        logger.info("AuditorTaskSet: user waiting for everyone else")
        # all_locusts_spawned.wait()
        logger.info("AuditorTaskSet: user released")

    def on_stop(self):
        logger.info("logging out")
        # Log out from Appian
        super().on_stop()

    @task(0)
    
    def update_risk_assessment(self):
        task_name = "update_risk_assessment"
        try:
            logger.info(f"Doing task {task_name}")
            om_tasks = OMTasks()
            risk_assessment_tasks = RiskAssessmentTasks()

            site_name = "internal-audit"
            page_name = "auditable-entities"

            logger.info("Get auditable entities site page")
            orders_site_page = risk_assessment_tasks.get_auditable_entities_page(appian=self.appian, site_name=site_name, page_name=page_name)

            #logger.info("Create new order")
            #orders_site_page = om_tasks.create_engagement_from_engagements_page_then_refresh_engagements(site_page=orders_site_page)

            logger.info("Click on Auditable Entity")
            orders_site_page = risk_assessment_tasks.update_risk_assessment(site_page=orders_site_page)

            logger.info(f"Task {task_name}: end of processing")

        except Exception as e:
            logger.error(f"Error in {task_name}", exc_info=e)

    @task(80)
    def view_engagement_tabs(self):
        task_name = "navigating the record views"
        logger.info(f"Doing task {task_name}")

        try: 
            
            record_view_tasks = RecordView()

            site_name = "internal-audit"
            page_name = "engagements"

            homepage = record_view_tasks.get_home_page(appian=self.appian, site_name=site_name, page_name=page_name)

            logger.info("Click on an Engagement")

            
            homepage = record_view_tasks.select_engagement_and_navigate_across_views(site_page=homepage)

            logger.info("Click on a view")
        
        
            time.sleep(5)
        
            self.appian.visitor.visit_site(
                    site_name="internal-audit", page_name="home", locust_request_label="Visit Home Page"
                )

            logger.info(f"End task {task_name}")

        except Exception as e:
            logger.error(f"Error in {task_name}", exc_info=e)


    @task(20)
    def fieldwork(self):
        task_name = "Fieldwork tasks"
        logger.info(f"Doing task {task_name}")

        try:
            fieldwork_task = FieldworkTasks()

            site_name = "internal-audit"
            page_name = "home"

            homepage = fieldwork_task.get_home_page(appian=self.appian, site_name=site_name, page_name=page_name)

            logger.info("Click on to Homepage")

            homepage = fieldwork_task.select_engagement_and_navigate_to_fieldwork_tab(site_page=homepage)

            logger.info("Click on to Engagement and Fieldwork Tab")

        except Exception as e:
            logger.error(f"Error in {task_name}", exc_info=e)


class HeadOfAuditTaskSet(AppianTaskSet):
    # Task Set for a user who just views OM customers
    def __init__(self, parent: AppianTaskSet) -> None:
        self.site_name = "internal-audit"
        super().__init__(parent)

    def on_start(self, portals_mode: bool = False, config_path: str = DEFAULT_CONFIG_PATH,
                 is_mobile_client: bool = False) -> None:
        logger.info("HeadOfAuditTaskSet: on_start starting")

        # Enable self-signed certs
        self.client.verify = False

        # Capture request and response debug
        self.client.record_mode = CLIENT_RECORD_MODE_ENABLED

        # Log in to Appian
        super().on_start()

        logger.info("HeadOfAuditTaskSet: user waiting for everyone else")
        # all_locusts_spawned.wait()
        logger.info("HeadOfAuditTaskSet: user released")

    def on_stop(self):
        logger.info("logging out")
        # Log out from Appian
        super().on_stop()

    @task(0)
    def review_risk_assessment(self):
        task_name = "review_risk_assessment"
        try:
            logger.info(f"Doing task {task_name}")
            
            review_task = ReviewTasks()
            om_tasks = OMTasks()

            site_name = "internal-audit"
            page_name = "tasks"

            logger.info("Get Review All Tasks")
            orders_site_page = review_task.get_tasks_page(appian=self.appian, site_name=site_name, page_name=page_name)
            logger.info("Selecting Random Review Task")

            review_task.select_random_review(site_page=orders_site_page)

            logger.info(f"End task {task_name}")
            #print(orders_site_page)
            
            #review_task.select_random_review(site_page=orders_site_page)

            

            logger.info(f"Finished task {task_name}")

        except Exception as e:
            logger.error(f"Error in {task_name}", exc_info=e)

class AuditorUserActor(HttpUser):
    actor_config_ref = "auditor"
    # HttpUser for an Auditor
    logger.info("AuditorUserActor locust starting")

    tasks = [AuditorTaskSet]

    # wait_time determines how long each user waits between #@task runs.
    # A random wait time will be chosen between min_wait and max_wait (seconds)
    wait_time = between(CONFIG["actor_config"][actor_config_ref]["wait_from"],
                        CONFIG["actor_config"][actor_config_ref]["wait_to"])
    # weight determines how often this actor is spawned versus other actors
    weight = CONFIG["actor_config"][actor_config_ref]["weight"]

    host = f'https://{CONFIG["cluster_name"]}.{CONFIG["cluster_domain"]}'

    # An auth attribute is required, even if we want to use credentials instead

    auditor = CONFIG["auditor"]
    auth = auditor["auth_auditor"]
    # auth does need to be populated, but to use multiple credentials we then populate credentials:
    credentials = auditor["credentials_auditor"]



class HeadOfAuditUserActor(HttpUser):
    actor_config_ref = "head_audit"
    # HttpUser for a Valo Order Management user who just views customers
    logger.info("HeadOfAuditUserActor locust starting")

    tasks = [HeadOfAuditTaskSet]

    # wait_time determines how long each user waits between #@task runs.
    # A random wait time will be chosen between min_wait and max_wait (seconds)
    wait_time = between(CONFIG["actor_config"][actor_config_ref]["wait_from"],
                        CONFIG["actor_config"][actor_config_ref]["wait_to"])
    # weight determines how often this actor is spawned versus other actors
    weight = CONFIG["actor_config"][actor_config_ref]["weight"]

    host = f'https://{CONFIG["cluster_name"]}.{CONFIG["cluster_domain"]}'

    # An auth attribute is required, even if we want to use credentials instead
    head_audit = CONFIG["head_audit"]
    auth = head_audit["auth_head_audit"]
    # auth does need to be populated, but to use multiple credentials we then populate credentials:
    credentials = head_audit["credentials_head_audit"]
