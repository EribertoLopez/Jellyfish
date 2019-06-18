import sys
import argparse
import pandas as pd
from HTC_submission_helper import *

def main():
	ap = argparse.ArgumentParser()
	ap.add_argument("-s", "--server", required=True, help="The server that this plan will be planned in.")
	ap.add_argument("-f", "--file", required=True, help="The name of the template that will be scripted.")
	ap.add_argument("-n", "--name", type=str, default='Untitled Experiment', help="The name of your plan.")
	ap.add_argument("-t", "--temp", type=int, default=30, help="The temperature that the culturing plate will be grown to saturation. Default will be 30C.")
	args = vars(ap.parse_args())

	# Next, parse the planning template to fill in field values
	experimental_design_df = load_template_file(args['file'])

	# Use canvas to organize plan
	db = session(args['server']) # Aq session
	canvas = planner.Planner(db)
	media_ObjectType = db.ObjectType.find_by_name('800 mL Liquid')
	culture_condition_list = []
	for index, row in experimental_design_df.iterrows():
		strain_sample = get_strain_sample(db, row)
		strain_item = get_strain_item(db, strain_sample, row)
		strain_ObjectType = db.ObjectType.find_by_name(row.Strain_containerType)
		media_sample = db.Sample.find_by_name(row.Media)
		# Fill in Define Culture Condition operation
		ccond_op = submit_define_culture_condition(
	        canvas,
	        strain_sample = strain_sample,
	        strain_item = strain_item,
	        strain_ObjectType = strain_ObjectType,
	        media_sample = media_sample,
	        media_ObjectType = media_ObjectType,
	        replicates = row.Replicates,
	        inducer_param = get_inducer_parameter(db, row),
	        antibio_param = get_antibio_parameter(db, row),
	        control_param = get_control_parameter(db, row),
	        options_param = get_options_parameter(db, row)
	    )
		culture_condition_list.append(ccond_op)

	incubation_temperature = args['temp']
	culture_plate_container = db.ObjectType.find_by_name("96 U-bottom Well Plate")
	options_param = {}
	# Fill in Inoculate Culture Plate
	inoculation_op = submit_inoculate_culture_plate(
	    canvas,
	    culture_condition_list,
	    incubation_temperature,
	    culture_plate_container,
	    options_param
	)
	# Saving Plan to server
	canvas.name=(args['name'])
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