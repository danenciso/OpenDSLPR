from openalpr import Alpr
import cv2, sys, time

class Recognize():
    global alpr, path
    alpr = Alpr("us", "/etc/openalpr/openalpr.conf", "/usr/share/openalpr/runtime_data")
    path = ''

    def __init__(self, no_of_speculations, country_region, directory_path):
        global alpr, path
        if not alpr.is_loaded():
            print("Error loading OpenALPR")
            sys.exit(1)
        alpr.set_top_n(no_of_speculations)
        alpr.set_default_region(country_region)
        path = directory_path
        print("OpenAlpr is loaded")
        time.sleep(2)

    def put(self, frame):
        global alpr, path
        cv2.imwrite(path + "/frame.jpg", frame)
        self.__utility(path + "/frame.jpg")

    def __utility(self, image_name):
        global alpr, path
        results, i = alpr.recognize_file(image_name), 0
        for plate in results['results']:
            i += 1
            print("Plate #%d" % i)
            print("   %12s %12s" % ("Plate", "Confidence"))
            for candidate in plate['candidates']:
                prefix = "-"
                if candidate['matches_template']:
                    prefix = "*"
                print("  %s %12s%12f" % (prefix, candidate['plate'], candidate['confidence']))