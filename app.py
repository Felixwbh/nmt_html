#!/usr/bin/env python

import sqlite3
import bcrypt
from flask import Flask, request, abort, jsonify, session, g
from flask_cors import CORS
from data_process.process import *
from data_process.align import *
from fairseqq.interactive_new import load_model, load_model1, translate
from fast_align.build.test import *
from datetime import datetime, date

app = Flask(__name__)
CORS(app, supports_credentials=True)
HOST = '127.0.0.1'
PORT = 5000
app.secret_key = b'wehb2@8dfv)(*(><'
DATABASE = './app.db'

# preload model
task, align_dict, models, tgt_dict, translator, use_cuda, args = load_model()
task1, align_dict1, models1, tgt_dict1, translator1, use_cuda1, args1 = load_model1()


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/translatece', methods=['POST'])
def handle_translatece():
    if request.method == 'POST':
        data = request.get_json()
        my_input = data['input']

        # preprocess
        pre_input = preprocess1(my_input)

        # translate
        results = translate(task, align_dict, models, tgt_dict, translator, args, use_cuda, pre_input)
        pre_trans = results[0].hypos[0].split('\t')[2]

        # postprocess
        #nalign = results[0].alignments[0]

        save_translation_history(my_input, pre_trans)

        return jsonify(
            result=True,
            code=200,
            msg="翻译成功",
            data=pre_trans,
        )
    else:
        return abort(403)

@app.route('/translatecetag', methods=['POST'])
def handle_translatecetag():
    if request.method == 'POST':
        data = request.get_json()
        my_input = data['input']

        # preprocess
        pre_input, val = preprocess(my_input)
        session['val'] = val
        # translate
        results = translate(task, align_dict, models, tgt_dict, translator, args, use_cuda, pre_input)
        pre_trans = results[0].hypos[0].split('\t')[2]

        # postprocess
        add(pre_input, pre_trans)
        nalign = results[0].alignments[0]
        salign()
        delete()

        save_translation_history(my_input, pre_trans)

        return jsonify(
            result=True,
            code=200,
            msg="翻译成功",
            data=pre_trans,
        )
    else:
        return abort(403)

@app.route('/translateec', methods=['POST'])
def handle_translateec():
    if request.method == 'POST':
        data = request.get_json()
        my_input = data['input']

        # preprocess
        pre_input = preprocess1(my_input)

        # translate
        results = translate(task1, align_dict1, models1, tgt_dict1, translator1, args1, use_cuda1, pre_input)
        pre_trans = results[0].hypos[0].split('\t')[2]

        # postprocess
        #nalign = results[0].alignments[0]

        save_translation_history(my_input, pre_trans)

        return jsonify(
            result=True,
            code=200,
            msg="翻译成功",
            data=pre_trans,
        )
    else:
        return abort(403)

@app.route('/translateectag', methods=['POST'])
def handle_translateectag():
    if request.method == 'POST':
        data = request.get_json()
        my_input = data['input']

        # preprocess
        pre_input, val = preprocess(my_input)
        session['val'] = val
        # translate
        results = translate(task1, align_dict1, models1, tgt_dict1, translator1, args1, use_cuda1, pre_input)
        pre_trans = results[0].hypos[0].split('\t')[2]

        # postprocess
        add1(pre_input, pre_trans)
        nalign = results[0].alignments[0]
        salign1()
        delete()

        save_translation_history(my_input, pre_trans)

        return jsonify(
            result=True,
            code=200,
            msg="翻译成功",
            data=pre_trans,
        )
    else:
        return abort(403)


@app.route('/align', methods=['POST'])
def acc_align():
    if request.method == 'POST':
        data = request.get_json()
        trans = data['translation']

        salign2()
        val = session['val']
        back_trans = backprocess(trans, val)
        # print(back_trans)

        save_align_history(trans, back_trans)

        return jsonify(
            result=True,
            code=200,
            msg="对齐成功",
            data=back_trans,
        )
    else:
        return abort(403)

