import re
from flask import Flask, request, render_template

def process_input(input):
    return [float(s.strip()) for s in re.split("\s+", input.strip())]

def gen_combos(elems):
    bins = [str(bin(i))[2:].zfill(len(elems)) for i in range(2**len(elems))]
    combos = []
    for bi in bins:
        combo = []
        for b, elem in zip(bi, elems):
            if int(b):
                combo.append(elem)
        combos.append(combo)
    return combos

def score(combos, target):
    totals = [sum(combo) for combo in combos]
    diffs = [total - target for total in totals]
    table = list(zip(combos, totals, diffs))
    table.sort(key=lambda x : x[2], reverse=True)
    return table

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("form.html")

@app.route("/", methods=["POST"])
def result():
    input = request.form["input"]
    target = float(request.form["target"])
    values = process_input(input)
    combos = gen_combos(values)
    table = score(combos, target)
    return render_template("result.html", table=table)

if __name__ == "__main__":
   app.run()