import csv
import datetime


# Funkcja do wczytywania danych lekarzy z pliku CSV
def load_doctors_from_csv(filename):
    doctors = {}
    try:
        with open(filename, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                doctors[row['doctor_number']] = {
                    'password': row['password'],
                    'name': row['name']
                }
        print(f"Doctors data loaded successfully from {filename}")
    except Exception as e:
        print(f"Error reading doctors CSV: {e}")
    return doctors


# Funkcja do wczytywania danych pacjentów z pliku CSV
def load_patients_from_csv(filename):
    patients = {}
    try:
        with open(filename, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                patients[row['patient_id']] = {
                    'name': row['name'],
                    'prescribed_drugs': row['prescribed_drugs'],
                    'diseases': row['diseases']
                }
        print(f"Patients data loaded successfully from {filename}")
    except Exception as e:
        print(f"Error reading patients CSV: {e}")
    return patients


# Funkcja do wczytywania historii wydań z pliku CSV
def load_history_from_csv(filename):
    history = []
    try:
        with open(filename, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                history.append(row)
        print(f"History data loaded successfully from {filename}")
    except Exception as e:
        print(f"Error reading history CSV: {e}")
    return history


# Funkcja do wczytywania danych lekarstw z pliku CSV
def load_drugs_from_csv(filename):
    drugs = {}
    try:
        with open(filename, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                drugs[row['drug_name']] = {
                    'description': row['description'],
                    'quantity': int(row['quantity'])
                }
        print(f"Drugs data loaded successfully from {filename}")
    except Exception as e:
        print(f"Error reading drugs CSV: {e}")
    return drugs


# Funkcja do zapisywania danych pacjentów do pliku CSV
def save_patients_to_csv(filename, patients_db):
    try:
        with open(filename, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['patient_id', 'name', 'prescribed_drugs', 'diseases'])
            writer.writeheader()
            for patient_id, patient_data in patients_db.items():
                row = {'patient_id': patient_id}
                row.update(patient_data)
                writer.writerow(row)
        print(f"Patients data saved successfully to {filename}")
    except Exception as e:
        print(f"Error writing patients CSV: {e}")


# Funkcja do zapisywania historii wydań do pliku CSV
def save_history_to_csv(filename, history):
    try:
        with open(filename, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['doctor_number', 'patient_id', 'drug_name', 'quantity', 'date'])
            writer.writeheader()
            for entry in history:
                writer.writerow(entry)
        print(f"History data saved successfully to {filename}")
    except Exception as e:
        print(f"Error writing history CSV: {e}")


# Funkcja do zapisywania danych lekarstw do pliku CSV
def save_drugs_to_csv(filename, drugs_db):
    try:
        with open(filename, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['drug_name', 'description', 'quantity'])
            writer.writeheader()
            for drug_name, drug_data in drugs_db.items():
                row = {'drug_name': drug_name}
                row.update(drug_data)
                writer.writerow(row)
        print(f"Drugs data saved successfully to {filename}")
    except Exception as e:
        print(f"Error writing drugs CSV: {e}")


# Funkcja do uwierzytelniania lekarza
def authenticate(doctors_db):
    doctor_number = input("Podaj numer lekarza: ")
    password = input("Podaj hasło: ")  # Zmieniono z getpass.getpass() na input()

    if doctor_number in doctors_db and doctors_db[doctor_number]["password"] == password:
        print(f"\nWitaj, {doctors_db[doctor_number]['name']}!\n")
        return doctor_number
    else:
        print("Nieprawidłowy numer lekarza lub hasło.")
        return None


# Menu główne aplikacji
def main_menu():
    print("1. Wydać lek")
    print("2. Zobaczyć historię wydań")
    print("3. Wyszukać pacjenta")
    print("4. Dodać nowego pacjenta")
    print("5. Aktualizować informacje o pacjencie")
    print("6. Zarządzaj lekarstwami")
    print("7. Wyloguj się")


# Menu zarządzania lekarstwami
def drugs_menu():
    print("1. Dodaj nowe lekarstwo")
    print("2. Usuń lekarstwo")
    print("3. Aktualizuj informacje o lekarstwie")
    print("4. Wyświetl wszystkie lekarstwa")
    print("5. Powrót do menu głównego")


# Funkcja obsługująca wybór z menu głównego
def handle_choice(choice, doctor_number, patients_db, history, drugs_db):
    if choice == "1":
        issue_drug(doctor_number, patients_db, history, drugs_db)
    elif choice == "2":
        view_history(history)
    elif choice == "3":
        search_patient(patients_db)
    elif choice == "4":
        add_new_patient(patients_db)
    elif choice == "5":
        update_patient_info(patients_db)
    elif choice == "6":
        manage_drugs(drugs_db)
    elif choice == "7":
        print("Wylogowywanie...")
        return False
    else:
        print("Nieprawidłowy wybór, spróbuj ponownie.")
    return True


# Funkcja obsługująca wybór z menu zarządzania lekarstwami
def handle_drugs_choice(choice, drugs_db):
    if choice == "1":
        add_new_drug(drugs_db)
    elif choice == "2":
        remove_drug(drugs_db)
    elif choice == "3":
        update_drug_info(drugs_db)
    elif choice == "4":
        view_all_drugs(drugs_db)
    elif choice == "5":
        return False
    else:
        print("Nieprawidłowy wybór, spróbuj ponownie.")
    return True


# Funkcja do wydawania leku
def issue_drug(doctor_number, patients_db, history, drugs_db):
    patient_id = input("Podaj ID pacjenta: ")
    if patient_id not in patients_db:
        print("Nie znaleziono pacjenta o podanym ID.")
        return

    drug_name = input("Podaj nazwę leku: ")
    if drug_name not in drugs_db:
        print("Nie znaleziono leku o podanej nazwie.")
        return

    quantity = int(input("Podaj ilość: "))
    if quantity > drugs_db[drug_name]['quantity']:
        print(f"Niewystarczająca ilość {drug_name}. Dostępna ilość: {drugs_db[drug_name]['quantity']}.")
        return

    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    history_entry = {
        'doctor_number': doctor_number,
        'patient_id': patient_id,
        'drug_name': drug_name,
        'quantity': quantity,
        'date': date
    }
    history.append(history_entry)
    drugs_db[drug_name]['quantity'] -= quantity
    save_history_to_csv('history.csv', history)
    save_drugs_to_csv('drugs.csv', drugs_db)
    print(f"Lek {drug_name} (ilość: {quantity}) został wydany pacjentowi {patients_db[patient_id]['name']}.")


# Funkcja do przeglądania historii wydań
def view_history(history):
    for entry in history:
        print(
            f"Lekarz {entry['doctor_number']} wydał lek {entry['drug_name']} (ilość: {entry['quantity']}) pacjentowi {entry['patient_id']} dnia {entry['date']}.")


# Funkcja do wyszukiwania pacjenta
def search_patient(patients_db):
    patient_id = input("Podaj ID pacjenta: ")
    if patient_id in patients_db:
        patient = patients_db[patient_id]
        print(f"\nPacjent: {patient['name']}")
        print(f"Przepisane leki: {patient['prescribed_drugs']}")
        print(f"Choroby: {patient['diseases']}\n")
    else:
        print("Nie znaleziono pacjenta o podanym ID.")


# Funkcja do dodawania nowego pacjenta
def add_new_patient(patients_db):
    patient_id = input("Podaj ID nowego pacjenta: ")
    if patient_id in patients_db:
        print("Pacjent o takim ID już istnieje.")
        return

    name = input("Podaj imię i nazwisko pacjenta: ")
    prescribed_drugs = input("Podaj przepisane leki: ")
    diseases = input("Podaj choroby: ")

    patients_db[patient_id] = {
        'name': name,
        'prescribed_drugs': prescribed_drugs,
        'diseases': diseases
    }

    save_patients_to_csv('patients.csv', patients_db)
    print("Nowy pacjent został dodany.")


# Funkcja do aktualizowania informacji o pacjencie
def update_patient_info(patients_db):
    patient_id = input("Podaj ID pacjenta do aktualizacji: ")
    if patient_id not in patients_db:
        print("Nie znaleziono pacjenta o podanym ID.")
        return

    print("Pozostaw puste pole, aby nie zmieniać istniejącej wartości.")

    name = input(f"Podaj nowe imię i nazwisko pacjenta ({patients_db[patient_id]['name']}): ")
    prescribed_drugs = input(f"Podaj nowe przepisane leki ({patients_db[patient_id]['prescribed_drugs']}): ")
    diseases = input(f"Podaj nowe choroby ({patients_db[patient_id]['diseases']}): ")

    if name:
        patients_db[patient_id]['name'] = name
    if prescribed_drugs:
        patients_db[patient_id]['prescribed_drugs'] = prescribed_drugs
    if diseases:
        patients_db[patient_id]['diseases'] = diseases

    save_patients_to_csv('patients.csv', patients_db)
    print("Informacje o pacjencie zostały zaktualizowane.")


# Funkcja do zarządzania lekarstwami
def manage_drugs(drugs_db):
    running = True
    while running:
        drugs_menu()
        choice = input("Wybierz opcję: ")
        running = handle_drugs_choice(choice, drugs_db)
        print()


# Funkcja do dodawania nowego lekarstwa
def add_new_drug(drugs_db):
    drug_name = input("Podaj nazwę nowego lekarstwa: ")
    if drug_name in drugs_db:
        print("Lekarstwo o takiej nazwie już istnieje.")
        return

    description = input("Podaj opis lekarstwa: ")
    quantity = int(input("Podaj ilość: "))

    drugs_db[drug_name] = {
        'description': description,
        'quantity': quantity
    }

    save_drugs_to_csv('drugs.csv', drugs_db)
    print("Nowe lekarstwo zostało dodane.")


# Funkcja do usuwania lekarstwa
def remove_drug(drugs_db):
    drug_name = input("Podaj nazwę lekarstwa do usunięcia: ")
    if drug_name not in drugs_db:
        print("Nie znaleziono lekarstwa o podanej nazwie.")
        return

    del drugs_db[drug_name]
    save_drugs_to_csv('drugs.csv', drugs_db)
    print("Lekarstwo zostało usunięte.")


# Funkcja do aktualizowania informacji o lekarstwie
def update_drug_info(drugs_db):
    drug_name = input("Podaj nazwę lekarstwa do aktualizacji: ")
    if drug_name not in drugs_db:
        print("Nie znaleziono lekarstwa o podanej nazwie.")
        return

    print("Pozostaw puste pole, aby nie zmieniać istniejącej wartości.")

    description = input(f"Podaj nowy opis lekarstwa ({drugs_db[drug_name]['description']}): ")
    quantity = input(f"Podaj nową ilość lekarstwa ({drugs_db[drug_name]['quantity']}): ")

    if description:
        drugs_db[drug_name]['description'] = description
    if quantity:
        drugs_db[drug_name]['quantity'] = int(quantity)

    save_drugs_to_csv('drugs.csv', drugs_db)
    print("Informacje o lekarstwie zostały zaktualizowane.")


# Funkcja do wyświetlania wszystkich lekarstw
def view_all_drugs(drugs_db):
    for drug_name, drug_data in drugs_db.items():
        print(f"Lekarstwo: {drug_name}")
        print(f"Opis: {drug_data['description']}")
        print(f"Ilość: {drug_data['quantity']}\n")


def main():
    doctors_db = load_doctors_from_csv('doctors.csv')
    patients_db = load_patients_from_csv('patients.csv')
    history = load_history_from_csv('history.csv')
    drugs_db = load_drugs_from_csv('drugs.csv')

    if not doctors_db:
        print("Failed to load doctors data. Exiting.")
        return
    if not patients_db:
        print("Failed to load patients data. Exiting.")
        return
    if not drugs_db:
        print("Failed to load drugs data. Exiting.")
        return

    authenticated_doctor = None
    while not authenticated_doctor:
        authenticated_doctor = authenticate(doctors_db)

    running = True
    while running:
        main_menu()
        choice = input("Wybierz opcję: ")
        running = handle_choice(choice, authenticated_doctor, patients_db, history, drugs_db)
        print()


if __name__ == "__main__":
    main()
