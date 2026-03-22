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

