# Jellyfish
Scripts for planning and accessing information about Aquarium High Throughput Culturing operation types through the Trident API.

_Aequorea victoria_ or the Crystal Jelly, is best known as the source of bioluminescent proteins, aequorin & green fluorescent protein (GFP). Their discoverers, Osamu Shimomura and colleagues, won the 2008 Nobel Prize in Chemistry for their work on GFP. This repository automates the phenotypic charaterization of genetically modified organisms expressing fluorecent proteins.

## Planned Example and Execution

Scripts automate the planning of 'Define Culture Conditions' operations which take JSON parsable parameters 
![High Throughput Culturing Plan](/docs/_images/plan_example.png?raw=true "High Throughput Culturing Plan")

Once planned the operations sort and organize conditions into a high throughput container.
![Inoculate Culture Plate Example](/docs/_images/inoculate_culture_plate_example.png?raw=true "Inoculate Culture Plate Example")

After execution, the virtual container will have representations of user defined experimental conditions.
![Culture Component Representations](/docs/_images/cultureComponent_representation.png?raw=true "Culture Component Representations")

## Getting Started

1. Go to `Jellyfish/aquarium_resources`

2. Copy `default_resources.py` to `resources.py` 

3. Fill in the values for `username` and `password` details.
   

