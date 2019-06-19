# Aquarium_HTC
Scripts for accessing information about Aquarium High Throughput Culturing operation types through Trident API.

## Setup

1. Copy `default_resources.py` to `resources.py` and fill in the values for
   `username` and `password` details.

## Aquarium High Throughput Culturing Planning

1. Fill in the `HTC_Scripting_Template_v*.xlsx` with the strains and conditions desired for your experiment.

- Replicates
  - *_int_* - The amount of replicates desired for a contiion

- Media
  - *_String_* - The name of the media sample as found in the Aquarium database you are using.

- Control Tag
  - *_Dict_* - The key represents the type of control and value represents positive or negative. Then, you can add your own additional information. 
  - Will tag culture condition as a control and place this culture(s) into all the plates that are generated.

    For a flow cytometry control, use the example below.
    {
      "flourescence_control": "positive",
      "channel": "tdTomato"
    }
    
    Example growth control:
    {
      "growth_control": "negative"
    }

- Strain
  - You can select a strain by filling in the Strain name or id.
  - Strain_name *_String_* - The name of the strain sample as found in the Aquarium database you are using.
  - Strain_id *_int_* - The strain sample id number as found in the Aquarium database you are using.

- Inducer(s)
  - The scripting template allows for upto 3 different types of inducers
  - Each inducer has a name and a list of final concentrations that pertain to that inducer.
  - Inducer_A_name *_String_* - The name of the inducer sample as found in the Aquarium database you are using.
  - A_FinalConcnetrations *_list of strings_* - a list of final concentrations.

