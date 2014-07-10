"""
A script to filter given signals
"""
import sys
import os
import json
import getopt
CMD_USAGE = """
    usage: signalfilter.py --inputs="/inputs/folder/" --outputs="/output/folder/"
"""
SLIDING_BUFFER = []
SLIDING_BUFFER_SIZE = 12


def constrained_amplitude_filter(input_signal, sub_signal):
    """

    :param input_signal:
    :param sub_signal:
    """
    low_amplitude = -100
    high_amplitude = 0
    if input_signal <= low_amplitude or input_signal >= high_amplitude:
        return sub_signal
    else:
        return input_signal


def sliding_ave_filter(input_signal):
    """

    :param input_signal:
    """
    global SLIDING_BUFFER
    global SLIDING_BUFFER_SIZE
    if len(SLIDING_BUFFER) < SLIDING_BUFFER_SIZE:
        SLIDING_BUFFER.append(input_signal)
        return input_signal
    else:
        SLIDING_BUFFER[:(SLIDING_BUFFER_SIZE-1)] = SLIDING_BUFFER[1:SLIDING_BUFFER_SIZE]
        SLIDING_BUFFER[SLIDING_BUFFER_SIZE-1] = input_signal
        sorted_buffer = sorted(SLIDING_BUFFER)
        ave_value = 0
        for x in sorted_buffer[1:(SLIDING_BUFFER_SIZE-1)]:
            ave_value += x
        ave_value /= (SLIDING_BUFFER_SIZE - 2)
        return ave_value


def filter_signals(input_files, output_folder):
    """

    :param input_files:
    :param output_folder:
    """
    for input_file in input_files:
        with open(input_file, 'rb') as json_file:
            json_data = json.load(json_file)
            beacons = json_data['interestedBeacons']
            for beacon in beacons:
                rssis = beacon['rssis']
                prev_val = rssis[0]
                for idx, val in enumerate(rssis):
                    rssis[idx] = constrained_amplitude_filter(val, prev_val)
                    prev_val = val
                rssis[:] = [sliding_ave_filter(x) for x in rssis]
                rssis[:] = rssis[SLIDING_BUFFER_SIZE:]
            _, name = os.path.split(input_file)
            output_file = os.path.join(output_folder, name+'_filter')
            with open(output_file, 'wb') as filter_json_file:
                json.dump(json_data, filter_json_file)


def main(argv):
    """

    :param argv: system argument
    """
    try:
        optlist, _ = getopt.getopt(argv[1:], "hi:o:",
                                   ["help", "inputs=", "outputs="])
    except getopt.GetoptError:
        print("Command line arguments error, please try --help for help")
        return 1

    inputs = ''
    outputs = ''
    for opt, opt_arg in optlist:
        if opt in ("-h", "--help"):
            print CMD_USAGE
            return 0
        if opt in ("-i", "--inputs"):
            inputs = opt_arg
            if not os.path.exists(inputs):
                print("Input files folder not exist")
                return 1
        elif opt in ("-o", "--outputs"):
            outputs = opt_arg
            try:
                if not os.path.exists(outputs):
                    os.makedirs(outputs)
            except OSError:
                print("Create output folder failed.")
                return 1

    # print the messages
    print("Inputs folder: " + inputs)
    print("Output folder: " + outputs)

    input_files = []
    for root, _, files in os.walk(inputs):
        for name in files:
            if name.endswith('.raw'):
                input_files.append(os.path.abspath(os.path.join(root, name)))

    if len(input_files) == 0:
        print("No signal collection files.")

    filter_signals(input_files, outputs)


if __name__ == "__main__":
    sys.exit(main(sys.argv))