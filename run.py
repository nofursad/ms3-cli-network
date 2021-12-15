"""
Importing the library to use in system
"""
import re
import time
import sys
from datetime import datetime
from tabulate import tabulate
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


def login_menu(username):
    """
    This function display the menu item when user login to the system.
    """
    while True:
        newscreen()
        print(f"Welcome back to Network {username}\n")
        print("1. Update User Detail")
        print("2. Add Friend")
        print("3. View Friend")
        print("4. View Friend Request")
        print("5. Logout")

        choice = input("Please choose an option by entering number "
                       "between 1 to 5\n").strip()

        if choice == '1':
            update_menu()
        elif choice == '2':
            ad_menu()
        elif choice == '3':
            vf_menu()
        elif choice == '4':
            vfr_menu()
        elif choice == '5':
            userID = None
            username = None
            break
        else:
            input("Invalid selection. Please enter number between "
                  "1 to 5\nPress Enter to continue...\n")


def update_menu():
    """
    This function display the menu item when user select update user menu
    request from login menu.
    """
    while True:
        newscreen()
        print("UPDATE USER DETAILS\n")
        print("1. Update User Information")
        print("2. Delete User")
        print("3. Main Menu")

        choice = input("Please choose an option by entering "
                       "1, 2 or 3\n").strip()

        if choice == '1':
            update_user_detail()
        elif choice == '2':
            delete_user()
        elif choice == '3':
            break
        else:
            print("Invalid selection. Please enter 1, 2, or 3"
                  "\nPress Enter to continue...\n")


def update_user_detail():
    """
    Takes username from the user that required the update and
    search for it. Prompt user for new information to update
    the data that system hold. Update the old data that system
    holds with new data provided by user.
    """
    while True:
        newscreen()
        user_sheet = SHEET.worksheet("users")
        row_number = user_sheet.find(username).row
        fname = user_sheet.cell(row_number, 1).value

        # Getting new data from user, validate them and update the
        # old data in system
        print(f"Updating the detail for {username}")
        print("You can only update your Name, Mobile Number and "
              "Email address.\n")
        print(f"Hi {fname}, please enter new details to update your "
              "information that we hold:\n")
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
                print("Please enter valid phone number as show in example.\n")
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

        new_data = (fname, lname, mobile, email)
        print("Updating new details...\n")

        # Updating the new data to the row in USERS spreedsheet of
        # current user.
        for i in range(4):
            user_sheet.update_cell(row_number, i+1, new_data[i])

        print(f"New Details has been updated for {fname}.")
        input("Press Enter to continue...")
        break


def delete_user():
    """
    Takes the username from user that user want to delete
    Retrive the data and confirm with user for deletion of data
    Delete the user after user confirm
    """
    while True:
        newscreen()
        user_sheet = SHEET.worksheet("users")
        friend_sheet = SHEET.worksheet("connections")
        row_number = user_sheet.find(username).row
        fname = user_sheet.cell(row_number, 1).value

        # Getting conformation from user to delete the account
        # by confirmting the username.
        print(f"Do you want to delete the account for {fname}?\n")
        confirmation = input("please type username to confirm or 'n' to "
                             "cancel it...\n").strip()

        if confirmation == username:
            print(f"Deleting user {username}...\n")
            user_sheet.delete_rows(row_number)
            while True:
                if friend_sheet.find(userID):
                    row = friend_sheet.find(userID).row
                    friend_sheet.delete_rows(row)
                else:
                    break
            print(f"The user {username} is deleted. Your will be redirected "
                  "to main menu now.")
            input("Press Enter to continue..")
            main()
            # break
        elif confirmation == "n":
            print(f"The account for {fname} is not deleted. You will be "
                  "redirected to previous menu now.")
            input("Press Enter to continue...")
            break
        else:
            input("Invalid input please try again.\nPress Enter to "
                  "try again...")


def ad_menu():
    """
    This function display the menu item when user select
    add friend from login menu.
    """
    while True:
        newscreen()
        print("ADD FRIEND\n")
        print("1. Add Friend")
        print("2. Main Menu")

        choice = input("\nPlease choose an option by entering "
                       "1 or 2\n").strip()

        if choice == '1':
            add_friend()
        elif choice == '2':
            break
        else:
            print("Invalid selection. Please enter 1 or 2."
                  "\nPress Enter to continue...\n")


