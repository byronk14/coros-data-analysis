import csv
import os
from fitparse import FitFile, FitParseError
import argparse


def main(input_dir, output_dir):
    print('total files: ', len(os.listdir(input_dir)))

    for file in os.listdir(input_dir):
        try:

            print('processing file --- ', file)

            fitfile = FitFile(input_dir + f'/{file}')
            #fitfile = FitFile(input_dir + '/458722383560212480.fit')

            msg_organized_dict = dict()
            msg_field_names = dict()

            data_messages = list(fitfile.get_messages())

            for message in data_messages:
        
                if message.mesg_type.name not in msg_organized_dict:
                    msg_organized_dict[message.mesg_type.name] = []
                    msg_organized_dict[message.mesg_type.name].append(message)


                    msg_field_names[message.mesg_type.name] = []
                    for field in message.fields:
                        if field.name not in msg_field_names[message.mesg_type.name]:
                            msg_field_names[message.mesg_type.name].append(field.name)

                else:
                    msg_organized_dict[message.mesg_type.name].append(message)

                    for field in message.fields:
                        if field.name not in msg_field_names[message.mesg_type.name]:
                            msg_field_names[message.mesg_type.name].append(field.name)

            for k, v in msg_organized_dict.items():
                #with open(output_dir + f'/458722383560212480.fit_{k}.csv', 'w', newline='') as csvfile:
                with open(output_dir + f'/{file}_{k}.csv', 'w', newline='') as csvfile:

                    writer = csv.DictWriter(csvfile, fieldnames=sorted(msg_field_names[k]))

                    writer.writeheader()
                
                    for record in msg_organized_dict[k]:
                        data = record.get_values()
                        writer.writerow(data)
            
        except FitParseError as e:
            print(f"Error: Failed to process records for file: {e}")
            continue
            

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert .fit file to CSV.")
    parser.add_argument("input_dir", help="Path dir to the input .fit file")
    parser.add_argument("output_dir", help = "path dir to the output of .csv files")

    args = parser.parse_args()

    main(args.input_dir, args.output_dir)