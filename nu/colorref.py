import time

from nu.isomorph import *

examples = ["colorref_largeexample_4_1026", "colorref_largeexample_6_960", "colorref_smallexample_2_49",
            "colorref_smallexample_4_7", "colorref_smallexample_4_16", "colorref_smallexample_6_15",
            "cref9vert3comp_10_27", "cref9vert_4_9"]

example = ["week4/torus24"]

final = {}
results = {}


def analyse():
    global results
    global final
    counter = 0
    for file in example:
        graphs = getGraphGrls(file)
        for g in graphs:
            g.num = counter
            counter += 1
            if not results:
                results[g] = []
            else:
                check = False
                for k in results.keys():
                    isIso = isIsomorphic(g, k)
                    if isIso[0]:
                        check = True
                        results[k] = results.get(k) + [g]
                        if isIso[1]:
                            results[k] = results.get(k) + ["DISCRETE"]
                        break
                if not check:
                    results[g] = []
        final[file] = results
        results = {}
    return final


def printResults():
    global final
    global results
    for f in final.keys():
        print(f'File: {f}')
        for k in final.get(f).keys():
            print("\t", [k] + [v for v in final.get(f).get(k)])


if __name__ == "__main__":
    start = time.time()

    analyse()
    printResults()

    print(time.time() - start)