@app.route('/translatehtml', methods=['POST'])
def handle_translatehtml():
    if request.method == 'POST':
        data = request.get_json()
        test = data['input']
        pretrans = []
        ans = []
        answer = open('answer.html', 'w', encoding='utf-8')
        def findsentesnce(i):
            num = i
            sentence = ""
            while test[i] != '<':
                sentence += test[i]
                i += 1
            # print(sentence)
            pretrans.append(sentence)
            translate = sentence
            ans.append(int(1))
            answer.write(translate)
            return i - num

        def find(i):
            while (i < len(test)):
                if test[i] != '>':
                    answer.write(test[i])
                    ans.append(test[i])
                    i += 1
                else:
                    answer.write('>')
                    ans.append('>')
                    j = i
                    while (test[j] != '<'):
                        j -= 1
                    if (test[j] == '<' and test[j + 1] == 's' and test[j + 2] == 'c' and test[j + 3] == 'r' and test[
                        j + 4] == 'i' and test[j + 5] == 'p' and test[j + 6] == 't'):
                        # if(test[i-7]=='<' and test[i-6] == 's' and test[i-5] == 'c' and test[i-4] == 'r' and test[i-3] == 'i' and test[i-2] == 'p' and test[i-1] == 't'):
                        i += 1
                        while (test[i - 8] != '<' or test[i - 7] != '/' or test[i - 6] != 's' or test[i - 5] != 'c' or
                               test[i - 4] != 'r' or test[i - 3] != 'i' or test[i - 2] != 'p' or test[i - 1] != 't'):
                            answer.write(test[i])
                            ans.append(test[i])
                            i += 1
                        answer.write('>')
                        ans.append('>')
                    if (test[j] == '<' and test[j + 1] == 'n' and test[j + 2] == 'o' and test[j + 3] == 's' and test[
                        j + 4] == 'c' and test[j + 5] == 'r' and test[j + 6] == 'i' and test[j + 7] == 'p' and test[
                        j + 8] == 't'):
                        i += 1
                        while (test[i - 10] != '<' or test[i - 9] != '/' or test[i - 8] != 'n' or test[i - 7] != 'o' or
                               test[i - 6] != 's' or test[i - 5] != 'c' or test[i - 4] != 'r' or test[i - 3] != 'i' or
                               test[i - 2] != 'p' or test[i - 1] != 't'):
                            answer.write(test[i])
                            ans.append(test[i])
                            i += 1
                        answer.write('>')
                        ans.append('>')
                    i += 1
                    if i >= len(test):
                        break
                    while (test[i] == ' ' or test[i] == '\n' or test[i] == '\t'):
                        answer.write(test[i])
                        ans.append(test[i])
                        i += 1
                        if i >= len(test):
                            break
                    if i >= len(test):
                        break
                    if test[i] == '<' or test[i] == '.':
                        continue
                    else:
                        num = findsentesnce(i)
                        i += num

        for j in range(0, len(test)):
            while (test[j] != '<' or test[j + 1] != 'b' or test[j + 2] != 'o' or test[j + 3] != 'd' or test[
                j + 4] != 'y' ):
                answer.write(test[j])
                ans.append(test[j])
                j += 1
            find(j)
            break

        def tranhtml(pretrans,ans):
            pre_input = []
            results = []
            prealign = []
            #print(len(pretrans))
            #print(pretrans)
            for sen in range(0,len(pretrans)):
                pre_input.append(preprocess1(pretrans[sen]))
            #print(pre_input)
            #print(len(pre_input))
            for sen in range(0,len(pre_input)):
                #print(pre_input[sen])
                result = translate(task, align_dict, models, tgt_dict, translator, args, use_cuda, pre_input[sen])
                #print(result)
                tmp = result[0].hypos[0].split('\t')[2]
                results.append(tmp)
                tmpstring = ""
                tmpstring += str(pre_input[sen]) + "|||" + str(tmp)
                prealign.append(tmpstring)
            print(prealign)
            batchalign = align_batch(prealign)
            print(batchalign)
            #print(len(results))
            y = 0
            ans1 =""
            for x in range(0, len(ans)):
                if ans[x] == 1:
                    ans[x] = results[y]
                    y += 1
            for x in ans:
                ans1 += str(x)
            return ans1
            #pre_input = preprocess(pretrans)
            #results=translate(pre_input)
            #add()
            #salign()
            #delete()

        #print(len(pretrans))
        #print(pretrans)
        end = tranhtml(pretrans, ans)
        return jsonify(
            result=True,
            code=200,
            msg="对齐成功",
            data=end,
        )
    else:
        return abort(403)

