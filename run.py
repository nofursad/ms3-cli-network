"""
Importing the library to use in system
"""
import sys
import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPE_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPE_CREDS)
SHEET = GSPREAD_CLIENT.open('Networking')


def newscreen():
    """
    newscreening the screen for new menu or sub-menu
    """
    print('\033c')


def login():
    """
    Login in function for user to login to the system
    Takes username from the user and match it to database
    Give access to system if user exist
    """
    newscreen()
    print("LOGIN TO NETWORK\n")
    user_sheet = SHEET.worksheet("users")
    user = input("Please Enter your username:\nOr Press Enter to go back to main menu.\n").strip()
    if user == "":
        main()
    else:
        search_result = user_sheet.find(user)
        if search_result is None:
            print(
                f"Invalid Username. Username '{user}' not found in system. Please try again."
            )
            input("Press Enter to continue...")
        else:
            global userID
            userID = user_sheet.cell(user_sheet.find(user).row, 8).value
            global username
            username = user
            login_menu(username)


def main():
    """
    Main Menu to display to user at the main screen when the system loads
    """
    while True:
        newscreen()
        header()
        print('Welcome to CLI Networking:')
        print("Main Menu\n")
        print("1. Login")
        print("2. New User")
        print("3. Exit")

        choice = input("Please choose an option by entering 1, 2 or 3\n").strip()

        if choice == '1':
            login()
        elif choice == '2':
            createuser()
        elif choice == '3':
            sys.exit(0)
        else:
            input("Invalid selection. Please enter 1, 2, or 3\nPress Enter to continue...\n")


def header():
    """
    This function print the header in the main page to welcome the
    user when user first open the system.
    """
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    time.sleep(0.2)
    print("@@                                                                                                                 @@")
    time.sleep(0.2)
    print("@@      @@@@  @@       @@@@@@      @@      @@ @@@@@@@@@ @@@@@@@@@@ @@        @@      @@@      @@@@@@    @@    @@   @@")
    time.sleep(0.2)
    print("@@     @@     @@         @@        @@@     @@ @@            @@     @@        @@     @@ @@     @@   @@   @@   @@    @@")
    time.sleep(0.2)
    print("@@   @@       @@         @@        @@ @@   @@ @@            @@     @@        @@   @@     @@   @@   @@   @@ @@      @@")
    time.sleep(0.2)
    print("@@   @@       @@         @@        @@  @@  @@ @@@@@@        @@     @@   @@   @@  @@       @@  @@@@@@    @@@@       @@")
    time.sleep(0.2)
    print("@@   @@       @@         @@        @@   @@ @@ @@            @@     @@  @@@@  @@   @@     @@   @@ @@     @@ @@      @@")
    time.sleep(0.2)
    print("@@     @@     @@         @@        @@     @@@ @@            @@     @@@@    @@@@     @@ @@     @@   @@   @@   @@    @@")
    time.sleep(0.2)
    print("@@      @@@@  @@@@@@@  @@@@@@      @@      @@ @@@@@@@@@     @@     @@@      @@@      @@@      @@    @@  @@    @@   @@")
    time.sleep(0.2)
    print("@@                                                                                                                 @@")
    time.sleep(0.2)
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")


if __name__ == "__main__":
    main()
