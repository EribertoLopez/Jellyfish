from aquarium_resources.resources import resources

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
    glycerol_stock_plates = []
    for op in plan.operations:
        if op.operation_type.name == 'Make Glycerol Stock Plates':
            for fv in op.output_array('Glycerol Stock Plate'):
                glycerol_stock_plates.append(fv.item.id)
    glycerol_stock_plates = db.Collection.find(glycerol_stock_plates)
    return glycerol_stock_plates



