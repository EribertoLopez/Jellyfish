import argparse
import sys
import pandas as pd
from HTC_submission_helper import *

def main():
	ap = argparse.ArgumentParser(descritption="Process the template and plan a HTC experiment in Aquarium.")
	ap.add_argument("-s", "--server", required=True, help="The server that this plan will be planned in.")
	ap.add_argument("-f", "--file", required=True, help="The name of the template that will be scripted.")
	ap.add_argument("-n", "--name", type=str, help="The name of the plan")

	args = vars(ap.parse_args())
	server = args['server']
	template_filename = args['file']
	plan_name = args['name']

	# Next, parse the planning template to fill in field values
	experimental_design_df = load_template_file(template_filename)

	db = session(server)
	# Use canvase to organize plan
	canvas = planner.Planner(db)
	media_ObjectType = db.ObjectType.find_by_name('800 mL Liquid')
	culture_condition_list = []
	for index, row in experimental_design_df.iterrows():
		strain_sample = get_strain_sample(db, row)
		media_sample = db.Sample.find_by_name(row.Media)
		ccond_op = submit_define_culture_condition(
	        canvas,
	        strain_sample = strain_sample,
	        strain_item = get_strain_item(db, strain_sample, row),
	        strain_ObjectType = db.ObjectType.find_by_name(row.Strain_containerType),
	        media_sample = media_sample,
	        media_ObjectType = media_ObjectType,
	        replicates = row.Replicates,
	        inducer_param = get_inducer_parameter(db, row),
	        antibio_param = get_antibio_parameter(db, row),
	        control_param = get_control_parameter(db, row),
	        options_param = get_options_parameter(db, row)
	    )
		culture_condition_list.append(ccond_op)

	incubation_temperature = 30
	culture_plate_container = db.ObjectType.find_by_name("96 U-bottom Well Plate")
	options_param = {}
	inoculation_op = submit_inoculate_culture_plate(
	    canvas,
	    culture_condition_list,
	    incubation_temperature,
	    culture_plate_container,
	    options_param
	)
	
	canvas.name=(plan_name)
	canvas.layout.topo_sort()
	canvas.layout.draw()
	canvas.create()
	canvas.save()



def load_template_file(filename):
	experimental_design_df = pd.read_excel(filename)
	experimental_design_df = experimental_design_df.set_index('CultureCondition')
	experimental_design_df = experimental_design_df.fillna(value='None')
	return experimental_design_df

if __name__ == '__main__':
	main()