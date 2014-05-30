"""
A script to write out lib svm expected data format from my collecting data
"""
import os
import sys
import csv
import getopt
import subprocess

CMD_USAGE = """
    usage: writelibsvmdataformat.py --inputs="/inputs/folder/" --output="/output/lib_svm_data" <options>
    <options>:
             -f, --features specify the feature space size, default is 10
"""
# by default feature space to be 10
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


def check_data(data_file):
    """
    :param data_file: the input lib svm format data, to be verified.
    """
    check_py = r'../external/libsvm/tools/checkdata.py'
    if not os.path.exists(check_py):
        print("checkdata.py not exist.")
        return

    try:
        subprocess.call(check_py + " " + data_file)
    except OSError as e:
        print("Execution check data failed: " + e.message)


def main(argv):
    """
    :param argv: command line arguments
    :rtype : error code, success 0 and fail 1
    """
    try:
        optlist, _ = getopt.getopt(argv[1:], "hi:o:f:",
                                   ["help", "inputs=", "output=", "features="])
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
        elif opt in ("-f", "--features"):
            global FEATURE_SPACE
            FEATURE_SPACE = int(opt_arg)

    # print the messages
    print("Inputs folder: " + inputs)
    print("Output file: " + output_file)
    print("Feature space size: " + str(FEATURE_SPACE))
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
    check_data(output_file)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))