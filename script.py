import os
import shutil
import customtkinter
from tkinter import messagebox

# Modes: "System" (standard), "Dark", "Light"
customtkinter.set_appearance_mode("Dark")
# Themes: "blue" (standard), "green", "dark-blue"
customtkinter.set_default_color_theme("blue")


class MyGUI(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.files_list = ""
        self.count = 0
        self.source_folder = ""
        self.destination_folder = ""

        # Set the window title and size
        self.title("Files Selector")
        self.minsize(width=600, height=400)

        # Create a frame
        frame = customtkinter.CTkFrame(master=self)
        frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Initialize fonts
        label_font = customtkinter.CTkFont(size=12)
        button_font = customtkinter.CTkFont(size=16, weight="bold")
        main_label_font = customtkinter.CTkFont(size=20, weight="bold")

        # Create label for the path
        self.label = customtkinter.CTkLabel(
            master=frame, text="Photo Folder Path", font=label_font
        )
        self.label.pack(padx=80, pady=(10, 1), anchor="w")

        # Create a text box for the path
        self.path_text = customtkinter.CTkTextbox(
            master=frame,
            width=400,
            height=1,
            wrap="word",
            font=label_font,
        )
        self.path_text.pack(padx=10)

        # Create label for the files
        self.label = customtkinter.CTkLabel(
            master=frame, text="Files names", font=label_font
        )
        self.label.pack(padx=80, pady=(10, 1), anchor="w")

        # Create a text box for the files
        self.text_area = customtkinter.CTkTextbox(
            master=frame,
            width=400,
            height=200,
            wrap="word",
            font=label_font,
        )
        self.text_area.pack(padx=10)

        # Create a button to run program
        self.run_btn = customtkinter.CTkButton(
            master=frame,
            width=400,
            height=40,
            text="Select Files",
            font=button_font,
            command=self.make_file_list,
        )
        self.run_btn.pack(pady=20)

        # Bind the Enter key and Ctrl + V
        self.text_area.bind("<KeyPress>", self.shortcut)
        self.text_area.bind("<Control-v>", self.paste_from_clipboard)

        # Start the main loop
        self.mainloop()

    # Bind the Enter key
    def shortcut(self, event):
        # Check if the Enter key was pressed
        if event.keysym == "Return" and event.state == 0:
            self.make_file_list()

    # Bind the Ctrl + V
    def paste_from_clipboard(self, event):
        # Get clipboard text
        clipboard_text = self.clipboard_get()

        # Insert clipboard text into self.text_area
        self.text_area.insert(customtkinter.END, clipboard_text)

        # Return 'break' to prevent propagation to other widgets
        return "break"

    # Create a list of files
    def make_file_list(self):
        self.files_list = [
            i + ".ARW"
            for i in self.text_area.get("1.0", customtkinter.END).strip().split(" ")
        ]
        self.source_folder = self.path_text.get("1.0", customtkinter.END).strip()
        self.destination_folder = self.source_folder + "\\favorite"

        self.move_files_to_folder()

    # Move files
    def move_files_to_folder(self):
        # Create destination folder if it doesn't exist
        if not os.path.exists(self.destination_folder):
            os.makedirs(self.destination_folder)

        for filename in self.files_list:
            # Create source and destination paths
            self.source_file = os.path.join(self.source_folder, filename)
            self.destination_file = os.path.join(self.destination_folder, filename)

            if os.path.exists(self.source_file):
                # Move file to destination
                shutil.move(self.source_file, self.destination_file)
                self.count += 1
            else:
                messagebox.showinfo("Error", f"File {filename} was not found")

        # Show success message
        messagebox.showinfo("Done", f"{self.count} files moved!")


if __name__ == "__main__":
    MyGUI()
