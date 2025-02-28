import tkinter as tk
from tkinter import ttk, messagebox

from models.Loger import Loger
from models.Searcher import Searcher

searcher_in_db = Searcher()

def display_films(films):
    if not films:
        return "No Films Found"

    films_dict = {}

    for title, description, actor, year in films:
        if title not in films_dict:
            films_dict[title] = {"description": description, "year": year, "actors": []}
        films_dict[title]["actors"].append(actor)

    response = ""
    for title, info in films_dict.items():
        actors_list = ", ".join(info["actors"])
        response += f"{title}\n{info['description']}\nАктеры: {actors_list}\nГод: {info['year']}\n"
        response += "\n======================================================================\n"
    return response.strip()


def search_films():
    title = title_entry.get() or None
    genre = genre_var.get() or None
    year = year_entry.get() or None
    actor = actor_entry.get() or None
    print(title, genre, year, actor)
    try:
        results = searcher_in_db.get_films(
            title if title else None,
            genre if genre else None,
            year  if year else None,
            actor if actor else None
        )
        results_text.delete(1.0, tk.END)
        results_text.insert(tk.END, display_films(results))

    except Exception as e:
        messagebox.showerror("Ошибка", str(e))

def top_queries():
    logger = Loger()
    results_top_queries = logger.get_top_queries()

    response = "\n".join([f"{query} - {quantity}" for query, quantity in results_top_queries])

    results_text.delete(1.0, tk.END)
    results_text.insert(tk.END, response)


def recent_queries():
    logger = Loger()
    results_top_queries = logger.get_recent_queries()

    response = "\n".join([f"{query} - {date}" for query, date in results_top_queries])

    results_text.delete(1.0, tk.END)
    results_text.insert(tk.END, response)



def validate_numeric_input(P):
    return P.isdigit() or P == ""

def run():
    global title_entry, genre_var, year_entry, actor_entry, results_text
    genres = searcher_in_db.get_genres()

    root = tk.Tk()
    vcmd = root.register(validate_numeric_input)

    root.title("Поиск фильмов в Sakila")
    root.geometry("768x1024")
    root.configure(bg="grey")

    tk.Label(root, text="Название фильма:", bg="grey").pack()
    title_entry = tk.Entry(root, width=50)
    title_entry.pack()

    tk.Label(root, text="Жанр:", bg="grey").pack()
    genre_var = tk.StringVar()
    genre_dropdown = ttk.Combobox(root, textvariable=genre_var, values=genres, state="readonly")
    genre_dropdown.pack()

    tk.Label(root, text="Год выпуска:", bg="grey").pack()
    year_entry = tk.Entry(root, width=50, validate="key", validatecommand=(vcmd, "%P"))
    year_entry.pack()

    tk.Label(root, text="Актер:", bg="grey").pack()
    actor_entry = tk.Entry(root, width=50)
    actor_entry.pack()

    buttons_frame = tk.Frame(root, bg="grey")
    buttons_frame.pack(pady=5)

    search_button = tk.Button(buttons_frame, text="Искать", command=search_films, bg="white")
    search_button.pack(side="left", padx=5)

    top_queries_button = tk.Button(buttons_frame, text="Топ по рейтингу", command=top_queries, bg="white")
    top_queries_button.pack(side="left", padx=5)

    recent_queries_button = tk.Button(buttons_frame, text="Топ по дате", command=recent_queries, bg="white")
    recent_queries_button.pack(side="left", padx=5)

    results_text = tk.Text(root, height=30, width=90)
    results_text.pack()

    root.mainloop()

if __name__ == "__main__":
    run()
