#!/usr/bin/env python

import json
import time
import os

from honssh.config import Config
from honssh.utils import validation


class Plugin(object):
    def __init__(self):
        self.cfg = Config.getInstance()
        self.auth_attempts = []
        self.login_success = False
        self.log_file = self.cfg.get(['folders', 'log_path']) + '/honssh.json'

    def connection_made(self, sensor):
        pass

    def login_successful(self, sensor):
        self.log_event(sensor, 'honssh.ssh.new_connection')

    def login_failed(self, sensor):
        self.log_event(sensor, 'honssh.ssh.login_failed')

    def connection_lost(self, sensor):
        self.log_event(sensor, 'honssh.ssh.lost_connection')

    def channel_opened(self, sensor):
        self.log_event(sensor, 'honssh.ssh.channel_opened')

    def channel_closed(self, sensor):
        self.log_event(sensor, 'honssh.ssh.channel_closed')

    def command_entered(self, sensor):
        channel = sensor['session']['channel']
        command = channel['command']
        command_string = command['command'].replace('\n', '\\n')
        channel['command_string'] = command_string
        if command['success']:
            outcome = 'executed'
        else:
            outcome = 'blocked'
        self.log_event(sensor, 'command.' + outcome)

    def port_forwarding_requested(self, conn_details):
        # TODO: Fix session creation so we can log events such as this, which can happen before/without SSH connection setup
        sensor = {'session': {'peer_ip': conn_details['srcIP'], 'peer_port': conn_details['srcPort']}}
        self.log_event(sensor, 'honssh.ssh.port_forwarding_requested', {'dstIP': conn_details['dstIP'], 'dstPort': conn_details['dstPort']})

    def download_finished(self, sensor):
        self.log_event(sensor, 'honssh.download.finished')

    def validate_config(self):
        props = [['output-json', 'enabled']]
        for prop in props:
            if not self.cfg.check_exist(prop, validation.check_valid_boolean):
                return False
        return True

    def log_event(self, sensor, event, extra=None):
        if extra:
            sensor.update(extra)
        message = sensor
        if 'session_id' in message['session']:
            message['shasum'] = message['session']['session_id']
        message['eventid'] = event
        message['timestamp'] = time.time()
        self.log_to_file(self.log_file, message)

    def log_to_file(self, the_file, string):
        set_permissions = False

        if not os.path.isfile(the_file):
            set_permissions = True

        f = file(the_file, 'a')
        f.write(json.dumps(string) + '\n')
        f.close()

        if set_permissions:
            os.chmod(the_file, 0644)
