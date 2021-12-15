"""
Importing the library to use in system
"""
import re
import sys
from datetime import datetime
import gspread
import phonenumbers
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
    print("\033c")


def login():
    """
    Login in function for user to login to the system
    Takes username from the user and match it to database
    Give access to system if user exist
    """
    newscreen()
    print("LOGIN TO NETWORK\n")
    user_sheet = SHEET.worksheet("users")
    user = input("Please Enter your username:\nOr Press Enter to go back to "
                 "main menu.\n").strip()
    if user == "":
        main()
    else:
        search_result = user_sheet.find(user)
        if search_result is None:
            print(
                f"Invalid Username. Username '{user}' not found in system. "
                "Please try again."
            )
            input("Press Enter to continue...")
        else:
            global userID
            userID = user_sheet.cell(user_sheet.find(user).row, 8).value
            global username
            username = user
            login_menu(username)


def timestamp():
    """
    Getting the current time and returning the value
    """
    timestamp = datetime.now()
    timestamp = timestamp.strftime("%Y%m%d%H%M%S")
    return timestamp


def createuser():
    """
    Function to create the new user for the first time user.
    User will be asked to enter the details about them to
    create new user account. User details will be add to
    the users sheet.Timestamp will be added automatically
    when the user is created successfully.
    """
    while True:
        newscreen()
        print("CREATE A NEW USER")
        print("Please answer the below questions to create new user:\n")

        # Getting user information and validating them before storing
        # in google sheet
        while True:
            fname = input("Please enter your first name: \n").strip()
            if fname.isalpha():
                break
            else:
                print("Please Enter a valid first name.\n")
        while True:
            lname = input("Please enter your last name:\n").strip()
            if lname.isalpha():
                break
            else:
                print("Please Enter a valid last name.\n")
        # Checking if the input is valid U.K. mobile number
        # before storing it
        while True:
            mobile = input("Please enter your U.K. mobile number "
                           "(e.g.07XXXXXXXXX):\n").strip()
            validate_mobile = phonenumbers.parse(mobile, "GB")
            mobile_list = SHEET.worksheet("users").col_values(3)
            if phonenumbers.is_valid_number(validate_mobile):
                if mobile in mobile_list:
                    print("Mobile number already exist in database. "
                          "Please try different number")
                else:
                    break
            else:
                print("Please enter valid phone number as show "
                      "in example.\n")
        # Checking if the input is valid email address before storing it
        while True:
            email = input("Please enter your email address:\n").strip()
            email_list = SHEET.worksheet("users").col_values(4)
            email_format = (
                r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
            if re.fullmatch(email_format, email):
                if email in email_list:
                    print("Email Address already exist in database. "
                          "Please try different email address")
                else:
                    break
            else:
                print("Please enter valid email address.\n")
        # Checking if the input is valid date in valid format and the
        # age requirement meets before storing it
        while True:
            dob = input("Please enter your date of birth "
                        "(DD/MM/YYYY):\n").strip()
            dob_format = "%d/%m/%Y"
            try:
                if datetime.strptime(dob, dob_format):
                    dob_acquire = datetime.strptime(dob, dob_format)
                    current_time = datetime.now()
                    alpha = str((current_time - dob_acquire)/365.25)
                    age = int(alpha[0:2])
                    if 18 <= age:
                        break
                    elif current_time < dob_acquire:
                        print("Sorry, future date are not accepted.")
                    else:
                        input("Sorry, but minimum age requirement is not "
                              "meet.\nPress Enter to go to main menu.")
                        main()
            except ValueError:
                print("Invalid DOB. Please try again.\n")
        # validating to make sure new username is not duplicate
        # to any username in database.
        while True:
            username = input("Please enter a username that "
                             "you use to log in:\n").strip()
            username_list = SHEET.worksheet("users").col_values(6)
            if username in username_list:
                print(f"Sorry, Username '{username}' not avaliable. "
                      "Try another please.\n")
            else:
                break
        time_stamp = timestamp()

        print(f"Hi {fname}, Welcome to Network.\n")
        print(f"Creating the new user for {fname}....\n")

        # Adding the information provided by new user in database
        data = (fname, lname, mobile, email, dob, username, time_stamp)
        SHEET.worksheet("users").append_row(data)
        print(f"New user created for {fname} successfully. "
              "Please use username '{username}' to log in.\n")
        print("You will be redirect to main menu, please use "
              "username you created to login.")

        input("Press Enter to continue...")
        break


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
