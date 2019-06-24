# Aquarium_HTC
Scripts for planning and accessing information about Aquarium High Throughput Culturing operation types through the Trident API.

## Aquarium High Throughput Culturing Planning

**Make sure that the object entered into the template is JSON parable. Any word should be surrounded by quotes.**

1. Fill in the `HTC_Scripting_Template_v*.xlsx` with the strains and conditions desired for your experiment.

- **Replicates**
  - **_Int_** - The amount of replicates desired for a contiion

- **Media**
  - **_String_** - The name of the media sample as found in the Aquarium database you are using.

- **Control Tag**
  - Will tag culture condition as a control and place this culture(s) into all the plates that are generated.
  - **_JSON_** - The key represents the type of control and value represents positive or negative. Then, you can add your own additional information.

  For a flow cytometry control, use the example below.
  ```
    {
      "flourescence_control": "positive",
      "channel": "tdTomato"
    }
  ```
  Growth control example:
  ```
    {
      "growth_control": "negative"
    }
  ```
  

- **Strain**
  - You can select a strain by filling in the Strain name or id.
  - Strain_name **_(String)_** - The name of the strain sample as found in the Aquarium database you are using.
  - Strain_id **_(Int)_** - The strain sample id number as found in the Aquarium database you are using.

- **Inducer(s)**
  - The scripting template allows for upto 3 different types of inducers
  - Each inducer has a name and a list of final concentrations that pertain to that inducer.
  - Inducer_A_name **_(String)_** - The name of the inducer sample as found in the Aquarium database you are using.
  - A_FinalConcentrations **_(list of strings)_** - a list of final concentrations.
    - **ie:** 50_nM or 50nM 
    - **ie:** 0.15_nM, 50_nM, 100nM, 200nM

- **Antibiotics**
  - Antibiotic_name **_(String)_** - The name of the anitbiotic as found in the Aquarium database you are using.
  - Antibiotic_FinalConcentration **_(list of strings)_** - a list of final concentrations
    - **ie:** 50_ug/mL

- **Options**
  - Is a special case for prototyping or uncommon conditions.
  - **_JSON_** - If using options, make sure that the object is JSON parable

## Setup

1. Copy `default_resources.py` to `resources.py` and fill in the values for
   `username` and `password` details.

## Running

```bash
python3 HTC_template_planning.py --help
```

shows the command-line arguments for the script

```bash
optional arguments:
  -h, --help            show this help message and exit
  -s SERVER, --server SERVER
                        The server that this plan will be planned in. Either Production, Nursery, or Local.
  -f FILE, --file FILE  The name of the template that will be scripted.
  -n NAME, --name NAME  The name of your plan.
  -t TEMP, --temp TEMP  The temperature that the culturing plate will be grown
                        to saturation. Default will be 30C.
```

You must provide the name of the server you will be sending your plan to and the name of the file that will be scripted.

The command

```bash
python3 HTC_template_planning.py -s Production -f HTC_Scripting_Template_v3.xlsx -n "Nobel Prize Experiment"

```

will plan the experiment described in the HTC_Scripting_Template_v3.xlsx on the the Aquarium Production server. 


