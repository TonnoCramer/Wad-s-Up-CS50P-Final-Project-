""" This python module assists tourists in choosing the best Dutch Wadden island for them."""
import random
import sys
import time
import webbrowser
from pytube import YouTube

import cowsay
import pandas as pd
import colorama
from colorama import Fore

colorama.init(autoreset=True)


def main():
    """Main doesn't need a docstring."""

    # Get user input if tourist wants to visit a Dutch Wadden island
    answer = input("Do you want to visit a Dutch Wadden island? (yes/no): ")

    # Get user name
    name = input("what is your name: ")

    # Capitalize first letter of the name
    name = name.capitalize()

    # Call and print "check" that checks if a user wants to go to a Dutch Wadden island
    print(check(answer, name))

    # Call "preferences" that calculates the likert-scale
    # pylint: disable = no-value-for-parameter # Disables the pylint check for next line
    islands = preferences(
        *user_input()
    )  # "*" unpacks tuple for 3 arguments during function call

    # Call "determine_winner" that determines the winner and assign it to "wnnr"
    wnnr = determine_winner(islands)

    # Call "stats" that converts dictionary in pandas dataframe.
    # and unpacks de datafram, mean and median.
    pd_df_islands, mean, median = stats(islands)
    print("\n", pd_df_islands)
    print("\nMean is: ", mean)
    print("Median is: ", median)

    # Call "your_destiny" that prints winning island
    your_destiny(name, wnnr)

    # Let the user know that a youtube movie will be started
    print("\nA youtube movie about your favorite island follows in a few seconds")

    # Call "countdown" that counts down to zero
    countdown(3)

    # Call "youtube" that plays video of the winning island
    youtube(wnnr)


def check(answer, name):
    """Function checks if the user is interested
    in visiting a Dutch Wadden islands
    """

    if answer.lower() in ["y", "yes"]:
        return (
            "\nYour on the right site "
            + name
            + "!"
            + "\nWadsup helps you to decide which Dutch Wadden "
            "island is your island.\nwadsup uses CS50 (common sense 50 \U0001F609) to "
            "detect your destination."
        )

    # Refers to alternative website if the user doesn't want
    # to go to a Dutch Wadden Island after all and ends program.
    if answer.lower() in ["n", "no"]:
        sys.exit(
            name
            + "perhaps you can gain ideas for a vacation on this site:"
            + "https://www.theatlantic.com/ideas/archive/2023/08/vacation-personality-"
            "happiness-travel-relax/675187/"
        )
    # After multiple invalid user inputs say bye, bye to the user and end program
    else:
        # ask again
        again = input("Please a 'yes' or a 'no': ")
        # if yes or no
        if again.lower() in ["y", "yes", "n", "no"]:
            return check(again, name)
        # else exit program
        sys.exit("bye, bye")


def user_input():
    """Function collects user input regarding their preferences"""

    # List with valid userinput
    lis = ["1", "2", "3", "4", "5"]
    # Create empty list to store user input
    inpt = []

    print("Please answer the following questions to find your Dutch Wadden Island\n")
    # While True loop to get valid userinput (prompts user again by invalid user input)
    while True:
        # First characteristic (car free)
        print(
            "How important is it to you to go to an island where there are no cars allowed?\n"
            "1- Not at all important\n2- Slightly important\n"
            + "3- Moderately important\n4- Important \n5- Extremely important"
        )

        no_cars = input("Your choice please:")

        if no_cars not in lis:
            print("Not an appropriate choice.")
        else:
            inpt.append(no_cars)
            break
    # While True loop to get valid userinput (prompts user again by invalid user input)
    while True:
        # Second characteristic (transportation costs from mainland to island)
        print(
            "\nTo visit an island you have to use a ferry. The prices vary from $5 to $32 for a "
            "return ticket. How important is the price for a ferry?\n1- Not at all important\n"
            "2- Slightly important\n3- Moderately important\n4- Important \n5- Extremely important"
        )

        ferry = input("Your choice please:")

        if ferry not in lis:
            print("Not an appropriate choice.")
        else:
            inpt.append(ferry)
            break

    # While True loop to get valid userinput (prompts user again by invalid user input)
    while True:
        # Third characteristic (cycle network's total length on an island)
        print(
            "\nThe length of the bicycle network differs considerably per island."
            " How important is the total lenght of the cycle network on an island?\n"
            "1- Not at all important\n2- Slightly important\n"
            "3- Moderately important\n4- Important \n5- Extremely important"
        )

        cycle_network = input("Your choice please:")
        # Feed back for user that input is not correct
        if cycle_network not in lis:
            print("Not an appropriate choice.")
        else:
            inpt.append(cycle_network)
            break

    return inpt


