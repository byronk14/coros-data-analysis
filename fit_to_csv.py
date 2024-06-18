import csv
import os
from fitparse import FitFile, FitParseError
import argparse


def validate_fit_file(file_path):
    try:
        fitfile = FitFile(file_path)
        fitfile.parse()
        return True
    except FitParseError as e:
        print(f"Error: {e}")
        return False

def main(input_dir, output_dir):
    print('total files: ', len(os.listdir(input_dir)))
    for file in os.listdir(input_dir):
        print('processing file --- ', file)

        if not validate_fit_file(input_dir + file):
            print("Invalid FIT file header or structure.")
            pass

        fitfile = FitFile(input_dir + file)

        all_fieldnames = set()
        try:
            for record in fitfile.get_messages('record'):
                for field in record:
                    all_fieldnames.add(field.name)
        

            # Open a CSV file for writing
            file_clean = file.replace('.fit', '')
            with open(output_dir + f'{file_clean}.csv', 'w', newline='') as csvfile:

                writer = csv.DictWriter(csvfile, fieldnames=sorted(all_fieldnames))

                writer.writeheader()
            
                for record in fitfile.get_messages('record'):
                    data = record.get_values()
                    writer.writerow(data)
        
        except FitParseError as e:
            print(f"Error: Failed to process records for file {file}: {e}")
            pass 

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert .fit file to CSV.")
    parser.add_argument("input_dir", help="Path dir to the input .fit file")
    parser.add_argument("output_dir", help = "path dir to the output of .csv files")

    args = parser.parse_args()

    main(args.input_dir, args.output_dir)