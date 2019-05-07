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
        input = request.form['input']

        # preprocess ok
        pre_input = preprocess(input)

        # translate
        # trans_output = translate(my_model, pre_input)
        results = translate(task, align_dict, models, tgt_dict, translator, args, use_cuda, pre_input)
        pre_trans = results[0].hypos[0].split('\t')[2]

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
            'data': results[0].hypos,
        })
    else:
        return abort(403)

    
@app.route('/salign', methods=['GET'])
def acc_align():
    if request.method == 'GET':
        salign2()
        return jsonify({
            'status': "ok",
        })


if __name__ == '__main__':
    app.run()
