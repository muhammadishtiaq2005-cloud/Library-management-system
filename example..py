


import tkinter as tk
from tkinter import ttk, messagebox

# ------------------ Book Class ------------------
class Book:
    def __init__(self, book_id, title, author, quantity):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.quantity = quantity

    def check_availability(self):
        return self.quantity > 0

    def update_quantity(self, quantity):
        self.quantity += quantity


# ------------------ User Class ------------------
class User:
    def __init__(self, name, degree):
        self.name = name
        self.degree = degree
        self.borrowed_books = []

    def borrow_book(self, book):
        if book.check_availability():
            book.update_quantity(-1)
            self.borrowed_books.append(book)
            return True
        return False

    def return_book(self, book):
        if book in self.borrowed_books:
            book.update_quantity(1)
            self.borrowed_books.remove(book)
            return True
        return False


# ------------------ Library Class ------------------
class Library:
    def __init__(self):
        self.books = []
        self.users = {}

    def add_book(self, book):
        self.books.append(book)

    def get_user(self, name, degree):
        if name not in self.users:
            self.users[name] = User(name, degree)
        return self.users[name]


# ------------------ Main Application ------------------
class LibraryApp:
    def __init__(self, root, library, user):
        self.root = root
        self.library = library
        self.user = user

        self.root.title("AI Library Management System")
        self.root.geometry("800x600")

        # Title
        tk.Label(root, text=f"Welcome {self.user.name} ({self.user.degree})!", font=("Arial", 16, "bold")).pack(pady=10)

        # Already Borrowed Books
        self.borrowed_label = tk.Label(root, text="", font=("Arial", 12), fg="blue", justify="left")
        self.borrowed_label.pack(pady=5)
        self.update_borrowed_books()

        # Books Table
        self.tree = ttk.Treeview(root, columns=("ID", "Title", "Author", "Quantity"), show="headings", height=15)
        self.tree.pack(pady=20, fill="both", expand=True)

        for col in ("ID", "Title", "Author", "Quantity"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=180, anchor="center")

        self.load_books()

        # Buttons
        frame = tk.Frame(root)
        frame.pack(pady=10)

        tk.Button(frame, text="Borrow Book", command=self.borrow_book).grid(row=0, column=0, padx=10)
        tk.Button(frame, text="Return Book", command=self.return_book).grid(row=0, column=1, padx=10)
        tk.Button(frame, text="Exit", command=root.quit).grid(row=0, column=2, padx=10)

    # Load books in table
    def load_books(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for book in self.library.books:
            self.tree.insert("", "end", values=(book.book_id, book.title, book.author, book.quantity))

    # Borrow Book
    def borrow_book(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a book first")
            return

        values = self.tree.item(selected)["values"]
        book_id = values[0]
        book = next((b for b in self.library.books if b.book_id == book_id), None)

        if book and self.user.borrow_book(book):
            messagebox.showinfo("Success", f"You borrowed '{book.title}'")
        else:
            messagebox.showerror("Error", "Book not available")

        self.load_books()
        self.update_borrowed_books()

    # Return Book
    def return_book(self):
        if not self.user.borrowed_books:
            messagebox.showwarning("Warning", "You have no borrowed books")
            return

        book_titles = [book.title for book in self.user.borrowed_books]
        top = tk.Toplevel(self.root)
        top.title("Return Book")
        top.geometry("300x200")

        tk.Label(top, text="Select a book to return:").pack(pady=10)
        book_var = tk.StringVar(value=book_titles[0])
        dropdown = ttk.Combobox(top, values=book_titles, textvariable=book_var, state="readonly")
        dropdown.pack(pady=5)

        def confirm_return():
            selected_title = book_var.get()
            book = next((b for b in self.user.borrowed_books if b.title == selected_title), None)
            if book and self.user.return_book(book):
                messagebox.showinfo("Success", f"You returned '{book.title}'")
                top.destroy()
                self.load_books()
                self.update_borrowed_books()

        tk.Button(top, text="Return", command=confirm_return).pack(pady=10)

    # Update Borrowed Books Label
    def update_borrowed_books(self):
        if self.user.borrowed_books:
            borrowed_list = "\n".join([f"- {book.title}" for book in self.user.borrowed_books])
            self.borrowed_label.config(text=f"{self.user.name} already borrowed:\n{borrowed_list}")
        else:
            self.borrowed_label.config(text=f"{self.user.name} has not borrowed any books yet.")


# ------------------ Login Window ------------------
class LoginWindow:
    def __init__(self, root, library):
        self.root = root
        self.library = library
        self.root.title("Login / Sign Up")
        self.root.geometry("300x200")

        tk.Label(root, text="Enter Your Name:").pack(pady=5)
        self.name_entry = tk.Entry(root, width=25)
        self.name_entry.pack(pady=5)

        tk.Label(root, text="Enter Your Degree:").pack(pady=5)
        self.degree_entry = tk.Entry(root, width=25)
        self.degree_entry.pack(pady=5)

        tk.Button(root, text="Login", command=self.login_user).pack(pady=10)

    def login_user(self):
        name = self.name_entry.get().strip()
        degree = self.degree_entry.get().strip()

        if not name or not degree:
            messagebox.showerror("Error", "Please fill all fields")
            return

        if degree.upper() != "BS AI":
            messagebox.showerror("Access Denied", "Only BS AI students are allowed!")
            return

        user = self.library.get_user(name, degree)
        self.root.destroy()

        # Open main library window
        main_root = tk.Tk()
        app = LibraryApp(main_root, self.library, user)
        main_root.mainloop()


# ------------------ Run Application ------------------
if __name__ == "__main__":
    library = Library()

    # --- 20 AI Related Books ---
    ai_books = [
        ("Artificial Intelligence: A Modern Approach", "Stuart Russell & Peter Norvig"),
        ("Deep Learning", "Ian Goodfellow, Yoshua Bengio, Aaron Courville"),
        ("Hands-On Machine Learning with Scikit-Learn and TensorFlow", "Aurélien Géron"),
        ("Pattern Recognition and Machine Learning", "Christopher Bishop"),
        ("Reinforcement Learning: An Introduction", "Richard Sutton & Andrew Barto"),
        ("Python Machine Learning", "Sebastian Raschka"),
        ("Grokking Artificial Intelligence Algorithms", "Rishal Hurbans"),
        ("Introduction to Artificial Intelligence", "Philip C. Jackson"),
        ("Speech and Language Processing", "Daniel Jurafsky & James H. Martin"),
        ("Computer Vision: Algorithms and Applications", "Richard Szeliski"),
        ("Probabilistic Graphical Models", "Daphne Koller & Nir Friedman"),
        ("Neural Networks and Deep Learning", "Michael Nielsen"),
        ("Bayesian Reasoning and Machine Learning", "David Barber"),
        ("Artificial Intelligence for Humans", "Jeff Heaton"),
        ("Building Machine Learning Powered Applications", "Emmanuel Ameisen"),
        ("Applied Artificial Intelligence", "Mariya Yao"),
        ("Data Science for Business", "Provost & Fawcett"),
        ("AI Superpowers", "Kai-Fu Lee"),
        ("The Hundred-Page Machine Learning Book", "Andriy Burkov"),
        ("Fundamentals of Deep Learning", "Nikhil Buduma")
    ]

    for i, (title, author) in enumerate(ai_books, start=1):
        library.add_book(Book(i, title, author, quantity=5))

    root = tk.Tk()
    login = LoginWindow(root, library)
    root.mainloop()
