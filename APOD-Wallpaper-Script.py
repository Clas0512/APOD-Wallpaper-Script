import nasapy
import os
from datetime import datetime
import urllib.request
from appscript import app, mactypes
from PIL import Image


# This function retrieves andvalidates a date input from the user.
def get_date():
    while True:
        day = input("Enter the day: ")
        month = input("Enter the month: ")
        year = input("Enter the year: ")
        
        if not day.isdigit() or not month.isdigit() or not year.isdigit():
            print("Invalid input. Day, month, and year must be numeric values.")
            continue
        year = int(year)
        day = day.zfill(2)
        month = month.zfill(2)
        day = int(day)
        month = int(month)
        
        if not (1 <= day <= 31) or not (1 <= month <= 12):
            print("Invalid date. Please enter valid day, month, and year.")
            continue
        
        return day, month, year

# API_KEY should be your private Nasa API Key.
API_KEY = "YOUR_API_KEY"

nasa = nasapy.Nasa(key=API_KEY)

#This loop prompts the user to choose between "Today" or "Another specific day".
while True:
    choose = input("Today or another specific day?\n(t/s): ")
    choose = choose.lower()

    if choose == "t":
        d = datetime.today().strftime("%Y-%m-%d")
        break
    elif choose == "s":
        day, month, year = get_date()
        d = f"{year}-{month}-{day}"
        break
    else:
        print("Invalid input. Please enter 't' for today or 's' for a specific day.")

apod = nasa.picture_of_the_day(date=d, hd=True)


# Check the media type available:
if apod["media_type"] == "image":

    # Displaying hd images only:
    if "hdurl" in apod.keys():

        # Saving name for image:
        title = d + "_" + apod["title"].replace(" ", "_").replace(":", "_") + ".jpg"

        # Path of the directory:
        desktop_path = os.path.expanduser("~/Desktop")
        image_dir = desktop_path + "/APOD"

        # Path of the image:
        file_path = image_dir + "/" + title

        # Checking if the directory already exists?
        dir_res = os.path.exists(image_dir)

        # If it doesn't exist then make a new directory:
        if dir_res == False:
            os.makedirs(image_dir)

        # --------------------------(OPTIONAL)-------------------------- #
        # If it exist then print a statement:
        # else:
            # print("Directory already exists!\n")
        # -------------------------------------------------------------- #

        # Retrieving the image:
        urllib.request.urlretrieve(
            url=apod["hdurl"], filename=os.path.join(image_dir, title)
        )


        # -------------------------------------------------------------- #
        # --------------------------(OPTIONAL)-------------------------- #
        # -------------------------------------------------------------- #
        # Displaying information related to image:

        # if "date" in apod.keys():
        #     print("Date image released: ", apod["date"])
        #     print("\n")
        # if "copyright" in apod.keys():
        #     print("This image is owned by: ", apod["copyright"])
        #     print("\n")
        # if "title" in apod.keys():
        #     print("Title of the image: ", apod["title"])
        #     print("\n")
        # if "explanation" in apod.keys():
        #     print("Description for the image: ", apod["explanation"])
        #     print("\n")
        # if "hdurl" in apod.keys():
        #     print("URL for this image: ", apod["hdurl"])
        #     print("\n")
        # -------------------------------------------------------------- #
        # -------------------------------------------------------------- #
        # -------------------------------------------------------------- #


        # Displaying main image:
        image = Image.open(os.path.join(image_dir, title))
        image.show()

        choose = input("Do you like it?? If you want to set as wallpaper\n(y/n):")
        if choose == 'y' or choose == 'Y':
            app('Finder').desktop_picture.set(mactypes.File(file_path))
            exit
        elif choose == 'n' or choose == 'N':
            print("Astronomy Picture of the Day saved. \nExiting...")
            exit
        else :
            print("Otomatic setted.\nExiting...")
            app('Finder').desktop_picture.set(mactypes.File(file_path))
            exit
        # Setting main image as wallpaper:

# If media type is not image:
else:
    print("Media type is not image. So it cannot be wallpaper.\nExiting...")
    exit
