# Import required libraries
import tkinter as tk
from tkinter import messagebox
import requests

# Base URL for the PotterDB API
API_BASE_URL = "https://api.potterdb.com/v1/"


# Main application class
class HarryPotterInfoApp:
    # Constructor method for HarryPotterInfoApp
    def __init__(self, root):
        self.root = root 
        self.root.title("Harry Potter Info App")
        self.root.geometry("800x600")

        # Create a container frame for pages
        self.container = tk.Frame(self.root)
        self.container.pack(fill="both", expand=True)

        # Dictionary to store frames
        self.frames = {}

        # Create pages
        for page_class in (WelcomePage, MainAppPage, CharacterSelectPage, SpellSelectPage, MovieSelectPage, PotionSelectPage):
            frame = page_class(parent=self.container, controller=self)
            self.frames[page_class] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(WelcomePage) # Start with the WelcomePage

    
    # Show the selected frame function
    def show_frame(self, page_class):
        frame = self.frames[page_class] # Get the selected frame
        # Raise the selected frame
        if frame is not None: 
            frame.tkraise()


# Welcome page class
class WelcomePage(tk.Frame):
    # Constructor method for WelcomePage
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Background image
        background_image = tk.PhotoImage(file="./img/bg.png").subsample(1, 1)
        background_label = tk.Label(self, image=background_image)
        background_label.image = background_image
        background_label.place(width=800, height=700, anchor="nw")

        # Welcome button
        welcome_button = tk.Button(
            self,
            text="Welcome to Harry's World",
            font=("Garamond", 18, "bold"),
            command=lambda: controller.show_frame(MainAppPage),
            relief="raised",
            bg="#213555",
            fg="#F1F0E8"
        )
        welcome_button.place(relx=0.5, rely=0.6, anchor='center')


# Main application page class
class MainAppPage(tk.Frame):
    # Constructor method for MainAppPage
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Background image
        background_image = tk.PhotoImage(file="./img/bg2.png").subsample(1, 1)
        background_label = tk.Label(self, image=background_image)
        background_label.image = background_image
        background_label.place(width=800, height=700, anchor="nw")

        # Movies button
        self.fetch_movies_button = tk.Button(
            self, text="Movies", command=self.show_movies,
            width=20, height=2, font=("Garamond", 14, "bold"),
            bg="#8E1616", fg="#FFD65A"
        )
        self.fetch_movies_button.place(relx=0.5, rely=0.18, anchor='center')

        # Characters button
        self.fetch_characters_button = tk.Button(
            self, text="Characters", command=self.show_characters,
            width=20, height=2, font=("Garamond", 14, "bold"),
            bg="#8E1616", fg="#FFD65A"
        )
        self.fetch_characters_button.place(relx=0.5, rely=0.32, anchor='center')

        # Spells button
        self.fetch_spells_button = tk.Button(
            self, text="Spells", command=self.show_spells,
            width=20, height=2, font=("Garamond", 14, "bold"),
            bg="#8E1616", fg="#FFD65A"
        )
        self.fetch_spells_button.place(relx=0.5, rely=0.46, anchor='center')

        # Potions button
        self.potion_button = tk.Button(
            self, text="Potions", command=self.show_potions,
            width=20, height=2, font=("Garamond", 14, "bold"),
            bg="#8E1616", fg="#FFD65A"
        )
        self.potion_button.place(relx=0.5, rely=0.60, anchor='center')

        # Exit button
        self.exit_button = tk.Button(self, text="Exit", command=self.controller.root.quit,
            width=20, height=2, font=("Garamond", 14, "bold"),
            bg="#8E1616", fg="#FFD65A"
        )
        self.exit_button.place(relx=0.5, rely=0.74, anchor='center')

    
    # Open character selection window function
    def show_characters(self):
        self.controller.show_frame(CharacterSelectPage)


    # Open spell selection window function
    def show_spells(self):
        self.controller.show_frame(SpellSelectPage)


    # Open movie selection window function
    def show_movies(self):
        self.controller.show_frame(MovieSelectPage)
    
    
    # Open potion selection window function
    def show_potions(self):
        self.controller.show_frame(PotionSelectPage)


