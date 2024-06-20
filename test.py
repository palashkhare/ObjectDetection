# Program To Read video 
# and Extract Frames 
  
import cv2
from PIL import Image

from yoloV8.annotation.predict import YoloObjectDetection


model = YoloObjectDetection()

# Function to extract frames
def FrameCapture(path):
    # Path to video file
    vidObj = cv2.VideoCapture(path)
    video = cv2.VideoWriter("/home/kanika/workspace/ObjectDetection/out.avi", 0, 1, (640,360))


    # Used as counter variable
    count = 0

    # checks whether frames were extracted 
    success = 1

    while success:
        # vidObj object calls read
        # function extract frames
        success, image = vidObj.read()
        print("===> ", count)
        # Saves the frames with frame-count
        data, img = model.predict(image=image, return_image=True)
        #img = Image.fromarray(img).save("/home/kanika/workspace/ObjectDetection/plugins/temp/frame%d.jpg" % count)
        #cv2.imwrite("/home/kanika/workspace/ObjectDetection/plugins/temp/frame%d.jpg" % count, img) 
        video.write(img)
        count += 1
    video.release()
  
# Driver Code 
if __name__ == '__main__': 
  
    # Calling the function 
    FrameCapture("/home/kanika/workspace/ObjectDetection/plugins/4236790-sd_640_360_25fps.mp4") 