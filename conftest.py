import os
import time
import json
import pytest

from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from playwright.sync_api import TimeoutError

from clients.gmail_client import Gmail
from clients.trello_client import TrelloAPIClient, TrelloUIClient

@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv()

@pytest.fixture(scope="session")
def trello_api_client():
    trello_client = TrelloAPIClient(api_key=os.getenv("DROXI_API_KEY"),
                                    token = os.getenv("DROXI_API_TOKEN"),
                                    board_id=os.getenv("DROXI_BOARD_ID"))
    return trello_client


@pytest.fixture(scope="session")
def gmail_client():
    gmail_client = Gmail()
    with open('mock_gmail_data.json', 'r') as file:
        data_object = json.load(file)
        gmail_client.parse_data(data_object)
    return gmail_client


@pytest.fixture(scope="function")
def trello_ui_client():
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=False) # in headless true mode it asks for mfa
            page = browser.new_page()
            trello_ui_client = TrelloUIClient(page=page,
                                              username=os.getenv("DROXI_TRELLO_EMAIL"),
                                              password=os.getenv("DROXI_TRELLO_PASSWORD"))
            trello_ui_client.login()
            trello_ui_client.wait_for_dashboard()
            trello_ui_client.navigate_to_board(os.getenv("DROXI_BOARD_LINK"))
            yield trello_ui_client
        except TimeoutError as e:
            trello_ui_client.page.screenshot(path=f'screenshots/{str(time.time())}_error.png')
            raise e
        browser.close()
