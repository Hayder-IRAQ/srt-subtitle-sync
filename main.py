"""
SRT Subtitle Sync Tool — Professional GUI Application
Adjust subtitle timing for any SRT file, individually or in batch.

Author  : Hayder Odhafa (حيدر عذافة)
GitHub  : https://github.com/Hayder-IRAQ
Version : 1.0
License : MIT

Install: pip install customtkinter
"""

import re
import threading
from datetime import datetime, timedelta
from pathlib import Path
from tkinter import filedialog, messagebox
import customtkinter as ctk


class SRTSyncApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("SRT Subtitle Sync Tool")
        self.geometry("750x700")
        self.minsize(700, 650)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.selected_files: list[str] = []
        self.output_directory: str = ""
        self.processing = False

        self._setup_ui()

    def _setup_ui(self):
        # Main scrollable container
        self.main_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # ═══════════════════════════════════════════════════════════════
        # HEADER
        # ═══════════════════════════════════════════════════════════════
        header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 25))

        ctk.CTkLabel(
            header_frame,
            text="🎬 SRT Subtitle Sync Tool",
            font=ctk.CTkFont(size=28, weight="bold")
        ).pack()

        ctk.CTkLabel(
            header_frame,
            text="Adjust subtitle timing with precision",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        ).pack(pady=(5, 0))

        # ═══════════════════════════════════════════════════════════════
        # FILE SELECTION SECTION
        # ═══════════════════════════════════════════════════════════════
        file_section = ctk.CTkFrame(self.main_frame)
        file_section.pack(fill="x", pady=(0, 20))

        # Section header
        file_header = ctk.CTkFrame(file_section, fg_color="transparent")
        file_header.pack(fill="x", padx=15, pady=(15, 10))

        ctk.CTkLabel(
            file_header,
            text="📁 Select SRT Files",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(side="left")

        self.file_count_label = ctk.CTkLabel(
            file_header,
            text="0 files selected",
            font=ctk.CTkFont(size=13),
            text_color="#888"
        )
        self.file_count_label.pack(side="right")

        # File listbox
        self.file_listbox = ctk.CTkTextbox(
            file_section,
            height=100,
            font=ctk.CTkFont(size=12),
            state="disabled",
            fg_color="#2b2b2b"
        )
        self.file_listbox.pack(fill="x", padx=15, pady=(0, 15))

        # File buttons
        btn_frame = ctk.CTkFrame(file_section, fg_color="transparent")
        btn_frame.pack(fill="x", padx=15, pady=(0, 15))

        self.add_files_btn = ctk.CTkButton(
            btn_frame,
            text="➕ Add Files",
            command=self._add_files,
            width=130,
            height=40,
            font=ctk.CTkFont(size=14),
            fg_color="#0d6efd",
            hover_color="#0b5ed7"
        )
        self.add_files_btn.pack(side="left", padx=(0, 10))

        self.add_folder_btn = ctk.CTkButton(
            btn_frame,
            text="📂 Add Folder",
            command=self._add_folder,
            width=130,
            height=40,
            font=ctk.CTkFont(size=14),
            fg_color="#6c757d",
            hover_color="#5c636a"
        )
        self.add_folder_btn.pack(side="left", padx=(0, 10))

        self.clear_btn = ctk.CTkButton(
            btn_frame,
            text="🗑️ Clear All",
            command=self._clear_files,
            width=110,
            height=40,
            font=ctk.CTkFont(size=14),
            fg_color="#dc3545",
            hover_color="#bb2d3b"
        )
        self.clear_btn.pack(side="left")

        # ═══════════════════════════════════════════════════════════════
        # TIME ADJUSTMENT SECTION
        # ═══════════════════════════════════════════════════════════════
        time_section = ctk.CTkFrame(self.main_frame)
        time_section.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(
            time_section,
            text="⏱️ Time Adjustment",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(anchor="w", padx=15, pady=(15, 15))

        time_content = ctk.CTkFrame(time_section, fg_color="transparent")
        time_content.pack(fill="x", padx=15, pady=(0, 15))

        ctk.CTkLabel(
            time_content,
            text="Seconds to add/subtract:",
            font=ctk.CTkFont(size=14)
        ).pack(side="left")

        self.time_var = ctk.StringVar(value="-0.5")
        self.time_entry = ctk.CTkEntry(
            time_content,
            textvariable=self.time_var,
            width=100,
            height=40,
            font=ctk.CTkFont(size=16),
            justify="center"
        )
        self.time_entry.pack(side="left", padx=(15, 25))

        # Quick buttons
        quick_values = [("-2s", -2), ("-1s", -1), ("-0.5s", -0.5), ("+0.5s", 0.5), ("+1s", 1), ("+2s", 2)]
        for text, val in quick_values:
            ctk.CTkButton(
                time_content,
                text=text,
                command=lambda v=val: self.time_var.set(str(v)),
                width=55,
                height=35,
                font=ctk.CTkFont(size=12),
                fg_color="#404040",
                hover_color="#505050"
            ).pack(side="left", padx=2)

        # ═══════════════════════════════════════════════════════════════
        # OUTPUT SETTINGS SECTION
        # ═══════════════════════════════════════════════════════════════
        output_section = ctk.CTkFrame(self.main_frame)
        output_section.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(
            output_section,
            text="💾 Output Settings",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(anchor="w", padx=15, pady=(15, 15))

        # Suffix row
        suffix_row = ctk.CTkFrame(output_section, fg_color="transparent")
        suffix_row.pack(fill="x", padx=15, pady=(0, 10))

        ctk.CTkLabel(
            suffix_row,
            text="File name suffix:",
            font=ctk.CTkFont(size=14)
        ).pack(side="left")

        self.suffix_var = ctk.StringVar(value="_Synced")
        self.suffix_entry = ctk.CTkEntry(
            suffix_row,
            textvariable=self.suffix_var,
            width=150,
            height=38,
            font=ctk.CTkFont(size=14)
        )
        self.suffix_entry.pack(side="left", padx=(15, 25))

        self.overwrite_var = ctk.BooleanVar(value=False)
        self.overwrite_check = ctk.CTkCheckBox(
            suffix_row,
            text="Overwrite original files",
            variable=self.overwrite_var,
            font=ctk.CTkFont(size=14),
            command=self._toggle_output_options
        )
        self.overwrite_check.pack(side="left")

        # Output directory row
        ctk.CTkLabel(
            output_section,
            text="Save location:",
            font=ctk.CTkFont(size=14)
        ).pack(anchor="w", padx=15, pady=(10, 5))

        output_dir_row = ctk.CTkFrame(output_section, fg_color="transparent")
        output_dir_row.pack(fill="x", padx=15, pady=(0, 15))

        self.output_dir_var = ctk.StringVar(value="Same folder as original file")
        self.output_dir_label = ctk.CTkLabel(
            output_dir_row,
            textvariable=self.output_dir_var,
            font=ctk.CTkFont(size=13),
            text_color="#aaa",
            anchor="w",
            width=350
        )
        self.output_dir_label.pack(side="left", fill="x", expand=True)

        self.browse_output_btn = ctk.CTkButton(
            output_dir_row,
            text="📁 Choose Folder",
            command=self._select_output_directory,
            width=140,
            height=38,
            font=ctk.CTkFont(size=13),
            fg_color="#198754",
            hover_color="#157347"
        )
        self.browse_output_btn.pack(side="left", padx=(10, 5))

        self.reset_output_btn = ctk.CTkButton(
            output_dir_row,
            text="↺ Reset",
            command=self._reset_output_directory,
            width=80,
            height=38,
            font=ctk.CTkFont(size=13),
            fg_color="#6c757d",
            hover_color="#5c636a"
        )
        self.reset_output_btn.pack(side="left")

        # ═══════════════════════════════════════════════════════════════
        # PROGRESS SECTION
        # ═══════════════════════════════════════════════════════════════
        progress_section = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        progress_section.pack(fill="x", pady=(0, 15))

        self.status_label = ctk.CTkLabel(
            progress_section,
            text="Ready to sync",
            font=ctk.CTkFont(size=13),
            text_color="#888"
        )
        self.status_label.pack(pady=(0, 8))

        self.progress_bar = ctk.CTkProgressBar(progress_section, height=12, corner_radius=6)
        self.progress_bar.pack(fill="x")
        self.progress_bar.set(0)

        # ═══════════════════════════════════════════════════════════════
        # START BUTTON
        # ═══════════════════════════════════════════════════════════════
        self.process_btn = ctk.CTkButton(
            self.main_frame,
            text="🚀  START SYNC",
            command=self._start_processing,
            height=60,
            font=ctk.CTkFont(size=20, weight="bold"),
            fg_color="#198754",
            hover_color="#157347",
            corner_radius=10
        )
        self.process_btn.pack(fill="x", pady=(10, 15))

        # Footer
        ctk.CTkLabel(
            self.main_frame,
            text="Supports .srt subtitle files",
            font=ctk.CTkFont(size=11),
            text_color="#666"
        ).pack()

    # ═══════════════════════════════════════════════════════════════════════
    # FILE MANAGEMENT METHODS
    # ═══════════════════════════════════════════════════════════════════════

    def _add_files(self):
        files = filedialog.askopenfilenames(
            title="Select SRT Files",
            filetypes=[("SRT Files", "*.srt"), ("All Files", "*.*")]
        )
        if files:
            for f in files:
                if f not in self.selected_files:
                    self.selected_files.append(f)
            self._update_file_list()

    def _add_folder(self):
        folder = filedialog.askdirectory(title="Select Folder Containing SRT Files")
        if folder:
            for f in Path(folder).rglob("*.srt"):
                if str(f) not in self.selected_files:
                    self.selected_files.append(str(f))
            self._update_file_list()

    def _clear_files(self):
        self.selected_files.clear()
        self._update_file_list()

    def _update_file_list(self):
        self.file_listbox.configure(state="normal")
        self.file_listbox.delete("1.0", "end")
        for f in self.selected_files:
            self.file_listbox.insert("end", f"• {Path(f).name}\n")
        self.file_listbox.configure(state="disabled")
        count = len(self.selected_files)
        self.file_count_label.configure(text=f"{count} file{'s' if count != 1 else ''} selected")

    # ═══════════════════════════════════════════════════════════════════════
    # OUTPUT DIRECTORY METHODS
    # ═══════════════════════════════════════════════════════════════════════

    def _select_output_directory(self):
        directory = filedialog.askdirectory(title="Select Output Folder")
        if directory:
            self.output_directory = directory
            # Show shortened path if too long
            display_path = directory if len(directory) < 50 else f"...{directory[-47:]}"
            self.output_dir_var.set(display_path)

    def _reset_output_directory(self):
        self.output_directory = ""
        self.output_dir_var.set("Same folder as original file")

    def _toggle_output_options(self):
        if self.overwrite_var.get():
            self.suffix_entry.configure(state="disabled")
            self.browse_output_btn.configure(state="disabled")
            self.reset_output_btn.configure(state="disabled")
        else:
            self.suffix_entry.configure(state="normal")
            self.browse_output_btn.configure(state="normal")
            self.reset_output_btn.configure(state="normal")

    # ═══════════════════════════════════════════════════════════════════════
    # PROCESSING METHODS
    # ═══════════════════════════════════════════════════════════════════════

    def _validate_inputs(self) -> tuple[bool, float]:
        if not self.selected_files:
            messagebox.showwarning("No Files", "Please select at least one SRT file first.")
            return False, 0.0

        try:
            seconds = float(self.time_var.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for time adjustment.")
            return False, 0.0

        return True, seconds

    def _start_processing(self):
        if self.processing:
            return

        valid, seconds = self._validate_inputs()
        if not valid:
            return

        self.processing = True
        self._set_ui_state(False)

        thread = threading.Thread(target=self._process_files, args=(seconds,), daemon=True)
        thread.start()

    def _set_ui_state(self, enabled: bool):
        state = "normal" if enabled else "disabled"
        self.add_files_btn.configure(state=state)
        self.add_folder_btn.configure(state=state)
        self.clear_btn.configure(state=state)
        self.time_entry.configure(state=state)
        self.process_btn.configure(state=state)

        if not self.overwrite_var.get():
            self.suffix_entry.configure(state=state)
            self.browse_output_btn.configure(state=state)
            self.reset_output_btn.configure(state=state)

        self.overwrite_check.configure(state=state)

    def _process_files(self, seconds: float):
        total = len(self.selected_files)
        success_count = 0
        error_files = []
        self._output_paths = []

        for i, filepath in enumerate(self.selected_files):
            progress = (i + 1) / total
            self.after(0, lambda p=progress: self.progress_bar.set(p))
            self.after(0, lambda f=filepath, idx=i+1: self.status_label.configure(
                text=f"Processing ({idx}/{total}): {Path(f).name}"
            ))

            try:
                self._sync_file(filepath, seconds)
                success_count += 1
            except Exception as e:
                error_files.append((filepath, str(e)))

        self.after(0, lambda: self._processing_complete(success_count, error_files, total))

    def _sync_file(self, filepath: str, seconds: float):
        time_pattern = r'\d{2}:\d{2}:\d{2}[,.]\d{3}'

        def adjust_time(match):
            time_str = match.group()
            clean_time = time_str.replace(',', '.')

            try:
                dt = datetime.strptime(clean_time, '%H:%M:%S.%f')
                new_dt = dt + timedelta(seconds=seconds)

                # Handle negative times
                if new_dt.day != dt.day:
                    if seconds < 0:
                        new_dt = datetime.strptime("00:00:00.000", '%H:%M:%S.%f')
                    else:
                        new_dt = datetime.strptime("23:59:59.999", '%H:%M:%S.%f')

                result = new_dt.strftime('%H:%M:%S.%f')
                main_part, ms_part = result.split('.')
                return f"{main_part},{ms_part[:3]}"
            except ValueError:
                return time_str

        # Try UTF-8 first, fall back to latin-1 for older SRT files
        try:
            with open(filepath, 'r', encoding='utf-8-sig') as f:
                content = f.read()
        except UnicodeDecodeError:
            with open(filepath, 'r', encoding='latin-1') as f:
                content = f.read()

        new_content = re.sub(time_pattern, adjust_time, content)

        if self.overwrite_var.get():
            output_path = filepath
        else:
            path = Path(filepath)
            suffix = self.suffix_var.get() if self.suffix_var.get() else "_Synced"

            if self.output_directory:
                output_path = str(Path(self.output_directory) / f"{path.stem}{suffix}{path.suffix}")
            else:
                output_path = str(path.parent / f"{path.stem}{suffix}{path.suffix}")

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        # Store output path for showing to user
        if not hasattr(self, '_output_paths'):
            self._output_paths = []
        self._output_paths.append(output_path)

    def _processing_complete(self, success: int, errors: list, total: int):
        self.processing = False
        self._set_ui_state(True)

        if errors:
            error_msg = "\n".join([f"• {Path(f).name}: {e}" for f, e in errors[:5]])
            if len(errors) > 5:
                error_msg += f"\n... and {len(errors) - 5} more"
            messagebox.showwarning(
                "Completed with Errors",
                f"Successfully processed {success} of {total} files.\n\nErrors:\n{error_msg}"
            )
        else:
            # Show where files were saved
            if self._output_paths:
                first_output = self._output_paths[0]
                output_folder = str(Path(first_output).parent)
                messagebox.showinfo(
                    "Success! ✅",
                    f"Successfully synced {success} file(s)!\n\nSaved to:\n{output_folder}\n\nFile: {Path(first_output).name}"
                )
            else:
                messagebox.showinfo("Success! ✅", f"Successfully synced {success} file(s)!")

        self.status_label.configure(text=f"Completed: {success}/{total} files processed successfully")
        self.progress_bar.set(0)


if __name__ == '__main__':
    app = SRTSyncApp()
    app.mainloop()