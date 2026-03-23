What is this project?
This is a data pipeline built in Python that takes raw heart disease patient data and processes it into something clean, reliable, and ready for analysis. The idea is simple — real world data is messy, and you can't just trust it as is. Our pipeline reads the raw data, checks every single row against a set of validation rules, separates the good from the bad, and then generates a report with insights from the clean data.

How does it work?
When you run the pipeline it goes through two main steps. First it reads the raw data file and validates every row. If a row has something wrong with it, like an impossible age or a blood pressure value that isn't a number, it gets rejected and saved separately with a note explaining exactly what was wrong. If the row passes all the checks it gets saved to the clean dataset. The pipeline also automatically detects and removes any duplicate records before validation happens. Once cleaning is done, the second step reads the clean data and generates a summary report showing things like the average patient age, the highest heart rate recorded, the distribution of chest pain types, and the percentage of patients with heart disease.

How to run it?
Make sure you are inside the project folder in your terminal, then run one of these commands depending on what you want to do.

To run the full pipeline from start to finish:
python main.py all

To only clean and validate the data:
python main.py clean

To only generate the analysis report:
python main.py analyze

When you run clean or all, the program will automatically show you the available CSV files in the data folder and ask you to pick which one you want to process. Just keep in mind that you need to run clean at least once before analyze, otherwise there is no clean data file to read from.

Project Structure
The project is split into separate files, each with its own responsibility. The main.py file is the entry point and the only file you run directly — it handles the command line interface, the file selection menu, and controls the flow of the pipeline. The ingest.py file inside the src folder handles all file reading and writing, as well as duplicate removal. The validate.py file contains all the rules that decide whether a row of data is valid or not. The report.py file does the math and prints the final analysis. All the data files live inside the data folder — the raw input file goes in there, and the clean and rejected output files get generated there automatically when you run the pipeline.

Who built what?
This project was built by two people. 
Edda was responsible for the system and data flow, which includes main.py and ingest.py — the command line interface, reading and writing files, and handling duplicates. 
Lyra was responsible for the data logic, which includes validate.py and report.py — the validation rules for every column and the analysis report.
