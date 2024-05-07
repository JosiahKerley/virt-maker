import os
from unittest import TestCase
from virtmaker.template import *


class Test(TestCase):
    inputs = [{
        "params": {
            "foo": "bar",
            "baz": "{{ foo }}"
        },
        "spec": {
            "steps": [
                {"somestep": {
                    "someval": "{{ baz }}"
                }}
            ]
        }
    }]
    outputs = [{'params': {'foo': 'bar', 'baz': 'bar'}, 'spec': {'steps': [{'somestep': {'someval': 'bar'}}]}}]

    def tearDown(self):
        if os.path.exists('to.yml'):
            os.remove('to.yml')
        if os.path.exists('prepend.yml'):
            os.remove('prepend.yml')
        if os.path.exists('from.yml'):
            os.remove('from.yml')
        if os.path.exists('from1.yml'):
            os.remove('from1.yml')
        if os.path.exists('from2.yml'):
            os.remove('from2.yml')

    def test_merge_before_1(self):
        first = {"one": [1, 2, 3], "two": 2, "three": {3: 4}}
        second = {"one": [4, 5, 6], "two": "two", "three": {3: 5}}
        output = {'one': [4, 5, 6, 1, 2, 3], 'two': 2, 'three': {3: 4}}
        self.assertEqual(mergeBefore(first, second), output)

    def test_merge_before_2(self):
        first = {"one": [1, 2, 3], "two": 2, 'three': {3: {4: 5}}}
        second = {"one": [4, 5, 6], "two": "two", 'three': {3: {5: 4}}}
        output = {'one': [4, 5, 6, 1, 2, 3], 'two': 2, 'three': {3: {4: 5, 5: 4}}}
        self.assertEqual(mergeBefore(first, second), output)

    def test_merge_before_3(self):
        first = {"one": {"two": "three"}}
        second = {"one": {"four": "five"}}
        output = {"one": {"two": "three", "four": "five"}}
        self.assertEqual(mergeBefore(first, second), output)

    def test_merge_after_1(self):
        first = {"one": [1, 2, 3], "two": 2, "three": {3: 4}}
        second = {"one": [4, 5, 6], "two": "two", "three": {3: 5}}
        output = {'one': [1, 2, 3, 4, 5, 6], 'two': 'two', 'three': {3: 5}}
        self.assertEqual(mergeAfter(first, second), output)

    def test_merge_after_2(self):
        first = {"one": [1, 2, 3], "two": 2, 'three': {3: {4: 5}}}
        second = {"one": [4, 5, 6], "two": "two", 'three': {3: {5: 4}}}
        output = {'one': [1, 2, 3, 4, 5, 6], 'two': 'two', 'three': {3: {4: 5, 5: 4}}}
        self.assertEqual(mergeAfter(first, second), output)


    def test_traverse_basic(self):
        for idx, input in enumerate(self.inputs):
            self.assertEqual(traverse(input, input['params']), self.outputs[idx])

    def test_template2spec_basic(self):
        for idx, input in enumerate(self.inputs):
            self.assertEqual(template2spec(input), self.outputs[idx]['spec'])

    def test_template2spec_from_filewritten_1(self):
        with open('from.yml', 'w') as f:
            f.write('''
            params:
              find: me
            ''')
        input = load('''
        params:
          some: val
          find: you
        spec:
          steps:
            - some: "{{ some }}"
            - find: "{{ find }}"
        ''', Loader=Loader)
        output = {'steps': [{'some': 'val'}, {'find': 'you'}]}
        self.assertEqual(output, template2spec(input))

    def test_template2spec_from_filewritten_2(self):
        with open('from.yml', 'w') as f:
            f.write('''
            params:
              find: me
              foo: bar
            ''')
        input = load('''
        from: from.yml
        params:
          some: val
          find: you
        spec:
          steps:
            - some: "{{ some }}"
            - find: "{{ find }}"
            - foo: "{{ foo }}"
        ''', Loader=Loader)
        output = {'steps': [{'some': 'val'}, {'find': 'you'}, {'foo': 'bar'}]}
        self.assertEqual(output, template2spec(input))


    def test_template2spec_from_filewritten_3(self):
        with open('from1.yml', 'w') as f:
            f.write('''
            params:
              find: me
              foo: bar
            ''')
        with open('from2.yml', 'w') as f:
            f.write('''
            from: from1.yml
            ''')
        input = load('''
        from: from2.yml
        params:
          some: val
          find: you
        spec:
          steps:
            - some: "{{ some }}"
            - find: "{{ find }}"
            - foo: "{{ foo }}"
        ''', Loader=Loader)
        output = {'steps': [{'some': 'val'}, {'find': 'you'}, {'foo': 'bar'}]}
        self.assertEqual(output, template2spec(input))

    def test_template2spec_to_filewritten_1(self):
        with open('to.yml', 'w') as f:
            f.write('''
            params:
              find: me
            ''')
        input = load('''
        to: to.yml
        params:
          some: val
          find: you
        spec:
          steps:
            - some: "{{ some }}"
            - find: "{{ find }}"
        ''', Loader=Loader)
        output = {'steps': [{'some': 'val'}, {'find': 'me'}]}
        self.assertEqual(output, template2spec(input))

    def test_template2spec_prepend_filewritten_1(self):
        with open('prepend.yml', 'w') as f:
            f.write('''
            params:
              find: me
              foo: bar
            ''')
        input = load('''
        prepend:
          - prepend.yml
        params:
          some: val
          find: you
        spec:
          steps:
            - some: "{{ some }}"
            - find: "{{ find }}"
        ''', Loader=Loader)
        output = {'steps': [{'some': 'val'}, {'find': 'you'}]}
        self.assertEqual(output, template2spec(input))

    # def test_yaml_merging(self):
    #     input = load('''
    #     meta:
    #       pre_steps: &pre_steps
    #         - one:
    #         - two:
    #       steps: &steps
    #         - three:
    #         - four:
    #     spec:
    #       steps:
    #         - three:
    #         - four:
    #         <<: *pre_steps
    #     ''', Loader=Loader)
    #     print(json.dumps(input, indent=2))

