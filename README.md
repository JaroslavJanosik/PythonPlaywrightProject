Simple Automation Framework based on Python, PyTest and Playwright.

### How to use this framework?
- install Microsoft Visual Studio Code IDE
- install Git on your system
- install Python 3.11.5 on your system
- install Poetry and setup environment:
```shell
python -m pip install poetry
python -m poetry config virtualenvs.in-project true
```
- restart PC
- clone the repository to your workspace
- open project folder with VSCode
- open terminal from the project root
- execute commands below:
```shell
python -m poetry shell
python -m poetry install
poetry run playwright install
```
- run all tests using the command ```pytest```

### Test case
```
Feature: Seznam Email

    Scenario: Sending an Email with an Attachment

        Given the user is on the application's login page
        When the user logs in with valid credentials
        Then the home page should load successfully
        When the user clicks on the Compose e-mail button in the navigation panel
        Then a modal window should open
        When the user fills in the recipient, subject, and email body
        And attaches a file
        And clicks on the Send e-mail button
        Then the email should be sent successfully
        And the modal window should close
        And a notification message should be displayed
        When the user clicks on the Sent button in the navigation panel
        Then a list of sent emails should appear in the content section
        And the sent email should be the most recent item in the list
        And the recipient should receive the email
        When the user logs out from the application
        Then they should be returned to the application's login page
  ```
