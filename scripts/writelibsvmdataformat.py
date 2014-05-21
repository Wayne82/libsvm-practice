"""
A script to write out lib svm expected data format from my collecting data
"""
import os
import sys
import csv
import getopt

CMD_USAGE = """
    usage: writelibsvmdataformat.py --inputs="/inputs/folder/" --output="/output/lib_svm_data"
"""
FEATURE_SPACE = 10


def write_libsvm_data(input_files, output_file):
    """

    :param input_files: input files, each of which contains a single label at
                        first row, and a bunch of data following
    :param output_file: output file, which meet lib svm expected data format
    """
    with open(output_file, 'wb') as output_csv_file:
        output_writer = csv.writer(output_csv_file, delimiter=' ')
        for input_file in input_files:
            with open(input_file, 'rb') as input_csv_file:
                input_reader = csv.reader(input_csv_file, delimiter=' ')
                # assume there is only one item in each row
                label = input_reader.next()
                i = 1   # start from index 1
                line = [label[0]]
                for row in input_reader:
                    if int(row[0]) != 0:
                        line.append(':'.join([str(i), row[0]]))
                    i += 1
                    if i > FEATURE_SPACE:
                        output_writer.writerow(line)
                        i = 1
                        line = [label[0]]


def main(argv):
    """
    :param argv: command line arguments
    :rtype : error code, success 0 and fail 1
    """
    try:
        optlist, _ = getopt.getopt(argv[1:], "hi:o:",
                                   ["help", "inputs=", "output="])
    except getopt.GetoptError:
        print("Command line arguments error, please try --help for help")
        return 1

    inputs = ''
    output_file = ''
    for opt, opt_arg in optlist:
        if opt in ("-h", "--help"):
            print CMD_USAGE
            return 0
        if opt in ("-i", "--inputs"):
            inputs = opt_arg
            if not os.path.exists(inputs):
                print("Input files folder not exist")
                return 1
        elif opt in ("-o", "--output"):
            output_file = opt_arg

    # print the messages
    print("Inputs folder: " + inputs)
    print("Output file: " + output_file)
    assert isinstance(output_file, str)
    assert isinstance(inputs, str)
    input_files = []
    for root, _, files in os.walk(inputs):
        for name in files:
            if name.endswith('.csv'):
                input_files.append(os.path.abspath(os.path.join(root, name)))

    if len(input_files) == 0:
        print("No input files.")
        return 1

    write_libsvm_data(input_files, output_file)


if __name__ == "__main__":
    sys.exit(main(sys.argv))