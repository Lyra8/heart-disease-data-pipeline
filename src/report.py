def generate_report(clean_data):
    if not clean_data:
        print("Error: No clean data available to analyze.")
        return

    total_patients = len(clean_data)
    total_age = 0
    max_hr_list = []
    chest_pain_counts = {}
    disease_count = 0 

    for row in clean_data:
        # 1. Summary Statistics
        total_age += int(row['Age'])
        max_hr_list.append(int(row['Max HR']))
        
        # 2. Distributions
        cp_type = row.get('Chest pain type', 'Unknown')
        if cp_type in chest_pain_counts:
            chest_pain_counts[cp_type] += 1
        else:
            chest_pain_counts[cp_type] = 1

        # 3. Meaningful Patterns
        if row.get('Heart Disease') == 'Presence':
            disease_count += 1

    # Final Math Calculations
    average_age = total_age / total_patients
    highest_hr = max(max_hr_list)
    disease_percentage = (disease_count / total_patients) * 100 

    # 4. Terminal Output (Task 4)
    print("\n*** Data Analysis Report ***")
    print(f"Total Valid Records: {total_patients}")
    print(f"Average Patient Age: {average_age:.1f} years")
    print(f"Highest Max Heart Rate: {highest_hr} bpm")
    print(f"Heart Disease Presence: {disease_percentage:.1f}% of valid patients")
    print("Chest Pain Type Distribution:")
    for cp_type, count in chest_pain_counts.items():
        print(f"  Type {cp_type}: {count} patients")
    print("****************************\n")