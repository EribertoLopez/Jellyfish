## Planning

The `Jellyfish` repository comes an Excel sheet planning template. The following describes how to properly fill out the template, then how to plan experiment using `plan_experiment.py`. 

1. Go to `Jellyfish/templates/default_template` and make a copy of `HTC_Scripting_Template_v*.xlsx`. Feel free to name the copy to something else.

2. Fill in the `HTC_Scripting_Template_v*.xlsx` with the strains and conditions desired for your experiment.

- **Replicates**
  - **_Int_** - The number of replicates desired for a condition.

- **Media**
  - **_String_** - The name of the media sample as found in the Aquarium database you are using.

- **Control Tag**
  - Will tag culture condition as a control and place this culture(s) into all the plates that are generated.
  - **_JSON_** - The key represents the type of control and value represents positive or negative. Then, you can add your own additional information. 
  **Make sure that the object entered into the template is JSON parable. Any word should be surrounded by quotes.**

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
  - Antibiotic_FinalConcentration **_(String)_** - a list of final concentrations
    - **ie:** 50_ug/mL

- **Options**
  - Is a special case for prototyping or uncommon conditions.
  - **_JSON_** - **Make sure that the object entered into the template is JSON parable. Any word should be surrounded by quotes.**

## Setup

1. Copy `default_resources.py` to `resources.py` and fill in the values for
   `username` and `password` details.

## Running

```bash
python3 plan_experiment.py --help
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

The default planning server is set to `Production`, if you wish to change it use the `-s` flag and type in either `Production, Nursery, or Local`

The command

```bash
python3 -W ignore plan_experiment.py -s Nursery -f path/to/My_Experimental_Intent_Template.xlsx -n "Nobel Prize Experiment"

```

will plan the experiment described in the My_Experimental_Intent_Template.xlsx on the the Aquarium Nursery server. Furthermore, the `-W ignore` command prevents Trident API AllowableField Warning messages.

