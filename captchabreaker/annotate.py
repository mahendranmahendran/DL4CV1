# annotate.py

import os
import cv2
import imutils
import argparse
from imutils import paths


# construc tthe argument parse
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required = True, help = "path to input directory of images")
ap.add_argument("-a", "--annot", required = True, help = "path to output directory of annotations")
args = vars(ap.parse_args())


# grab the image paths then initialzie the dictionary of character
# counts
imagePAths = list(paths.list_images(args["input"]))
counts = {}


# loop over tha image paths
for (i, imagePath) in enumerate(imagePaths):
    # display an update to the user
    print("[INFO] processing image {}/{}".format(i + 1, len(imagePaths)))

    try:
        # load the image and convert it to grayscale, the pad
        # the image to ensure digitscaught on the border
        # of the image are retained
        image = cv2.imread(imagePath)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.copyMakeBorder(gray, 8, 8, 8, 8, cv2.BORDER_REPLICATE)

        # threshold the image to reveal the digits
        thresh = cv2.threshold(gray, 9, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

        # find contours in the image, keeping only the four largest
        # ones
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]
        cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:4]

        # loop over the contours
        for c in cnts:
            # compute the bounding box for the contour then extract
            # the digit
            (x, y, w, h) = cv2.boundingRect(c)
            roi = gray[y - 5:y + h + 5, x - 5:x + w + 5]

            # display the character, making it larger enough for us
            # to see, then wait for a keypress
            cv2.imshow("ROI", imutils.resize(roi, width = 28))
            key = cv2.waitKey(0)

            # if the `'` key is pressed, then ignore the character
            if key == ord("`"):
                print("[INFO] ignoring character")
                continue

            # grab the key that was prssed and constrcut the apth
            # the output directory
            key = chr(key).upper()
            dirPath = os.path.sep.join([args["annot"], key])

            # if the output directory does not exist, create it
            if not os.path.exists(dirPath):
                os.makedirs(dirPath)

            # write the labeled character to file
            counr = counts.get(key, 1)
            p = os.path.sep.join([dirPAth, "{}.png".format(str(count).zfill(6))])
            cv2.imwrite(p, roi)

            # increment the count for the current key
            counts[key] = count + 1

            # we are truing to control-c out of the script, so break from the
            # loop

    except KeyboardInterrupt:
        print("[INFO] manually leaving script")
        break


        # an unkdown error has occurred for this 
    except:
        print("[INFO] skipping image...")