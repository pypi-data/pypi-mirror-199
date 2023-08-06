from .errorHandler import bcolors


class RequestError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f"{bcolors.FAIL}{self.message}{bcolors.WHITE}"


class TokenError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f"{bcolors.FAIL}TokenError: {self.message}"


class DataNull(Exception):
    def __str__(self):
        return f"{bcolors.WARNING}No new data found from API request.\n{bcolors.WHITE}"


class NullPages(Exception):
    def __init__(self, column):
        self.column = column

    def __str__(self):
        return f"finishing {self.column} syncronization with no changes committed to corresponding table\n\n{bcolors.WHITE}"


class ConnectionDatabaseError(Exception):
    def __init__(self, array):
        self.array = array

    def print_finalized(self):
        print(f"\n{bcolors.FAIL}Failed to connect to database:\n")

        for error in self.array:
            print(
                f"{bcolors.WARNING}{error['Database_connection_error']}",
                end=f"\nPlease check your database connection parameters\n\n {bcolors.WHITE}",
            )
