import re
import json
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
        inducer_a = { str(row.Inducer_A_name): {"final_concentration": format_final_concentration(row.A_FinalConcentrations)} }
        inducers_dict.update(inducer_a)
    if row.Inducer_B_name is not 'None':
        inducer_b = { str(row.Inducer_B_name): {"final_concentration": format_final_concentration(row.B_FinalConcentrations)} }
        inducers_dict.update(inducer_b)
    if row.Inducer_C_name is not 'None':
        inducer_c = { str(row.Inducer_C_name): {"final_concentration": format_final_concentration(row.C_FinalConcentrations)} }
        inducers_dict.update(inducer_c)
    return json.dumps(inducers_dict)

def format_final_concentration(final_concentration_token):
    fconc_arr = final_concentration_token.split(',')
    formatted_arr = []
    for fconc in fconc_arr:
        if '_' in fconc:
            formatted_arr.append(fconc)
        else:
            if '.' in fconc:
                matching_string = r"\d+\.\d+"
            else:
                matching_string = r"\d+"
            qty = re.findall(matching_string, fconc)[0]
            units = fconc.split(qty)[-1]
            fconc = qty + "_" + units
            formatted_arr.append(fconc)
    return formatted_arr
                                 
def format_parameter_string(string):
    return string.replace(' ','').replace('{', '').replace('}', '').split(',')

# TODO: Start planning with antibiotics
def get_antibio_parameter(db, row):
    antibiotics_dict = {}
    if row.Antibiotic_name is not 'None':
        antibiotic = { str(row.Antibiotic_name): {"final_concentration": format_final_concentration(row.Antibiotic_FinalConcentration)} }
        antibiotics_dict.update(antibiotic)
    else:
        return antibiotics_dict
    return json.dumps(antibiotics_dict)
    
def get_control_parameter(db, row):
    control_dict = {}
    if row.Control_Tag is not 'None':
        format_str = format_parameter_string(row.Control_Tag)
        for string in format_str:
            key, value = string.split(':')
            control_dict[key] = value
    else:
        return control_dict
    return json.dumps(control_dict)
    
def get_options_parameter(db, row):
    options_dict = {}
    if row.Options is not 'None':
        format_str = format_parameter_string(row.Options)
        for string in format_str:
            key, value = string.split(':')
            control_dict[key] = value
    else:
        return options_dict
    return json.dumps(options_dict)

def submit_inoculate_culture_plate(canvas, culture_condition_list, incubation_temperature, culture_plate_container, options_param):
    op = canvas.create_operation_by_name("Inoculate Culture Plate")
    # Inputs
    canvas.set_field_value(op.input("Temperature (°C)"), value=incubation_temperature)
    canvas.set_field_value(op.input("Option(s)"), value=options_param)
    input_val_array = [input_val for input_val in generate_input_array_values(culture_condition_list)]
    for i in range(len(input_val_array)-1): # Add to the input array
        op.add_to_field_value_array(name="Culture Condition", role='input')
    for idx, cc_op in enumerate(culture_condition_list): # Wire culuture conditions to input array
        strain_item = cc_op.outputs[0].item
        input_array = op.field_value_array(name='Culture Condition', role='input')
        canvas.add_wire(cc_op.outputs[0], input_array[idx])
        canvas.set_field_value(cc_op.output("Culture Condition"), item=strain_item)
    op.set_field_value_array(name="Culture Condition", role='input', values=input_val_array) # Fill in the input field value array
    # Outputs
    for i in range(total_culturing_plates(culture_condition_list, culture_plate_container)-1):
        op.add_to_field_value_array(name="Culture Plate", container=culture_plate_container, role='output')

    return op

def generate_input_array_values(culture_condition_list):
    for idx, cc_op in enumerate(culture_condition_list):
            fvs_dict = {fv.name: fv for fv in cc_op.field_values}
            value = {
                'sample': fvs_dict['Culture Condition'].sample,
                'item': fvs_dict['Culture Condition'].item,
                'container': fvs_dict['Culture Condition'].object_type
            }
            yield value

def get_inducer_combinations(inducer_parameter):
    count_arr = []
    for inducer_name, fconc in json.loads(inducer_parameter).items():
        count_arr.append(int(len(fconc['final_concentration'])))
    return count_arr

def get_total_experimental_wells(culture_condition_list):        
    total_experimental_wells = 0
    for op in culture_condition_list:
        fvs_dict = {fv.name: fv for fv in op.field_values}
        replicates = int(fvs_dict['Replicates'].value)
        for i_cond in get_inducer_combinations(fvs_dict['Inducer(s)'].value):
            replicates *= i_cond
        total_experimental_wells += replicates
    return total_experimental_wells

def total_culturing_plates(culture_condition_list, culture_plate_container):
    max_wells_per_plate = culture_plate_container.rows * culture_plate_container.columns
    total_wells = get_total_experimental_wells(culture_condition_list)
    culturing_plates = 0
    while total_wells > 0:
        culturing_plates += 1
        total_wells -= max_wells_per_plate
    return culturing_plates




