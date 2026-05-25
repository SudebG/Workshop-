import json
import os
from datetime import datetime, timezone

DATA_FILE = "notes.json"


def load_notes():
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data if isinstance(data, list) else []


def save_notes(notes):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(notes, file, indent=2, ensure_ascii=False)


def now_iso():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def add_note():
    title = input("Enter title: ").strip()
    content = input("Enter note: ").strip()

    if not title:
        print("Title cannot be empty.")
        return

    if not content:
        print("Note cannot be empty.")
        return

    notes = load_notes()
    next_id = max((note["id"] for note in notes), default=0) + 1
    note = {
        "id": next_id,
        "title": title,
        "content": content,
        "created_at": now_iso(),
        "updated_at": now_iso(),
    }
    notes.append(note)
    save_notes(notes)
    print("Note saved.")


def view_notes():
    notes = load_notes()

    if not notes:
        print("No notes found.")
        return

    print("\nSaved notes:")
    for note in notes:
        print(f"ID: {note['id']} | Title: {note['title']}")
        print(f"{note['content']}")
        print(f"Updated: {note['updated_at']}")
        print("-" * 40)


def search_notes():
    keyword = input("Enter keyword to search: ").strip().lower()

    if not keyword:
        print("Keyword cannot be empty.")
        return

    notes = load_notes()
    matches = [note for note in notes if keyword in note["title"].lower() or keyword in note["content"].lower()]

    if not matches:
        print("No matching notes found.")
        return

    print("\nSearch results:")
    for note in matches:
        print(f"ID: {note['id']} | Title: {note['title']}")
        print(f"{note['content']}")
        print("-" * 40)


def edit_note():
    notes = load_notes()

    if not notes:
        print("No notes found.")
        return

    note_id = input("Enter note ID to edit: ").strip()

    try:
        note_id = int(note_id)
    except ValueError:
        print("Invalid note ID.")
        return

    note = next((item for item in notes if item["id"] == note_id), None)
    if not note:
        print("Note not found.")
        return

    new_title = input(f"Current title: {note['title']}\nEnter new title (leave blank to keep): ").strip()
    new_content = input(f"Current content: {note['content']}\nEnter new content (leave blank to keep): ").strip()

    if new_title:
        note["title"] = new_title
    if new_content:
        note["content"] = new_content

    if not new_title and not new_content:
        print("No changes made.")
        return

    note["updated_at"] = now_iso()
    save_notes(notes)
    print("Note updated.")


def delete_note():
    notes = load_notes()

    if not notes:
        print("No notes found.")
        return

    note_id = input("Enter note ID to delete: ").strip()

    try:
        note_id = int(note_id)
    except ValueError:
        print("Invalid note ID.")
        return

    updated_notes = [note for note in notes if note["id"] != note_id]

    if len(updated_notes) == len(notes):
        print("Note not found.")
        return

    save_notes(updated_notes)
    print("Note deleted.")


def main():
    while True:
        print("\n1. Add note")
        print("2. View notes")
        print("3. Search notes")
        print("4. Edit note")
        print("5. Delete note")
        print("6. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_note()
        elif choice == "2":
            view_notes()
        elif choice == "3":
            search_notes()
        elif choice == "4":
            edit_note()
        elif choice == "5":
            delete_note()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