# Movie selection page class
class MovieSelectPage(tk.Frame):
    # Constructor method for MovieSelectPage
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        """ Left Frame for Buttons """
        self.left_frame = tk.Frame(self, relief=tk.RIDGE, borderwidth=2, padx=10, pady=10, bg="#1a472a")
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Create Buttons
        self.fetch_movies_button = tk.Button(self.left_frame, text="Show All Movies", command=self.fetch_movies,
            width=15, height=2, font=("Garamond", 12, "bold"),
            bg="#2a623d", fg="#FBF5DD"
        )
        self.fetch_movies_button.pack(side=tk.TOP, pady=5)

        self.exit_button = tk.Button(self.left_frame, text="Back", command=lambda: controller.show_frame(MainAppPage),
            width=15, height=2, font=("Garamond", 12, "bold"),
            bg="#2a623d", fg="#FBF5DD"
        )
        self.exit_button.pack(side=tk.BOTTOM, pady=50)

        # Right Frame for Listbox and Details
        self.right_frame = tk.Frame(self, relief=tk.RIDGE, borderwidth=2)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Background image
        background_image = tk.PhotoImage(file="./img/bg3.png").subsample(1, 1)
        background_label = tk.Label(self.right_frame, image=background_image)
        background_label.image = background_image
        background_label.place(relwidth=1, relheight=1)

        # Listbox to show movie titles
        self.movie_listbox = tk.Listbox(self.right_frame, height=15, width=60, font=("Garamond", 12), bg="#2a623d", fg="#FBF5DD", relief=tk.RAISED, justify=tk.CENTER, highlightthickness=0, selectbackground="#2a623d", selectforeground="#FBF5DD")
        self.movie_listbox.pack(pady=(50, 20), anchor=tk.CENTER)

        # Text area for movie details
        self.movie_details_text = tk.Text(self.right_frame, wrap=tk.WORD, height=10, width=60, bg="#2a623d", fg="#FBF5DD")
        self.movie_details_text.pack(padx=10, pady=50, anchor=tk.CENTER)

        # Initialize movie list
        self.movies = []

        # Bind event to handle movie selection
        self.movie_listbox.bind('<<ListboxSelect>>', self.on_movie_select)
        

    # Function to fetch movies
    def fetch_movies(self):
        try:
            # Fetch movies from API
            response = requests.get("https://api.potterdb.com/v1/movies")
            response.raise_for_status()
            movies = response.json()["data"] # Store movies here
            
            # Update movie list
            self.movies = movies 
            self.movie_listbox.delete(0, tk.END) # Clear the listbox

            # If no movies found, show a message
            if not movies:
                messagebox.showinfo("No Results", "No movies found.")
                return

            # Add movies to the listbox
            for movie in movies:
                self.movie_listbox.insert(tk.END, movie["attributes"]["title"])
                
        # Handle exceptions and show an error message
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch movies: {e}")


    # Function to handle movie selection and display details
    def on_movie_select(self, event):
        selected_index = self.movie_listbox.curselection()
        if not selected_index:
            return

        selected_title = self.movie_listbox.get(selected_index)

        # Find the selected movie in the list
        selected_movie = next(
            (movie for movie in self.movies if movie.get('attributes', {}).get('title') == selected_title), None
        )

        # Display movie details using a formatted string
        if selected_movie:
            details = '\n'.join(
                f"{key.capitalize()}: {value}" for key, value in selected_movie['attributes'].items()
            )
            self.movie_details_text.delete(1.0, tk.END)
            self.movie_details_text.insert(tk.END, details)
        else:
            messagebox.showinfo("Movie Not Found", "Movie details not available.")


