@@ -1,135 +1,81 @@
import pandas as pd
import spacy
import tkinter as tk
from tkinter import messagebox

# Load the NLP model
nlp = spacy.load("en_core_web_sm")

# Load the dataset
try:
    df = pd.read_csv('mediiii.csv')
    if df.empty:
        raise ValueError("The CSV file is empty.")
    if not all(col in df.columns for col in ['symptom', 'medicine', 'dosage']):
        raise ValueError("The CSV file must contain 'symptom', 'medicine', and 'dosage' columns.")
except FileNotFoundError:
    print("Error: mediiii.csv file not found.")
    exit()
except ValueError as e:
    print(f"Error: {e}")
    exit()
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    exit()
df = pd.read_csv('mediiii.csv')

# Function to preprocess text using NLP and extract symptoms
def extract_symptoms(user_input):
    doc = nlp(user_input.lower())
    extracted_symptoms = []
    for token in doc:
        if token.text in df['symptom'].str.lower().tolist():
            extracted_symptoms.append(token.text)
    return extracted_symptoms

# Function to get recommended medicine based on symptoms
def recommend_medicine(selected_symptoms):
    filtered_df = df[df['symptom'].str.lower().apply(
        lambda x: any(sym.lower() in x for sym in selected_symptoms))]
    print(f"Filtering for symptoms: {', '.join(selected_symptoms)}")
    filtered_df = df[df['symptom'].str.lower().isin([sym.lower() for sym in selected_symptoms])]
    print(f"Filtered DataFrame:\n{filtered_df}")
    if not filtered_df.empty:
        medicine = filtered_df.iloc[0]['medicine']
        dosage = filtered_df.iloc[0]['dosage']
        return medicine, dosage
    else:
        return None, "No recommendation found. Please consult a doctor."

# Function to list all available medicines
def list_all_medicines():
    return df['medicine'].unique().tolist()

# Function to get details of a specific medicine
def specific_medicine(medicine_name):
    filtered_df = df[df['medicine'].str.lower() == medicine_name.lower()]
    if not filtered_df.empty:
        return "\n".join([f"{key}: {value}" for key, value in filtered_df.iloc[0].to_dict().items()])
    else:
        return "Medicine not found. Please consult a doctor."

