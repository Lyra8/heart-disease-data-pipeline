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

    is_valid = len(errors) == 0  # The row passed inspection
    return is_valid, " | ".join(errors)   #returns the pass or fail status,takes the list of errors and joins them together into a single text string


def clean_dataset(raw_data):
    # store the records that pass all rules
    clean_records = []
    
    # store the records that fail the rules
    rejected_records = []

    # Loop through every patient record in the raw data
    for row in raw_data:
        
        # Send the row to our inspector function and get the results
        is_valid, error_message = check_row(row)
        
        # If the row passed all checks, Add the valid row to our clean list
        if is_valid:
            if 'Heart Disease' not in row:
                row['Heart Disease'] = 'Unknown'
            clean_records.append(row)  

        # If the row failed any check, Add the invalid row to our rejected list
        else:
            # Create a brand new column in this bad row and save the exact error message
            row['Rejection_Reason'] = error_message
            rejected_records.append(row)

    # Hand both completed lists back to the main program
    return clean_records, rejected_records