# Character selection page class
class CharacterSelectPage(tk.Frame):
    # Constructor method for CharacterSelectPage
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.characters = []  # Store fetched characters here

        """ Left Frame For Buttons """
        self.left_frame = tk.Frame(self, relief=tk.RIDGE, borderwidth=2, padx=10, pady=10, bg="#740001")
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Button to fetch characters
        tk.Button(self.left_frame, text="Show All Characters", command=self.fetch_characters, width=15, height=2, font=("Garamond", 12, "bold"), bg="#ae0001", fg="#eeba30").pack(side=tk.TOP, pady=10)
        
        # Button to go back
        tk.Button(self.left_frame, text="Back", command=lambda: controller.show_frame(MainAppPage), width=15, height=2, font=("Garamond", 12, "bold"), bg="#ae0001", fg="#eeba30").pack(side=tk.BOTTOM, pady=50)
        
        
        """ Right Frame For Listbox and Details """
        self.character_right_frame = tk.Frame(self, relief=tk.RIDGE, borderwidth=2)
        self.character_right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20)
        
        # Background image
        background_image = tk.PhotoImage(file="./img/bg4.png").subsample(1, 1)
        background_label = tk.Label(self.character_right_frame, image=background_image)
        background_label.image = background_image
        background_label.place(relwidth=1, relheight=1)

        # Frame to show filters
        self.character_filters_frame = tk.Frame(self.character_right_frame, relief=tk.RIDGE, borderwidth=2, bg="#740001", width=100)
        self.character_filters_frame.pack(side=tk.TOP, fill=tk.X, expand=True)

        # Filters
        tk.Label(self.character_filters_frame, text="Page:", font=("Garamond", 12, "bold"), bg="#740001", fg="#eeba30").pack(side=tk.LEFT, padx=5)
        self.page_entry = tk.Entry(self.character_filters_frame, width=5, bg="#d3a625", fg="#000000")
        self.page_entry.pack(side=tk.LEFT, padx=5)
        self.page_entry.insert(0, "1")  # Default page is 1

        tk.Label(self.character_filters_frame, text="Filter by Name:", font=("Garamond", 12, "bold"), bg="#740001", fg="#eeba30").pack(side=tk.LEFT, padx=5)
        self.name_entry = tk.Entry(self.character_filters_frame, width=15, bg="#d3a625", fg="#000000")
        self.name_entry.pack(side=tk.LEFT, padx=5)

        tk.Button(self.character_filters_frame, text="Apply Filter", command=self.apply_filter,
                  font=("Garamond", 12, "bold"), bg="#ae0001", fg="#eeba30").pack(side=tk.RIGHT, padx=5, pady=5)

        # Listbox to show characters
        self.character_listbox = tk.Listbox(self.character_right_frame, height=15, width=70, font=("Garamond", 12), bg="#ae0001", fg="#eeba30", relief=tk.RAISED, justify=tk.CENTER, highlightthickness=0, selectbackground="#ae0001", selectforeground="#eeba30")
        self.character_listbox.pack(pady=(10, 40), anchor=tk.CENTER, expand=True)

        # Text widget to show character details
        self.character_details_text = tk.Text(self.character_right_frame, wrap=tk.WORD, height=10, width=70, bg="#ae0001", fg="#eeba30")
        self.character_details_text.pack(padx=10, pady=50, anchor=tk.CENTER, expand=True)

        # Bind events 
        self.character_listbox.bind('<<ListboxSelect>>', self.on_character_select)
        self.page_entry.bind("<Return>", lambda event: self.fetch_characters())


    # Apply filter function
    def apply_filter(self):
        name_filter = self.name_entry.get().strip().lower()

        params = {}

        if name_filter:
            # Use 'name_cont' for partial name match as per API example
            params["filter[name_cont]"] = name_filter

        if not params:
            messagebox.showinfo("Filter", "Please enter a name to filter.")
            return

        try:
            # Fetch data from the API with filters applied
            url = f"https://api.potterdb.com/v1/characters"
            response = requests.get(url, params=params)
            response.raise_for_status()
            filtered_characters = response.json().get("data", [])

            # Update the listbox with filtered characters
            self.character_listbox.delete(0, tk.END)

            if not filtered_characters:
                messagebox.showinfo("No Results", "No characters found with the selected filters.")
                return

            for char in filtered_characters:
                self.character_listbox.insert(
                    tk.END, char.get('attributes', {}).get('name', 'Unknown')
                )
            self.characters = filtered_characters  # Save filtered characters
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply filter: {e}")

    
    # Fetch characters for a specific page function
    def fetch_characters(self):
        page = self.page_entry.get()
        if not page.isdigit() or int(page) < 1:
            messagebox.showwarning("Input Error", "Please enter a valid page number.")
            return

        try:
            response = requests.get(f"https://api.potterdb.com/v1/characters?page[number]={page}")
            response.raise_for_status()
            self.characters = response.json().get("data", [])  # Store characters here

            self.character_listbox.delete(0, tk.END)

            if not self.characters:
                messagebox.showinfo("No Results", "No characters found on this page.")
                return

            for char in self.characters:
                self.character_listbox.insert(
                    tk.END, char.get('attributes', {}).get('name', 'Unknown')
                )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch characters: {e}")

    
    # Display character details function
    def on_character_select(self, event):
        selected_index = self.character_listbox.curselection()
        if not selected_index:
            return

        # Get the selected character
        selected_name = self.character_listbox.get(selected_index)
        selected_character = next(
            (char for char in self.characters if char.get("attributes", {}).get("name") == selected_name), None
        )

        # Display character details
        if selected_character:
            details = "\n".join(
                f"{key}: {', '.join(value) if isinstance(value, list) else value}"
                for key, value in selected_character.get("attributes", {}).items()
            )
            self.character_details_text.delete(1.0, tk.END)
            self.character_details_text.insert(tk.END, details)
        else:
            messagebox.showinfo("Character Not Found", "Character details not available.")


