# Python Dependancies
import os
import sys
sys.path.append(os.getcwd())
import argparse
import pandas as pd
import numpy as np

from urllib.request import urlopen
# Trident
import pydent
from pydent import AqSession
from pydent import planner
# Modules
from HTC_submission_helper import session

# Will set the session to desired database
 
def generate_collection_part_associations(collection):
    for pa in collection.part_associations:
        yield pa

def generate_data_associations(data_associations):
    for da in data_associations:
        yield da

def get_part_collection_loc(collection):
    alpha_rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    alpha_dict = dict(zip(range(0, len(alpha_rows)), alpha_rows))
    dict_arr = []
    for pa in generate_collection_part_associations(collection):
        d = dict()
        d['Container Type'] = "96-pcr"
        d['plate_id'] = collection.id
        d['Storage (C)'] = 'cold_80'
        d['Well Index'] = alpha_dict[pa.row] +  str(pa.column+1)
        d['Well Label'] = pa.part.id
        d['Vol (uL)'] = 40
        for da in generate_data_associations(pa.part.data_associations):
            d[da.key] = da.object[da.key]
        dict_arr.append(d)
    return dict_arr
           
def get_glycerol_stock_plates(db, plan_id):
	plan = db.Plan.find(plan_id)
	glycerol_ops = [op for op in plan.operations if op.operation_type.name == 'Make Glycerol Stock Plates']
	glycerol_stock_plates = db.Collection.find([op.outputs[0].item.id for op in glycerol_ops])
	return glycerol_stock_plates

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-s", "--server", required=True, help="The server that this plan will be planned in. Either Production, Nursery, or Local.")
    ap.add_argument("-p", "--plans", required=True, nargs='+', type=int, help="The plan ids of the plans where the glycerol stock plates were created.")
    args = vars(ap.parse_args())
    db = session(args['server'])
    cwd_path = os.getcwd()
    for plan_id in args['plans']:
        plan_dir_path = cwd_path + '/plan_{}'.format(plan_id)
        os.makedirs(plan_dir_path, exist_ok=True)
        os.chdir(plan_dir_path)
        for collection in get_glycerol_stock_plates(db, plan_id):
            filename = f'{collection.object_type.name} {collection.id} plate.csv'.replace(' ', '_')
            df = pd.DataFrame(get_part_collection_loc(collection))
            df.to_csv(filename)

if __name__ == "__main__":
    main()




