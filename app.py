from flask import Flask, request, abort, redirect, json, jsonify
from data_process.process import *
from data_process.align import *
from fairseqq.interactive_new import load_model, translate

app = Flask(__name__)

# preload model
task, align_dict, models, tgt_dict, translator, use_cuda, args=load_model()


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/translate', methods=['POST'])
def login():
    if request.method == 'POST':
        # get input from request
        myinput = request.form['input']

        # preprocess ok
        pre_input = preprocess(myinput)

        # translate
        # trans_output = translate(my_model, pre_input)
        results = translate(task, align_dict, models, tgt_dict, translator, args, use_cuda, pre_input)
        pre_trans = results[0].hypos[0].split('\t')[2]

        trans = pre_trans
        #print(pre_input)
        #print(pre_trans)
        # postprocess
        add(pre_input, pre_trans)
        nalign = results[0].alignments[0]
        #print(repr(results))
        salign()

        delete()
        return jsonify({
            'status': "ok",
            'code': 200,
            'data': pre_trans,
        })
    else:
        return abort(403)

@app.route('/align', methods=['POST'])
def acc_align():
    if request.method == 'POST':
        salign2()
        trans = request.form['translation']
        back_trans = backprocess(trans)
        print(back_trans)
        return jsonify({
            'status': "ok",
        })

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
