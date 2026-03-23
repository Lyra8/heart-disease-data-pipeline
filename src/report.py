def generate_report(clean_data):
    if not clean_data:
        print("!!! No clean data available for analysis.")
        return

    count = len(clean_data)
    total_age = 0
    hr_values = []
    disease_count = 0
    cp_distribution = {}

    has_disease_data = False

    for row in clean_data:
        # We use lowercase keys because clean_dataset normalized them
        total_age += int(float(row.get('age', 0)))
        
        hr = row.get('max hr')
        if hr: hr_values.append(int(float(hr)))
        
        # Patterns
        hd = str(row.get('heart disease', '')).strip().lower()
        if hd == 'presence':
            disease_count += 1
            
        # Groupings
        cp = row.get('chest pain type', 'Unknown')
        cp_distribution[cp] = cp_distribution.get(cp, 0) + 1

    print("\n" + "="*30)
    print("      ANALYSIS REPORT")
    print("="*30)
    print(f"Total Validated Records: {count}")
    print(f"Average Patient Age:    {total_age / count:.1f}")
    
    if hr_values:
        print(f"Max Heart Rate Range:   {min(hr_values)} - {max(hr_values)} bpm")
    
    if has_disease_data:
        print(f"Heart Disease Rate:     {(disease_count / count) * 100:.1f}%")
    print("\nChest Pain Distribution:")
    for cp, val in cp_distribution.items():
        print(f" - {cp}: {val}")
    print("="*30 + "\n")