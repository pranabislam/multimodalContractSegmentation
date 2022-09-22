import cv2
import math
from pdf2image import convert_from_path
import numpy as np

# Following tutorial here: https://stackoverflow.com/a/57044083

# There are other model options we can try out. Download east from here: 
# https://www.dropbox.com/s/r2ingd0l3zt8hxs/frozen_east_text_detection.tar.gz?dl=1
net = cv2.dnn.readNet("../../frozen_east_text_detection.pb")
image_name = "SAMPLE_IMAGES_CybergyHoldings_AffiliateAgreement/pg2.jpg"
frame = cv2.imread(image_name, 0)

# Open a sample of the image. Press any key to close
cv2.imshow('image', frame)
cv2.waitKey(0)
cv2.destroyAllWindows()

inpWidth = inpHeight = 320  # A default dimension
# Preparing a blob to pass the image through the neural network
# Subtracting mean values used while training the model.
image_blob = cv2.dnn.blobFromImage(frame, 1.0, (inpWidth, inpHeight), (123.68, 116.78, 103.94), True, False)

# Change number of input channels to 1 for grayscale input
# (currently throws error expecting colored image)
output_layer = []
output_layer.append("feature_fusion/Conv_7/Sigmoid")
output_layer.append("feature_fusion/concat_3")

net.setInput(image_blob)
output = net.forward(output_layer)
scores = output[0]
geometry = output[1]

confThreshold = 0.5
nmsThreshold = 0.3
[boxes, confidences] = cv2.dnn.NMSBoxes(scores, geometry, confThreshold)
indices = cv2.dnn.NMSBoxesRotated(boxes, confidences, confThreshold, nmsThreshold)
