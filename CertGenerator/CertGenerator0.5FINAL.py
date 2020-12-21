import cv2 as cv
import pandas as pd
from PIL import Image
import os

# NO-DATE VERSION #

## ---------- Defining Paths for File Reading and Writing ----------
template_path = 'templateFinal.png'
participants_path = 'ParticipantsOrders3.csv'          #########
dated_template_output_path = 'dated_templates'
png_output_path = 'png_output'
pdf_output_path = 'pdf_output'

# load csv file into a python dataframe
df = pd.read_csv(participants_path)

print(df)                                                                                                               ###

## ---------- Configuring Name & Date Font details ----------
name_colour = (45, 155, 255) #ff9b2d
name_height = 100
name_thickness = -1
name_baseline = 0
if name_thickness > 0 :
    name_baseline += name_thickness

date_colour = (45, 155, 255)
date_height = 80
date_thickness = -1
date_baseline = 0
if date_thickness > 0:
    date_baseline += date_thickness

# create freetype2 obj to define custom font for text
fontFileName = 'GlacialIndifferenceRegular.otf'
ft = cv.freetype.createFreeType2()
ft.loadFontData(fontFileName, 0)


## ---------- Configuring Name & Date Coordinates Relative to Certificate Centre ----------
# coordinate adjustments; offsets printed text away from centre of the cert
# for x coord, +ve is towards rhs; for y coord, +ve is towards top
name_x_coord_adj = 0
name_y_coord_adj = -200
date_x_coord_adj = 0
date_y_coord_adj = -100


## ---------- Helper Function to Calculate Coordinates from Given Text ----------
# helper function to calculate given text's coordinates relative to image centre
# returns tuple of optimised (x,y) coordinates for given text
def getTxtCoords (img, text, xCoordTrim, yCoordTrim):

    # get size of name to be printed:
    # calculates and returns the approximate size of a box that contains the specified text
    txt_size = ft.getTextSize(text, name_height, name_thickness)

    # get the x y coordinates where the name is to be written on the template:
    # we use this to find the centre coords of the page relative to the
    # the method .putText only accepts 'int' arguments
    txt_x = (img.shape[1] - txt_size[0][0]) / 2 + xCoordTrim
    txt_y = (img.shape[0] + txt_size[0][1]) / 2 - yCoordTrim
    txt_x = int(txt_x)
    txt_y = int(txt_y)

    return (txt_x, txt_y)


## ---------- Populating Templates with Name of Participants ----------

img = cv.imread(template_path)

# iterating through each row of dataframe:
for row in df.itertuples():
    row_number = row[0]

    firstName = row[1].strip()
    lastName = row[2].strip()
    fullName = (firstName + " " + lastName)

    if (len(fullName) > 30):
        print ("#### " + fullName + " is too long; trimmed. ####")

    name_txt = fullName[:29] # max character no. = 30

    #name_txt = row[1][:29].strip() # max character no. = 30  # is for old version where full name was provided
    email_address = row[3]

    #dated_img = cv.imread(dated_cert_template_path)
    dated_img = cv.imread(template_path)

    nameCoords = getTxtCoords(dated_img, name_txt, name_x_coord_adj, name_y_coord_adj)

    ft.putText(dated_img,
               name_txt,
               nameCoords,
               name_height,
               name_colour,
               name_thickness,
               cv.LINE_AA,
               True)

    # define output path along with the name of the certificate generated:
    cert_path_png = png_output_path + '/' + email_address + '.png'

    # Save the certificate:
    cv.imwrite(cert_path_png, dated_img)

    # Print visual cue of completed png cert generation
    print(str(row_number) + " " + name_txt + ' png certificate generation complete')

    # Converting image to PDF file & saving
    im = Image.open(cert_path_png)
    if im.mode == "RGBA":
            im = im.convert("RGB")
    cert_path_pdf = pdf_output_path + '/' + email_address + '.pdf'
    #if not os.path.exists(cert_path_pdf):
    #    im.save(cert_path_pdf, "PDF", resolution = 100.0)
    im.save(cert_path_pdf, "PDF", subsampling=0, resolution=100.0)

    # Print visual cue of completed pdf cert generation
    print(str(row_number) + " " + name_txt + ' pdf certificate generation complete')
