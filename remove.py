import cv2
import numpy as np

# Resizes a image and maintains aspect ratio
def maintain_aspect_ratio_resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    # Grab the image size and initialize dimensions
    dim = None
    (h, w) = image.shape[:2]

    # Return original image if no need to resize
    if width is None and height is None:
        return image

    # We are resizing height if width is none
    if width is None:
        # Calculate the ratio of the height and construct the dimensions
        r = height / float(h)
        dim = (int(w * r), height)
    # We are resizing width if height is none
    else:
        # Calculate the ratio of the 0idth and construct the dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # Return the resized image
    return cv2.resize(image, dim, interpolation=inter)

# Load template, convert to grayscale, perform canny edge detection
template = cv2.imread('data\Azul R2.JPG')
template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
template = cv2.Canny(template, 50, 200)
(tH, tW) = template.shape[:2]
cv2.imshow("template", template)

# Load original image, convert to grayscale
original_image = cv2.imread('data\Azul R2.JPG')
final = original_image.copy()
gray = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
found = None

# Dynamically rescale image for better template matching
for scale in np.linspace(0.2, 1.0, 20)[::-1]:

    # Resize image to scale and keep track of ratio
    resized = maintain_aspect_ratio_resize(gray, width=int(gray.shape[1] * scale))
    r = gray.shape[1] / float(resized.shape[1])

    # Stop if template image size is larger than resized image
    if resized.shape[0] < tH or resized.shape[1] < tW:
        break

    # Detect edges in resized image and apply template matching
    canny = cv2.Canny(resized, 50, 200)
    detected = cv2.matchTemplate(canny, template, cv2.TM_CCOEFF)
    (_, max_val, _, max_loc) = cv2.minMaxLoc(detected)

    # Uncomment this section for visualization
    '''
    clone = np.dstack([canny, canny, canny])
    cv2.rectangle(clone, (max_loc[0], max_loc[1]), (max_loc[0] + tW, max_loc[1] + tH), (0,255,0), 2)
    cv2.imshow('visualize', clone)
    cv2.waitKey(0)
    '''

    # Keep track of correlation value
    # Higher correlation means better match
    if found is None or max_val > found[0]:
        found = (max_val, max_loc, r)

# Compute coordinates of bounding box
(_, max_loc, r) = found
(start_x, start_y) = (int(max_loc[0] * r), int(max_loc[1] * r))
(end_x, end_y) = (int((max_loc[0] + tW) * r), int((max_loc[1] + tH) * r))

# Draw bounding box on ROI to remove
cv2.rectangle(original_image, (start_x, start_y), (end_x, end_y), (0,255,0), 2)
cv2.imshow('detected', original_image)

# Erase unwanted ROI (Fill ROI with white)
cv2.rectangle(final, (start_x, start_y), (end_x, end_y), (255,255,255), -1)
cv2.imshow('final', final)
cv2.waitKey(0)