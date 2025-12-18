import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import threading
from main_function.detector import MLDetector

# Set appearance mode and color theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class SecretHunterApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window configuration
        self.title("Sensitive Detector")
        self.geometry("1000x700")
        
        # Initialize the AI detector instance
        self.detector = MLDetector()
        self.scanning = False

        # Configure grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar setup
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar, text="Leak Detection", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.pack(padx=20, pady=(20, 10))

        self.btn_select = ctk.CTkButton(self.sidebar, text="Select Folder", command=self.select_folder)
        self.btn_select.pack(padx=20, pady=10)
        
        self.path_label = ctk.CTkLabel(self.sidebar, text="Not selected", text_color="gray", wraplength=180)
        self.path_label.pack(padx=20, pady=(0, 20))

        self.btn_start = ctk.CTkButton(self.sidebar, text="Start scanning", fg_color="#e63946", hover_color="#d62828", command=self.start_scan_thread)
        self.btn_start.pack(padx=20, pady=10)

        # Main content area setup
        self.main_area = ctk.CTkFrame(self, corner_radius=10)
        self.main_area.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.main_area.grid_rowconfigure(2, weight=1)
        self.main_area.grid_columnconfigure(0, weight=1)

        self.status_label = ctk.CTkLabel(self.main_area, text="Waiting for action", font=ctk.CTkFont(size=16))
        self.status_label.grid(row=0, column=0, sticky="w", padx=20, pady=(20,0))

        self.progress_bar = ctk.CTkProgressBar(self.main_area)
        self.progress_bar.grid(row=1, column=0, sticky="ew", padx=20, pady=(10, 20))
        self.progress_bar.set(0)

        # Textbox for displaying results
        self.result_box = ctk.CTkTextbox(self.main_area, font=("Consolas", 14))
        self.result_box.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 20))
        
        # Configure text tags for coloring output based on risk level
        # Critical: Red / High: Orange / Medium: Yellow / Info: Light Gray / Success: Green
        self.result_box.tag_config("critical", foreground="#FF4444") 
        self.result_box.tag_config("high", foreground="#FF8800")
        self.result_box.tag_config("medium", foreground="#FFCC00")
        self.result_box.tag_config("info", foreground="#CCCCCC")
        self.result_box.tag_config("success", foreground="#00FF00")

        # Initial log message
        self.log("Please select target folder", "info")
        
        # Check if the model is loaded correctly
        if self.detector.model:
            self.log("System: AI Model loaded successfully.", "success")
        else:
            self.log("System: Failed to load AI model.", "critical")

    def select_folder(self):
        # Open dialog to select directory
        folder = filedialog.askdirectory()
        if folder:
            self.path_label.configure(text=os.path.basename(folder))
            self.target_path = folder
            self.log(f"Target selected: {folder}", "info")

    def log(self, message, tag=None):
        # Insert message into the result box with optional color tag
        if tag:
            self.result_box.insert(tk.END, message + "\n", tag)
        else:
            self.result_box.insert(tk.END, message + "\n")
            
        self.result_box.see(tk.END)

    def start_scan_thread(self):
        # Check if a target folder is selected
        if not hasattr(self, 'target_path'):
            messagebox.showwarning("Hint", "Please select target folder first")
            return
        
        # Prevent multiple scans running at the same time
        if self.scanning:
            return

        self.scanning = True
        self.btn_start.configure(state="disabled", text="Scanning...")
        self.result_box.delete("1.0", tk.END) 
        
        # Start scanning in a separate thread to keep UI responsive
        threading.Thread(target=self.run_scan, daemon=True).start()

    def run_scan(self):
        file_list = []
        
        # Walk through the directory and filter files
        for root, dirs, files in os.walk(self.target_path):
            # Ignore common non-source directories
            if '.git' in dirs: dirs.remove('.git') 
            if 'venv' in dirs: dirs.remove('venv') 
            if '__pycache__' in dirs: dirs.remove('__pycache__')

            for f in files:
                # Filter by file extensions
                if f.endswith(('.py', '.js', '.json', '.txt', '.md', '.env', '.yml', '.xml', '.html')):
                    file_list.append(os.path.join(root, f))

        total = len(file_list)
        if total == 0:
            self.log("Did not find any target files.", "info")
            self.finish_scan()
            return

        self.log(f"Start analyzing {total} files...\n", "info")
        
        found_issues = 0
        
        for i, filepath in enumerate(file_list):
            # Stop if scanning is cancelled (though cancel button is not implemented yet)
            if not self.scanning: break 

            # Update progress bar and status label
            progress = (i + 1) / total
            self.progress_bar.set(progress)
            self.status_label.configure(text=f"Analyzing: {os.path.basename(filepath)} ({i+1}/{total})")
            
            try:
                # Skip empty files
                if os.path.getsize(filepath) == 0:
                    continue

                # Read file content
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    lines = content.splitlines()

                    for line_idx, line in enumerate(lines, 1):
                        # Call the AI detector for the current line
                        results = self.detector.scan_line(line, line_idx)
                        
                        for res in results:
                            found_issues += 1
                            
                            # Determine color tag and text label based on risk level
                            risk_tag = "medium"
                            risk_label = "[MEDIUM]"
                            
                            risk = res['risk'].upper()
                            
                            risk_tag = "medium"
                            risk_label = "[MEDIUM]"
                            
                            if risk == "CRITICAL":
                                risk_tag = "critical"
                                risk_label = "[CRITICAL]"
                            elif risk == "HIGH":
                                risk_tag = "high"
                                risk_label = "[HIGH]"
                            elif risk == "LOW":
                                risk_tag = "info"
                                risk_label = "[LOW]"

                            
                            # Construct and log the result message
                            header_msg = f"{risk_label} {os.path.basename(filepath)} : Line {res['line']} (Score: {res['score']}%)"
                            self.log(header_msg, risk_tag)
                            
                            # Log the matched content
                            content_msg = f"      Match: {res['word']}"
                            self.log(content_msg, "info")
                            self.log("-" * 60, "info")
                            
            except Exception:
                # Silently ignore read errors to continue scanning
                pass

        # Summary log
        if found_issues == 0:
            self.log("\nScan complete. No leaks found.", "success")
        else:
            self.log(f"\nScan complete. Found {found_issues} potential leaks.", "high")
            
        self.finish_scan()

    def finish_scan(self):
        # Reset UI state after scanning
        self.scanning = False
        self.btn_start.configure(state="normal", text="Start scanning")
        self.status_label.configure(text="Scan finished")

if __name__ == "__main__":
    app = SecretHunterApp()
    app.mainloop()