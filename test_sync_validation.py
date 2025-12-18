import pytest
from pytest_check import check

def test_urgent_cards_api(trello_api_client, gmail_client):
    cards = trello_api_client.get_cards()
    gmail_urgent_messages = [msg for msg in gmail_client.messages if 'urgent' in msg.body.lower()]
    urgent_cards = [card for card in cards if any(label['name'] == 'Urgent' for label in card.get('labels', []))]
    for card in urgent_cards:
        matching_messages = [msg for msg in gmail_urgent_messages if msg.subject == card['name'].split("Task:")[-1]]
        check.not_equal(matching_messages,[],f"No matching urgent email found for card '{card['name']}'")
        if matching_messages:
            merged_bodies = "\n".join([msg.body for msg in matching_messages])
            check.equal(card['desc'], merged_bodies, f"Card description does not match merged_bodies email bodies for card '{card['name']}'")
        gmail_urgent_messages = list(set(gmail_urgent_messages) - set(matching_messages))
    check.equal(gmail_urgent_messages, [], f"These urgent mails don't have a matching trello card:{gmail_urgent_messages}")
