import os
import json
import threading
import websocket
import requests
import shutil
import pathlib
import zipfile
import queue

from .State import _State
from .Base import _Base, _check_for_error
from .Datasource import _Datasource

RETRY_AFTER = 5  # seconds

class _MessageHandler(_Base):

    def __init__(self, state, token, host):
        super().__init__(token, host)

        self.wshost = self.host.replace('http', 'ws', 1)
        self.state: _State = state

        self.task_queue = queue.Queue()

        self.ws = websocket.WebSocketApp(
            self.wshost,
            on_open=self._on_open,
            on_message=self._on_message,
            on_close=self._on_close,
            on_error=self._on_error
        )

        self.handlers = {
            'client-info': self.client_info,
            'new-project': self.new_project,
            'project-complete': self.project_complete,
            'round-complete': self.round_complete,
            'hyperparams-updated': self.hyperparams_updated,
            'dynamic-trainer': self.dynamic_trainer,
            'round-error': self.round_error,
            'startup-snapshot': self.startup_snapshot,
            'feature-forward': self.feature_forward,
            'feature-backward': self.feature_backward,
            'label-train': self.label_train,
            'label-test': self.label_test
        }
        self.worker_handlers = [
            'client-info',
            'new-project',
            'round-complete',
            'dynamic-trainer',
            'project-complete',
            'startup-snapshot',
            'feature-forward',
            'feature-backward',
            'label-train',
            'label-test'
        ]

    def connect_to_ws(self):
        t = threading.Thread(target=self.ws.run_forever, kwargs={'reconnect': RETRY_AFTER})
        t.daemon = False
        t.start()

        worker_t = threading.Thread(target=self._worker)
        worker_t.daemon = True
        worker_t.start()

    def _worker(self):
        while True:
            task = self.task_queue.get()
            self.handlers[task['event']](task['j'], task['project_key'])
            self.task_queue.task_done()

    def _on_open(self, ws):
        print('>>> Connection to DynamoFL established.')
        self.ws.send('{ "action": "auth", "token": "' + self.token + '" }')

    def _on_message(self, ws, res):
        j = json.loads(res)

        project_key = None
        if 'data' in j and 'project' in j['data'] and 'key' in j['data']['project']:
            project_key = j['data']['project']['key']

        if j['event'] in self.handlers:
            if j['event'] in self.worker_handlers:
                self.task_queue.put_nowait({'event': j['event'], 'j': j, 'project_key': project_key})
            else:
                self.handlers[j['event']](j, project_key)

    def _on_close(self, ws, close_status_code, close_msg):
        print('Connection closed')
        print(close_msg)

    def _on_error(self, ws, error):
        print('Connection error:')
        print(error)
        print(f'Will attempt to reconnect every {RETRY_AFTER} seconds...')

    """
    Message Handlers
    """

    def client_info(self, j, _):
        self.state.instance_id = j['data']['id']
        self.state.initiate_project_participants(should_fetch_bridges=True, should_spawn_train=True)

    def new_project(self, j, _):
        project_key = j['data']['projectKey']

        # Check if datasource type exists for backwards compatibility
        datasource_type = None
        if 'datasourceType' in j['data']:
            datasource_type = j['data']['datasourceType']

        datasource_key = j['data']['datasourceKey']
        trainer_key = j['data']['trainerKey']
        hyper_param_values = {}
        if 'hyperParamValues' in j['data']:
            hyper_param_values = j['data']['hyperParamValues']
        not_sampled = False
        if 'notSampled' in j['data']:
            not_sampled = j['data']['notSampled']

        if datasource_type == 'horizontal' or datasource_type == None:
            self.state.project_participants.append({
                'project_key': project_key,
                'datasource_key': datasource_key,
                'trainer_key': trainer_key,
                'hyper_param_values': hyper_param_values
            })

            if not_sampled:
                return

            info = self._make_request('GET', f'/projects/{project_key}')
            self.state.train_and_test_callback(datasource_key, info)
            return

        vertical_participant = {
            'project_key': project_key,
            'datasource_key': datasource_key,
            'trainer_key': trainer_key,
            'hyper_param_values': hyper_param_values,
        }

        if datasource_type == 'label':
            self.state.label_participants.append(vertical_participant)
        if datasource_type == 'feature':
            self.state.feature_participants.append(vertical_participant)

    def project_complete(self, _, project_key):
        self.state.project_participants = list(filter(lambda x : x['project_key'] != project_key, self.state.project_participants))

    def round_complete(self, j, project_key):
        samples = []
        if 'samples' in j['data']:
            samples = j['data']['samples']

        for p in self.state.project_participants:
            if project_key == p['project_key']:
                if p['datasource_key'] in samples:
                    self.state.train_and_test_callback(p['datasource_key'], j['data']['project'])

    """
        Handler functions related to VFL
    """
    def feature_forward(self, j, project_key):
        for p in self.state.feature_participants:
            if project_key == p['project_key']:
                mode = j['data']['mode']
                round = j['data']['project']['currentRound']

                ds: _Datasource = self.state.datasources[p['datasource_key']]
                trainers = ds.trainers[p['trainer_key']]

                file_path = get_vertical_file_path(mode, project_key, ds.key, round)
                trainers['train'](j['data']['batch'], file_path, ds.key, p['hyper_param_values'])

                upload_url = self._make_request('POST', f'/projects/{project_key}/vertical/upload', {
                    'round': round,
                    'datasourceKey': p['datasource_key'],
                    'mode': mode,
                })['url']

                with open(file_path, 'rb') as f:
                    requests.put(upload_url, data=f)

                self._make_request('POST', f'/projects/{project_key}/vertical/verify', {
                    'round': round,
                    'datasourceKey': p['datasource_key'],
                    'mode': mode,
                })

    def feature_backward(self, j, project_key):
        for p in self.state.feature_participants:
            if project_key == p['project_key']:
                mode = 'backward'
                round = j['data']['project']['currentRound']

                ds: _Datasource = self.state.datasources[p['datasource_key']]
                trainers = ds.trainers[p['trainer_key']]

                # Download gradients
                download_url = self._make_request('POST', f'/projects/{project_key}/vertical/download', {
                    'round': j['data']['project']['currentRound'],
                    'datasourceKey': p['datasource_key'],
                    'mode': mode,
                })['url']

                r = requests.get(download_url)
                _check_for_error(r)

                gradients_path = get_vertical_file_path(mode, project_key, ds.key, round)
                with open(gradients_path, 'wb') as f:
                    f.write(r.content)

                trainers['test'](j['data']['batch'], gradients_path, ds.key, p['hyper_param_values'])

    def label_train(self, j, project_key):
        for p in self.state.label_participants:
            if project_key == p['project_key']:
                round = j['data']['project']['currentRound']

                ds: _Datasource = self.state.datasources[p['datasource_key']]
                trainers = ds.trainers[p['trainer_key']]

                # Download activations
                download_url = self._make_request('POST', f'/projects/{project_key}/vertical/download', {
                    'round': round,
                    'datasourceKey': p['datasource_key'],
                    'mode': 'forward',
                })['url']

                r = requests.get(download_url)
                _check_for_error(r)

                activations_path = get_vertical_file_path('forward', project_key, ds.key, round)
                gradients_path = get_vertical_file_path('backward', project_key, ds.key, round)
                with open(activations_path, 'wb') as f:
                    f.write(r.content)

                # Start training
                trainers['train'](j['data']['batch'], activations_path, gradients_path, ds.key, p['hyper_param_values'])

                # Upload gradients
                upload_url = self._make_request('POST', f'/projects/{project_key}/vertical/upload', {
                    'round': round,
                    'datasourceKey': p['datasource_key'],
                    'mode': 'backward',
                })['url']

                with open(gradients_path, 'rb') as f:
                    requests.put(upload_url, data=f)

                self._make_request('POST', f'/projects/{project_key}/vertical/verify', {
                    'round': round,
                    'datasourceKey': p['datasource_key'],
                    'mode': 'backward',
                })

    def label_test(self, j, project_key):
        for p in self.state.label_participants:
            if project_key == p['project_key']:
                mode = 'test'
                round = j['data']['project']['currentRound']

                ds: _Datasource = self.state.datasources[p['datasource_key']]
                trainers = ds.trainers[p['trainer_key']]

                # Download activations
                download_url = self._make_request('POST', f'/projects/{project_key}/vertical/download', {
                    'round': round,
                    'datasourceKey': p['datasource_key'],
                    'mode': mode,
                })['url']

                r = requests.get(download_url)
                _check_for_error(r)

                activations_path = get_vertical_file_path(mode, project_key, ds.key, round)
                with open(activations_path, 'wb') as f:
                    f.write(r.content)

                result = trainers['test'](j['data']['batch'], activations_path, ds.key, p['hyper_param_values'])
                print('round: ', j['data']['project']['currentRound'], 'result: ', result)

                # Upload result to stats endpoint
                self._make_request('POST', f'/projects/{project_key}/stats', {
                    'round': round,
                    'datasource': p['datasource_key'],
                    'scores': result,
                    'numPoints': len(j['data']['batch']),
                })

    def hyperparams_updated(self, j, project_key):
        for p in self.state.project_participants:
            if project_key == p['project_key'] and p['datasource_key'] == j['data']['datasourceKey']:
                p['hyper_param_values'] = j['data']['hyperParamValues']

    def dynamic_trainer(self, j, project_key):
        if os.path.isdir(f'dynamic_trainers/{project_key}'):
            return

        filename = j['data']['filename']

        url = f'{self._get_route()}/projects/{project_key}/files/{filename}'
        r = requests.get(url, headers=self._get_headers())
        _check_for_error(r)

        filepath = f'dynamic_trainers/{project_key}_{filename}'

        directory = os.path.dirname(filepath)
        pathlib.Path(directory).mkdir(parents=True, exist_ok=True)

        with open(filepath, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                f.write(chunk)

        with zipfile.ZipFile(filepath, 'r') as zip_ref:
            parent_dir_name = zip_ref.namelist()[0][:-1]
            zip_ref.extractall(directory)
        shutil.move(directory + '/' + parent_dir_name, directory + '/' + project_key)
        os.remove(filepath)

    def round_error(self, j, project_key):
        for p in self.state.project_participants:
            print('Federation error occured:\n  ' + j['data']['errorMessage'])

    def startup_snapshot(self, j, _):
        datasource_key = j['data']['datasourceKey']
        snapshot = j['data']['snapshot']
        
        for p in snapshot['projects']:
            if (p['currentRound'] == p['rounds']):
                return

            self.state.train_and_test_callback(datasource_key, p)

def get_vertical_file_path(type, project_key, ds, round):
    return f'{type}_{project_key}_{ds}_{round}.any'
