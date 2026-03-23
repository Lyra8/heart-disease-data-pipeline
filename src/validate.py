def check_row(row):
    """
    Comprehensive validation for every field in the Heart Disease dataset.
    Ensures all numeric fields are actually numbers and within medical bounds.
    """
    errors = []
    
    # Helper to safely get and clean values from the normalized row
    def get_val(key):
        val = row.get(key.lower().strip())
        return str(val).strip() if val is not None else ""

    # --- 1. ID ---
    raw_id = get_val('id')
    
    if not raw_id:
        errors.append("Missing Patient ID")
    # This rejects IDs starting with / or # instead of cleaning them
    elif raw_id.startswith('/') or raw_id.startswith('#'):
        errors.append(f"ID '{raw_id}' contains invalid prefix characters")
    else:
        try:
            # We use float first to handle "630106.0" then int
            patient_id = int(float(raw_id))
            if patient_id < 0:
                errors.append(f"Invalid negative ID: {patient_id}")
        except ValueError:
            errors.append(f"ID '{raw_id}' is not a valid numeric format")
     # ---  AGE ---
    try:
        age_str = get_val('age')
        if not age_str:
            errors.append("Missing Age")
        else:
            age = int(float(age_str))
            if age <= 0 or age > 120:
                errors.append(f"Age {age} is out of range (1-120)")
    except ValueError:
        errors.append(f"Age '{get_val('age')}' is not a valid number")

    # --- 2. SEX & CHEST PAIN TYPE ---
    try:
        sex = int(float(get_val('sex')))
        if sex not in [0, 1]:
            errors.append(f"Sex {sex} must be 0 (F) or 1 (M)")
    except ValueError:
        errors.append("Sex must be a numeric code (0 or 1)")

    try:
        cp = int(float(get_val('chest pain type')))
        if cp not in [1, 2, 3, 4]:
            errors.append(f"Chest pain type {cp} must be 1-4")
    except ValueError:
        errors.append("Chest pain type must be a numeric code (1-4)")

    # --- 3. BLOOD PRESSURE & CHOLESTEROL ---
    try:
        bp = int(float(get_val('bp')))
        if bp < 50 or bp > 250:
            errors.append(f"BP {bp} is outside realistic bounds (50-250)")
    except ValueError:
        errors.append("BP must be a numeric value")

    try:
        chol = int(float(get_val('cholesterol')))
        if chol < 50 or chol > 600:
            errors.append(f"Cholesterol {chol} is outside realistic bounds")
    except ValueError:
        errors.append("Cholesterol must be a numeric value")

    # --- 4. HEART METRICS (EKG, Max HR, FBS) ---
    try:
        fbs = int(float(get_val('fbs over 120')))
        if fbs not in [0, 1]:
            errors.append("FBS over 120 must be 0 or 1")
    except ValueError:
        errors.append("FBS must be a numeric code")

    try:
        ekg = int(float(get_val('ekg results')))
        if ekg not in [0, 1, 2]:
            errors.append("EKG results must be 0, 1, or 2")
    except ValueError:
        errors.append(f"EKG results '{get_val('ekg results')}' is not a valid number")

    try:
        hr = int(float(get_val('max hr')))
        if hr < 40 or hr > 220:
            errors.append(f"Max HR {hr} is out of range")
    except ValueError:
        errors.append("Max HR must be a numeric value")

    # --- 5. EXERCISE & ST METRICS ---
    try:
        angina = int(float(get_val('exercise angina')))
        if angina not in [0, 1]:
            errors.append("Exercise angina must be 0 or 1")
    except ValueError:
        errors.append("Exercise angina must be numeric")

    try:
        st_dep = float(get_val('st depression'))
        if st_dep < 0 or st_dep > 10:
            errors.append("ST depression out of range")
    except ValueError:
        errors.append(f"ST depression '{get_val('st depression')}' is not a number")

    try:
        slope = int(float(get_val('slope of st')))
        if slope not in [1, 2, 3]:
            errors.append("Slope of ST must be 1, 2, or 3")
    except ValueError:
        errors.append("Slope of ST must be numeric")

    # --- 6. VESSELS & THALLIUM ---
    try:
        vessels = int(float(get_val('number of vessels fluro')))
        if vessels < 0 or vessels > 4:
            errors.append("Vessels must be 0-4")
    except ValueError:
        errors.append("Vessels must be numeric")

    try:
        thallium = int(float(get_val('thallium')))
        if thallium not in [3, 6, 7]:
            errors.append("Thallium must be 3, 6, or 7")
    except ValueError:
        errors.append("Thallium must be numeric")

    # Final check: Heart Disease column (if present)
    hd = get_val('heart disease').lower()
    if hd and hd not in ['presence', 'absence']:
        errors.append("Heart Disease must be 'Presence' or 'Absence'")

    return len(errors) == 0, " | ".join(errors)

def clean_dataset(raw_data):
    clean_records = []
    rejected_records = []
    
    seen_ids = set()    # To catch duplicate Patient IDs
    seen_rows = set()   # To catch exact row duplicates (identical data)

    SEX_MAP = {0: 'Female', 1: 'Male'}
    CP_MAP = {1: 'Typical Angina', 2: 'Atypical Angina', 3: 'Non-anginal Pain', 4: 'Asymptomatic'}

    for row in raw_data:
        # 1. Normalize Headers (Lowercasing & Stripping)
        norm_row = {k.strip().lower(): v for k, v in row.items() if k is not None}
        
        # 2. Get ID for duplicate checking
        current_id = str(norm_row.get('id', '') or '').strip()

        if current_id in seen_ids:
            norm_row['rejection_reason'] = f"Duplicate Patient ID: {current_id}"
            rejected_records.append(norm_row)
            continue
            
        # 4. Exact Row Duplicate Check 
        row_fingerprint = tuple(norm_row.items())
        if row_fingerprint in seen_rows:
            norm_row['rejection_reason'] = "Exact duplicate of existing record"
            rejected_records.append(norm_row)
            continue

        # 5. Medical Validation 
        is_valid, error_msg = check_row(norm_row)
        
        if is_valid:
            # 6. Clean what can be fixed (Interpret Encodings)
            try:
                # Convert codes to text
                s_val = int(float(norm_row['sex']))
                norm_row['sex'] = SEX_MAP.get(s_val, "Unknown")
                
                cp_val = int(float(norm_row['chest pain type']))
                norm_row['chest pain type'] = CP_MAP.get(cp_val, "Unknown")
                
                # Record these as 'seen' and add to clean list
                seen_ids.add(current_id)
                seen_rows.add(row_fingerprint)
                clean_records.append(norm_row)
                
            except Exception as e:
                norm_row['rejection_reason'] = f"Encoding conversion failed: {str(e)}"
                rejected_records.append(norm_row)
        else:
            # 7. "Keep track of issues"
            norm_row['rejection_reason'] = error_msg
            rejected_records.append(norm_row)

    return clean_records, rejected_records