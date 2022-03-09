import cProfile

from nu.isomorph import *

examples = ["colorref_largeexample_4_1026", "colorref_largeexample_6_960", "colorref_smallexample_2_49",
            "colorref_smallexample_4_7", "colorref_smallexample_4_16", "colorref_smallexample_6_15",
            "cref9vert3comp_10_27", "cref9vert_4_9"]

# example = ["week4/torus24"]
example = ["colorref_largeexample_4_1026"]

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
                results[(g, False)] = []
            else:
                check = False
                for k in results.keys():
                    isIso = isIsomorphic(g, k[0])
                    if isIso[0]:
                        check = True
                        results[k] = results.get(k) + [g]
                        if isIso[1]:
                            results[(k[0], True)] = results.get(k)
                            results.pop(k)
                        break
                if not check:
                    results[(g, False)] = []
        final[file] = results
        results = {}
    return final


def printResults():
    global final
    global results
    for f in final.keys():
        print(f'File: {f}')
        for k in final.get(f).keys():
            if k[1]:
                print("\t", [k[0]] + [v for v in final.get(f).get(k)] + ["DISCRETE"])
            else:
                print("\t", [k[0]] + [v for v in final.get(f).get(k)])


if __name__ == "__main__":
    cProfile.run('analyse()')
