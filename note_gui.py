import tkinter as tk
from tkinter import messagebox, simpledialog

import note


class NoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Note Taking App")
        self.root.geometry("900x600")

        self.selected_note_id = None

        self.title_var = tk.StringVar()
        self.search_var = tk.StringVar()

        self._build_ui()
        self.refresh_notes()

    def _build_ui(self):
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(1, weight=1)

        header = tk.Label(self.root, text="Tkinter Note Taking App", font=("Arial", 18, "bold"))
        header.grid(row=0, column=0, columnspan=2, pady=(12, 8), sticky="ew")

        left_frame = tk.Frame(self.root)
        left_frame.grid(row=1, column=0, padx=12, pady=8, sticky="nsew")
        left_frame.grid_rowconfigure(2, weight=1)

        tk.Label(left_frame, text="Title", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky="w", pady=(0, 4))
        title_entry = tk.Entry(left_frame, textvariable=self.title_var, font=("Arial", 12))
        title_entry.grid(row=1, column=0, sticky="ew")

        tk.Label(left_frame, text="Content", font=("Arial", 12, "bold")).grid(row=2, column=0, sticky="w", pady=(12, 4))
        self.content_text = tk.Text(left_frame, height=12, width=50, font=("Arial", 12))
        self.content_text.grid(row=3, column=0, sticky="nsew")

        button_frame = tk.Frame(left_frame)
        button_frame.grid(row=4, column=0, pady=(12, 0), sticky="ew")
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        button_frame.grid_columnconfigure(2, weight=1)

        tk.Button(button_frame, text="Save Note", command=self.save_note).grid(row=0, column=0, padx=4, sticky="ew")
        tk.Button(button_frame, text="Delete Note", command=self.delete_selected_note).grid(row=0, column=1, padx=4, sticky="ew")
        tk.Button(button_frame, text="Clear", command=self.clear_form).grid(row=0, column=2, padx=4, sticky="ew")

        self.status_label = tk.Label(left_frame, text="Ready", fg="darkblue", anchor="w")
        self.status_label.grid(row=5, column=0, sticky="w", pady=(12, 0))

        right_frame = tk.Frame(self.root)
        right_frame.grid(row=1, column=1, padx=12, pady=8, sticky="nsew")
        right_frame.grid_rowconfigure(1, weight=1)

        search_frame = tk.Frame(right_frame)
        search_frame.grid(row=0, column=0, sticky="ew")
        search_frame.grid_columnconfigure(0, weight=1)

        tk.Label(search_frame, text="Search", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky="w")
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, font=("Arial", 12))
        search_entry.grid(row=1, column=0, sticky="ew", padx=(0, 8))
        tk.Button(search_frame, text="Search", command=self.search_notes).grid(row=1, column=1, sticky="e")
        tk.Button(search_frame, text="Show All", command=self.refresh_notes).grid(row=1, column=2, padx=(8, 0), sticky="e")

        tk.Label(right_frame, text="Saved Notes", font=("Arial", 12, "bold")).grid(row=1, column=0, sticky="w", pady=(12, 4))
        self.notes_listbox = tk.Listbox(right_frame, font=("Arial", 11), selectmode=tk.SINGLE)
        self.notes_listbox.grid(row=2, column=0, sticky="nsew")
        self.notes_listbox.bind("<<ListboxSelect>>", self.on_note_select)

        scrollbar = tk.Scrollbar(right_frame, orient="vertical", command=self.notes_listbox.yview)
        scrollbar.grid(row=2, column=1, sticky="ns")
        self.notes_listbox.configure(yscrollcommand=scrollbar.set)

    def refresh_notes(self):
        self.selected_note_id = None
        self.notes_listbox.delete(0, tk.END)
        notes = note.load_notes()

        if not notes:
            self.status_label.config(text="No notes found.")
            return

        for note_item in notes:
            display_text = f"{note_item['id']} | {note_item['title']}"
            self.notes_listbox.insert(tk.END, display_text)

        self.status_label.config(text=f"{len(notes)} note(s) loaded.")

        self.clear_form()

    def search_notes(self):
        keyword = self.search_var.get().strip().lower()
        self.notes_listbox.delete(0, tk.END)

        notes = note.load_notes()
        matches = [
            item for item in notes
            if keyword in item["title"].lower() or keyword in item["content"].lower()
        ]

        if not matches:
            self.status_label.config(text="No matching notes found.")
            self.clear_form()
            return

        for note_item in matches:
            self.notes_listbox.insert(tk.END, f"{note_item['id']} | {note_item['title']}")

        self.status_label.config(text=f"{len(matches)} matching note(s).")
        self.clear_form()

    def on_note_select(self, event):
        selection = self.notes_listbox.curselection()
        if not selection:
            return

        selected_text = self.notes_listbox.get(selection[0])
        note_id = int(selected_text.split(" | ", 1)[0])
        self.selected_note_id = note_id

        notes = note.load_notes()
        current_note = next((item for item in notes if item["id"] == note_id), None)

        if current_note:
            self.title_var.set(current_note["title"])
            self.content_text.delete("1.0", tk.END)
            self.content_text.insert("1.0", current_note["content"])
            self.status_label.config(text=f"Editing note #{note_id}.")

    def clear_form(self):
        self.title_var.set("")
        self.content_text.delete("1.0", tk.END)
        self.selected_note_id = None
        self.notes_listbox.selection_clear(0, tk.END)

    def save_note(self):
        title = self.title_var.get().strip()
        content = self.content_text.get("1.0", tk.END).strip()

        if not title:
            messagebox.showwarning("Missing title", "Please enter a title.")
            return

        if not content:
            messagebox.showwarning("Missing content", "Please enter note content.")
            return

        notes = note.load_notes()

        if self.selected_note_id is not None:
            current = next((item for item in notes if item["id"] == self.selected_note_id), None)
            if current is None:
                messagebox.showerror("Error", "Selected note no longer exists.")
                self.refresh_notes()
                return

            current["title"] = title
            current["content"] = content
            current["updated_at"] = note.now_iso()
            note.save_notes(notes)
            self.status_label.config(text=f"Note #{self.selected_note_id} updated.")
        else:
            next_id = max((item["id"] for item in notes), default=0) + 1
            note_item = {
                "id": next_id,
                "title": title,
                "content": content,
                "created_at": note.now_iso(),
                "updated_at": note.now_iso(),
            }
            notes.append(note_item)
            note.save_notes(notes)
            self.status_label.config(text=f"Note #{next_id} saved.")

        self.refresh_notes()

    def delete_selected_note(self):
        if self.selected_note_id is None:
            messagebox.showwarning("No note selected", "Select a note to delete.")
            return

        confirm = messagebox.askyesno("Confirm delete", f"Delete note #{self.selected_note_id}?")
        if not confirm:
            return

        notes = note.load_notes()
        updated_notes = [item for item in notes if item["id"] != self.selected_note_id]
        note.save_notes(updated_notes)
        self.status_label.config(text=f"Note #{self.selected_note_id} deleted.")
        self.refresh_notes()


def main():
    root = tk.Tk()
    app = NoteApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
