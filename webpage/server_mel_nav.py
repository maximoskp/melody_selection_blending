from flask import Flask, render_template, request, redirect, Response, jsonify
import json
import numpy as np
import os
cwd = os.getcwd()
import sys
import datetime
# use folders of generation functions
# sys.path.insert(0, cwd + '/../saved_data')
sys.path.insert(0, cwd + '/..')
import pickle
import music21 as m21
import MBL_music_processing_functions as mpf
import MBL_melody_features_functions as mff
import MBL_evolution as evo
import MP_file_export_functions as fef

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

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
    tmp_json['s_features_2'] = s_features_2.tolist()
    tmp_json['s_names_1'] = s_names_1
    tmp_json['s_names_2'] = s_names_2
    return jsonify(tmp_json)

@app.route('/blend', methods=['POST'])
def blend():
    data = request.get_data()
    dat_json = json.loads(data)
    print('dat_json: ', dat_json);
    deut_file = dat_json['name1']
    han_file = dat_json['name2']
    deut_name = deut_file.split("/")[-1].split(".")[0]
    han_name = han_file.split("/")[-1].split(".")[0]
    target_features = dat_json['target']
    request_code = datetime.datetime.now().strftime("%I_%M_%S%p_%b_%d_%Y")
    session_folder = deut_name+'_'+han_name+'_'+request_code
    print('APP_ROOT: ', APP_ROOT)
    os.mkdir(APP_ROOT+'/results/'+session_folder)
    output = APP_ROOT+'/results/'+session_folder+'/'
    # evo constants
    nGens = 20
    nPop = 20

    # vvvvv WE ACTUALLY NEED ALL THESE FOR EXTRACTING INTITIAL FEATURES vvvvv
    # vvvvv TO FORM THE FINAL "BLENDED" TARGET FEATURES vvvvv
    # parse pieces
    ds = m21.converter.parse(deut_file)
    hs = m21.converter.parse(han_file)

    # put a piano instrument to both parents - this also needs to happen in evolution
    for i in hs.recurse():
        if 'Instrument' in i.classes:
            i.activeSite.replace(i, m21.instrument.Piano())
    for i in ds.recurse():
        if 'Instrument' in i.classes:
            i.activeSite.replace(i, m21.instrument.Piano())

    # transpose
    d_trans = mpf.neutral_transposition(ds)
    h_trans = mpf.neutral_transposition(hs)

    # fix lowest octave
    d_fix = mpf.fix_lowest_octave(d_trans)
    h_fix = mpf.fix_lowest_octave(h_trans)

    # compute features
    df = mff.get_features_of_stream(d_fix)
    hf = mff.get_features_of_stream(h_fix)

    # compute markov transitions
    dm = mff.compute_melody_markov_transitions(d_fix)
    hm = mff.compute_melody_markov_transitions(h_fix)

    # make base folder based on names
    base_name = 'results/'+session_folder+'/'

    # first write inputs to midi
    fef.write_stream_to_midi(ds, appendToPath=base_name, fileName=deut_name+'.mid')
    fef.write_stream_to_midi(hs, appendToPath=base_name, fileName=han_name+'.mid')

    # make markov target - which remains the same during all simulations
    target_markov = ( dm + hm )/2.0
    evoSession = evo.EvoSession( deut_file, han_file, target_features, target_markov, nPop=nPop, nGen=nGens, print_gens=True )
    # write to midi files
    fef.write_stream_to_midi(evoSession.best_individual.stream, appendToPath=base_name, fileName='bl_'+deut_name+han_name+'.mid')

    tmp_json = {}
    tmp_json['blended'] = evoSession.best_individual.features.tolist()
    return jsonify(tmp_json)

if __name__ == '__main__':
    print('--- --- --- main')
    app.run(host='0.0.0.0', port=8515, debug=True)