def add_friend():
    """
    This function will get the name of the person that user want to
    look for and search the database to see if any user with the name
    exist. If user found with the matching name( than user will get
    option to send request to add them in connection.)
    """
    while True:
        newscreen()
        # connecting to the worksheet to retrive the data
        user_sheet = SHEET.worksheet("users")
        friend_sheet = SHEET.worksheet("connections")
        search = input("Please enter the first or last name of a user that "
                       "you want to search,\nOr Hit Enter to go to previous "
                       "menu:\n").strip()
        search_result = user_sheet.findall(search)
        search_result_id = []

        # Printing the list of matching name found in database
        if search == "":
            break
        elif search_result == []:
            input(f"No user with the name {search} found in the database."
                  "\nPress Enter to search different name...")
        else:
            print(f"We found below user/s with name {search} in our "
                  "database.\n")
            i = 1
            for user in search_result:
                row_num = user.row
                fname = user_sheet.cell(row_num, 1).value
                lname = user_sheet.cell(row_num, 2).value
                search_result_id.append(user_sheet.cell(row_num, 8).value)
                print(f"{i}. {fname} {lname}")
                i += 1

            # getting number in front of name on list from user to add
            # as friend and send request
            while True:
                confirm = input("\nType a number infront of user to add "
                                "them as friend or type 'n' to go to "
                                "previous menu.\n").strip()
                if confirm.isdigit() and len(search_result_id) >= int(confirm):
                    data = [userID, search_result_id[int(confirm)-1], "n"]
                    friend_sheet.append_row(data)
                    input("Friend request send.\nPress Enter to continue...")
                    break
                elif confirm == "n":
                    input("You will be redirected to previous menu. \nPress "
                          "Enter to continue...")
                    break
                else:
                    print(f"{confirm} is not a valid option. Please enter "
                          "valid option.")


def vf_menu():
    """
    This function display the menu item when user select view friend
    from login menu.
    """
    while True:
        newscreen()
        print("VIEW FRIENDS\n")
        print("1. View Friends")
        print("2. Remove Friend")
        print("3. Main Menu")

        choice = input("Please choose an option by entering "
                       "1, 2 or 3\n").strip()

        if choice == '1':
            view_friends()
        elif choice == '2':
            remove_friend()
        elif choice == "3":
            break
        else:
            input("Invalid selection. Please enter 1, 2 or 3\nPress "
                  "Enter to continue...\n")


def view_friends():
    """
    This function takes username and get the list of user that is
    connected with current user and print the list of the name.
    """
    # connecting to the worksheet to retrive the data
    friend_sheet = SHEET.worksheet("connections")
    user_sheet = SHEET.worksheet("users")
    print("Preparing list of your friends...\n")

    all_friends_list = friend_sheet.findall(userID)

    # Getting the ID of other user who are friend with current user
    # global users_ids
    users_ids = []
    for friend in all_friends_list:
        if (friend_sheet.cell(friend.row, 3).value) == "y":
            if (friend.col) == 1:
                users_ids.append(friend_sheet.cell(friend.row, 2))
            else:
                users_ids.append(friend_sheet.cell(friend.row, 1))
    users_data = []

    # Retriving and printing the information of user's friends in table
    # using the user ID of user's friends
    if users_ids == []:
        input("You are not yet connected to anyone.\nPress Enter to "
              "continue...")
    else:
        print("You are friend with below people")
        i = 1
        for user_id in users_ids:
            row = user_sheet.find(user_id.value).row
            user_full_data = user_sheet.row_values(row)
            user_full_data.insert(0, i)
            users_data.append(user_full_data[:-3])
            i += 1
        table_header = [
            'First Name', 'Last Name',
            'Phone No', 'Email ID', 'Date of Birth']
        print(tabulate(users_data, headers=table_header, tablefmt="grid"))
        input("\nThese are all the friend/s you are connected to.\n"
              "Press Enter to continue...")
    return users_ids


def remove_friend():
    """
    This function will give option to the user to remove the friend
    from the friend list of the user.
    """
    friend_sheet = SHEET.worksheet("connections")
    # Getting user id of friends of current user and displaying
    #  list for user to select from.
    users_ids = view_friends()
    if users_ids == []:
        pass
    else:
        while True:
            del_friend = input("Please enter the number infront of name "
                               "to delete the connection or type 'e' to "
                               "exit.\n").strip()
            if del_friend.isdigit() and int(del_friend) <= len(users_ids):
                print("Deleting from friend list...")
                friend_sheet.delete_rows((users_ids[int(del_friend)-1]).row)
                input("Deletion completed.\nPress Enter to continue...")
                break
            elif del_friend == "e":
                input("Redirecting you to previous menu.\n"
                      "Press Enter to continue...")
                break
            else:
                input("Invalid option entered. Please try again.")
                break


