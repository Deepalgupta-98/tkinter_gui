import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
import subprocess
import pyttsx3
import pywhatkit
import boto3
import os
from googlesearch import search
from geopy.geocoders import Nominatim
import speech_recognition as sr
from twilio.rest import Client
import cv2
import numpy as np



def get_coordinates():
    # Create a new Tkinter window for input dialog
    input_window = tk.Toplevel()
    input_window.title("Enter City")

    # Create a label and an entry widget for city input
    label = tk.Label(input_window, text="Enter city:")
    label.pack()

    city_entry = tk.Entry(input_window)
    city_entry.pack()

    def on_ok():
        city = city_entry.get()
        if city:
            geolocator = Nominatim(user_agent="my")
            location = geolocator.geocode(city)
            if location:
                # Create a new Tkinter window for displaying coordinates
                result_window = tk.Toplevel()
                result_window.title("Coordinates")

                # Display the coordinates
                coordinates_label = tk.Label(result_window, text=f"Coordinates for {city}:")
                coordinates_label.pack()

                latitude_label = tk.Label(result_window, text=f"Latitude: {location.latitude}")
                latitude_label.pack()

                longitude_label = tk.Label(result_window, text=f"Longitude: {location.longitude}")
                longitude_label.pack()
            else:
                tk.messagebox.showerror("Error", f"Could not find coordinates for {city}")
        else:
            tk.messagebox.showwarning("Warning", "Please enter a city name.")

        input_window.destroy()  # Close the input dialog

    def on_cancel():
        input_window.destroy()  # Close the input dialog

    # Create OK and Cancel buttons
    ok_button = tk.Button(input_window, text="OK", command=on_ok)
    cancel_button = tk.Button(input_window, text="Cancel", command=on_cancel)

    ok_button.pack()
    cancel_button.pack()




def open_notepad():
    os.system("notepad")
    
def open_chrome():
    os.system("chrome")
    
def open_calculator():
    subprocess.Popen(['calc.exe'])
    
def sms():
    account_sid = 'accnt sid'
    auth_token = 'auth token'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_='virtual no',
        to= ' recipent phoneno '
        body="msg "
    )

    
def image():
    image = np.zeros((300,300,3), np.uint8)
    image[:222] = (123,245,255)     #yellow color
    image[123:220] = (234,193,123) #skyblue color
    image[220:300] = (123,245,250)  #yellow color
    image[:,100:200] = (0,56,122)  #brown color  
    cv2.imwrite('image.jpg',image)  #filename , varname
    cv2.imshow('hi',image)
    cv2.waitKey()
    cv2.destroyAllWindows()

   
    
def google_search():
    # Create a new tkinter window
    search_window = tk.Toplevel()
    search_window.title("Google Search")
    
    # Use speech recognition to get user's search query
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        # Initialize the text-to-speech engine
         engine = pyttsx3.init()
        engine.say("Please say your search query.")
        engine.runAndWait()
        print("Listening...")
        audio = recognizer.listen(source)
        
    try:
        search_query = recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        search_query = None
    
    if search_query:
        # Perform the Google search
        search_results = list(search(search_query, num_results=10))
        
        # Create a text widget to display the search results
        text_widget = tk.Text(search_window)
        text_widget.pack()
        
        # Insert the search results into the text widget
        for index, result in enumerate(search_results, start=1):
            text_widget.insert(tk.END, f"{index}. {result}\n")
        
        # Disable text widget editing
        text_widget.config(state=tk.DISABLED)
        engine.say("Here are the search results for your query.")
    else:
        engine.say("I couldn't understand your query. Please try again.")
    
    engine.runAndWait()


    
    
def create_bucket():
    bucket = boto3.client('s3')

    bucket.create_bucket(
    Bucket='bucket name',
    ACL='private',
    CreateBucketConfiguration={'LocationConstraint': 'regionname'})

def ec2_instance():
    launch = boto3.client('ec2')
    launch.run_instances(ImageId="ami-id",
                
                    InstanceType="t2.micro",
                    MaxCount=1,
                    MinCount=1)
    print("launched instance")



def open_whatsapp():
    def send_message():
        phone_number = phone_entry.get()
        message = message_entry.get()

        if phone_number and message:
            try:
                pywhatkit.sendwhatmsg_instantly(phone_number, message)
                messagebox.showinfo("Success", "Message sent successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to send message: {str(e)}")
        else:
            messagebox.showwarning("Warning", "Please enter both phone number and message.")
        
        input_window.destroy()

    def cancel_message():
        input_window.destroy()

    # Create a new Tkinter window for input dialog
    input_window = tk.Toplevel()
    input_window.title("WhatsApp Message")

    # Create labels and entry widgets for phone number and message
    phone_label = tk.Label(input_window, text="Phone Number:")
    phone_label.pack()

    phone_entry = tk.Entry(input_window)
    phone_entry.pack()

    message_label = tk.Label(input_window, text="Message:")
    message_label.pack()

    message_entry = tk.Entry(input_window)
    message_entry.pack()

    # Create OK and Cancel buttons
    ok_button = tk.Button(input_window, text="OK", command=send_message)
    cancel_button = tk.Button(input_window, text="Cancel", command=cancel_message)

    ok_button.pack()
    cancel_button.pack()


    
