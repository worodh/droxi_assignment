import requests
from playwright.sync_api import TimeoutError

class TrelloAPIClient:
    BASE_URL = "https://api.trello.com/1"

    def __init__(self, api_key, token, board_id=None):
        self.api_key = api_key
        self.token = token
        self.board_id = board_id

    def _get(self, endpoint, params=None):
        if params is None:
            params = {}
        params.update({
            'key': self.api_key,
            'token': self.token
        })
        response = requests.get(f"{self.BASE_URL}/{endpoint}", params=params)
        response.raise_for_status()
        return response.json()

    def get_lists(self):
        return self._get(f"boards/{self.board_id}/lists")

    def get_cards(self):
        return self._get(f"boards/{self.board_id}/cards")


class TrelloUIClient:
    BOARD_LISTS = ["To Do", "In Progress", "Done"]
    def __init__(self, page, username, password):
        self.page = page
        self.username = username
        self.password = password

    def login(self):
        self.page.goto("https://trello.com/login")
        self.page.fill("#username-uid1", self.username)
        self.page.click("#login-submit")
        self.page.fill("#password", self.password)
        self.page.click("#login-submit")

    def wait_for_dashboard(self):
        # self.page.wait_for_selector('[id="content"]')
        self.page.wait_for_url("**/boards")

    def navigate_to_board(self, board_url):
        self.page.goto(board_url)

    def get_urgent_cards(self):
        # Scroll down all lists to ensure all cards are loaded, otherwise the locator may miss some cards
        lists = self.page.locator('[data-testid="list-cards"]')
        count = lists.count()
        for i in range(count):
            lists.nth(i).evaluate("node => node.scrollTop = node.scrollHeight")

        return self.page.locator(
            'li[data-testid="list-card"]:has(span[data-testid="compact-card-label"][data-color*="red"])'
        )

    def get_card_data(self, card_element):
        card_element.click()
        title = self.page.locator('#card-back-name').inner_text()
        try:
            description = self.page.locator('div[data-testid="description-content-area"]').inner_text()
        except TimeoutError:
            description = ""
        labels = self.page.locator('span[data-testid="card-label"]').all_inner_texts()
        list_name = self.page.locator("header").inner_text()

        self.page.locator('span[data-testid="CloseIcon"]').click()
        return {
            'title': title,
            'description': description,
            'labels': labels,
            'list_name': list_name
        }

    def get_card_by_name(self, card_name):
        return self.page.locator(f'a[data-testid="card-name"]:has-text("{card_name}")')