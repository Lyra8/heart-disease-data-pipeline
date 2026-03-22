def check_row(row):
    errors = []  
    
    try:  #age
        age = int(row.get('Age', -1))  # Default to -1 if 'Age' is missing
        if age <= 0 or age > 120: 
            errors.append("Age out of bounds")
    except ValueError:
        errors.append("Age is not a number")

    try: #sex
        sex = int(row.get('Sex', -1))
        if sex not in [0, 1]:
            errors.append("Sex must be 0 or 1")
    except ValueError:
        errors.append("Sex is not a number")
    
    try: #chest pain
        cp = int(row.get('Chest pain type', -1))
        if cp not in [1, 2, 3, 4]:
            errors.append("Chest pain type must be 1, 2, 3, or 4")
    except ValueError:
        errors.append("Chest pain type is not a number")

    try: #blood preassure
        bp = int(row.get('BP', -1))
        if bp <= 50 or bp > 250:
            errors.append("BP out of bounds")
    except ValueError:
        errors.append("BP is not a number")

    try: #cholosterol
        cholesterol = int(row.get('Cholesterol', -1))
        if cholesterol < 0 or cholesterol > 600:
            errors.append("Cholesterol out of bounds")
    except ValueError:
        errors.append("Cholesterol is not a number")

    try: #max hr
        max_hr = int(row.get('Max HR', -1))
        if max_hr < 50 or max_hr > 220:
            errors.append("Max HR out of bounds")
    except ValueError:
        errors.append("Max HR is not a number")
    
    hd = row.get('Heart Disease')
    if hd is not None and hd != "":
        if hd not in ["Presence", "Absence"]:
            errors.append("Heart Disease must be Presence or Absence")

    is_valid = len(errors) == 0  # The row passed inspection
    return is_valid, " | ".join(errors)   #returns the pass or fail status,takes the list of errors and joins them together into a single text string


def clean_dataset(raw_data):
    # store the records that pass all rules
    clean_records = []
    
    # store the records that fail the rules
    rejected_records = []
    seen_records = set()

    # Dictionaries to interpret encoded values
    sex_map = {0: 'Female', 1: 'Male'}
    cp_map = {1: 'Typical Angina', 2: 'Atypical Angina', 3: 'Non-anginal Pain', 4: 'Asymptomatic'}


    for row in raw_data:
        # Check for duplicate records first
        row_string = str(row.items())
        if row_string in seen_records:
            row['Rejection_Reason'] = "Duplicate record"
            rejected_records.append(row)
            continue
            
        seen_records.add(row_string)

        is_valid, error_message = check_row(row)
        
        # If the row passed all checks, Add the valid row to our clean list
        if is_valid:
            if 'Heart Disease' not in row:
                row['Heart Disease'] = 'Unknown' 

        # Translate the encoded values into readable text
            sex_val = int(row.get('Sex', -1))
            if sex_val in sex_map:
                row['Sex'] = sex_map[sex_val]
            
            cp_val = int(row.get('Chest pain type', -1))
            if cp_val in cp_map:
                row['Chest pain type'] = cp_map[cp_val]
                    
            clean_records.append(row)

        else:

            row['Rejection_Reason'] = error_message
            rejected_records.append(row)

    return clean_records, rejected_records