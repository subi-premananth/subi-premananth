
from googletrans import Translator
import langid
import tkinter as tk
from tkinter import ttk, messagebox
from gtts import gTTS
import io
import pygame
import speech_recognition as sr  # Add this line
import threading  # Required for handling threads

# Global variable for controlling the listening process
listening = False

class LanguageDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Multilanguage Translator(Text-voice, Speech-Text, Auto Deduction, Filtering, Swap)")

        # Initialize language map
        self.language_map = {
            "af": "Afrikaans", "ar": "Arabic", "bg": "Bulgarian", "bn": "Bengali",
            "ca": "Catalan", "cs": "Czech", "cy": "Welsh", "da": "Danish", "de": "German",
            "el": "Greek", "en": "English", "es": "Spanish", "et": "Estonian", "fa": "Persian",
            "fi": "Finnish", "fr": "French", "gu": "Gujarati", "he": "Hebrew", "hi": "Hindi",
            "hr": "Croatian", "hu": "Hungarian", "id": "Indonesian", "it": "Italian", "ja": "Japanese",
            "kn": "Kannada", "ko": "Korean", "lt": "Lithuanian", "lv": "Latvian", "mk": "Macedonian",
            "ml": "Malayalam", "mr": "Marathi", "ne": "Nepali", "nl": "Dutch", "no": "Norwegian",
            "pa": "Punjabi", "pl": "Polish", "pt": "Portuguese", "ro": "Romanian", "ru": "Russian",
            "si": "Sinhala", "sk": "Slovak", "sl": "Slovenian", "so": "Somali", "sq": "Albanian",
            "sr": "Serbian", "sv": "Swedish", "sw": "Swahili", "ta": "Tamil", "te": "Telugu",
            "th": "Thai", "tl": "Tagalog", "tr": "Turkish", "uk": "Ukrainian", "ur": "Urdu",
            "vi": "Vietnamese", "zh-cn": "Chinese (Simplified)", "zh-tw": "Chinese (Traditional)"
        }

        # Create reverse language map: Flip key-value pairs of language_map
        self.reverse_language_map = {v: k for k, v in self.language_map.items()}

        # Heading Label
        self.heading_label = tk.Label(self.root, text="Multilanguage Translator(Text-voice, Speech-Text, Auto Deduction, Filtering, Swap)", font=("Arial", 12, "bold"))
        self.heading_label.grid(row=0, column=0, columnspan=2, pady=10)

        self.detected_language = tk.StringVar()

        # Create frames
        self.frame1 = tk.Frame(self.root)
        self.frame2 = tk.Frame(self.root)
        self.frame3 = tk.Frame(self.root)

        # Grid configuration for all frames (3 rows and 2 columns)
        self.frame1.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        self.frame2.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        self.frame3.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # Configure grid columns so they all have equal weight
        self.root.grid_columnconfigure(0, weight=1, uniform="equal")
        self.root.grid_columnconfigure(1, weight=1, uniform="equal")

        # ComboBoxes
        self.language_combobox = ttk.Combobox(self.root, values=["Auto-Deduct"] + list(self.language_map.values()),
                                              state="normal", width=20)
        self.language_combobox.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        self.language_combobox.set("Auto-Deduct")

        self.language_combobox2 = ttk.Combobox(self.root, values=list(self.language_map.values()), state="normal",
                                               width=20)
        self.language_combobox2.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        self.language_combobox2.set("Select a Translation language")

        # Second row: Text areas
        self.text_area1 = tk.Text(self.frame2, height=10, width=50)
        self.text_area1.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        self.text_area2 = tk.Text(self.frame2, height=10, width=50)
        self.text_area2.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

        # Third row: Buttons (First Column - Left to Right in the same row)
        self.translate_voice_button = tk.Button(self.frame3, text="Translate Voice")
        self.translate_voice_button.grid(row=3, column=0, padx=5, pady=10, sticky="ew", columnspan=1)
        self.translate_voice_button.config(command=self.translate_voice)

        self.listen_input_button = tk.Button(self.frame3, text="Listen Input")
        self.listen_input_button.grid(row=3, column=1, padx=5, pady=10, sticky="ew", columnspan=1)
        self.listen_input_button.config(command=self.listen_input)


        self.clear_button = tk.Button(self.frame3, text="Clear", command=self.clear_text_area)
        self.clear_button.grid(row=3, column=2, padx=5, pady=10, sticky="ew", columnspan=1)
        self.clear_button.config(command=self.clear_text_area)


        self.stop_button = tk.Button(self.frame3, text="Stop")
        self.stop_button.grid(row=3, column=3, padx=5, pady=10, sticky="ew", columnspan=1)
        self.stop_button.config(command=self.stop_voice)


        # Third row: Buttons (Second Column - Left to Right in the same row)
        self.translate_button = tk.Button(self.frame3, text="Translate")
        self.translate_button.grid(row=3, column=15, padx=5, pady=10, sticky="ew", columnspan=1)
        self.translate_button.config(command=self.translate_text)

        self.listen_output_button = tk.Button(self.frame3, text="Listen Output")
        self.listen_output_button.grid(row=3, column=20, padx=5, pady=10, sticky="ew", columnspan=1)
        self.listen_output_button.config(command=self.listen_output)

        self.swap_Button = tk.Button(self.frame3, text="Swap")
        self.swap_Button.grid(row=3, column=25, padx=5, pady=10, sticky="ew", columnspan=1)
        self.swap_Button.config(command=self.swapLanguages)


        # Bind events
        self.text_area1.bind("<KeyRelease>", self.on_text_change)
        self.language_combobox.bind("<<ComboboxSelected>>", self.on_select_language)
        self.language_combobox.bind("<KeyRelease>", self.on_combo_change)
        self.language_combobox2.bind("<<ComboboxSelected>>", self.on_select_language2)
        self.language_combobox2.bind("<KeyRelease>", self.on_combo_change2)


    def detect_language(self, text):
        """Detect the language of the entered text using langid."""
        if not text.strip():
            return None
        lang_code, _ = langid.classify(text)
        return lang_code

    def auto_deduct(self):
        """Automatically detect and update the language in the combo box."""
        entered_text = self.text_area1.get("1.0", "end-1c").strip()
        if not entered_text:
            # Reset to default when no text is entered
            self.language_combobox.set("Select Languages")
            return

        detected_lang_code = self.detect_language(entered_text)
        if detected_lang_code:
            detected_lang_name = self.language_map.get(detected_lang_code, "Unknown Language")
            self.language_combobox.set(f"{detected_lang_name}")
        else:
            self.language_combobox.set("Auto-Deduct")

    def on_text_change(self, event):
        """Trigger Auto-Deduct when the user types in text_area1."""
        self.auto_deduct()

    def on_combo_change(self, event):
        """Filter languages in the first combo box."""
        typed = self.language_combobox.get().lower()
        filtered_languages = [lang for lang in ["Auto-Deduct"] + list(self.language_map.values()) if
                              typed in lang.lower()]
        self.language_combobox['values'] = filtered_languages

    def on_combo_change2(self, event):
        """Filter languages in the second combo box."""
        typed = self.language_combobox2.get().lower()
        filtered_languages = [lang for lang in list(self.language_map.values()) if typed in lang.lower()]
        self.language_combobox2['values'] = filtered_languages

    def on_select_language(self, event):
        """Handle selection in the first combo box."""
        selected_lang = self.language_combobox.get()
        self.detected_language.set(selected_lang)

    def on_select_language2(self, event):
        """Handle selection in the second combo box."""
        selected_lang2 = self.language_combobox2.get()
        print(f"Language selected in ComboBox2: {selected_lang2}")  # Debugging or additional actions.

    def reset_combo_box(self, event):
        """Reset the first combo box."""
        if self.language_combobox.get() == "":
            self.language_combobox['values'] = ["Auto-Deduct"] + list(self.language_map.values())
            #self.language_combobox.set("Auto-Deduct")

    def reset_combo_box2(self, event):
        """Reset the second combo box."""
        if self.language_combobox2.get() == "":
            self.language_combobox2['values'] = list(self.language_map.values())

    def clear_text_area(self):
        self.text_area1.delete("1.0", "end-1c")
        self.text_area2.delete("1.0", "end-1c")
        # Clear text areas but keep the language combo box as is
        #if self.language_combobox.get() != "Auto-Deduct":
         #   self.language_combobox.set("Auto-Deduct")  # Reset combo box to "Auto-Deduct"

    # Function to translate text
    def translate_text(self):
        # Get input text from text area 1
        input_text = self.text_area1.get("1.0", "end-1c")

        # Get selected language code from combobox
        target_language = self.reverse_language_map.get(self.language_combobox2.get(), None)

        if not target_language:
            messagebox.showerror("Error", "Please select a valid target language.")
            return

        # Translate input text
        translator = Translator()
        translated = translator.translate(input_text, dest=target_language)

        # Display translated text in text area 2
        self.text_area2.delete("1.0", "end")  # Clear previous content
        self.text_area2.insert("1.0", translated.text)  # Insert translated text

    def listen_input(self):
        # Get the selected language
        selected_language = self.language_combobox.get()

        # Validate language selection
        if selected_language == "Auto-Deduct" or not selected_language:
            messagebox.showwarning("Warning", "Please select a valid input language.")
            return

        # Map the selected language to its code
        language_code = self.reverse_language_map.get(selected_language)
        if not language_code:
            messagebox.showerror("Error", "Invalid language selected.")
            return

        # Get the text from the Text widget
        text_content = self.text_area1.get("1.0", tk.END).strip()

        # Validate if the text area has content
        if not text_content:
            messagebox.showwarning("Warning", "Text area is empty. Please enter the message first.")
            return

        # Perform text-to-speech
        try:
            # Generate speech with gTTS
            tts = gTTS(text=text_content, lang=language_code)
            audio_data = io.BytesIO()
            tts.write_to_fp(audio_data)
            audio_data.seek(0)

            # Initialize pygame mixer to play audio
            pygame.mixer.init()
            sound = pygame.mixer.Sound(audio_data)
            sound.play()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to convert text to speech: {e}")

    def listen_output(self):
        # Get the selected language
        selected_language = self.language_combobox2.get()

        # Validate language selection
        if selected_language ==  "Auto-Deduct" or not selected_language:
            messagebox.showwarning("Warning", "Please select a valid Output language.")
            return

        # Map the selected language to its code
        language_code = self.reverse_language_map.get(selected_language)
        if not language_code:
            messagebox.showerror("Error", "Invalid language selected.")
            return

        # Get the text from the Text widget
        text_content = self.text_area2.get("1.0", tk.END).strip()

        # Validate if the text area has content
        if not text_content:
            messagebox.showwarning("Warning", "Text area is empty. Please enter the message first.")
            return

        # Perform text-to-speech
        try:
            # Generate speech with gTTS
            tts = gTTS(text=text_content, lang=language_code)
            audio_data = io.BytesIO()
            tts.write_to_fp(audio_data)
            audio_data.seek(0)

            # Initialize pygame mixer to play audio
            pygame.mixer.init()
            sound = pygame.mixer.Sound(audio_data)
            sound.play()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to convert text to speech: {e}")

        # Function to handle the voice recognition process

    def translate_voice(self):
        global listening

        # Check if both languages are selected
        selected_language_1 = self.language_combobox.get()
        selected_language_2 = self.language_combobox2.get()

        # Ensure that both languages are selected and that they are not default values like "Auto-Deduct"
        if not selected_language_1 or not selected_language_2 or \
                selected_language_1 == "Select Language" or selected_language_2 == "Select Language" or \
                selected_language_1 == "Auto-Deduct" or selected_language_2 == "Select a language":
            messagebox.showwarning("Input Error", "Please select both languages")
            return

        # Clear text areas before starting
        self.text_area1.delete(1.0, tk.END)
        self.text_area2.delete(1.0, tk.END)

        # Initialize recognizer class (for recognizing speech)
        recognizer = sr.Recognizer()

        def listen():
            global listening
            with sr.Microphone() as source:
                try:
                    recognizer.adjust_for_ambient_noise(source)
                    self.text_area1.insert(tk.END, "Listening for speech...\n")

                    while listening:
                        try:
                            # Capture the speech from the microphone
                            audio = recognizer.listen(source)
                            if not listening:  # Stop if the listening process was stopped
                                break

                            # Recognize speech using Google Speech Recognition with the selected input language
                            input_language = self.reverse_language_map.get(self.language_combobox.get(),
                                                                           'en')  # Default to English if not found
                            text = recognizer.recognize_google(audio, language=input_language)
                            self.text_area1.delete(1.0, tk.END)
                            self.text_area1.insert(tk.END, text)
                        except sr.UnknownValueError:
                            if listening:  # Only display error messages if still listening
                                self.text_area1.delete(1.0, tk.END)
                                self.text_area1.insert(tk.END, "Could not understand the audio. Please try again.")
                        except sr.RequestError as e:
                            if listening:  # Only display error messages if still listening
                                self.text_area1.delete(1.0, tk.END)
                                self.text_area1.insert(tk.END, f"Speech recognition service error: {e}")
                        except Exception as e:
                            if listening:  # Only display error messages if still listening
                                self.text_area1.delete(1.0, tk.END)
                                self.text_area1.insert(tk.END, f"An unexpected error occurred: {e}")
                except Exception as e:
                    self.text_area1.delete(1.0, tk.END)
                    self.text_area1.insert(tk.END, f"Error initializing microphone: {e}")

        # Start the listening process in a separate thread
        listening = True
        threading.Thread(target=listen, daemon=True).start()

    def stop_voice(self, event=None):
        global listening
        listening = False  # Stop the listening process

        # Get the recognized text from text_area1
        text_to_translate = self.text_area1.get(1.0, tk.END).strip()

        if text_to_translate:
            self.translate_voice_text(text_to_translate)  # Translate the recognized text
        else:
            self.text_area2.insert(tk.END, "No text to translate.")

    def translate_voice_text(self, text_to_translate):
        # Initialize translator class
        translator = Translator()
        try:
            # Perform translation
            src_lang = self.reverse_language_map.get(self.language_combobox.get(), "auto")  # Source language
            dest_lang = self.reverse_language_map.get(self.language_combobox2.get(), "en")  # Destination language
            translated_text = translator.translate(text_to_translate, src=src_lang, dest=dest_lang)

            # Display the translated text in text_area2
            self.text_area2.delete(1.0, tk.END)
            self.text_area2.insert(tk.END, translated_text.text)
        except Exception as e:
            self.text_area2.delete(1.0, tk.END)
            self.text_area2.insert(tk.END, f"Error during translation: {e}")

    def swapLanguages(self):
        # Get the current values of the combo boxes
        source_language = self.language_combobox.get()
        target_language = self.language_combobox2.get()

        # Swap the values
        self.language_combobox.set(target_language)
        self.language_combobox2.set(source_language)


# Create the main window
root = tk.Tk()

# Initialize the application
app = LanguageDetectionApp(root)

# Start the Tkinter event loop
root.mainloop()
