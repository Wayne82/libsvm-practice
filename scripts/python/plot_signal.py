"""
A script to plot signals
"""
import sys
import os
import getopt
import json
import matplotlib.pyplot as plt
CMD_USAGE = """

"""
MAX_PLOT_SIZE = 5000


def plot_signal(signal):
    with open(signal, "rb") as json_file:
        json_data = json.load(json_file)
        beacons = json_data['interestedBeacons']
        legends = []
        print "Plotting ", signal
        for beacon in beacons:
            signal = beacon['rssis']
            size = len(signal)
            if size > MAX_PLOT_SIZE:
                size = MAX_PLOT_SIZE
                signal = signal[:size]
            x = range(1, size+1)
            plt.plot(x, signal)
            legends.append('{0} m'.format(beacon['realDistance']))
        plt.legend(legends)
        plt.show()


def plot_signals(signal_files):
    for signal in signal_files:
        plot_signal(signal)


def main(argv):
    """

    :param argv:
    :return:
    """
    try:
        optlist, _ = getopt.getopt(argv[1:], "hi:",
                                   ["help", "inputs="])
    except getopt.GetoptError:
        print("Command line arguments error, please try --help for help")
        return 1

    inputs = ""
    for opt, opt_arg in optlist:
        if opt in ("-h", "--help"):
            print CMD_USAGE
            return 0
        if opt in ("-i", "--inputs"):
            inputs = opt_arg

    print "Input data folder: ", inputs
    signals = []
    for root, _, files in os.walk(inputs):
        for name in files:
            if name.endswith(".raw") or name.endswith(".raw_filter"):
                signals.append(os.path.abspath(os.path.join(root, name)))

    if len(signals) == 0:
        print "There is no data to plot."
    else:
        plot_signals(signals)


if __name__ == "__main__":
    sys.exit(main(sys.argv))