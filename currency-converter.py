import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk, ImageEnhance
import requests

class CurrencyConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter")
        self.root.geometry("600x600")  # Set the window size

        # Center the window on the screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_coordinate = int((screen_width / 2) - (600 / 2))
        y_coordinate = int((screen_height / 2) - (600 / 2))
        self.root.geometry(f"600x600+{x_coordinate}+{y_coordinate}")

        # Define currency symbols including additional countries
        self.currency_symbols = {
            "USD": "$",
            "EUR": "€",
            "GBP": "£",
            "JPY": "¥",
            "AUD": "A$",
            "CAD": "C$",
            "CHF": "CHF",
            "CNY": "¥",
            "SEK": "kr",
            "NZD": "NZ$",
            "PKR": "₨",      # Pakistan Rupee
            "AED": "د.إ",    # UAE Dirham
            "SAR": "ر.س",    # Saudi Riyal
            # Add more currencies and their symbols as needed
        }

        # Load and enhance background image
        self.bg_image = Image.open("money.png")  # or "moneyy.png"
        self.bg_image = self.bg_image.resize((600, 600), Image.LANCZOS)  # Resize to fit the new width
        
        # Enhance the image to make it lighter
        enhancer = ImageEnhance.Brightness(self.bg_image)
        self.bg_image = enhancer.enhance(0.5)  # Adjust brightness (0.5 makes it lighter)
        
        self.bg_image = ImageTk.PhotoImage(self.bg_image)

        # Create a label to hold the background image
        self.bg_label = tk.Label(self.root, image=self.bg_image)
        self.bg_label.place(relwidth=1, relheight=1)  # Set to cover the entire window

        # Create a frame on top of the background image
        self.frame_initial = tk.Frame(self.root, bg="#FFFFFF", bd=5, relief=tk.RAISED)
        self.frame_initial.place(relwidth=0.8, relheight=0.3, relx=0.1, rely=0.05)  # Centered with adjusted size

        self.show_initial_screen()

    def show_initial_screen(self):
        titleLabel = tk.Label(self.frame_initial, text="Currency Converter", font=("Arial Black", 20, "bold"), bg="#FFFFFF", fg="#00695C")
        titleLabel.pack(pady=10)

        startButton = tk.Button(self.frame_initial, text="Start Conversion", width=20, height=2, font=("Arial Black", 12), bg="#009688", fg="white", relief=tk.RAISED, borderwidth=5, command=self.show_conversion_screen)
        startButton.pack(pady=10)

    def show_conversion_screen(self):
        self.frame_initial.destroy()
        self.frame_conversion = tk.Frame(self.root, bg="#FFFFFF", bd=5, relief=tk.RAISED)
        self.frame_conversion.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)  # Centered with adjusted size

        titleLabel = tk.Label(self.frame_conversion, text="Currency Converter", font=("Arial Black", 20, "bold"), bg="#FFFFFF", fg="#00695C")
        titleLabel.pack(pady=10)

        self.amount_label = tk.Label(self.frame_conversion, text="Amount:", font=("Arial Black", 12), bg="#FFFFFF", fg="#004D40")
        self.amount_label.pack(pady=5)

        self.amount_entry = tk.Entry(self.frame_conversion, font=("Arial Black", 10), width=30, borderwidth=2, relief=tk.SOLID)
        self.amount_entry.pack(pady=5)

        self.from_currency_label = tk.Label(self.frame_conversion, text="From Currency:", font=("Arial Black", 12), bg="#FFFFFF", fg="#004D40")
        self.from_currency_label.pack(pady=5)

        self.from_currency_combobox = ttk.Combobox(self.frame_conversion, values=list(self.currency_symbols.keys()), font=("Arial Black", 10), width=25)
        self.from_currency_combobox.pack(pady=5)

        self.to_currency_label = tk.Label(self.frame_conversion, text="To Currency:", font=("Arial Black", 12), bg="#FFFFFF", fg="#004D40")
        self.to_currency_label.pack(pady=5)

        self.to_currency_combobox = ttk.Combobox(self.frame_conversion, values=list(self.currency_symbols.keys()), font=("Arial Black", 10), width=25)
        self.to_currency_combobox.pack(pady=5)

        convertButton = tk.Button(self.frame_conversion, text="Convert", command=self.convert_currency, font=("Arial Black", 12), bg="#4CAF50", fg="white", width=20)
        convertButton.pack(pady=10)

        clearButton = tk.Button(self.frame_conversion, text="Clear", command=self.clear_fields, font=("Arial Black", 12), bg="#B0BEC5", fg="black", width=20)
        clearButton.pack(pady=5)

        self.result_label = tk.Label(self.frame_conversion, text="", font=("Arial Black", 12, "bold"), bg="#FFFFFF", fg="#004D40")
        self.result_label.pack(pady=10)

    def convert_currency(self):
        amount = self.amount_entry.get()
        from_currency = self.from_currency_combobox.get()
        to_currency = self.to_currency_combobox.get()

        if not amount or not from_currency or not to_currency:
            messagebox.showerror("Input Error", "Please fill all fields")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for amount")
            return

        url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            conversion_rate = data['rates'][to_currency]
            converted_amount = amount * conversion_rate

            from_symbol = self.currency_symbols.get(from_currency, "")
            to_symbol = self.currency_symbols.get(to_currency, "")

            self.result_label.config(text=f"{from_symbol}{amount} {from_currency} = {to_symbol}{converted_amount:.2f} {to_currency}")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to get conversion rate. Please check your internet connection.\n{str(e)}")

    def clear_fields(self):
        self.amount_entry.delete(0, tk.END)
        self.from_currency_combobox.set("")
        self.to_currency_combobox.set("")
        self.result_label.config(text="")

if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyConverterApp(root)
    root.mainloop()