# ================== Auth ==================


def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def insert_db(query, args=(), one=False):
    db = get_db()
    cur = db.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    db.commit()
    return (rv[0] if rv else None) if one else rv


def insert_db_return_id(query, args=(), one=False):
    db = get_db()
    cur = db.cursor().execute(query, args)
    rv = cur.fetchall()
    gen_id = cur.lastrowid
    cur.close()
    db.commit()
    return (rv[0] if rv else None) if one else rv, gen_id


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def save_translation_history(source, target):
    if 'username' not in session or 'uid' not in session:
        return

    uid = session['uid']
    rst = insert_db(
        '''INSERT INTO translations (user_id, source, target, created_at) VALUES (?, ?, ?, ?)''',
        args=(uid, source, target, datetime.now()),
    )
    return


def save_align_history(translation, align):
    if 'username' not in session or 'uid' not in session:
        return

    uid = session['uid']
    rst = insert_db(
        '''UPDATE translations SET target=?, created_at=?
         WHERE user_id=? AND target=?''',
        args=(align, datetime.now(), uid, translation),
    )
    return


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route("/auth/register", methods=['POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        username = data['username']
        password = data['password']
        re_password = data['rePassword']
        if password != re_password:
            return jsonify(
                result=False,
                code=403,
                msg="两次输入的密码不一致",
                data=None,
            )
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        try:
            rst, uid = insert_db_return_id(
                '''INSERT INTO users (username, password) VALUES (?, ?)''',
                args=(username, hashed_password),
            )
        except sqlite3.IntegrityError:
            return jsonify(
                result=False,
                code=403,
                msg="用户名已存在",
                data=None,
            )

        return jsonify(
            result=True,
            code=200,
            msg="注册成功",
            data={
                'id': uid,
            }
        )


@app.route("/auth/login", methods=['POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data['username']
        password = data['password']
        rst = query_db(
            '''SELECT * FROM users WHERE username=?''',
            args=[username],
        )
        if len(rst) == 0:
            return jsonify(
                result=False,
                code=403,
                msg="用户名或密码错误",
                data=None,
            )
        if not bcrypt.checkpw(password.encode('utf-8'), rst[0]['password']):
            return jsonify(
                result=False,
                code=403,
                msg="用户名或密码错误",
                data=None,
            )
        # successfully logged in, set session
        session['username'] = username
        session['uid'] = rst[0]['id']
        print(repr(session))
        return jsonify(
            result=True,
            code=200,
            msg="登录成功",
            data={
                'id': rst[0]['id'],
            }
        )


@app.route("/auth/logout", methods=['GET'])
def logout():
    if request.method == 'GET':
        print(repr(session))
        session.pop('username')
        session.pop('uid')
        return jsonify(
            result=True,
            code=200,
            msg="注销成功",
            data=None,
        )


@app.route("/translation/history", methods=['GET'])
def get_translation_history():
    if request.method == 'GET':
        if 'username' not in session or 'uid' not in session:
            return jsonify(
                result=True,
                code=200,
                msg="查询成功",
                data=[],
            )
        else:
            rst = query_db(
                '''SELECT * FROM translations WHERE user_id=?''',
                args=[session['uid']],
            )
            history_list = []
            for r in rst:
                history_list.append({
                    'id': r['id'],
                    'source': r['source'],
                    'target': r['target'],
                    'created_at': r['created_at']
                })
            return jsonify(
                result=True,
                code=200,
                msg="查询成功",
                data=history_list,
            )


@app.route("/translation/history/delete", methods=['POST'])
def delete_translation_history():
    if request.method == 'POST':
        if 'username' not in session or 'uid' not in session:
            return jsonify(
                result=False,
                code=400,
                msg="未登录",
                data=None,
            )
        else:
            uid = session['uid'];
            data = request.get_json()
            id_del = data['id']
            rst = insert_db(
                '''DELETE FROM translations WHERE id=? AND user_id=?''',
                args=[id_del, uid],
            )
            return jsonify(
                result=True,
                code=200,
                msg="删除成功",
                data=None,
            )


if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