def cropped_gray_photo():
    
    def crop_image(input_path, output_path, left, top, right, bottom):
        im = Image.open(input_path)
        cropped_image = im.crop((left, top, right, bottom))
        cropped_image.save(output_path)
    
    def convert_to_grayscale(input_path, output_path):
        image = Image.open(input_path)
        gray_image = image.convert("L")
        gray_image.save(output_path)
    
    cap = cv2.VideoCapture(0)
    status, photo = cap.read()
    cv2.imwrite("k.jpg", photo)


    crop_coordinates = (200, 200, 500, 400)

    crop_image("k.jpg", "k_cropped.jpg", *crop_coordinates)

    convert_to_grayscale("k_cropped.jpg", "k_cropped_gray.jpg")

    cropped_image = cv2.imread("k_cropped_gray.jpg")
    cv2.imshow("Cropped and Grayscale Image", cropped_image)
    cv2.waitKey()
    cv2.destroyAllWindows()
    
    
def video():
    cap = cv2.VideoCapture(0)

    while True:
        status, photo = cap.read()
        photo[0:200, 0:200] = photo[200:400, 100:300]
        cv2.imshow("my", photo)
        if cv2.waitKey(10)==13:
            break
    
    cv2.destroyAllWindows()
    
    
def camera():
    cap = cv2.VideoCapture(0)  # Open the camera (camera index 0)
    cap
    status, pic = cap.read()
    status
    cv2.imshow("my window", pic)
    cv2.waitKey(8000)
    cv2.destroyAllWindows()
    
def txt_speech():
    def speak():
        text = entry.get()
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
        subwindow.destroy()

    def cancel():
        subwindow.destroy()

    subwindow = tk.Toplevel(top)
    subwindow.title("Text to Speech")
   # subwindow.geometry("400x1")
    subwindow['bg'] = 'black'

    label = tk.Label(subwindow, text="Enter text to speak:", font=("Times New Romen", 10))
    label.pack(pady=10)

    entry = tk.Entry(subwindow, font=("Times New Romen", 12))
    entry.pack(padx=20, pady=5)

    speak_button = tk.Button(subwindow, text="Speak", command=speak)
    speak_button.pack(pady=10)

    cancel_button = tk.Button(subwindow, text="Cancel", command=cancel)
    cancel_button.pack()

    
def showinfo():
    top.destroy()
    messagebox.showinfo("exit tkinter", "window is closed")
    
top = tk.Tk()    #This line creates a new Tk instance, which represents the main window of the GUI application.
#top.geometry("110x123")
top['bg'] = 'green'




notepad_button = tk.Button(top, text="open notepad", command=open_notepad)
notepad_button.grid(row=2, column=1, padx=15, pady=15)


calculator_button = tk.Button(top, text="Open Calculator", command=open_calculator)
calculator_button.grid(row=3, column=1, padx=15, pady=15)

chrome_button = tk.Button(top, text="Open Chrome", command=open_chrome)
chrome_button.grid(row=4, column=1, padx=15, pady=15)

sms_button = tk.Button(top  ,text ='sms', command = sms )
sms_button.grid(row=2, column=2, padx=15, pady=15)

camera_button = tk.Button(top  ,text ='camera', command =camera)
camera_button.grid(row=3, column=2, padx=8, pady=9)

whatsapp_button = tk.Button(top, text="Open whatsapp", command=open_whatsapp)
whatsapp_button.grid(row=4, column=2, padx=15, pady=15)


video_button = tk.Button(top, text="b&w_photo", command=cropped_gray_photo)
video_button.grid(row=2, column=3, padx=15, pady=15)


video_button = tk.Button(top, text="live video", command=video)
video_button.grid(row=3, column=3, padx=15, pady=15)


ec2_button = tk.Button(top, text="Launch instance", command=ec2_instance)
ec2_button.grid(row=4, column=3, padx=15, pady=15) 


bucket_button = tk.Button(top, text="Create Bucket", command=create_bucket)
bucket_button.grid(row=2, column=4, padx=15, pady=15)


image_button = tk.Button(top, text="image", command=image)
image_button.grid(row=3, column=4, padx=15, pady=15)

google_search_button = tk.Button(top, text="Google Search (Voice)", command=google_search)
google_search_button.grid(row=4, column=4,  padx=15, pady=15)

get_coordinates_button = tk.Button(top, text="coordinates", command=get_coordinates)
get_coordinates_button.grid(row=5, column=1, padx=15, pady=15)

speak_button = tk.Button(top, text="Text to Speech", command=txt_speech)
speak_button.grid(row=5, column=2, padx=15, pady=15)


exit_button = tk.Button(top, text="exit", command=showinfo)
exit_button.grid(row=5, column=3, padx=15, pady=15)


top.mainloop()   #Finally, we start the event loop with mainloop().
                # This line starts the main event loop of the application, which listens for user interactions & keep GUI responsive
code explaination:
Importing the library : we import a necessaries library for performing the various tasks function like for aws operation import a boto3 for sending an WhatsApp message (pywhatkit) for text_to_speech(pyttsx3) and many more.

def get_coordinates():
    # Create a new Tkinter window for input dialog
    input_window = tk.Toplevel()
    input_window.title("Enter City")
# Create a label and an entry widget for city input
    label = tk.Label(input_window, text="Enter city:")
    label.pack()

    city_entry = tk.Entry(input_window)
    city_entry.pack()
