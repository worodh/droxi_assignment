import pytest
from pytest_check import check

def test_urgent_cards(trello_ui_client):
    urgent_cards = trello_ui_client.get_urgent_cards()
    assert urgent_cards.count() == 3
    for i in range(urgent_cards.count()):
        urgent_card = urgent_cards.nth(i)
        card_data = trello_ui_client.get_card_data(urgent_card)
        print(card_data)

def test_specific_card_ui(trello_ui_client):
    card = trello_ui_client.get_card_by_name("summarize the meeting")
    card_data = trello_ui_client.get_card_data(card)
    check.equal(card_data['title'], "summarize the meeting", "Card title does not match expected value")
    check.equal(card_data['description'], "For all of us\nPlease do so", "Card description does not match expected value")
    check.is_in('New', card_data['labels'], "Card does not have 'New' label")
    check.equal(card_data['list_name'], 'To Do', "Card is not in the expected list 'To Do'")
