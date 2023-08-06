import cv2
import logging
import os

class CaptureFace:
    def __init__(self, save_image : bool = False, image_location : str = 'dataset', 
                haarcascade_frontalface_location : str = './haarcascade_frontalface_default.xml') -> None:
        self.save_image = save_image # if save_image is set to False it will return image bytes 
        self.image_location = image_location # only use when save_image flag is set to True
        self.haarcascade_frontalface_location = haarcascade_frontalface_location # By default it will search on place where you are importing this class
    
    def capture_image(self, user_name)-> bytes:
        logging.info("Initiating camera ----")
        cam = cv2.VideoCapture(0)
        cam.set(3, 640) # set video width
        cam.set(4, 480) # set video height
        logging.info("Camera is initiated ----")
        face_detector = cv2.CascadeClassifier(self.haarcascade_frontalface_location)
        face_id = user_name
        logging.info("Press 'ESC' to terminate capture")
        logging.info("Initializing face capture. Look the camera and wait ...")
        count = 0
        while(count<=1):

            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_detector.detectMultiScale(gray, 1.3, 5)

            for (x,y,w,h) in faces:

                cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)     
                count += 1

                # Save the captured image into the datasets folder
                if self.save_image:
                    logging.warning("Make sure provided path is correct")
                    pathFile = self.image_location + '/' + str(face_id) + ".jpg"
                    logging.warning(pathFile)
                    cv2.imwrite(pathFile, gray[y:y+h,x:x+w])
                    image_bytes  = cv2.imencode('.jpg', gray[y:y+h,x:x+w])[1].tobytes()
                    cam.release()
                    cv2.destroyAllWindows()
                else:
                    image_bytes  = cv2.imencode('.jpg', gray[y:y+h,x:x+w])[1].tobytes()
                    cam.release()
                    cv2.destroyAllWindows()
                return image_bytes

            k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
            if k == 27:
                break

if __name__ == "__main__":
    camera = CaptureFace(save_image=True)
    result = camera.capture_image("TestUser2")
    print(result)