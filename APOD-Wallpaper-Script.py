import nasapy
import os
from datetime import datetime
import urllib.request
from gtts import gTTS
from appscript import app, mactypes
from IPython.display import display, clear_output
from PIL import Image


# API_KEY should be your private Nasa API Key.
API_KEY = "YOUR API KEY"

nasa = nasapy.Nasa(key=API_KEY)
d = datetime.today().strftime("%Y-%m-%d")

apod = nasa.picture_of_the_day(date=d, hd=True)


# Check the media type available:
if apod["media_type"] == "image":

    # Displaying hd images only:
    if "hdurl" in apod.keys():

        # Saving name for image:
        title = d + "_" + apod["title"].replace(" ", "_").replace(":", "_") + ".jpg"

        # Path of the directory:
        image_dir = "/Users/clas0512/Desktop/APOD"

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
        # display(Image(os.path.join(image_dir, title)))
        image = Image.open(os.path.join(image_dir, title))
        display(image)
        os.system("sleep 5")
        clear_output()

        # Setting main image as wallpaper:
        app('Finder').desktop_picture.set(mactypes.File(file_path))

# If media type is not image:
else:
    exit
