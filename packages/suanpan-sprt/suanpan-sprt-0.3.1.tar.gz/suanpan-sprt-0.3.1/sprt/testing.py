import uuid
import json


class TestNode(object):
    def __init__(self, working_dir, file, function='main'):
        self.id = uuid.uuid4().hex
        self.file = file
        self.working_dir = working_dir
        self.function = function
        self.params = {}
        self.node_id = 'test_node'

    def set_params(self, **kwargs):
        self.params = kwargs

    @staticmethod
    def _dumps(value):
        if isinstance(value, dict) or isinstance(value, list):
            value = json.dumps(value)

        return value

    def get_request(self, *args):
        _args = {f'in{index + 1}': self._dumps(arg) for index, arg in enumerate(args)}
        ret = {
            'id': self.id,
            'file': self.file,
            'working_dir': self.working_dir,
            'function': self.function,
            'context': {
                'node_id': self.node_id,
                'params': self.params,
                'args': _args
            }
        }
        return ret
