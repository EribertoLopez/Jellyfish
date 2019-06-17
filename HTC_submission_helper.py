import json
import re
# Trident
import pydent
from pydent import AqSession
from pydent import planner
from resources import resources 

# Log into database
def session(server):
    db = AqSession(
        resources['aquarium']['login'],
        resources['aquarium']['password'],
        resources['aquarium']['aquarium_url'][server]
    )
    return db

# First, plan a define culture condition operation. 
def submit_define_culture_condition(canvas, strain_sample, strain_item, strain_ObjectType,
                                    media_sample, media_ObjectType, replicates, inducer_param, 
                                    antibio_param, control_param, options_param):
    op = canvas.create_operation_by_name("Define Culture Conditions")
    # Output
    canvas.set_field_value(op.output("Culture Condition"), sample=strain_sample, container=strain_ObjectType, item=strain_item)
    # Inputs
    canvas.set_field_value(op.input('Strain'), sample=strain_sample, container=strain_ObjectType, item=strain_item)
    canvas.set_field_value(op.input('Media'),  sample=media_sample,  container=media_ObjectType)
    # JSON Parsable Paramters
    canvas.set_field_value(op.input('Replicates'),    value=int(replicates))
    canvas.set_field_value(op.input('Inducer(s)'),    value=inducer_param)
    canvas.set_field_value(op.input('Antibiotic(s)'), value=antibio_param)
    canvas.set_field_value(op.input('Control Tag'),   value=control_param)
    canvas.set_field_value(op.input('Option(s)'),     value=options_param)
    return op


def get_strain_sample(db, row):
    if row.Strain_name is not 'None':
        return db.Sample.find_by_name(row.Strain_name)
    else:
        return db.Sample.find(row.Strain_id)
    
def get_strain_item(db, strain_sample, row):
    if row.Strain_item_id is not 'None':
        return db.Item.find(int(row.Strain_item_id))
    else:
        for item in strain_sample.items:
            if item.location != 'deleted':
                if item.object_type.name == row.Strain_containerType:
                    return item
    
def get_inducer_parameter(db, row):
    # ie: { inducer_A_name: { final_concentration: ["XXX_nM"] } }
    inducers_dict = {}
    if row.Inducer_A_name is not 'None':
        inducer_a = { str(row.Inducer_A_name): {"final_concentration": formmat_final_concentration(row.A_FinalConcentrations)} }
        inducers_dict.update(inducer_a)
    if row.Inducer_B_name is not 'None':
        inducer_b = { str(row.Inducer_B_name): {"final_concentration": formmat_final_concentration(row.B_FinalConcentrations)} }
        inducers_dict.update(inducer_b)
    if row.Inducer_C_name is not 'None':
        inducer_c = { str(row.Inducer_C_name): {"final_concentration": formmat_final_concentration(row.C_FinalConcentrations)} }
        inducers_dict.update(inducer_c)
    
    return json.dumps(inducers_dict)

def formmat_final_concentration(final_concentration_token):
    fconc_arr = final_concentration_token.split(',')
    formatted_arr = []
    for fconc in fconc_arr:
        if '_' in fconc:
            formatted_arr.append(fconc)
        else:
            qty = re.findall(r'\d+', fconc)[0]
            units = fconc.split(qty)[-1]
            fconc = qty + "_" + units
            formatted_arr.append(fconc)
    return formatted_arr
                                                                                                   
# TODO: Start planning with antibiotics
def get_antibio_parameter(db, row):
    antibiotics_dict = dict()
    if row.Antibiotics:
        antibiotics_dict.update({})
    else:
        return {}
    return json.dumps(antibiotics_dict)
    
def get_control_parameter(db, row):
    control_dict = dict()
    if row.Control_Tag:
        control_dict.update({})
    else:
        return {}
    return json.dumps(control_dict)
    
def get_options_parameter(db, row):
    options_dict = dict()
    if row.Options:
        options_dict.update({})
    else:
        return {}
    return json.dumps(options_dict)

def submit_inoculate_culture_plate(canvas, culture_condition_list, incubation_temperature, culture_plate_container, options_param):
    op = canvas.create_operation_by_name("Inoculate Culture Plate")
    canvas.set_field_value(op.input("Temperature (°C)"), value=incubation_temperature)
    canvas.set_field_value(op.input("Option(s)"), value=options_param)
    canvas.set_field_value(op.output("Culture Plate"), container=culture_plate_container)
    input_val_array = [input_val for input_val in generate_input_array_values(culture_condition_list)]
    
    for i in range(len(input_val_array)-1):
        op.add_to_field_value_array(name="Culture Condition", role='input')
        
    for idx, cc_op in enumerate(culture_condition_list):
        print()
        strain_item = cc_op.outputs[0].item
        print(strain_item)
        input_array = op.field_value_array(name='Culture Condition', role='input')
        canvas.add_wire(cc_op.outputs[0], input_array[idx])
        canvas.set_field_value(cc_op.output("Culture Condition"), item=strain_item)
        
    op.set_field_value_array(name="Culture Condition", role='input', values=input_val_array)
    return op

def culture_condition_generator(culture_condition_list):
    for idx, cc_op in enumerate(culture_condition_list):
        yield idx, cc_op.output('Culture Condition')
        
def generate_input_array_values(culture_condition_list):
    for idx, cc_op in enumerate(culture_condition_list):
            fvs_dict = {fv.name: fv for fv in cc_op.field_values}
            value = {
                'sample': fvs_dict['Culture Condition'].sample,
                'item': fvs_dict['Culture Condition'].item,
                'container': fvs_dict['Culture Condition'].object_type
            }
            yield value

