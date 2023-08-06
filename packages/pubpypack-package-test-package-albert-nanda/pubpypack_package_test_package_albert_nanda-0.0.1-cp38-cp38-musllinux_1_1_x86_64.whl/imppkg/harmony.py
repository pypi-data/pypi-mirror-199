import sys
from imppkg.harmonic_mean import harmonic_mean


def main():
    result = 0.0
    try:
        nums = [float(num) for num in sys.argv[1:]]
    except ValueError:
        nums = []

    try:
        result = harmonic_mean(10)
    except ZeroDivisionError:
        pass
    print(result)
