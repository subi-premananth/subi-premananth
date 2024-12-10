from playsound import playsound
import os  # You only need to import it once
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import threading
import speech_recognition as sr
from googletrans import Translator
import pyttsx3
from gtts import gTTS

class MultiLanguageTranslator:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi-Language Text-Voice-Speech Translator")
        self.root.geometry("1000x600")



        # Custom languages list
        self.languages = {
            "Afrikaans": "af", "Albanian": "sq", "Arabic": "ar", "Armenian": "hy",
            "Basque": "eu", "Belarusian": "be", "Bengali": "bn", "Bosnian": "bs",
            "Bulgarian": "bg", "Catalan": "ca", "Chinese (Simplified)": "zh-cn",
            "Chinese (Traditional)": "zh-tw", "Croatian": "hr", "Czech": "cs",
            "Danish": "da", "Dutch": "nl", "English": "en", "Estonian": "et",
            "Finnish": "fi", "French": "fr", "Georgian": "ka", "German": "de",
            "Greek": "el", "Gujarati": "gu", "Haitian Creole": "ht", "Hebrew": "he",
            "Hindi": "hi", "Hungarian": "hu", "Icelandic": "is", "Indonesian": "id",
            "Irish": "ga", "Italian": "it", "Japanese": "ja", "Kannada": "kn",
            "Kazakh": "kk", "Khmer": "km", "Korean": "ko", "Latvian": "lv",
            "Lithuanian": "lt", "Macedonian": "mk", "Malay": "ms", "Malayalam": "ml",
            "Marathi": "mr", "Mongolian": "mn", "Nepali": "ne", "Norwegian": "no",
            "Persian": "fa", "Polish": "pl", "Portuguese": "pt", "Punjabi": "pa",
            "Romanian": "ro", "Russian": "ru", "Serbian": "sr", "Sinhalese": "si",
            "Slovak": "sk", "Slovenian": "sl", "Spanish": "es", "Swahili": "sw",
            "Swedish": "sv", "Tamil": "ta", "Telugu": "te", "Thai": "th",
            "Turkish": "tr", "Ukrainian": "uk", "Urdu": "ur", "Vietnamese": "vi",
            "Welsh": "cy", "Yiddish": "yi"
        }

        # Configure rows and columns
        # Make rows and columns stretchable
        self.root.grid_rowconfigure(1, weight=1)  # Row 1
        self.root.grid_rowconfigure(2, weight=1)  # Row 2
        self.root.grid_rowconfigure(3, weight=1)  # Row 3
        self.root.grid_columnconfigure(0, weight=1)  # Column 0
        self.root.grid_columnconfigure(1, weight=1)  # Column 1

        # Create layout components
        self.create_widgets()

        # Flag to track if translation is allowed after stopping
        self.can_translate = False

    def create_widgets(self):

        # Heading label at the top
        self.heading_label = tk.Label(self.root, text="Multi Language Text-Voice-Speech Translator",
                                      font=("Helvetica", 16, "bold"), fg='blue')
        self.heading_label.grid(row=0, column=0, columnspan=2, padx=2, pady=10, sticky="nsew")

        # Row 1: Combo boxes
        self.combo_from = ttk.Combobox(self.root, font=("Helvetica", 12, "bold"))
        self.combo_from["values"] = self.languages
        self.combo_from.set("Translate From")
        self.combo_from.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        self.combo_from.bind("<KeyRelease>", self.filter_languages_from)
        self.combo_from.bind("<FocusIn>", self.show_all_languages_from)

        self.combo_to = ttk.Combobox(self.root, font=("Helvetica", 12, "bold"))
        self.combo_to["values"] = self.languages
        self.combo_to.set("Translate To")
        self.combo_to.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        self.combo_to.bind("<KeyRelease>", self.filter_languages_to)
        self.combo_to.bind("<FocusIn>", self.show_all_languages_to)

        # Row 2: Text areas
        self.text_input = tk.Text(self.root, font=("Helvetica", 12, "bold"), wrap="word", height=10)
        self.text_input.insert("1.0", "Enter Text")
        self.text_input.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.text_input.bind("<KeyPress>", self.enable_translate_button)

        self.text_output = tk.Text(self.root, font=("Helvetica", 12, "bold"), wrap="word", height=10, state=tk.DISABLED)
        self.text_output.insert("1.0", "Translation")
        self.text_output.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

        # Row 3: Buttons
        self.button_frame_left = tk.Frame(self.root)
        self.button_frame_left.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

        self.button_translate_voice = self.create_button(self.button_frame_left, "🎤 Translate Voice", self.translate_voice)
        self.button_listen_input = self.create_button(self.button_frame_left, "🔊 Listen Input", self.listen_input)
        self.button_clear = self.create_button(self.button_frame_left, "🗑️ Clear", self.clear_text)
        self.button_stop = self.create_button(self.button_frame_left, "🛑 Stop", self.stop_translation, state=tk.DISABLED)
        self.button_translate = self.create_button(self.button_frame_left, "🌐 Translate", self.translate, state=tk.DISABLED)

        self.button_frame_right = tk.Frame(self.root)
        self.button_frame_right.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")
        self.button_listen_output = self.create_button(self.button_frame_right, "🔊 Listen Output", self.listen_output)

    def create_button(self, parent, text, command, state=tk.NORMAL):
        """Helper method to create a button."""
        btn = tk.Button(parent, text=text, font=("Helvetica", 9, "bold"), command=command, padx=5, pady=5, state=state)
        btn.pack(side=tk.LEFT, expand=True, fill="x", padx=2)
        return btn

    def enable_buttons(self, enable=True):
        """Enable or disable all buttons except 'Stop'."""
        state = tk.NORMAL if enable else tk.DISABLED
        self.button_translate_voice.config(state=state)
        self.button_listen_input.config(state=state)
        self.button_clear.config(state=state)
        self.button_translate.config(state=state)
        self.button_listen_output.config(state=state)

    def enable_translate_button(self, event):
        """Enable the 'Translate' button as soon as the user starts typing in the input field."""
        if not self.can_translate:  # Enable translate only if voice input has been stopped
            self.button_translate.config(state=tk.NORMAL)

    def translate_voice(self):
        """Handle Translate Voice button press."""
        if self.combo_from.get() == "Translate From" or self.combo_to.get() == "Translate To":
            messagebox.showerror("Error", "Please select the input and output languages.")
            return

        self.enable_buttons(False)
        self.button_stop.config(state=tk.NORMAL)
        self.text_input.delete("1.0", tk.END)
        self.text_input.insert("1.0", "Speak now...")

        # Start voice recognition in a separate thread
        threading.Thread(target=self.recognize_voice, daemon=True).start()

    def recognize_voice(self):
        """Handle speech recognition."""
        recognizer = sr.Recognizer()
        input_lang_code = self.languages.get(self.combo_from.get(), "en")  # Default to "en" if not selected
        target_lang_code = self.languages.get(self.combo_to.get(), "en")  # Default to "en" if not selected

        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)

            try:
                audio = recognizer.listen(source, timeout=None)
                # Recognize speech in the selected input language
                text = recognizer.recognize_google(audio, language=input_lang_code)

                self.text_input.delete("1.0", tk.END)
                self.text_input.insert("1.0", text)

                # Translate the recognized text
                translator = Translator()
                result = translator.translate(text, src=input_lang_code, dest=target_lang_code)

                # Display the translated text in the output area
                self.text_output.config(state=tk.NORMAL)
                self.text_output.delete("1.0", tk.END)
                self.text_output.insert("1.0", result.text)
                self.text_output.config(state=tk.DISABLED)

            except sr.RequestError:
                messagebox.showerror("Error", "Could not request results from Google Speech Recognition service.")
            except sr.UnknownValueError:
                messagebox.showerror("Error", "Google Speech Recognition could not understand the audio.")
            finally:
                # Re-enable buttons
                self.enable_buttons(True)
                self.button_stop.config(state=tk.DISABLED)

    def stop_translation(self):
        """Handle Stop button press."""
        self.enable_buttons(True)
        self.button_stop.config(state=tk.DISABLED)

        self.text_output.config(state=tk.NORMAL)
        self.text_output.delete("1.0", tk.END)

        self.text_output.config(state=tk.DISABLED)

        # Enable translation after stopping the voice input
        self.can_translate = True
        self.button_translate.config(state=tk.NORMAL)

    def listen_input(self):
        """Speak the content of the input text area."""
        text = self.text_input.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Warning", "No text available in the input box!")
            return
        # Corrected: Fetch selected language code directly
        from_lang_code = self.languages.get(self.combo_from.get(), "en")  # Default to "en" if not selected
        threading.Thread(target=self.speak, args=(text, from_lang_code), daemon=True).start()

    def listen_output(self):
        """Speak the content of the output text area."""
        text = self.text_output.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Warning", "No text available in the output box!")
            return
        # Corrected: Fetch selected language code directly
        to_lang_code = self.languages.get(self.combo_to.get(), "en")  # Default to "en" if not selected
        threading.Thread(target=self.speak, args=(text, to_lang_code), daemon=True).start()

    def speak(self, text, lang_code):
        """Convert text to speech in the desired language."""
        try:
            # Attempt to use pyttsx3 if the language is supported
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')

            # Map language codes to pyttsx3 voices (if available)
            language_to_voice = {
                "en": "english",  # English
                "hi": "hindi",  # Hindi
                "ml": "malayalam",  # Malayalam
                "ta": "tamil",  # Tamil
                "bn": "bengali",  # Bengali
                "gu": "gujarati",  # Gujarati
                "mr": "marathi",  # Marathi
                "te": "telugu",  # Telugu
                "kn": "kannada",  # Kannada
                "pa": "punjabi",  # Punjabi
                "ur": "urdu",  # Urdu
                "ar": "arabic",  # Arabic
                "fr": "french",  # French
                "de": "german",  # German
                "es": "spanish",  # Spanish
                "it": "italian",  # Italian
                "ja": "japanese",  # Japanese
                "ko": "korean",  # Korean
                "zh": "chinese",  # Chinese
                "tr": "turkish",  # Turkish
                "pt": "portuguese",  # Portuguese
                "ru": "russian",  # Russian
                "pl": "polish",  # Polish
                "sv": "swedish",  # Swedish
                "no": "norwegian",  # Norwegian
                "fi": "finnish",  # Finnish
                "el": "greek",  # Greek
                "he": "hebrew",  # Hebrew
                "ro": "romanian",  # Romanian
                "sr": "serbian",  # Serbian
                "hr": "croatian",  # Croatian
                "cs": "czech",  # Czech
                "sl": "slovenian",  # Slovenian
                "da": "danish",  # Danish
                "th": "thai",  # Thai
                "vi": "vietnamese",  # Vietnamese
                "id": "indonesian",  # Indonesian
                "ms": "malaysian",  # Malaysian
                "sv": "swedish",  # Swedish
                "tl": "filipino",  # Filipino/Tagalog
                "is": "icelandic",  # Icelandic
                "lv": "latvian",  # Latvian
                "lt": "lithuanian",  # Lithuanian
                "et": "estonian",  # Estonian
                "bg": "bulgarian",  # Bulgarian
                "uk": "ukrainian",  # Ukrainian
                "hr": "croatian",  # Croatian
                "sq": "albanian",  # Albanian
                "hy": "armenian",  # Armenian
                "km": "khmer",  # Khmer
                "mn": "mongolian",  # Mongolian
                "ne": "nepali",  # Nepali
                "si": "sinhala",  # Sinhalese
                "km": "khmer",  # Khmer
                "iw": "hebrew",  # Hebrew
                "hy": "armenian",  # Armenian
            }

            # Attempt to select the voice for the specified language
            selected_voice = None
            for voice in voices:
                if language_to_voice.get(lang_code, "").lower() in voice.name.lower():
                    selected_voice = voice
                    break

            if selected_voice:
                engine.setProperty('voice', selected_voice.id)
                engine.say(text)
                engine.runAndWait()
            else:
                # Fallback to gTTS for unsupported languages
                self.speak_with_gtts(text, lang_code)
        except Exception as e:
            print(f"Error in speech synthesis with pyttsx3: {e}")
            # Fallback to gTTS in case of error
            self.speak_with_gtts(text, lang_code)


    def speak_with_gtts(self, text, lang_code):
        """Fallback to gTTS for speech synthesis."""
        try:
            temp_file = "temp_audio.mp3"
            tts = gTTS(text=text, lang=lang_code, slow=False)
            tts.save(temp_file)
            playsound(temp_file)  # Play the audio file
            os.remove(temp_file)  # Delete the temporary file after playback
        except Exception as e:
            messagebox.showerror("Error", f"gTTS playback failed: {e}")

    def clear_text(self):
        """Clear both input and output text areas."""
        self.text_input.delete("1.0", tk.END)
        self.text_input.insert("1.0", "Enter Text")
        self.text_output.config(state=tk.NORMAL)
        self.text_output.delete("1.0", tk.END)
        self.text_output.insert("1.0", "Translation")
        self.text_output.config(state=tk.DISABLED)

    def translate(self):
        """Handle translation."""
        try:
            from_lang_code = self.languages.get(self.combo_from.get(), "en")  # Default to "en" if not selected
            to_lang_code = self.languages.get(self.combo_to.get(), "en")  # Default to "en" if not selected
            text = self.text_input.get("1.0", tk.END).strip()

            if not text:
                messagebox.showwarning("Warning", "No text to translate!")
                return

            translator = Translator()
            result = translator.translate(text, src=from_lang_code, dest=to_lang_code)

            self.text_output.config(state=tk.NORMAL)
            self.text_output.delete("1.0", tk.END)
            self.text_output.insert("1.0", result.text)
            self.text_output.config(state=tk.DISABLED)

        except Exception as e:
            messagebox.showerror("Error", f"Error during translation: {e}")

    def filter_languages_from(self, event):
        """Filter languages in the from dropdown."""
        search_term = self.combo_from.get().lower()
        filtered_languages = [lang for lang in self.languages if search_term in lang.lower()]
        self.combo_from["values"] = filtered_languages

    def filter_languages_to(self, event):
        """Filter languages in the to dropdown."""
        search_term = self.combo_to.get().lower()
        filtered_languages = [lang for lang in self.languages if search_term in lang.lower()]
        self.combo_to["values"] = filtered_languages

    def show_all_languages_from(self, event):
        """Show all languages when focus is on the from dropdown."""
        self.combo_from["values"] = self.languages

    def show_all_languages_to(self, event):
        """Show all languages when focus is on the to dropdown."""
        self.combo_to["values"] = self.languages


# Main part of the program

if __name__ == "__main__":
    root = tk.Tk()  # Creates the main application window
    app = MultiLanguageTranslator(root)  # Instantiates the translator application
    root.mainloop()  # Runs the Tkinter event loop