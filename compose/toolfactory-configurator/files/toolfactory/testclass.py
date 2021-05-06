import argparse
import json
import os
import requests


from bioblend import galaxy

class ToolTester():
    # test a newly installed tool using bioblend
    """

 https://github.com/nsoranzo/bioblend-tutorial/blob/master/historical_exercises/api-scripts.exercises/run_tool.py
import sys
import json
import requests
import output

BASE_URL = 'http://localhost:8080'

# -----------------------------------------------------------------------------
def run_tool( tool_id, history_id, **kwargs ):
    full_url = BASE_URL + '/api/tools'

    #EXERCISE: POST...

# -----------------------------------------------------------------------------
if __name__ == '__main__':
    # e.g. ./run_tool.py Filter1 ebfb8f50c6abde6d '{ "input" : { "src": "hda", "id": "77f74776fd03cbc5" }, "cond" : "c6>=100.0" }'
    # e.g. ./run_tool.py sort1 f597429621d6eb2b '{ "input": { "src": "hda", "id": "b472e2eb553fa0d1" }, "column": "c6", "style": "alpha", "column_set_0|other_column" : "c2", "column_set_0|other_style": "num" }'
    tool_id, history_id = sys.argv[1:3]
    params = json.loads( sys.argv[3] ) if len( sys.argv ) >= 4 else {}
    response = run_tool( tool_id, history_id, **params )
    output.output_response( response )


    def get_testdata(self,urlin,fout):
       '''
        grab a test file
        GET /api/tools/{tool_id}/test_data_download?tool_version={tool_version}&filename={filename}
        http://localhost:8080/api/tools/tacrev/test_data_download?tool_version=2.00&filename=in
        '''
     """
    def __init__(self, args):
        self.galaxy = args.galaxy
        self.key = args.key
        self.tool_id = args.tool_id

    def run_test(self):
        """
    GET /api/tools/{tool_id}/test_data_download?tool_version={tool_version}&filename={filename}
    http://localhost:8080/api/tools/tacrev/test_data_download?tool_version=2.00&filename=input1
        """
        inputs = {}
        gi = galaxy.GalaxyInstance(url=self.galaxy, key=self.key, verify=False)
        chistory = gi.histories.get_most_recently_used_history()
        chistory_id = chistory['id']
        #contents = gi.histories.show_history(chistory_id, contents=True)
        #print('####chistory',chistory,'\n#### contents=',contents)
        #history = gi.histories.create_history(name=f"{self.tool_id}_test_history")
        #new_hist_id = history['id']
        fapi = ''.join([self.galaxy, '/api/tools/', self.tool_id, '/build'])
        build = gi.make_get_request(url=fapi,params={"history_id":chistory_id}).json()
        fapi = ''.join([self.galaxy, '/api/tools/', self.tool_id, '/test_data'])
        test_data = requests.get(fapi, params={'key':self.key, 'history_id':chistory_id})# gi.make_get_request(url=fapi,params={"history_id":chistory_id,'key':self.key}).json()
        print(test_data)
        testinputs = test_data.json()[0].get('inputs',None)
        print('testinputs',testinputs)
        stateinputs = build.get('state_inputs',None) # 'input1': {'values': [{'id': '7b326180327c3fcc', 'src': 'hda'}]}}
        if testinputs:
            for k in testinputs.keys():
                v = testinputs[k]
                if '|' in k:
                    nk = k.split('|')[-1]
                    inputs[nk] = v
                else:
                    inputs[k] = v
        if stateinputs:
            print('stateinputs',stateinputs)
            for k in stateinputs.keys():
                inp = stateinputs[k]
                if isinstance(inp,dict):
                    if inp.get('values',None):
                         for anin in inp['values']:
                            if anin.get('id', None) and anin.get('src', None):
                                gi.histories.copy_dataset(chistory_id, anin['id'], source=anin['src'])
                                print('******copied id', anin['id'])
                                up = {k:anin}
                                print(up)
                                inputs.update(up) # replace the input def
        print('after state inputs', inputs)
        fapi = ''.join([self.galaxy, '/api/tools'])
        r = gi.tools.run_tool(chistory_id, self.tool_id, inputs, input_format='legacy')
        print(f"Called test on {self.tool_id} - got {r}")

def _parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--galaxy", help='URL of target galaxy',default="http://localhost:8080")
    parser.add_argument("-a", "--key", help='Galaxy admin key', default="13073fde17d06591ce36e596e3c29904")
    parser.add_argument("-t", "--tool_id", help='Tool id to test', default="plotter")
    return parser


if __name__ == "__main__":
    args = _parser().parse_args()
    tt = ToolTester(args)
    tt.run_test()

