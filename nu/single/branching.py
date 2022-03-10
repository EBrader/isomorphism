from nu.single.isomorph import *

examples = ["colorref_largeexample_4_1026", "colorref_largeexample_6_960", "colorref_smallexample_2_49",
            "colorref_smallexample_4_7", "colorref_smallexample_4_16", "colorref_smallexample_6_15",
            "cref9vert3comp_10_27", "cref9vert_4_9"]

# example = ["week4/torus24"]
file = "colorref_largeexample_4_1026"

results = {}


def analyse():
    global results
    counter = 0
    graphs = getGraphGrls(file)
    for g in graphs:
        g.num = counter
        counter += 1
        if not results:
            results[g] = []
        else:
            check = False
            for k in results.keys():
                if results.get(g):
                    iso = isIsomorphic(g, k)
                else:
                    iso = isIsomorphic(g, k, True)
                if iso[0]:
                    check = True
                    results[k] = results.get(k) + [g]
                    break
            if not check:
                results[g] = []
    return results


if __name__ == "__main__":
    #   cProfile.run('analyse()')
    analyse()
    print(results)
