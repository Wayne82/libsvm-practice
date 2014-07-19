"""
A script to train using libsvm, this is modified from libsvm existing easy.py
"""
import os
import sys
import getopt
import subprocess
CMD_USAGE = """
    usage: libsvm_train.py --tools="folder/to/tools" --data="file/to/training_set" --class=0 or 1
    class 0: classification using SVC
    class 1: regression using SVR
"""
# Assume we are working on windows platform, so far.
SVM_TRAIN_BIN = ""
SVM_SCALE_BIN = ""
SVM_PREDICT_BIN = ""
SVM_CROSS_VALIDATE_BIN = ""
GNU_PLOT_BIN = ""


def check_tools_exist(tools_folder):
    """

    :param tools_folder:
    :return:
    """
    global SVM_TRAIN_BIN
    global SVM_SCALE_BIN
    global SVM_PREDICT_BIN
    global SVM_CROSS_VALIDATE_BIN
    SVM_TRAIN_BIN = os.path.join(tools_folder, "svm-train.exe")
    if not os.path.exists(SVM_TRAIN_BIN):
        print "svm-train executable not found"
        return 0

    SVM_SCALE_BIN = os.path.join(tools_folder, "svm-scale.exe")
    if not os.path.exists(SVM_SCALE_BIN):
        print "svm-scale executable not found"
        return 0

    SVM_PREDICT_BIN = os.path.join(tools_folder, "svm-predict.exe")
    if not os.path.exists(SVM_PREDICT_BIN):
        print "svm-predict executable not found"
        return 0

    SVM_CROSS_VALIDATE_BIN = os.path.join(tools_folder, "grid.py")
    if not os.path.exists(SVM_CROSS_VALIDATE_BIN):
        print "grid.py not found"
        return 0

    return 1


def check_training_set_exist(training_set):
    """

    :param training_set:
    :return:
    """
    if not os.path.exists(training_set):
        print "Training set not found: ", training_set
        return 0
    return 1


def check_gnu_plot():
    """


    """
    global GNU_PLOT_BIN
    GNU_PLOT_BIN = r"C:\Program Files (x86)\gnuplot\bin\gnuplot.exe"
    if not os.path.exists(GNU_PLOT_BIN):
        print "Gnu plot executable not found: ", GNU_PLOT_BIN
        return 0
    return 1


def get_scale_model_range_file_name(training_set):
    """

    :param training_set:
    :return:
    """
    file_name = training_set
    scaled_file = file_name + ".scale"
    model_file = file_name + ".model"
    range_file = file_name + ".range"
    return scaled_file, model_file, range_file


def libsvm_train_classification(training_set):
    scaled_file, model_file, range_file = \
        get_scale_model_range_file_name(training_set)

    # Step 1: scale data
    scale_cmd = '{0} -s "{1}" "{2}" > "{3}"'.format(
        os.path.abspath(SVM_SCALE_BIN),
        range_file,
        training_set,
        scaled_file)
    print "Scaling training set..."
    subprocess.Popen(scale_cmd, shell=True, stdout=subprocess.PIPE).communicate()

    # Step 2: cross validate to choose best parameters
    if os.path.exists(GNU_PLOT_BIN):
        gnu_out_file = training_set + '.out'
        gnu_png_file = training_set + '.png'
        cross_validate_cmd = \
            '{0} -svmtrain "{1}" -gnuplot "{2}" -out "{3}" -png "{4}" "{5}"'.format(
            os.path.abspath(SVM_CROSS_VALIDATE_BIN),
            os.path.abspath(SVM_TRAIN_BIN),
            os.path.abspath(GNU_PLOT_BIN),
            gnu_out_file,
            gnu_png_file,
            scaled_file)
    else:
        cross_validate_cmd = '{0} -svmtrain "{1}" "{2}"'.format(
            os.path.abspath(SVM_CROSS_VALIDATE_BIN),
            os.path.abspath(SVM_TRAIN_BIN),
            scaled_file)
    print "Cross validating..."
    output = subprocess.Popen(cross_validate_cmd, shell=True, stdout=subprocess.PIPE).stdout
    line = ""
    last_line = ""
    while True:
        last_line = line
        line = output.readline()
        if not line:
            break
    c, g, rate = map(float, last_line.split())
    print('Best c={0}, g={1} CV rate={2}'.format(c, g, rate))

    # Step 3: train data
    train_cmd = '{0} -c {1} -g {2} "{3}" "{4}"'.format(
        os.path.abspath(SVM_TRAIN_BIN), c, g, scaled_file, model_file)
    print "Training..."
    subprocess.Popen(train_cmd, shell=True, stdout=subprocess.PIPE).communicate()
    print 'Output model: {0}'.format(model_file)


