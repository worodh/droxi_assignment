import pytest

def test_urgent_cards_api(trello_api_client, gmail_client):
    cards = trello_api_client.get_cards()
    gmail_urgent_messages = [msg for msg in gmail_client.messages if 'Urgent' in msg.body]
    urgent_cards = [card for card in cards if any(label['name'] == 'urgent' for label in card.get('labels', []))]
    for card in urgent_cards:
        matching_messages = [msg for msg in gmail_urgent_messages if msg.subject == card['name']]
        assert matching_messages, f"No matching urgent email found for card '{card['name']}'"
        merged_bodies = "\n".join([msg.body for msg in matching_messages])
        assert card['desc'] == merged_bodies, f"Card description does not match merged_bodies email bodies for card '{card['name']}'"