def preferences(no_cars, ferry, cycle_network):
    """Function calculates the score on a Likert scale and updates dictionary."""

    # Dictionary of the 5 Dutch Wadden islands
    islands = {
        "Texel": 0,
        "Vlieland": 0,
        "Terschelling": 0,
        "Ameland": 0,
        "Schiermonnikoog": 0,
    }

    # Scoring first characteristic (car free)
    match no_cars:
        case "1":
            pass
        case "2":
            islands["Vlieland"] = +3
            islands["Schiermonnikoog"] += 3
        case "3":
            islands["Vlieland"] = +6
            islands["Schiermonnikoog"] += 6
        case "4":
            islands["Vlieland"] += 9
            islands["Schiermonnikoog"] += 9
        case "5":
            islands["Vlieland"] += 12
            islands["Schiermonnikoog"] += 12

    # Scoring second characteristic (ferry)
    match ferry:
        case "1":
            pass
        case "2":
            islands["Texel"] += 5
            islands["Ameland"] += 4
            islands["Schiermonnikoog"] += 4
            islands["Terschelling"] += 3
            islands["Vlieland"] += 3
        case "3":
            islands["Texel"] += 8
            islands["Ameland"] += 6
            islands["Schiermonnikoog"] += 6
            islands["Terschelling"] += 4
            islands["Vlieland"] += 4
        case "4":
            islands["Texel"] += 10
            islands["Ameland"] += 8
            islands["Schiermonnikoog"] += 8
            islands["Terschelling"] += 6
            islands["Vlieland"] += 6
        case "5":
            islands["Texel"] += 12
            islands["Ameland"] += 10
            islands["Schiermonnikoog"] += 10
            islands["Terschelling"] += 8
            islands["Vlieland"] += 8

    # Scoring third characteristic(length cycle network)
    match cycle_network:
        case "1":
            pass
        case "2":
            islands["Texel"] += 4
            islands["Ameland"] += 4
            islands["Terschelling"] += 3
        case "3":
            islands["Texel"] += 6
            islands["Ameland"] += 4
            islands["Terschelling"] += 2

        case "4":
            islands["Texel"] += 10
            islands["Ameland"] += 6
            islands["Terschelling"] += 4

        case "5":
            islands["Texel"] += 12
            islands["Ameland"] += 8
            islands["Terschelling"] += 6
    return islands


def determine_winner(islands):
    """Function determines winner. If multiple winners one island will be chosen at random"""
    max_island = islands[max(islands, key=islands.get)]
    max_islands = []
    for island in islands:
        if islands[island] == max_island:
            max_islands.append(island)
        else:
            pass
    winner = random.choice(max_islands)
    return winner


def stats(islands):
    """Function converts dictionary in pandas DataFrame and calculates mean and median."""
    pd_df_islands = pd.DataFrame.from_dict(islands, orient="index", columns=["Score"])

    mean = pd_df_islands.mean().item()
    median = pd_df_islands.median().item()

    return pd_df_islands, mean, median


def your_destiny(name, island):
    """function returns adviced island to user"""
    # pylint: disable=E1101
    if island not in [
        "Texel",
        "Vlieland",
        "Terschelling",
        "Ameland",
        "Schiermonnikoog",
    ]:
        sys.exit("This is not a Dutch Wadden island")

    name = name.capitalize()
    # Using cowsay for a bit of ascii art
    message = cowsay.tux(
        Fore.GREEN + name + "\n" + Fore.GREEN + island + " is your destiny! "
    )

    return message


def countdown(t):
    """Function counts down to zero after which the YouTube video
    about winning island is started.
    """
    while t > 0:
        # t counts down
        t -= 1
        time.sleep(1)
    # no return needed because Python implicit returns "None"


def youtube(island_url):
    """Function starts video of winning island."""
    match island_url:
        case "Ameland":
            video_url = "https://www.youtube.com/watch?v=pFNXMB2Z1S4"
        case "Schiermonnikoog":
            video_url = "https://www.youtube.com/watch?v=PwtbXzZMPhs"
        case "Terschelling":
            video_url = "https://www.youtube.com/watch?v=NMK2MuoOlNo"
        case "Texel":
            video_url = "https://www.youtube.com/watch?v=d7_ieUlPu_Y"
        case "Vlieland":
            video_url = "https://www.youtube.com/watch?v=v6wjltI4UYo"
        case _:
            sys.exit("This is not a Dutch Wadden Island")

    # Create a YouTube object
    yt = YouTube(video_url)

    # Get thumbnail URL
    thumbnail_url = yt.thumbnail_url

    # Open the video in a web browser
    webbrowser.open(video_url)

    return ("Thumbnail URL:", thumbnail_url)


if __name__ == "__main__":
    main()
