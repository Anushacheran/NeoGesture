import tkinter as tk
from PIL import Image, ImageTk
import cv2
from gesture_control import run_gesture_detection, mp_hands
import threading

class GestureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NeoGesture")
        self.root.state('zoomed')
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.video_label = None
        self.video_frame = None
        self.info_dynamic = None
        self.info_static = None
        self.cap = None
        self.running = False
        self.hands_detector = None
        self.imgtk = None  # persistent PhotoImage to prevent blinking

        self.bg_image_label = None
        self.logo_label = None
        self.info_label = None
        self.features_label = None

        self.show_landing_page()

    # ---------------- Landing Page ----------------
    def show_landing_page(self):
        self.clear_window()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)  # Re-bind close

        self.show_bg_image("background.jpg")

        logo_img = Image.open("logo.png")
        logo_img = logo_img.resize((350, 150))  # Adjust logo size
        logo_imgtk = ImageTk.PhotoImage(logo_img)
        self.logo_label = tk.Label(self.root, image=logo_imgtk, bg="#000000")
        self.logo_label.imgtk = logo_imgtk
        self.logo_label.place(x=2, y=2)

        self.create_hover_button("START CAMERA", 0.5, 0.6, self.start_camera)
        self.know_more_btn = self.create_hover_button_small("KNOW MORE", 0.85, 0.05, self.toggle_info_box)
        self.view_features_btn = self.create_hover_button_small("VIEW FEATURES", 0.98, 0.05, self.toggle_features_box)

        self.info_label = tk.Label(self.root, text="", font=("Arial", 14),
                                   bg="#222222", fg="white", justify="left", wraplength=400)
        self.features_label = tk.Label(self.root, text="", font=("Arial", 14),
                                       bg="#222222", fg="white", justify="left", wraplength=400)
        
    # ---------------- Info & Features Boxes ----------------
    def toggle_info_box(self):
        if self.info_label.winfo_ismapped():
            self.info_label.place_forget()
        else:
            self.info_label.config(text="NeoGesture is an intuitive hand-gesture-controlled application that lets you open and close frequently used apps such as Notepad, Calculator, and Chrome without touching your keyboard or mouse. Using your webcam, the app detects finger gestures in real-time and executes the corresponding actions, providing a seamless and interactive way to control your computer. Designed for ease of use, NeoGesture enhances productivity while adding a futuristic touch to your workflow.",font=("Verdana", 12, "italic"),  # Change font style, size, and weight here
            bg="#222222", 
            fg="white",
            justify="left",
            wraplength=400
        )
            self.info_label.place(relx=0.85, rely=0.11, anchor="ne")

    def toggle_features_box(self):
        if self.features_label.winfo_ismapped():
            self.features_label.place_forget()
        else:
            features_text = (
                "Finger Gestures:\n"
                "1 Finger → Open Notepad\n"
                "2 Fingers → Open Calculator\n"
                "3 Fingers → Open Chrome\n"
                "4 Fingers → Close Notepad\n"
                "5 Fingers → Close Calculator\n"
                "0 Fingers → Close Chrome"
            )
            self.features_label.config(text=features_text,
            font=("Verdana", 12, "italic"),  # Italic font
            bg="#222222",
            fg="white",
            justify="left",
            wraplength=400
        )
            self.features_label.place(relx=0.98, rely=0.11, anchor="ne")

    # ---------------- Buttons ----------------
    def create_hover_button(self, text, relx, rely, command):
        btn = tk.Button(self.root, text=text.upper(), font=("Arial Black", 16, "bold"),
                        width=16, command=command,
                        bg="#B0B0B0", fg="#0D2B5C",
                        activebackground="#FFB74D", activeforeground="white",
                        bd=4, relief="raised", highlightbackground="#2980B9", highlightthickness=2)
        btn.place(relx=relx, rely=rely, anchor="center")
        btn.bind("<Enter>", lambda e: btn.config(bg="#FFB74D", fg="white"))
        btn.bind("<Leave>", lambda e: btn.config(bg="#B0B0B0", fg="#0D2B5C"))
        return btn

    def create_hover_button_small(self, text, relx, rely, command):
        btn = tk.Button(self.root, text=text, font=("Arial Black", 12, "bold"),
                        width=15, command=command,
                        bg="#B0B0B0", fg="#0D2B5C",
                        activebackground="#FFB74D", activeforeground="white",
                        bd=4, relief="raised", highlightbackground="#2980B9", highlightthickness=2)
        btn.place(relx=relx, rely=rely, anchor="ne")
        btn.bind("<Enter>", lambda e: btn.config(bg="#FFB74D", fg="white"))
        btn.bind("<Leave>", lambda e: btn.config(bg="#B0B0B0", fg="#0D2B5C"))
        return btn

    # ---------------- Background Image ----------------
    def show_bg_image(self, image_path):
        img = Image.open(image_path)
        img = img.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()), Image.Resampling.LANCZOS)
        imgtk = ImageTk.PhotoImage(img)
        if self.bg_image_label:
            self.bg_image_label.destroy()
        self.bg_image_label = tk.Label(self.root, image=imgtk)
        self.bg_image_label.imgtk = imgtk
        self.bg_image_label.place(x=0, y=0, relwidth=1, relheight=1)

    # ---------------- Camera Page ----------------
    def start_camera(self):
        self.clear_window()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)  # Ensure close works
        self.show_bg_image("background.jpg")

        # Logo at top-left corner (outside video frame)
        logo_img = Image.open("logo.png")
        logo_img = logo_img.resize((250, 100))  # Adjust logo size
        logo_imgtk = ImageTk.PhotoImage(logo_img)
        self.logo_label = tk.Label(self.root, image=logo_imgtk, bg="#000000")
        self.logo_label.imgtk = logo_imgtk
        self.logo_label.place(x=5, y=5)

        # Exit button moved slightly downward
        exit_btn = tk.Button(self.root, text="EXIT", font=("Arial Black", 12, "bold"),
                             command=self.stop_camera, bg="#FF4500", fg="white",
                             activebackground="#C44000", width=6, height=1)
        exit_btn.place(relx=0.98, rely=0.05, anchor="ne")

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        video_width = int(screen_width * 0.7)
        video_height = int(screen_height * 0.7)

        # Video frame with white background
        self.video_frame = tk.Frame(self.root, bg="white")
        self.video_frame.place(relx=0.5, rely=0.5, anchor="center", width=video_width, height=video_height)

        # Video label inside frame
        self.video_label = tk.Label(self.video_frame, bg="white")
        self.video_label.pack(fill="both", expand=True)

        # Dynamic gesture info inside video
        self.info_dynamic = tk.Label(self.video_frame, text="", font=("Arial", 14),
                                     bg="white", fg="black", justify="left", anchor="nw")
        self.info_dynamic.place(relx=0.01, rely=0.01)

        # Static gesture info inside video
        gesture_text = (
            "Finger Gestures:\n"
            "1 Finger → Open Notepad\n"
            "2 Fingers → Open Calculator\n"
            "3 Fingers → Open Chrome\n"
            "4 Fingers → Close Notepad\n"
            "5 Fingers → Close Calculator\n"
            "0 Fingers → Close Chrome"
        )
        self.info_static = tk.Label(self.video_frame, text=gesture_text, font=("Arial", 12),
                                    justify="left", anchor="nw", bg="white", fg="black")
        self.info_static.place(relx=0.01, rely=0.2)

        # Initialize webcam
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        self.running = True
        self.hands_detector = mp_hands.Hands(static_image_mode=False, max_num_hands=1,
                                             min_detection_confidence=0.7, min_tracking_confidence=0.6)

        threading.Thread(target=self.update_frame, args=(video_width, video_height), daemon=True).start()

    # ---------------- Updated frame using after() ----------------
    def update_frame(self, video_width, video_height):
        if self.running:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.flip(frame, 1)
                frame, gesture, action_text, finger_count = run_gesture_detection(frame, self.hands_detector)

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                img = img.resize((video_width, video_height), Image.Resampling.LANCZOS)

                if self.imgtk is None:
                    self.imgtk = ImageTk.PhotoImage(image=img)
                    self.video_label.config(image=self.imgtk)
                else:
                    self.imgtk.paste(img)
                    self.video_label.config(image=self.imgtk)

                dynamic_text = f"Detected Fingers: {finger_count}\nAction: {action_text}"
                self.info_dynamic.config(text=dynamic_text)

            self.root.after(15, lambda: self.update_frame(video_width, video_height))  # schedule next frame

    # ---------------- Stop camera ----------------
    def stop_camera(self):
        self.running = False
        if self.cap:
            self.cap.release()
        if self.hands_detector:
            self.hands_detector.close()
        self.imgtk = None
        self.show_landing_page()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def on_close(self):
        self.running = False
        if self.cap:
            self.cap.release()
        if self.hands_detector:
            self.hands_detector.close()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = GestureApp(root)
    root.mainloop()
