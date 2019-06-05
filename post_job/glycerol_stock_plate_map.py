# Python Dependancies
import sys
import pandas as pd
import numpy as np
import os
from urllib.request import urlopen
# Trident
import pydent
from pydent import AqSession
from pydent import planner
# Modules
from resources import resources

# Will set the session to desired database
def session():
    db = AqSession(
        resources['aquarium']['login'],
        resources['aquarium']['password'],
        resources['aquarium']['aquarium_url']
    )
    return db

def get_collection_part_associations(collection):
    return collection.part_associations

def data_associations_generator(data_associations):
    for da in data_associations:
        yield da

def get_part_collection_loc(collection):
    alpha_rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    alpha_dict = dict(zip(range(0, len(alpha_rows)), alpha_rows))
    dict_arr = []
    for pa in get_collection_part_associations(collection):
        d = dict()
        d['plate_id'] = collection.id
        d['Well Index'] = alpha_dict[pa.row] +  str(pa.column+1)
        d['Well Label'] = pa.part.id
        d['Vol (uL)'] = 40
        part = pa.part
        for da in data_associations_generator(part.data_associations):
            d[da.key] = da.object[da.key]
        dict_arr.append(d)
    return dict_arr
           
def get_glycerol_stock_plates(db, plan_id):

	plan = db.Plan.find(plan_id)
	glycerol_ops = [op for op in plan.operations if op.operation_type.name == 'Make Glycerol Stock Plates']
	glycerol_stock_plates = db.Collection.find([op.outputs[0].item.id for op in glycerol_ops])
	return glycerol_stock_plates

def main():
	db = session()
	# read commandline arguments, first
	fullCmdArguments = sys.argv
	plan_id_list = fullCmdArguments[1:]
	for plan_id in plan_id_list:
		glycerol_stock_plates = get_glycerol_stock_plates(db, plan_id)
		for collection in glycerol_stock_plates:
		    filename = f'{collection.object_type.name} {collection.id} plate.csv'.replace(' ', '_')
		    df = pd.DataFrame(get_part_collection_loc(collection))
		    df.to_csv(filename)


if __name__ == "__main__":
    main()




