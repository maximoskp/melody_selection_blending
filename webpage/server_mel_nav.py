from flask import Flask, render_template, request, redirect, Response, jsonify
import json
import numpy as np
import os
cwd = os.getcwd()
import sys
# use folders of generation functions
# sys.path.insert(0, cwd + '/../saved_data')
sys.path.insert(0, cwd + '/..')
import pickle

with open('../saved_data/all_names.pickle', 'rb') as handle:
    all_names = pickle.load(handle)
with open('../saved_data/all_styles.pickle', 'rb') as handle:
    all_styles = pickle.load(handle)
with open('../saved_data/all_styles_idx.pickle', 'rb') as handle:
    all_styles_idx = pickle.load(handle)
with open('../saved_data/all_features.pickle', 'rb') as handle:
    all_features = pickle.load(handle)
with open('../saved_data/all_pca.pickle', 'rb') as handle:
    all_pca = pickle.load(handle)
with open('../saved_data/style_folders.pickle', 'rb') as handle:
    style_folders = pickle.load(handle)
# load sorted pcas and names
with open('../saved_data/s_pca_1.pickle', 'rb') as handle:
    s_pca_1 = pickle.load(handle)
with open('../saved_data/s_pca_2.pickle', 'rb') as handle:
    s_pca_2 = pickle.load(handle)
with open('../saved_data/s_features_1.pickle', 'rb') as handle:
    s_features_1 = pickle.load(handle)
with open('../saved_data/s_features_2.pickle', 'rb') as handle:
    s_features_2 = pickle.load(handle)
with open('../saved_data/s_names_1.pickle', 'rb') as handle:
    s_names_1 = pickle.load(handle)
with open('../saved_data/s_names_2.pickle', 'rb') as handle:
    s_names_2 = pickle.load(handle)

# server
app = Flask(__name__)
# app.config['SECRET_KEY'] = 'secret!'
# socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_initial_data', methods=['POST','GET'])
def get_initial_data():
    # data = request.get_data()
    # dat_json = json.loads(data)
    tmp_json = {}
    tmp_json['s_pca_1'] = s_pca_1.tolist()
    tmp_json['s_pca_2'] = s_pca_2.tolist()
    tmp_json['s_features_1'] = s_features_1.tolist()
    tmp_json['s_feaures_2'] = s_features_2.tolist()
    tmp_json['s_names_1'] = s_names_1
    tmp_json['s_names_2'] = s_names_2
    return jsonify(tmp_json)

if __name__ == '__main__':
    print('--- --- --- main')
    app.run(host='0.0.0.0', port=8515, debug=True)