# Spell selection page class
class SpellSelectPage(tk.Frame):
    # Constructor function for SpellSelectPage
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.spells = []  # Store fetched spells here

        # Left Frame for Buttons
        self.left_frame = tk.Frame(self, relief=tk.RIDGE, borderwidth=2, padx=10, pady=10, bg="#ecb939")
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.fetch_button = tk.Button(self.left_frame, text="Show All Spells", command=self.fetch_spells, width=15, height=2, font=("Garamond", 12, "bold"), bg="#f0c75e", fg="#726255")
        self.fetch_button.pack(side=tk.TOP, pady=10)

        self.exit_button = tk.Button(self.left_frame, text="Back", command=lambda: controller.show_frame(MainAppPage), width=15, height=2, font=("Garamond", 12, "bold"), bg="#f0c75e", fg="#726255")
        self.exit_button.pack(side=tk.BOTTOM, pady=50)
        
        # Right Frame for Details
        self.spell_right_frame = tk.Frame(self, relief=tk.RIDGE, borderwidth=2)
        self.spell_right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20)
        
        # Background image
        background_image = tk.PhotoImage(file="./img/bg5.png").subsample(1, 1)
        background_label = tk.Label(self.spell_right_frame, image=background_image)
        background_label.image = background_image
        background_label.place(relwidth=1, relheight=1)
        
        # Frame for Filters
        self.filter_frame = tk.Frame(self.spell_right_frame, relief=tk.RIDGE, borderwidth=2, bg="#ecb939", width=100)
        self.filter_frame.pack(side=tk.TOP, fill=tk.X, expand=True)
        
        # Page Entry
        self.page_label = tk.Label(self.filter_frame, text="Page:", font=("Garamond", 12, "bold"), bg="#ecb939", fg="#372e29")
        self.page_label.pack(side=tk.LEFT, padx=5)
        self.page_entry = tk.Entry(self.filter_frame, width=5, bg="#372e29", fg="#ecb939")
        self.page_entry.pack(side=tk.LEFT, padx=5)
        self.page_entry.insert(0, "1")  # Default page is 1

        # Name Filter
        self.name_label = tk.Label(self.filter_frame, text="Filter by Spell Name:", font=("Garamond", 12, "bold"), bg="#ecb939", fg="#372e29")
        self.name_label.pack(side=tk.LEFT, padx=5)
        self.name_entry = tk.Entry(self.filter_frame, width=15, bg="#372e29", fg="#ecb939")
        self.name_entry.pack(side=tk.LEFT, padx=5)
        
        self.filter_button = tk.Button(self.filter_frame, text="Apply Filter", command=self.apply_filter, font=("Garamond", 12, "bold"), bg="#f0c75e", fg="#726255")
        self.filter_button.pack(side=tk.RIGHT, padx=5, pady=5)

        # Listbox to show spells
        self.spell_listbox = tk.Listbox(self.spell_right_frame, height=15, width=70, font=("Garamond", 12), bg="#ecb939", fg="#372e29", relief=tk.RAISED, justify=tk.CENTER, highlightthickness=0, selectbackground="#ecb939", selectforeground="#372e29")
        self.spell_listbox.pack(pady=(10, 40), anchor=tk.CENTER, expand=True)

        # Spell Details Text
        self.spell_details_text = tk.Text(self.spell_right_frame, wrap=tk.WORD, height=10, width=70, bg="#ecb939", fg="#372e29")
        self.spell_details_text.pack(padx=10, pady=50, anchor=tk.CENTER, expand=True)

        # Bind selection event
        self.spell_listbox.bind('<<ListboxSelect>>', self.on_spell_select)
        self.page_entry.bind("<Return>", lambda event: self.fetch_spells())

    
    # Apply filter function
    def apply_filter(self):
        # Get the spell name filter
        name_filter = self.name_entry.get().strip().lower()
        # Fetch spells based on the filter
        if not name_filter:
            messagebox.showinfo("Filter", "Please enter a spell name filter.")
            return

        # Make the API request
        try:
            response = requests.get(f"{API_BASE_URL}spells", params={"filter[name_cont]": name_filter})
            response.raise_for_status()
            filtered_spells = response.json().get("data", [])

            # Clear the listbox and update it with the filtered spells
            self.spell_listbox.delete(0, tk.END)
            if not filtered_spells:
                messagebox.showinfo("No Results", "No spells found with the selected filters.")
                return

            # Insert the filtered spells into the listbox
            self.spell_listbox.insert(tk.END, *[spell.get('attributes', {}).get('name', 'Unknown') for spell in filtered_spells])
            self.spells = filtered_spells
        
        # Handle errors and show an error message
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply filter: {e}")

    
    # Fetch and display a list of spells
    def fetch_spells(self):
        try:
            page = int(self.page_entry.get())
            if page < 1:
                raise ValueError
            response = requests.get(f"{API_BASE_URL}spells?page[number]={page}") # Make the API request
            response.raise_for_status()
            self.spells = response.json().get("data", [])  # Store spells here

            self.spell_listbox.delete(0, tk.END)

            # If no spells found, show a message and return
            if not self.spells:
                messagebox.showinfo("No Results", "No spells found on this page.")
                return

            # Insert the spells into the listbox
            self.spell_listbox.insert(tk.END, *[spell.get('attributes', {}).get('name', 'Unknown') for spell in self.spells])
            
        # Handle errors and show an error message
        except (ValueError, Exception) as e:
            messagebox.showerror("Error", f"Failed to fetch spells: {e}")

    
    # Spell selection event handler
    def on_spell_select(self, event):
        selected_index = self.spell_listbox.curselection() # Get the selected index
        if not selected_index:
            return

        # Get the selected spell
        selected_name = self.spell_listbox.get(selected_index)
        selected_spell = next((s for s in self.spells if s["attributes"]["name"] == selected_name), None)

        # Display spell details in the text box
        if selected_spell:
            attributes = selected_spell["attributes"]
            details = "\n".join(f"{k.capitalize()}: {v}" for k, v in attributes.items())
            self.spell_details_text.delete(1.0, tk.END)
            self.spell_details_text.insert(tk.END, details)

        # If the spell is not found, show a message
        else:
            messagebox.showinfo("Spell Not Found", "Spell details not available.")


