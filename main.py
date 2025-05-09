import logging
import os
import sys
import time
from argparse import ArgumentParser
from datetime import date, datetime
from pathlib import Path

import schedule
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)


TOMHRM_BASE_URL = "https://tomhrm.app"
TOMHRM_LOGIN_URL = f"{TOMHRM_BASE_URL}/login"
TOMHRM_TIMESHEET_URL = f"{TOMHRM_BASE_URL}/timesheet"

SCREENSHOTS_DIR = Path(__file__).resolve().parent / "screenshots"

def report_work(
    headless: bool,
    username: str,
    password: str,
    workspace: str,
    screenshot_dir: Path,
    hours_worked: str = "8h"
) -> None:
    date_today = date.today()
    logger.info(f"Attempting to log time for {date_today.strftime('%Y-%m-%d')}...")

    with sync_playwright() as playwright_context:
        browser = playwright_context.firefox.launch(headless=headless)
        page = browser.new_page()

        try:
            logger.info(f"Navigating to login page: {TOMHRM_LOGIN_URL}")
            page.goto(TOMHRM_LOGIN_URL, wait_until="domcontentloaded")

            logger.info("Filling login form...")
            page.fill("#_username", username)
            page.fill("#_password", password)
            page.fill("#_tenant", workspace)

            logger.info("Submitting login form...")
            login_button_selector = "#main-form-login > div > button"
            page.wait_for_selector(login_button_selector, state="visible")
            page.click(login_button_selector)

            logger.info("Waiting for login to complete and redirect...")
            page.wait_for_url(f"{TOMHRM_BASE_URL}/**", wait_until="domcontentloaded", timeout=20000)

            logger.info(f"Navigating to timesheet: {TOMHRM_TIMESHEET_URL}")
            page.goto(TOMHRM_TIMESHEET_URL, wait_until="load")

            logger.info("Clicking 'Bulk Add'...")
            bulk_add_button = page.get_by_text("Bulk Add")
            bulk_add_button.wait_for(state="visible")
            bulk_add_button.click()

            logger.info("Waiting for bulk add form to appear...")
            bulk_add_input_selector = ".timePicker-bulk-add"
            page.wait_for_selector(bulk_add_input_selector, state="visible")

            date_str_today = date_today.strftime("%d-%m-%Y")
            logger.info(f"Looking for entry for date: {date_str_today}")

            weekday_inputs = page.query_selector_all(bulk_add_input_selector)
            found_day = False
            for weekday_input_element in weekday_inputs:
                data_day_format = weekday_input_element.get_attribute("data-dayformat")
                if data_day_format == date_str_today:
                    logger.info(f"Found entry for {date_str_today}. Filling with '{hours_worked}'.")
                    weekday_input_element.fill(hours_worked)

                    save_button = page.get_by_text("Save")
                    save_button.click()
                    logger.info("Time saved.")
                    found_day = True
                    break

            if not found_day:
                logger.info(f"No entry found for {date_str_today} in the bulk add section.")

        except PlaywrightTimeoutError as e:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = screenshot_dir / f"timeout_error_{timestamp}.png"
            logger.error(f"A timeout occurred: {e}")
            page.screenshot(path=screenshot_path)
            logger.info(f"Screenshot saved to {screenshot_path}")
        except Exception as e:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = screenshot_dir / f"unexpected_error_{timestamp}.png"
            logger.exception("An unexpected error occurred")
            try:
                page.screenshot(path=screenshot_path)
                logger.info(f"Screenshot saved to {screenshot_path}")
            except Exception as se:
                logger.error(f"Could not take screenshot: {se}")
        finally:
            logger.info("Closing browser.")
            browser.close()


def main() -> None:
    argparser = ArgumentParser()
    argparser.add_argument("--headed", action="store_true")
    argparser.add_argument("--schedule", action="store_true")
    argparser.add_argument("--screenshot-dir", type=Path, default=SCREENSHOTS_DIR)
    args = argparser.parse_args()

    screenshot_dir: Path = args.screenshot_dir
    screenshot_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Screenshots will be saved to: {screenshot_dir.resolve()}")

    try:
        username = os.environ["TOMHRM_USERNAME"]
        password = os.environ["TOMHRM_PASSWORD"]
        workspace = os.environ["TOMHRM_WORKSPACE"]   
    except KeyError as e:
        logger.error(f"Error: Environment variable {e} not set.")
        return
    
    def job():
        report_work(
            headless=not args.headed,
            username=username,
            password=password,
            workspace=workspace,
            screenshot_dir=screenshot_dir,
            hours_worked="8h"
        )
    
    if not args.schedule:
        job()
    else:
        if args.headed:
            input("Schedule job not in headless mode??")
            print("\nYou psycho.\n")

        report_time = "17:00"
        schedule.every().monday.at(report_time).do(job)
        schedule.every().tuesday.at(report_time).do(job)
        schedule.every().wednesday.at(report_time).do(job)
        schedule.every().thursday.at(report_time).do(job)
        schedule.every().friday.at(report_time).do(job)

        print(f"Scheduled. Next job runs in {schedule.idle_seconds()} seconds.")
        while True:
            schedule.run_pending()
            time.sleep(1)


if __name__ == "__main__":
    main()