# Tkinter UI setup
class MedicineBotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Medicine Recommendation Bot")
        self.root.title("Medicine Recommendation Bot with NLP")
        self.root.geometry("800x650")
        self.root.configure(bg="#ADD8E6")

        self.symptoms_set = df['symptom'].unique().tolist()  # Dynamic symptoms list
        self.homepage()

    def homepage(self):
        self.clear_frame()

        self.label = tk.Label(self.root, text="Medicine Recommendation Bot", font=("Helvetica", 16, "bold"), bg="#ADD8E6")
        self.label = tk.Label(self.root, text="Medicine Recommendation Bot with NLP", font=("Helvetica", 16, "bold"), bg="#ADD8E6")
        self.label.pack(pady=10)

        self.choice_label = tk.Label(self.root, text="Would you like to take a specific medicine or get a recommendation based on symptoms?", font=("Helvetica", 12), bg="#ADD8E6")
        self.choice_label = tk.Label(self.root, text="Would you like to get a recommendation based on symptoms?", font=("Helvetica", 12), bg="#ADD8E6")
        self.choice_label.pack(pady=5)

        self.choice_var = tk.StringVar(value="medicine")
        self.medicine_radio = tk.Radiobutton(self.root, text="Medicine", variable=self.choice_var, value="medicine", bg="#ADD8E6", font=("Helvetica", 12))
        self.medicine_radio.pack(anchor="w", padx=20)

        self.symptoms_radio = tk.Radiobutton(self.root, text="Symptoms", variable=self.choice_var, value="symptoms", bg="#ADD8E6", font=("Helvetica", 12))
        self.symptoms_radio.pack(anchor="w", padx=20)

        self.continue_button = tk.Button(self.root, text="Continue", command=self.next_step, font=("Helvetica", 12, "bold"), bg="#32CD32", fg="white")
        self.continue_button.pack(pady=20)
        self.symptom_input_label = tk.Label(self.root, text="Enter your symptoms (e.g., 'I have a headache and nausea'):", font=("Helvetica", 12), bg="#ADD8E6")
        self.symptom_input_label.pack(pady=5)

    def next_step(self):
        choice = self.choice_var.get()
        if choice == "medicine":
            self.medicine_step()
        elif choice == "symptoms":
            self.symptoms_step()

    def medicine_step(self):
        self.clear_frame()
        self.symptom_input = tk.Entry(self.root, width=50, font=("Helvetica", 12))
        self.symptom_input.pack(pady=5)

        self.medicine_label = tk.Label(self.root, text="Please select the medicine:", font=("Helvetica", 12), bg="#ADD8E6")
        self.medicine_label.pack(pady=5)

        # Dropdown menu for medicines
        medicines = list_all_medicines()
        self.medicine_var = tk.StringVar(value=medicines[0])
        self.medicine_menu = tk.OptionMenu(self.root, self.medicine_var, *medicines)
        self.medicine_menu.config(font=("Helvetica", 12), bg="#ADD8E6")
        self.medicine_menu.pack(pady=5)

        self.submit_button = tk.Button(self.root, text="Submit", command=self.show_medicine, font=("Helvetica", 12, "bold"), bg="#32CD32", fg="white")
        self.submit_button = tk.Button(self.root, text="Submit", command=self.process_symptoms, font=("Helvetica", 12, "bold"), bg="#32CD32", fg="white")
        self.submit_button.pack(pady=20)

        self.back_button = tk.Button(self.root, text="Back", command=self.homepage, font=("Helvetica", 12, "bold"), bg="#FF4500", fg="white")
        self.back_button.pack(pady=10)

    def show_medicine(self):
        medicine_name = self.medicine_var.get()
        medicine_details = specific_medicine(medicine_name)
        messagebox.showinfo("Medicine Details", medicine_details)

    def symptoms_step(self):
        self.clear_frame()
        self.quit_button = tk.Button(self.root, text="Quit", command=self.root.quit, font=("Helvetica", 12, "bold"), bg="#FF4500", fg="white")
        self.quit_button.pack(pady=10)

        self.symptom_label = tk.Label(self.root, text="Please select your symptoms:", font=("Helvetica", 12), bg="#ADD8E6")
        self.symptom_label.pack(pady=5)

        # Checkboxes for symptoms
        self.selected_symptoms = []
        self.checkbuttons = []
        for symptom in self.symptoms_set:
            var = tk.StringVar()
            chk = tk.Checkbutton(self.root, text=symptom, variable=var, onvalue=symptom, offvalue="", bg="#ADD8E6", font=("Helvetica", 12))
            chk.pack(anchor="w", padx=20)
            self.checkbuttons.append((chk, var))
        self.submit_button = tk.Button(self.root, text="Submit", command=self.show_recommendation, font=("Helvetica", 12, "bold"), bg="#32CD32", fg="white")
        self.submit_button.pack(pady=20)

        self.back_button = tk.Button(self.root, text="Back", command=self.homepage, font=("Helvetica", 12, "bold"), bg="#FF4500", fg="white")
        self.back_button.pack(pady=10)

    def show_recommendation(self):
        self.selected_symptoms = [var.get() for chk, var in self.checkbuttons if var.get()]
        if not self.selected_symptoms:
            messagebox.showerror("Error", "Please select at least one symptom.")
    def process_symptoms(self):
        user_input = self.symptom_input.get()
        if not user_input.strip():
            messagebox.showerror("Error", "Please enter your symptoms.")
            return
        medicine, dosage = recommend_medicine(self.selected_symptoms)
        messagebox.showinfo("Recommendation", f"For {', '.join(self.selected_symptoms)}, I recommend {medicine} with a dosage of {dosage}.")

        extracted_symptoms = extract_symptoms(user_input)
        if not extracted_symptoms:
            messagebox.showerror("Error", "No recognizable symptoms found. Please try again.")
        else:
            medicine, dosage = recommend_medicine(extracted_symptoms)
            if medicine:
                messagebox.showinfo("Recommendation", f"Recommended medicine: {medicine}\nDosage: {dosage}")
            else:
                messagebox.showinfo("Recommendation", "No recommendation found. Please consult a doctor.")

    def clear_frame(self):
        for widget in self.root.winfo_children():