# Potion selection page class
class PotionSelectPage(tk.Frame):
    # Constructor function for PotionSelectPage
    def __init__(self, parent, controller):
        # Initialize the parent class
        super().__init__(parent)
        self.controller = controller
        self.potions = []  # Store fetched potions here
        self.current_page = 1  # Default starting page

        """ Left Frame for Buttons """
        self.left_frame = tk.Frame(self, relief=tk.RIDGE, borderwidth=2, padx=10, pady=10, bg="#0e1a40")
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)
        # Fetch Button
        self.fetch_button = tk.Button(self.left_frame, text="Show All Potions", command=self.fetch_potions, width=15, height=2, font=("Garamond", 12, "bold"), bg="#222f5b", fg="#5d5d5d")
        self.fetch_button.pack(side=tk.TOP, padx=10, pady=5)
        # Exit Button
        self.exit_button = tk.Button(self.left_frame, text="Back", command=lambda: controller.show_frame(MainAppPage), width=15, height=2, font=("Garamond", 12, "bold"), bg="#222f5b", fg="#5d5d5d")
        self.exit_button.pack(side=tk.BOTTOM, padx=10, pady=50)

        """ Right Frame for Listbox and Details """
        self.potion_right_frame = tk.Frame(self, relief=tk.RIDGE, borderwidth=2)
        self.potion_right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Background image
        background_image = tk.PhotoImage(file="./img/bg6.png").subsample(1, 1)
        background_label = tk.Label(self.potion_right_frame, image=background_image)
        background_label.image = background_image
        background_label.place(relwidth=1, relheight=1)

        # Frame for pagination and filter
        self.pagination_frame = tk.Frame(self.potion_right_frame, relief=tk.RIDGE, borderwidth=2, bg="#0e1a40", width=50)
        self.pagination_frame.pack(side=tk.TOP, fill=tk.X, expand=True)

        # Navigation Arrows for Pagination
        self.prev_button = tk.Button(self.pagination_frame, text="←", command=self.prev_page, pady=5, font=("Garamond", 12, "bold"), bg="#222f5b", fg="#5d5d5d")
        self.prev_button.pack(side=tk.LEFT)
        self.page_label = tk.Label(self.pagination_frame, text=f"Page: {self.current_page}", font=("Garamond", 12, "bold"), bg="#0e1a40", fg="#5d5d5d")
        self.page_label.pack(side=tk.LEFT, padx=5)
        self.next_button = tk.Button(self.pagination_frame, text="→", command=self.next_page, pady=5, font=("Garamond", 12, "bold"), bg="#222f5b", fg="#5d5d5d")
        self.next_button.pack(side=tk.LEFT)

        # Name Filter
        self.name_label = tk.Label(self.pagination_frame, text="Filter by Potion Name:", font=("Garamond", 12, "bold"), bg="#0e1a40", fg="#5d5d5d")
        self.name_label.pack(side=tk.LEFT, padx=5)
        self.name_entry = tk.Entry(self.pagination_frame, font=("Garamond", 12), bg="#946b2d", fg="#000000")
        self.name_entry.pack(side=tk.LEFT, padx=5)
        # Filter Button
        self.filter_button = tk.Button(self.pagination_frame, text="Apply Filter", command=self.apply_filter, font=("Garamond", 12, "bold"), bg="#222f5b", fg="#5d5d5d")
        self.filter_button.pack(side=tk.RIGHT, padx=5, pady=5)

        # Listbox to show potions
        self.potion_listbox = tk.Listbox(self.potion_right_frame, height=15, width=70, font=("Garamond", 12), bg="#222f5b", fg="#5d5d5d", relief=tk.RAISED, justify=tk.CENTER, highlightthickness=0, selectbackground="#222f5b", selectforeground="#5d5d5d")
        self.potion_listbox.pack(pady=(10, 40), anchor=tk.CENTER, expand=True)

        # Text area for potion details
        self.potion_details_text = tk.Text(self.potion_right_frame, wrap=tk.WORD, height=10, width=70, bg="#222f5b", fg="#5d5d5d")
        self.potion_details_text.pack(padx=10, pady=50, anchor=tk.CENTER, expand=True)

        # Bind selection event
        self.potion_listbox.bind('<<ListboxSelect>>', self.on_potion_select)


    # Previous Page Function
    def prev_page(self):
        # Navigate to the previous page
        if self.current_page > 1:
            self.current_page -= 1
            self.page_label.config(text=f"Page: {self.current_page}")
            self.fetch_potions()


    # Next Page Function
    def next_page(self):
        # Navigate to the next page
        self.current_page += 1
        self.page_label.config(text=f"Page: {self.current_page}")
        self.fetch_potions()


    # Apply Filter Function
    def apply_filter(self):
        name_filter = self.name_entry.get().strip().lower() # Get the name filter
        if not name_filter:
            messagebox.showinfo("Filter", "Please enter a potion name filter.")
            return

        try:
            response = requests.get(f"https://api.potterdb.com/v1/potions?filter[name_cont]={name_filter}") # Make the API request
            response.raise_for_status()
            filtered_potions = response.json().get("data", []) # Store filtered potions here

            self.potion_listbox.delete(0, tk.END)

            # Update the listbox with filtered potions
            if not filtered_potions:
                messagebox.showinfo("No Results", "No potions found with the selected filters.")
                return

            # Insert the filtered potions into the listbox
            for potion in filtered_potions:
                self.potion_listbox.insert(tk.END, potion.get('attributes', {}).get('name', 'Unknown'))
            self.potions = filtered_potions
            
        # Handle errors and show an error message
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply filter: {e}")
    
    
    # Fetch Potions Function
    def fetch_potions(self):
        try:
            response = requests.get(f"https://api.potterdb.com/v1/potions?page[number]={self.current_page}") # Make the API request
            response.raise_for_status() # Raise an exception if the request fails
            self.potions = response.json().get("data", []) # Store potions here

            self.potion_listbox.delete(0, tk.END)

            # If no potions found, show a message and return
            if not self.potions:
                messagebox.showinfo("No Results", "No potions found on this page.")
                return
            # Insert the potions into the listbox
            self.potion_listbox.insert(tk.END, *[p.get('attributes', {}).get('name', 'Unknown') for p in self.potions])
        
        # Handle errors and show an error message
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch potions: {e}")

    
    # Potion Selection Function
    def on_potion_select(self, event):
        selected_index = self.potion_listbox.curselection() # Get the selected index
        # If no index is selected, return
        if not selected_index:
            return

        # Get the selected potion
        selected_potion = next(
            (p for p in self.potions if p['attributes']['name'] == self.potion_listbox.get(selected_index)),
            None
        )
        # Display potion details in the text box when a potion is selected
        if selected_potion:
            details = "\n".join(f"{k}: {v}" for k, v in selected_potion['attributes'].items())
            self.potion_details_text.delete(1.0, tk.END)
            self.potion_details_text.insert(tk.END, details)
        # If the potion is not found, show a message
        else:
            messagebox.showinfo("Potion Not Found", "Potion details not available.")
            

# Main function to run the application            
if __name__ == "__main__":
    root = tk.Tk() 
    root.resizable(False, False) # Prevent window resizing
    app = HarryPotterInfoApp(root)
    root.mainloop() # Start the main loop
    