def libsvm_train_regression(training_set):
    """

    :param training_set:
    """
    scaled_file, model_file, range_file = \
        get_scale_model_range_file_name(training_set)

    # Step 1: scale data
    scale_cmd = '{0} -s "{1}" "{2}" > "{3}"'.format(
        os.path.abspath(SVM_SCALE_BIN),
        range_file,
        training_set,
        scaled_file)
    print "Scaling training set..."
    subprocess.Popen(scale_cmd, shell=True, stdout=subprocess.PIPE).communicate()

    # Step 2: train data
    train_cmd = '{0} -s 3 -p 0.1 -t 0 "{1}" "{2}"'.format(
        os.path.abspath(SVM_TRAIN_BIN), scaled_file, model_file)
    print "Training..."
    subprocess.Popen(train_cmd, shell=True, stdout=subprocess.PIPE).communicate()
    print 'Output model: {0}'.format(model_file)


def predict(test_file, range_file, model_file):
    print "Predict test file: ", test_file
    test_file_scale = test_file + ".scale"
    predict_test_file = test_file + ".predict"

    # scale test file
    scale_cmd = '{0} -s "{1}" "{2}" > "{3}"'.format(
        os.path.abspath(SVM_SCALE_BIN),
        range_file,
        test_file,
        test_file_scale)
    print "Scaling test file..."
    subprocess.Popen(scale_cmd, shell=True, stdout=subprocess.PIPE).communicate()

    # predict
    predict_cmd = '{0} "{1}" "{2}" "{3}"'.format(
        os.path.abspath(SVM_PREDICT_BIN),
        test_file_scale,
        model_file,
        predict_test_file)
    print "Predicting test file..."
    subprocess.Popen(predict_cmd, shell=True, stdout=subprocess.PIPE).communicate()


def main(argv):
    """

    :param argv:
    :return:
    """
    try:
        optlist, _ = getopt.getopt(argv[1:], "ht:d:c:p:",
                                   ["help", "tools=", "data=", "class=", "predict="])
    except getopt.GetoptError:
        print("Command line arguments error, please try --help for help")
        return 1

    tools_folder = ""
    training_set = ""
    libsvm_class = -1
    test_file = ""
    for opt, opt_arg in optlist:
        if opt in ("-h", "--help"):
            print CMD_USAGE
            return 0
        if opt in ("-t", "--tools"):
            tools_folder = os.path.abspath(opt_arg)
        elif opt in ("-d", "--data"):
            training_set = os.path.abspath(opt_arg)
        elif opt in ("-c", "--class"):
            libsvm_class = opt_arg
        elif opt in ("-p", "--predict"):
            test_file = opt_arg

    if not os.path.exists(tools_folder):
        print "Tools folder doesn't exist: ", tools_folder
        return 1
    if not os.path.exists(training_set):
        print "Training set doesn't exist: ", training_set
        return 1
    print "Tools folder: ", tools_folder
    print "Data folder: ", training_set
    print "Libsvm class", libsvm_class
    if not check_tools_exist(tools_folder):
        return 1
    if not check_training_set_exist(training_set):
        return 1
    check_gnu_plot()

    if int(libsvm_class) == 0:
        libsvm_train_classification(training_set)
    elif int(libsvm_class) == 1:
        libsvm_train_regression(training_set)
    else:
        print "Invalid libsvm class, please type either 0 for classification or 1 for regression"

    if test_file:
        _, model_file, range_file = get_scale_model_range_file_name(training_set)
        predict(test_file, range_file, model_file)

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))