# Task 1
## Assumptions
- Gmail mailbox is accessible and contains Inbox and Trash folders
- Trello board exists with the columns: **To Do**, **In Progress**, **Done**
- Trello labels **New** and **Urgent** exists
- The sync process runs automatically and correctly
- All emails have a subject

## Test Coverage
- Email ->Trello card creation
- Subject and body mapping
- Label assignment
- Status synchronization
- Deduplicated messages are merged in card description
- Edge cases

## Manual Test Cases

### Basic Mapping
1. An email appearing in Gmail Inbox creates a new Trello card in the **To Do** column with the **New** label.
2. Trello card title matches the email subject.
3. If the email subject contains "Task:", the card title uses the text following "Task:".
4. Trello card description matches the email body.
5. If the email body contains the word "Urgent", the Trello card is created with the **Urgent** label.
6. Running the sync process multiple times does not create duplicate Trello cards.


### Status Synchronization
7. All cards located in **In Progress** has matching emails present in Gmail Inbox.
8. Moving a Trello card to **Done** moves the matching email to Gmail Trash.

### Deduplication & Merge Logic
9. Multiple emails with the same subject and identical body result in a single Trello card.
10. Multiple emails with the same subject and different bodies result in a single Trello card whose description contains the merged bodies in the defined order.

### Edge Cases
11. Special characters, emojis, images, and RTL text are preserved correctly.
12. Large email bodies are synchronized correctly and fully.