def vfr_menu():
    """
    This function display the menu item when user select view
    friend request from login menu.
    """
    while True:
        newscreen()
        print("VIEW FRIEND REQUESTS\n")
        print("1. Accept Incoming Friend Requests")
        print("2. Cancel Outgoing Friend Requests")
        print("3. Main Menu")

        choice = input("\nPlease choose an option by entering "
                       "1, 2 or 3\n").strip()

        if choice == '1':
            afr()
        elif choice == '2':
            cfr()
        elif choice == '3':
            break
        else:
            print("Invalid selection. Please enter 1, 2, or 3\n"
                  "Press Enter to continue...\n")


def afr():
    """
    This function display the list of name of the people who
    have send friend request to the user which has not been
    accept yet. And provide option to accept or ignore them.
    """
    while True:
        user_sheet = SHEET.worksheet("users")
        friend_sheet = SHEET.worksheet("connections")
        friend_requests = friend_sheet.findall(userID)
        afr = []
        # Getting the list of name of people who have send friend request.
        for frs in friend_requests:
            if frs.col == 2:
                if friend_sheet.cell(frs.row, 3).value == "n":
                    afr.append(friend_sheet.cell(frs.row, 1))
        if afr == []:
            input("You don't have any friend request to accept.\n"
                  "Press Enter to continue...")
            break
        else:
            print("You have received the friend request from below people:")
            i = 1
            for frs in afr:
                row = user_sheet.find(frs.value).row
                print(f"{i}. {user_sheet.cell(row, 1).value} "
                      f"{user_sheet.cell(row, 2).value}")
                i += 1
            # Getting confirmation from user either to accept
            # friend request or exit.
            confirm = input("\nPlease enter the number infront of name to "
                            "accept friend request.\nOr type 'n' to "
                            "exit.\n").strip()
            if confirm.isdigit() and len(afr) >= int(confirm):
                friend_sheet.update_cell(afr[int(confirm)-1].row, 3, "y")
                input("Friend request accept.\nPress Enter to continue...")
                break
            elif confirm == "n":
                input("Redirecting you to previous menu.\n"
                      "Press Enter to continuee...")
                break
            else:
                input("Invalid option entered.\nPress Enter to continue...")


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

        choice = input("Please choose an option by entering "
                       "1, 2 or 3\n").strip()

        if choice == '1':
            login()
        elif choice == '2':
            createuser()
        elif choice == '3':
            sys.exit(0)
        else:
            input("Invalid selection. Please enter 1, 2, or 3\n"
                  "Press Enter to continue...\n")


def header():
    """
    This function print the header in the main page to welcome the
    user when user first open the system.
    """
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
          "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    time.sleep(0.2)
    print("@@                                                                 "
          "                                                @@")
    time.sleep(0.2)
    print("@@      @@@@  @@       @@@@@@      @@      @@ @@@@@@@@@ @@@@@@@@@@ "
          "@@        @@      @@@      @@@@@@    @@    @@   @@")
    time.sleep(0.2)
    print("@@     @@     @@         @@        @@@     @@ @@            @@     "
          "@@        @@     @@ @@     @@   @@   @@   @@    @@")
    time.sleep(0.2)
    print("@@   @@       @@         @@        @@ @@   @@ @@            @@     "
          "@@        @@   @@     @@   @@   @@   @@ @@      @@")
    time.sleep(0.2)
    print("@@   @@       @@         @@        @@  @@  @@ @@@@@@        @@     "
          "@@   @@   @@  @@       @@  @@@@@@    @@@@       @@")
    time.sleep(0.2)
    print("@@   @@       @@         @@        @@   @@ @@ @@            @@     "
          "@@  @@@@  @@   @@     @@   @@ @@     @@ @@      @@")
    time.sleep(0.2)
    print("@@     @@     @@         @@        @@     @@@ @@            @@     "
          "@@@@    @@@@     @@ @@     @@   @@   @@   @@    @@")
    time.sleep(0.2)
    print("@@      @@@@  @@@@@@@  @@@@@@      @@      @@ @@@@@@@@@     @@     "
          "@@@      @@@      @@@      @@    @@  @@    @@   @@")
    time.sleep(0.2)
    print("@@                                                                 "
          "                                                @@")
    time.sleep(0.2)
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
          "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")


if __name__ == "__main__":
    main()
