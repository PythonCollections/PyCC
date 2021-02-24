import json, tkinter as tk, os
import cv2, imageio
from tkinter import filedialog


def detectfaces(img_path, display=False):
    try:
        if img_path.lower().endswith('jpeg') or img_path.lower().endswith('.jpg') or img_path.lower().endswith('.png'):
            print("Type assertained")
            color_img=cv2.imread(img_path)
        elif img_path.lower().endswith('.gif'):
            color_img=imageio.mimread(img_path)[0]
            color_img=cv2.cvtColor(color_img,cv2.COLOR_BGR2RGB)
    except Exception as e:
        raise e

    #Image Resizingtre
    h = color_img.shape[0]
    w = color_img.shape[1]
    if (w/h) > (1200/720):
        color_img = cv2.resize(color_img,(1200, int(h*1200/w)))
    else:
        color_img = cv2.resize(color_img, (int(w*720/h),720))

    # convert to grayscale images
    gray_img = cv2.cvtColor(color_img, cv2.COLOR_BGR2GRAY).copy()

    # load Haar cascade and detect faces
    cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml')
    faces = cascade.detectMultiScale(gray_img)
    print('Found {0} face{1} in {2}'.format(len(faces), 's' if (len(faces) > 1) else '', os.path.basename(img_path)))

    if display:
        # draw rectangles on faces
        for (x, y, w, h) in faces:
            cv2.rectangle(color_img, (x, y), (x+w, y+h), (0, 255, 0), 3)

        # display image with OpenCV
        cv2.imshow('Facial Detection', color_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return json.dumps({'countFaces': len(faces),
                       'imageLocation': img_path})



def main():
    root = tk.Tk()
    root.withdraw()
    img_path = filedialog.askopenfilename(initialdir= "./photos",
                                          title = "Choose an Image to analyse")
    print(img_path)
    output = detectfaces(img_path,display=True)
    print(output)

if __name__ == "__main__":
    main()