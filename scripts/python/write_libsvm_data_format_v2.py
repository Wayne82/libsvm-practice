"""
A script to write out lib svm expected data format from my collecting data
"""
import os
import sys
import csv
import json
import getopt
import subprocess

CMD_USAGE = """
    usage: write_libsvm_data_format.py --inputs="/inputs/folder/" --output="/output/lib_svm_data" <options>
    <options>:
             -f, --features specify the feature space size, default is 10
             -v, --verify the tool to verify output data no format error
"""
# by default feature space to be 10
FEATURE_SPACE = 10
LIMIT_SAMPLE_SIZE = 1000


def write_libsvm_data(input_files, output_file):
    """

    :param input_files:
    :param output_file:
    """
    with open(output_file, 'wb') as output_csv_file:
        output_writer = csv.writer(output_csv_file, delimiter=' ')
        for input_file in input_files:
            print "Write file: ", input_file
            with open(input_file, 'rb') as signal_file:
                json_data = json.load(signal_file)
                beacons = json_data['interestedBeacons']
                for beacon in beacons:
                    rssis = beacon['rssis']
                    length = len(rssis)
                    if length < FEATURE_SPACE:
                        continue
                    rows = 0
                    ending = FEATURE_SPACE
                    while ending <= length:
                        line = [beacon['realDistance']]
                        for idx, val in enumerate(rssis[(ending - FEATURE_SPACE):ending]):
                            if val != 0:
                                line.append(':'.join([str(idx + 1), str(val)]))
                        output_writer.writerow(line)
                        ending += FEATURE_SPACE
                        rows += 1
                        if rows >= LIMIT_SAMPLE_SIZE:
                            break


def check_data(check_tool, data_file):
    """
    :param data_file: the input lib svm format data, to be verified.
    """
    check_py = check_tool
    if not os.path.exists(check_py):
        print("checkdata.py not exist.")
        return
    subprocess.call([os.path.abspath(check_py), data_file], shell=True)


def main(argv):
    """
    :param argv: command line arguments
    :rtype : error code, success 0 and fail 1
    """
    try:
        optlist, _ = getopt.getopt(argv[1:], "hi:o:f:v:",
                                   ["help", "inputs=", "output=", "features=", "verify"])
    except getopt.GetoptError:
        print("Command line arguments error, please try --help for help")
        return 1

    inputs = ''
    output_file = ''
    check_tool = ''
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
        elif opt in ("-v", "--verify"):
            check_tool = opt_arg

    # print the messages
    print("Inputs folder: " + inputs)
    print("Output file: " + output_file)
    print("Feature space size: " + str(FEATURE_SPACE))
    print("Check tool: " + check_tool)
    assert isinstance(output_file, str)
    assert isinstance(inputs, str)
    input_files = []
    for root, _, files in os.walk(inputs):
        for name in files:
            if name.endswith('.raw_filter'):
                input_files.append(os.path.abspath(os.path.join(root, name)))

    if len(input_files) == 0:
        print("No input files.")
        return 1

    write_libsvm_data(input_files, output_file)
    check_data(check_tool, output_file)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))