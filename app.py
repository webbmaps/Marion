{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "94bc7a73-96ec-46ff-a4e1-89c6375c4853",
   "metadata": {},
   "outputs": [],
   "source": [
    "import streamlit as st\n",
    "import geemap\n",
    "import ee\n",
    "import os\n",
    "import geopandas as gpd\n",
    "import pandas as pd\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "6a14c56e-9ef4-4a3d-85d7-9ec67c4dcd33",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "\n",
       "            <style>\n",
       "                .geemap-dark {\n",
       "                    --jp-widgets-color: white;\n",
       "                    --jp-widgets-label-color: white;\n",
       "                    --jp-ui-font-color1: white;\n",
       "                    --jp-layout-color2: #454545;\n",
       "                    background-color: #383838;\n",
       "                }\n",
       "\n",
       "                .geemap-dark .jupyter-button {\n",
       "                    --jp-layout-color3: #383838;\n",
       "                }\n",
       "\n",
       "                .geemap-colab {\n",
       "                    background-color: var(--colab-primary-surface-color, white);\n",
       "                }\n",
       "\n",
       "                .geemap-colab .jupyter-button {\n",
       "                    --jp-layout-color3: var(--colab-primary-surface-color, white);\n",
       "                }\n",
       "            </style>\n",
       "            "
      ],
      "text/plain": [
       "<IPython.core.display.HTML object>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "geemap.ee_initialize( project= 'ee-jupyter-wu')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "0b10982a-db8b-41dc-a26b-e75c7a57bdea",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "\n",
       "            <style>\n",
       "                .geemap-dark {\n",
       "                    --jp-widgets-color: white;\n",
       "                    --jp-widgets-label-color: white;\n",
       "                    --jp-ui-font-color1: white;\n",
       "                    --jp-layout-color2: #454545;\n",
       "                    background-color: #383838;\n",
       "                }\n",
       "\n",
       "                .geemap-dark .jupyter-button {\n",
       "                    --jp-layout-color3: #383838;\n",
       "                }\n",
       "\n",
       "                .geemap-colab {\n",
       "                    background-color: var(--colab-primary-surface-color, white);\n",
       "                }\n",
       "\n",
       "                .geemap-colab .jupyter-button {\n",
       "                    --jp-layout-color3: var(--colab-primary-surface-color, white);\n",
       "                }\n",
       "            </style>\n",
       "            "
      ],
      "text/plain": [
       "<IPython.core.display.HTML object>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "data": {
      "application/vnd.jupyter.widget-view+json": {
       "model_id": "72be7b7878e14122a76889db4300c76d",
       "version_major": 2,
       "version_minor": 0
      },
      "text/plain": [
       "Map(center=[37.72529898295289, -88.93492152974316], controls=(WidgetControl(options=['position', 'transparent_…"
      ]
     },
     "execution_count": 3,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "Map=geemap.Map()\n",
    "\n",
    "#shp= 'https://raw.githubusercontent.com/webbmaps/map-data/refs/heads/main/marion_bound.geojson'\n",
    "shp= r\"C:\\Users\\User\\Desktop\\personal data\\boundary\\MArion_bound.shp\"\n",
    "marion= geemap.shp_to_ee(shp)\n",
    "#marion= r\"C:\\Users\\User\\Desktop\\Python\\marion_bound.geojson\"\n",
    "geo= marion.geometry()#makes geometry for geemap from shp \n",
    "\n",
    "\n",
    "image2018 = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \\\n",
    "    .filterBounds(geo) \\\n",
    "    .filterDate('2018-06-01', '2018-12-30') \\\n",
    "    .sort('CLOUDY_PIXEL_PERCENTAGE') \\\n",
    "    .median() \\\n",
    "    .clip(marion)  \n",
    "\n",
    "image2024= ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \\\n",
    "    .filterBounds(geo) \\\n",
    "    .filterDate('2024-06-01', '2024-12-30') \\\n",
    "    .sort('CLOUDY_PIXEL_PERCENTAGE') \\\n",
    "    .median() \\\n",
    "    .clip(marion)  \n",
    "\n",
    "vis_params = {\n",
    "    'min': 0.0,\n",
    "    'max': 3000,\n",
    "    'bands': ['B8', 'B4', 'B3']\n",
    "}\n",
    "\n",
    "Map.centerObject(marion, 13)\n",
    "Map.addLayer(marion,{}, 'City of Marion')\n",
    "Map.addLayer(image2018, vis_params, \"marion 2018\")\n",
    "Map.addLayer(image2024, vis_params, \"marion 2024\")\n",
    "\n",
    "Map"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "1b84c93e-0d20-4302-867b-f39d5dfbced9",
   "metadata": {},
   "source": [
    "ESA landcover sampler\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "e13ea659-50e9-461d-80f7-3d6971950d0b",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "\n",
       "            <style>\n",
       "                .geemap-dark {\n",
       "                    --jp-widgets-color: white;\n",
       "                    --jp-widgets-label-color: white;\n",
       "                    --jp-ui-font-color1: white;\n",
       "                    --jp-layout-color2: #454545;\n",
       "                    background-color: #383838;\n",
       "                }\n",
       "\n",
       "                .geemap-dark .jupyter-button {\n",
       "                    --jp-layout-color3: #383838;\n",
       "                }\n",
       "\n",
       "                .geemap-colab {\n",
       "                    background-color: var(--colab-primary-surface-color, white);\n",
       "                }\n",
       "\n",
       "                .geemap-colab .jupyter-button {\n",
       "                    --jp-layout-color3: var(--colab-primary-surface-color, white);\n",
       "                }\n",
       "            </style>\n",
       "            "
      ],
      "text/plain": [
       "<IPython.core.display.HTML object>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "esa= ee.ImageCollection('ESA/WorldCover/v100')\\\n",
    "        .filterBounds(geo)\\\n",
    "        .select('Map')\\\n",
    "        .first()\\\n",
    "        .clip(marion)\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "Map.add_legend(builtin_legend=\"ESA_WorldCover\")\n",
    "\n",
    "Map.addLayer(esa, {}, 'Landcover')\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "c4cdac56-b057-4147-be1c-8dfad4712772",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "\n",
       "            <style>\n",
       "                .geemap-dark {\n",
       "                    --jp-widgets-color: white;\n",
       "                    --jp-widgets-label-color: white;\n",
       "                    --jp-ui-font-color1: white;\n",
       "                    --jp-layout-color2: #454545;\n",
       "                    background-color: #383838;\n",
       "                }\n",
       "\n",
       "                .geemap-dark .jupyter-button {\n",
       "                    --jp-layout-color3: #383838;\n",
       "                }\n",
       "\n",
       "                .geemap-colab {\n",
       "                    background-color: var(--colab-primary-surface-color, white);\n",
       "                }\n",
       "\n",
       "                .geemap-colab .jupyter-button {\n",
       "                    --jp-layout-color3: var(--colab-primary-surface-color, white);\n",
       "                }\n",
       "            </style>\n",
       "            "
      ],
      "text/plain": [
       "<IPython.core.display.HTML object>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "sample=esa.sample(**{\n",
    "    'region': marion,\n",
    "    'scale': 30,\n",
    "    'numPixels': 3000,\n",
    "    'seed': 0,\n",
    "    'geometries': True\n",
    "})\n",
    "Map.addLayer(sample, {}, 'samples', False)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "cadd9230-0568-40b3-a469-7359f392acfb",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "\n",
       "            <style>\n",
       "                .geemap-dark {\n",
       "                    --jp-widgets-color: white;\n",
       "                    --jp-widgets-label-color: white;\n",
       "                    --jp-ui-font-color1: white;\n",
       "                    --jp-layout-color2: #454545;\n",
       "                    background-color: #383838;\n",
       "                }\n",
       "\n",
       "                .geemap-dark .jupyter-button {\n",
       "                    --jp-layout-color3: #383838;\n",
       "                }\n",
       "\n",
       "                .geemap-colab {\n",
       "                    background-color: var(--colab-primary-surface-color, white);\n",
       "                }\n",
       "\n",
       "                .geemap-colab .jupyter-button {\n",
       "                    --jp-layout-color3: var(--colab-primary-surface-color, white);\n",
       "                }\n",
       "            </style>\n",
       "            "
      ],
      "text/plain": [
       "<IPython.core.display.HTML object>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "data": {
      "text/plain": [
       "{'type': 'Feature',\n",
       " 'geometry': {'geodesic': False,\n",
       "  'type': 'Point',\n",
       "  'coordinates': [-88.96001295208606, 37.76079280169483]},\n",
       " 'id': '0',\n",
       " 'properties': {'Map': 30}}"
      ]
     },
     "execution_count": 6,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "sample.first().getInfo()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "d13d5727-74eb-4220-9bea-a14291cae693",
   "metadata": {},
   "source": [
    "Train the Classer"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "id": "2fe62e15-be84-47cb-ab47-0238dcacaf6e",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "\n",
       "            <style>\n",
       "                .geemap-dark {\n",
       "                    --jp-widgets-color: white;\n",
       "                    --jp-widgets-label-color: white;\n",
       "                    --jp-ui-font-color1: white;\n",
       "                    --jp-layout-color2: #454545;\n",
       "                    background-color: #383838;\n",
       "                }\n",
       "\n",
       "                .geemap-dark .jupyter-button {\n",
       "                    --jp-layout-color3: #383838;\n",
       "                }\n",
       "\n",
       "                .geemap-colab {\n",
       "                    background-color: var(--colab-primary-surface-color, white);\n",
       "                }\n",
       "\n",
       "                .geemap-colab .jupyter-button {\n",
       "                    --jp-layout-color3: var(--colab-primary-surface-color, white);\n",
       "                }\n",
       "            </style>\n",
       "            "
      ],
      "text/plain": [
       "<IPython.core.display.HTML object>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "bands= ['B8','B4', 'B3']\n",
    "\n",
    "label= 'Map'\n",
    "valid_samples = sample.filter(ee.Filter.notNull([label]))\n",
    "\n",
    "training= image2018.select(bands).sampleRegions(**{'collection': sample, 'properties': [label], 'scale': 30})\n",
    "trained= ee.Classifier.smileCart().train(training, label, bands)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "id": "d8f443fc-2f17-4997-acb8-0bffb5c1411f",
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "id": "7b210c8c-ed47-4d22-99ca-111691b363af",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "\n",
       "            <style>\n",
       "                .geemap-dark {\n",
       "                    --jp-widgets-color: white;\n",
       "                    --jp-widgets-label-color: white;\n",
       "                    --jp-ui-font-color1: white;\n",
       "                    --jp-layout-color2: #454545;\n",
       "                    background-color: #383838;\n",
       "                }\n",
       "\n",
       "                .geemap-dark .jupyter-button {\n",
       "                    --jp-layout-color3: #383838;\n",
       "                }\n",
       "\n",
       "                .geemap-colab {\n",
       "                    background-color: var(--colab-primary-surface-color, white);\n",
       "                }\n",
       "\n",
       "                .geemap-colab .jupyter-button {\n",
       "                    --jp-layout-color3: var(--colab-primary-surface-color, white);\n",
       "                }\n",
       "            </style>\n",
       "            "
      ],
      "text/plain": [
       "<IPython.core.display.HTML object>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "{'type': 'Feature', 'geometry': None, 'id': '0_0', 'properties': {'B3': 931.5, 'B4': 871.5, 'B8': 3654.5, 'Map': 30}}\n"
     ]
    }
   ],
   "source": [
    "print(training.first().getInfo())"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "a2638719-1712-4aa3-b3fe-b85186cabcd5",
   "metadata": {},
   "source": [
    "Results"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "id": "5a617049-7e05-4a7e-a0a7-9cf3ffa67be9",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "\n",
       "            <style>\n",
       "                .geemap-dark {\n",
       "                    --jp-widgets-color: white;\n",
       "                    --jp-widgets-label-color: white;\n",
       "                    --jp-ui-font-color1: white;\n",
       "                    --jp-layout-color2: #454545;\n",
       "                    background-color: #383838;\n",
       "                }\n",
       "\n",
       "                .geemap-dark .jupyter-button {\n",
       "                    --jp-layout-color3: #383838;\n",
       "                }\n",
       "\n",
       "                .geemap-colab {\n",
       "                    background-color: var(--colab-primary-surface-color, white);\n",
       "                }\n",
       "\n",
       "                .geemap-colab .jupyter-button {\n",
       "                    --jp-layout-color3: var(--colab-primary-surface-color, white);\n",
       "                }\n",
       "            </style>\n",
       "            "
      ],
      "text/plain": [
       "<IPython.core.display.HTML object>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "\n",
    "\n",
    "result18= image2018.select(bands).classify(trained)\n",
    "\n",
    "\n",
    "Map.addLayer(result18.randomVisualizer(),{}, 'Classed 2018')\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "id": "d2b5f096-715d-46c3-9087-3a23d7deac26",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "\n",
       "            <style>\n",
       "                .geemap-dark {\n",
       "                    --jp-widgets-color: white;\n",
       "                    --jp-widgets-label-color: white;\n",
       "                    --jp-ui-font-color1: white;\n",
       "                    --jp-layout-color2: #454545;\n",
       "                    background-color: #383838;\n",
       "                }\n",
       "\n",
       "                .geemap-dark .jupyter-button {\n",
       "                    --jp-layout-color3: #383838;\n",
       "                }\n",
       "\n",
       "                .geemap-colab {\n",
       "                    background-color: var(--colab-primary-surface-color, white);\n",
       "                }\n",
       "\n",
       "                .geemap-colab .jupyter-button {\n",
       "                    --jp-layout-color3: var(--colab-primary-surface-color, white);\n",
       "                }\n",
       "            </style>\n",
       "            "
      ],
      "text/plain": [
       "<IPython.core.display.HTML object>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "accuracy = trained.confusionMatrix()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "id": "0352cc1e-273e-45f5-8ed2-7b5d740ede9b",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "\n",
       "            <style>\n",
       "                .geemap-dark {\n",
       "                    --jp-widgets-color: white;\n",
       "                    --jp-widgets-label-color: white;\n",
       "                    --jp-ui-font-color1: white;\n",
       "                    --jp-layout-color2: #454545;\n",
       "                    background-color: #383838;\n",
       "                }\n",
       "\n",
       "                .geemap-dark .jupyter-button {\n",
       "                    --jp-layout-color3: #383838;\n",
       "                }\n",
       "\n",
       "                .geemap-colab {\n",
       "                    background-color: var(--colab-primary-surface-color, white);\n",
       "                }\n",
       "\n",
       "                .geemap-colab .jupyter-button {\n",
       "                    --jp-layout-color3: var(--colab-primary-surface-color, white);\n",
       "                }\n",
       "            </style>\n",
       "            "
      ],
      "text/plain": [
       "<IPython.core.display.HTML object>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "data": {
      "text/plain": [
       "1"
      ]
     },
     "execution_count": 11,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "accuracy.kappa().getInfo()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "752286db-5655-4eea-ac41-1ae51a733c0a",
   "metadata": {},
   "source": [
    "Make the legend pretty"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "id": "76868e2e-0778-48b3-aa26-a9a62bae6af0",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "\n",
       "            <style>\n",
       "                .geemap-dark {\n",
       "                    --jp-widgets-color: white;\n",
       "                    --jp-widgets-label-color: white;\n",
       "                    --jp-ui-font-color1: white;\n",
       "                    --jp-layout-color2: #454545;\n",
       "                    background-color: #383838;\n",
       "                }\n",
       "\n",
       "                .geemap-dark .jupyter-button {\n",
       "                    --jp-layout-color3: #383838;\n",
       "                }\n",
       "\n",
       "                .geemap-colab {\n",
       "                    background-color: var(--colab-primary-surface-color, white);\n",
       "                }\n",
       "\n",
       "                .geemap-colab .jupyter-button {\n",
       "                    --jp-layout-color3: var(--colab-primary-surface-color, white);\n",
       "                }\n",
       "            </style>\n",
       "            "
      ],
      "text/plain": [
       "<IPython.core.display.HTML object>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "class_values= esa.get('landcover_class_values').getInfo()\n",
    "class_palette = esa.get(\"landcover_class_palette\").getInfo()\n",
    "class_palette\n",
    "\n",
    "landcover = result18.set(\"classification_class_values\", class_values)\n",
    "landcover = landcover.set(\"classification_class_palette\", class_palette)\n"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "8d9f33a4-3189-4951-9a04-75bd376ad29e",
   "metadata": {},
   "source": [
    "second Image processing\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "id": "af3249ce-92d4-433a-a940-c99f1267d7a3",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "\n",
       "            <style>\n",
       "                .geemap-dark {\n",
       "                    --jp-widgets-color: white;\n",
       "                    --jp-widgets-label-color: white;\n",
       "                    --jp-ui-font-color1: white;\n",
       "                    --jp-layout-color2: #454545;\n",
       "                    background-color: #383838;\n",
       "                }\n",
       "\n",
       "                .geemap-dark .jupyter-button {\n",
       "                    --jp-layout-color3: #383838;\n",
       "                }\n",
       "\n",
       "                .geemap-colab {\n",
       "                    background-color: var(--colab-primary-surface-color, white);\n",
       "                }\n",
       "\n",
       "                .geemap-colab .jupyter-button {\n",
       "                    --jp-layout-color3: var(--colab-primary-surface-color, white);\n",
       "                }\n",
       "            </style>\n",
       "            "
      ],
      "text/plain": [
       "<IPython.core.display.HTML object>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "bands= ['B8','B4','B3']\n",
    "label= 'Map'\n",
    "valid_samples2 = sample.filter(ee.Filter.notNull([label]))\n",
    "\n",
    "training2= image2024.select(bands).sampleRegions(**{'collection': sample, 'properties': [label], 'scale': 30})\n",
    "trained2= ee.Classifier.smileCart().train(training2, label, bands)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "id": "97ddf3ec-1559-4461-adb4-d2655dabb430",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "\n",
       "            <style>\n",
       "                .geemap-dark {\n",
       "                    --jp-widgets-color: white;\n",
       "                    --jp-widgets-label-color: white;\n",
       "                    --jp-ui-font-color1: white;\n",
       "                    --jp-layout-color2: #454545;\n",
       "                    background-color: #383838;\n",
       "                }\n",
       "\n",
       "                .geemap-dark .jupyter-button {\n",
       "                    --jp-layout-color3: #383838;\n",
       "                }\n",
       "\n",
       "                .geemap-colab {\n",
       "                    background-color: var(--colab-primary-surface-color, white);\n",
       "                }\n",
       "\n",
       "                .geemap-colab .jupyter-button {\n",
       "                    --jp-layout-color3: var(--colab-primary-surface-color, white);\n",
       "                }\n",
       "            </style>\n",
       "            "
      ],
      "text/plain": [
       "<IPython.core.display.HTML object>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "{'type': 'Feature', 'geometry': None, 'id': '0_0', 'properties': {'B3': 931.5, 'B4': 871.5, 'B8': 3654.5, 'Map': 30}}\n"
     ]
    }
   ],
   "source": [
    "print(training.first().getInfo())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "id": "b3f808a8-5f33-443e-b10a-a68508fa9032",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "\n",
       "            <style>\n",
       "                .geemap-dark {\n",
       "                    --jp-widgets-color: white;\n",
       "                    --jp-widgets-label-color: white;\n",
       "                    --jp-ui-font-color1: white;\n",
       "                    --jp-layout-color2: #454545;\n",
       "                    background-color: #383838;\n",
       "                }\n",
       "\n",
       "                .geemap-dark .jupyter-button {\n",
       "                    --jp-layout-color3: #383838;\n",
       "                }\n",
       "\n",
       "                .geemap-colab {\n",
       "                    background-color: var(--colab-primary-surface-color, white);\n",
       "                }\n",
       "\n",
       "                .geemap-colab .jupyter-button {\n",
       "                    --jp-layout-color3: var(--colab-primary-surface-color, white);\n",
       "                }\n",
       "            </style>\n",
       "            "
      ],
      "text/plain": [
       "<IPython.core.display.HTML object>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "result24= image2024.select(bands).classify(trained2)\n",
    "\n",
    "Map.addLayer(result24.randomVisualizer(),{}, 'Classed 2024')\n",
    "#values are correct, color is random"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 16,
   "id": "6777ebee-ef6c-4ed8-9a51-3750f9a45eaa",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "\n",
       "            <style>\n",
       "                .geemap-dark {\n",
       "                    --jp-widgets-color: white;\n",
       "                    --jp-widgets-label-color: white;\n",
       "                    --jp-ui-font-color1: white;\n",
       "                    --jp-layout-color2: #454545;\n",
       "                    background-color: #383838;\n",
       "                }\n",
       "\n",
       "                .geemap-dark .jupyter-button {\n",
       "                    --jp-layout-color3: #383838;\n",
       "                }\n",
       "\n",
       "                .geemap-colab {\n",
       "                    background-color: var(--colab-primary-surface-color, white);\n",
       "                }\n",
       "\n",
       "                .geemap-colab .jupyter-button {\n",
       "                    --jp-layout-color3: var(--colab-primary-surface-color, white);\n",
       "                }\n",
       "            </style>\n",
       "            "
      ],
      "text/plain": [
       "<IPython.core.display.HTML object>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "class_values= esa.get('landcover_class_values').getInfo()\n",
    "class_palette = esa.get(\"landcover_class_palette\").getInfo()\n",
    "class_palette\n",
    "\n",
    "landcover = result24.set(\"classification_class_values\", class_values)\n",
    "landcover = landcover.set(\"classification_class_palette\", class_palette)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 20,
   "id": "9f7defbc-d93c-420f-beff-b080bb5421d5",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "\n",
       "            <style>\n",
       "                .geemap-dark {\n",
       "                    --jp-widgets-color: white;\n",
       "                    --jp-widgets-label-color: white;\n",
       "                    --jp-ui-font-color1: white;\n",
       "                    --jp-layout-color2: #454545;\n",
       "                    background-color: #383838;\n",
       "                }\n",
       "\n",
       "                .geemap-dark .jupyter-button {\n",
       "                    --jp-layout-color3: #383838;\n",
       "                }\n",
       "\n",
       "                .geemap-colab {\n",
       "                    background-color: var(--colab-primary-surface-color, white);\n",
       "                }\n",
       "\n",
       "                .geemap-colab .jupyter-button {\n",
       "                    --jp-layout-color3: var(--colab-primary-surface-color, white);\n",
       "                }\n",
       "            </style>\n",
       "            "
      ],
      "text/plain": [
       "<IPython.core.display.HTML object>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "# urban sprawl classifying, 0= not urban change, 1= yes urban\n",
    "target_classes = [50, 60]\n",
    "\n",
    "# Create masks for each target class in both images\n",
    "classified2018 = result18.updateMask(result18.eq(50))#.Or(result1.eq(60)))\n",
    "classified2024= result24.updateMask(result24.eq(50))#.Or(result2.eq(60)))\n",
    "\n",
    "# Generate boolean change map: 1 if class changed (50 <-> 60), 0 if same\n",
    "change_map = classified2018.neq(classified2024).rename('change')\n",
    "\n",
    "# Optional visualization: 0 = no change (transparent), 1 = change (red)\n",
    "vis_params = {'min': 0, 'max': 1, 'palette': ['39ff14', '008080']}\n",
    "Map.addLayer(change_map, vis_params, 'Urban Change 2018-2024')\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 19,
   "id": "c19623da-4398-404b-832f-79a00131edcb",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "\n",
       "            <style>\n",
       "                .geemap-dark {\n",
       "                    --jp-widgets-color: white;\n",
       "                    --jp-widgets-label-color: white;\n",
       "                    --jp-ui-font-color1: white;\n",
       "                    --jp-layout-color2: #454545;\n",
       "                    background-color: #383838;\n",
       "                }\n",
       "\n",
       "                .geemap-dark .jupyter-button {\n",
       "                    --jp-layout-color3: #383838;\n",
       "                }\n",
       "\n",
       "                .geemap-colab {\n",
       "                    background-color: var(--colab-primary-surface-color, white);\n",
       "                }\n",
       "\n",
       "                .geemap-colab .jupyter-button {\n",
       "                    --jp-layout-color3: var(--colab-primary-surface-color, white);\n",
       "                }\n",
       "            </style>\n",
       "            "
      ],
      "text/plain": [
       "<IPython.core.display.HTML object>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "data": {
      "image/png": "iVBORw0KGgoAAAANSUhEUgAAAxYAAAMWCAYAAABsvhCnAAAAOnRFWHRTb2Z0d2FyZQBNYXRwbG90bGliIHZlcnNpb24zLjEwLjEsIGh0dHBzOi8vbWF0cGxvdGxpYi5vcmcvc2/+5QAAAAlwSFlzAAAPYQAAD2EBqD+naQAAr8hJREFUeJzt3QeYFMX6uO3CBGJARSWIWTFjPuaEOQfUY8aImONRUY6KAczpmDBhzmBWzAlzjseARwQVMBJMgDLf9dTvq/33DrsI9C67Pfvc1zXCzg5j93RPd71V71vVrFQqlYIkSZIk5TBDnn8sSZIkSTCwkCRJkpSbgYUkSZKk3AwsJEmSJOVmYCFJkiQpNwMLSZIkSbkZWEiSJEnKzcBCkiRJUm4GFpIkSZJyM7CQ1GTsu+++YZFFFmnozWgUhgwZEpo1axYuuOCCht4USVKFMLCQVG9uvPHG2Hh98803G3pTmpR333037LXXXmHBBRcMzZs3D/PMM0/YZJNNQr9+/cJff/0Vmrphw4aFXr16hX/84x9h7rnnDvPOO2/YcMMNw1NPPVXj60eNGhW6desW5ptvvjDbbLOFjTbaKLz99tuTvO6uu+6Kn/uSSy4Zz3veszaff/552G233UKHDh1Cy5Ytw9JLLx3OOOOM8Ntvv4WGNHHixPi93W677eL5w/4uv/zy4ayzzgp//PFHjf/m+uuvD8sss0xo0aJF3Pf//Oc/k7xmwIAB4Z///GdYbLHF4v4utdRS4bjjjouf7eR88cUX8X29jkjFMFNDb4Akqe5cd911oXv37qFNmzZh7733jg29sWPHhqeffjoccMABYfjw4eHkk08OTdkDDzwQzj333LDDDjuErl27hj///DPcfPPNYdNNNw033HBD2G+//ao1tLfeeuvw3nvvhX/9618xCLnyyitj0PDWW2/Fzze56qqr4nOrr756+PHHHycb2BDUtGrVKhx++OEx8HvllVfCaaedFv8929dQCGzY/zXXXDOeR/PPP3/VtnEOPfPMM7GRn/Tt2ze+rkuXLuHYY48NL774YjjyyCPj+5x44olVryMwa9++fQy8FlpoofDBBx+Eyy+/PDz66KMxSJt11llr3J5jjjkmzDTTTGHcuHHTZf8l5VSSpHrSr1+/EpeZN954o9QYdO3atbTwwguXiuzXX3+t9XevvPJKacYZZyytu+66pTFjxkzye44DxwRffvllPDbnn39+qan58MMPS99//3215/7444/S0ksvXerQoUO15++66674Od1zzz1Vz3333Xelueaaq7T77rtXe+3QoUNLf/31V/z7csstV9pggw1q/P+fffbZ8T3Zjqx99tknPv/TTz+VGsq4ceNKL7300iTP9+rVK27bk08+WfXcb7/9VmrdunVp6623rvbaPffcszTbbLNV249nn312kve86aab4ntee+21NW7LwIEDS7PMMkupZ8+ejeo6Iql2pkJJalDjx48Pp556alh11VVjDy6pF+utt1549tlna60JuOaaa8Liiy8e03zoHX7jjTcmed/7778/pnCQRsGf9913X43/f3qkL7300rDCCivE15LussUWW1RLu6BH+8wzz6z6f1KnQa9/thd1m222iWkeNVlrrbXCaqutVu25W2+9Ne4zPbX0WJMWQ092Fr3ibDu92Ouvv35MIZncaAPpPXxGt912W5hjjjkm+T3bQJ1Jub/7PN9///3479g/PqO2bduG/ffff5Je+dNPPz3+/wcPHhxfP9dcc8VjSg94eYrP77//Hnu2GQFgW0m9+eabb+K/532yeJ7/H6MwbONyyy0XRxbKDR06NHzyySfh7/Dv+f9m8b5bbbVV+Prrr+MIT3LvvffG/+9OO+1U9RznyK677hpHFrLnAKlDM8zw97fVMWPGxD9536x27drFfz/LLLPU+m8Z4Zh99tlrTJnafffd47FJ6W6cw5tvvnncV86zRRddNH6Ok8P/e+21157k+R133DH++d///rfqOb6jnAOHHnpotdcedthh4ddffw2PPPJI1XM1pYXV9J7JhAkTwlFHHRUfnJuSisHAQlKDopFF+g4ND9JTaFR+//33sUFErUC522+/PZx//vnh4IMPjnnfBBw0+miIJE888URMzaCR2qdPn5jyQuO2phxt0oOOPvro2Cjk/3/SSSfFxvOrr75a9ZoDDzwwBj+rrLJKuPjii8MGG2wQ35dgICF//Msvv5ykUf7VV1/F98q+9uyzzw777LNPTKO56KKL4v+fNBOCh/KccxpuW265ZVhppZXCJZdcEvP7a0JDM70HqSZTako+zyeffDL873//i58h+fPsy5133hkb4qUSncnV0eimcc5nxN/J2SfoySLw4L14Dz53Gr6kHJUbOXJkTMuh/oFGNUHgEkss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pu8lzas2zLJEIEDgm9CDTvDICFVN9Rd/h2CEUYnyGaXuuOOOGLxMySgM5xVpTRxPalYINMoDwvJjlhr6f5cORUoe5zXBCqM5tY2aEcgSkDObVRY/E3RlvxvMAMUsVewfwTxBY01Ie2Nq6Owj1d5wvBhZktR4OWIhqd6x5kAq2M2iQUcPP402ekdpiNCLTdoFhdY1NY6nBGlUvBeFrKR/MCJBo5X1C7LvydStNMIvu+yy2AOfUnvooeZ3TG+64oorxjQcGjz0lJK7/vrrr8cGHelb5dO/EojQy3788cdXNYyzGLFgWtcePXrEVA/eg9ez3zSiyL3n304L0q+uuOKKWBS99NJLV1t5m8JmcvL5f08NajcoMj7vvPNijzo1H0zny/ZOK6Yj5XMhOCGQokf9+eefr2poZ0euKBimoH2NNdaIaUucFxxPirYpKObvCWk7vM/fpVzxOZNyw2fDKBTpeFkU+qc1Jggs2D5qOghM08rbjKKUB6QvvPBCfKSgh2lh0+fNZ8gjjZSQCsdoFucYdUU04HmOkYQpSa9iClzS30455ZQYKJQHsJyfbCffK845zoFrr702Hs/s6EI5XkfgR2DCdpZPa8t7sS4LCDhY34V1K0j349/x3eHzZIQkOwrId4sJAfjcBw0aFB8JnzWfOQg+yqURCr575VPbSmpkJjNjlCTlkqaJrO0xbNiwOH1m79694zSwTNe68sorlx5++OFJVsme3ErR5VOUon///qVlllkmvueyyy5bGjBgQI0rbzPdLe/Jqsus8ss0mVtuuWWcEjWZMGFCXHl40UUXLc0888ylBRdcsNSjR4+4WnNNWHmYbWKKztqwfayQzXSmPPj/M33np59+WvUapitl2tKpxbbvsccepfbt28ftnXvuuUsbb7xxXOk4rQw9NZ/n119/HaeMZbVppnjdZZddSt9+++0kr0vTzZavap3OA/6f2RXE2d955pmnNPvss5d22GGHuO+87pxzzqn270eOHBlfy+fO/rRt2zbuzzXXXFPtdVM63Wzaztoe5atEMx0vU6MyZW7Lli3j/6emqU8n977l5+drr70WzzP2hX3q2LFjnGqYc21KMT0t773EEktM8ru33347rgy+0EILxe/A/PPPX9pmm21Kb7755mTfM50XtT34DpXjOCy11FLx+7P44ouXLr744qrpmpPJvefkpuWF081KxdGM/zR0cCNJEtMEU9RMjze1AJKkYrHGQpI03dW0xgGpUeTgp5QhSVKxWGMhSZruqNmgmJwaFWYcor6ABzUmdTWjlSRp+jIVSpI03TFLF8XPFERTUM/aBBSbU4xc09SmkqTGz8BCkiRJUm7WWEiSJEnKzcBCkiRJUm4Vn8jKYlesgssCVNlFlyRJkiRNHlUTLJ7J4p3M3NekAwuCCmcYkSRJkqbdsGHDQocOHZp2YMFIRfow5pxzzobeHEmSJKkwxowZEzvpU5u6SQcWKf2JoMLAQpIkSZp6U1JSYPG2JEmSpNwMLCRJkiTlZmAhSZIkKbeKr7GQJElSZfrrr7/ChAkTGnozCm3mmWcOM844Y528l4GFJEmSCre2wogRI8KoUaMaelMqwlxzzRXatm2be803AwtJkiQVSgoq5p9//tCyZUsXQc4RoP3222/hu+++iz+3a9cu5GFgIUmSpEKlP6WgonXr1g29OYU366yzxj8JLvhM86RFWbwtSZKkwkg1FYxUqG6kzzJvvYqBhSRJkgrH9KfG91kaWEiSJEnKzcBCkiRJUm4Wb0uSJKnwmh00fVOjSteWpur1ffr0CQMGDAiffPJJLJhee+21w7nnnhuWWmqpqtf88ccf4bjjjgt33nlnGDduXNh8883DlVdeGdq0aVP1miOPPDK89NJL4cMPPwzLLLNMePfddyf5fz3++OPhtNNOCx999FFo0aJFWH/99cOFF14YFllkkVCfHLGYTjbbbLPQqVOnsNJKK4X11lsvvPPOO/Hk2WGHHULHjh3DiiuuGDbddNMwePDgGv/9l19+GVZdddX475dffvmwyy67hJ9//nm674ckSZKm3vPPPx8OO+yw8Oqrr4Ynn3wyFkrTPvz111+rXnPMMceEhx56KNxzzz3x9d9++23YaaedJnmv/fffP/zzn/+stc24/fbbh86dO8eggyDjhx9+qPF96pojFtPJ3XffHRcfwX333Rf23Xff8Nprr4Vu3bqFLbfcMhbNXH755eHAAw8Mzz333CT/vn379mHQoEFVU4IdddRRMRjhPWeYYYYwxxxzhMsuuyxGrrvttlv4+OOP42uZNuyqq64KSyyxxCTv+cEHH8QTnOnFZppppvCPf/wjXHHFFVX/D0mSJNWNgQMHVvv5xhtvjO20t956K44ojB49Olx//fXh9ttvj0EB+vXrF9t2BCNrrrlmfI72Hr7//vvw/vvvT/L/4f2Ykvess86KbUQcf/zxMdggmGGl7friiMV0koIKcOIQSDA0tdVWW1VV4nPCDBkypMZ/37x586oGPycL0e3WW28dTyii0WOPPTYGKyBY+fTTT8N7770XTyKClZrw/yeYYUiO1/KeDMlJkiSpfo0ePTr+Oc8881QFBDT8N9lkk6rXLL300mGhhRYKr7zyyhS/LxkuBBQEJbQZ+f/ccsst8X3rM6iAIxbT0T777BOeffbZ+PdHH310kt9feumlMRCozfjx4+OowldffRXTqh588MFag5WEYOWCCy6o8f2WXHLJqr+zGMrqq68e8/UkSZJUfyZOnBiOPvrosM4668QU97Sa+CyzzFKtMxrUV/C7KbXooouGJ554Iuy6667h4IMPjsHFWmutVWPbs645YjEd3XzzzWHYsGFxaOrEE0+s9rvevXvH+goKe2rDycboxMiRI2ME27dv3xisLLjgguHf//53jEanNlhJGK247rrrpui1kiRJmnaHHXZY7MylSLuuEYQcdNBBoWvXruGNN96ItRq0IXfeeedQKk1dwfnUcsSiAXCgu3fvHn788ce4FD0jCswS8NRTT03RKpKcHPvtt188aaiTwE033RSDlWw0moKVp59+erLvx0gIBUAUEO244451sIeSJEmqyeGHHx4efvjh8MILL4QOHTpUPd+2bdvYJhs1alS1UQs6lPndlKJetlWrVuG8886reu7WW2+NHdHU96ZajfrgiMV0wAlCVX9y//33x4CCnLqLLroo3HHHHXF2gPKhryzSn3777beq4TNmCyAdKhuskGZFsIIUrDz22GOTDVbI5SOoaNeuXRzdkCRJUt0rlUoxqGASn2eeeSamLJXXRlADke0QpmZ26NChMZVpStFeTEXb2ZT31IasT45YTAfUPzA97O+//x4P9HzzzRcj1W+++SbOVbzYYouFjTbaqKpIm2gSp556apwNitENirRPOeWUqpOCfLyePXtONlhhBGRywcqff/4ZZ5Di31xzzTV1tpy7JEmSJk1/YsanBx54IM7mmeomGF1ggh7+POCAA+KEPLTN5pxzznDEEUfEoCI7ykA2yi+//BL/PW3LtI7FsssuG7NamNzn4osvDmeccUbYfffdw9ixY8PJJ58cFl544bDyyiuH+tSsVN/JVg1szJgx8UDRuOcA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wOKqq64KnTp1isuD81hrrbXCY489VvX7P/74Ixx22GGhdevWYfbZZw9dunQJI0eObMhNliRJktTYAosOHTqEc845J7z11lvhzTffDJ07dw7bb799+Oijj+LvjznmmPDQQw+Fe+65Jzz//PPh22+/DTvttFNDbrIkSZKkxjbd7Lbbblvt57PPPjuOYrz66qsx6Lj++uvD7bffHgMO9OvXLyyzzDLx92uuuWYDbbUkSZKkRltj8ddff4U777wz/PrrrzElilGMCRMmhE022aTqNUsvvXRYaKGFwiuvvFLr+4wbNy6MGTOm2kOSJElShQcWH3zwQayfaN68eejevXu47777wrLLLhtGjBgRZpllljDXXHNVe32bNm3i72rTp0+f0KpVq6rHggsuOB32QpIkSWraGjywWGqppcK7774bXnvttXDIIYeErl27ho8//nia369Hjx5h9OjRVY9hw4bV6fZKkiRJaoSBBaMSSyyxRFh11VXjaMOKK64YLr300tC2bdswfvz4MGrUqGqvZ1YoflcbRj7SLFPpIU0vzGS2ww47hI4dO8ZzedNNNw2DBw+Ov3vjjTfCOuusE59faaWVwjPPPFPr++y8886hffv2oVmzZpN8ByRJkhqjBg8syk2cODHWSRBozDzzzOHpp5+u+t2nn34ahg4dGmswpMaqW7du8Vx977334ixnBx54YCiVSmHHHXcMvXr1is/ffffdYd999w2///57je9BWiAjeZIkSUXRoLNCkba05ZZbxoLssWPHxhmgnnvuufD444/H+ogDDjggHHvssWGeeeaJIw9HHHFEDCqcEUqNVYsWLcJWW21V9TPn6gUXXBB+/PHH8P3331dNRsCIBvVDrNtS0xTK2UkLJEmSiqBBA4vvvvsu7LPPPmH48OExkGCxPIIK0kdw8cUXhxlmmCEujMcoxuabbx6uvPLKhtxkaaqQ1seoxbzzzhvatWsXRyp23XXXmBbFqMaQIUMaehMlSZKKH1iwTsXf9f5eccUV8SEVTe/evWN9RUrne+CBB8KJJ54Ya4mWW265sO6664aZZmrQr6AkSVKdsVUj1QPSnwYMGBCeeuqp0LJly/gcRdsDBw6seg2LPRJgSJIkVYJGV7wtFd1FF10U7rjjjvDkk09WW4eFlL/k2muvDbPNNlvVqvKSJElFZ2Ah1aGvv/46HHfccXGK2I022ihOK7vGGmvE311zzTWxaHvJJZcMDz30UFwMkulkcfXVV4dTTz216n223nrr0KFDh/h3RjU23PDSBtojSZKkKdOsxDyYFWzMmDGxMJzF8hpyTYtmB/1fA7IudVu/W6gPfffuWy/vqzwur6f3Pbye3leSJDW1trQjFpIkSZJyM7CQJEmSlJuBhSRJkqTcDCwkSZIk5WZgIUmSJCk3AwtJkiRJubnytlTntq2H99y8Ht5TkiSp7jhiIUmSJCk3AwtJkiRJuRlYSJIkScrNwEKSJElSbgYWkiRJknIzsJAkSZKUm4GFJEmSpNwMLCRJkiTlZmAhSZIkKTcDC0mSJEm5GVhIkiRJys3AQpIkSVJuBhaSJEmScjOwkCRJkpSbgYUkSZKk3AwsJEmSJOVmYCFJkiQpNwMLSZIkSbkZWEiSJEnKzcBCkiRJUm4GFpIkSZJyM7CQJEmSlJuBhSRJkqTcDCwkSZIk5WZgIUmSJCk3AwtJkiRJuRlYSJIkScrNwEKSJElSbgYWkiRJknIzsJAkSZKUm4GFJEmSpNwMLCRJkiTlZmAhSZIkKTcDC0mSJEm5GVhIkiRJys3AQpIkSVJuBhaSJEmScjOwkCRJkpSbgYUkSZKk3AwsJEmSJOVmYCFJkiQpNwMLSZIkSbkZWEiSJEnKzcBCkiRJUm4GFpIkSZJyM7CQJEmSlJuBhSRJkqTcDCwkSZIk5WZgIUmSJCk3AwtJkiRJuRlYSJIkScrNwEKSJElSbgYWkiRJknIzsJAkSZKUm4GFJEmSpNwMLCRJkiTlZmAhSZIkKTcDC0mSJEm5GVhIkiRJys3AQpIkSVJuBhaSJEmScjOwkCRJkpSbgYUkSZKk3AwsJEmSJOVmYCFJkiQpNwMLSZIkSbkZWEiSJEkqdmDRp0+fsPrqq4c55pgjzD///GGHHXYIn376abXXbLjhhqFZs2bVHt27d2+wbZYkSZLUyAKL559/Phx22GHh1VdfDU8++WSYMGFC2GyzzcKvv/5a7XUHHXRQGD58eNXjvPPOa7BtliRJkjSpmUIDGjhwYLWfb7zxxjhy8dZbb4X111+/6vmWLVuGtm3bNsAWSpIkSSpcjcXo0aPjn/PMM0+152+77bYw77zzhuWXXz706NEj/Pbbbw20hZIkSZIa3YhF1sSJE8PRRx8d1llnnRhAJHvssUdYeOGFQ/v27cP7778fTjzxxFiHMWDAgBrfZ9y4cfGRjBkzZrpsvyRJktSUNZrAglqLDz/8MAwaNKja8926dav6+worrBDatWsXNt544/DFF1+ExRdfvMaC8F69ek2XbZYkSZLUiFKhDj/88PDwww+HZ599NnTo0GGyr11jjTXin4MHD67x96RKkVKVHsOGDauXbZYkSZLUSEYsSqVSOOKII8J9990XnnvuubDooov+7b95991345+MXNSkefPm8SFJkiSpiQQWpD/dfvvt4YEHHohrWYwYMSI+36pVqzDrrLPGdCd+v9VWW4XWrVvHGotjjjkmzhjVqVOnhtx0SZIkSY0lsLjqqquqFsHL6tevX9h3333DLLPMEp566qlwySWXxLUtFlxwwdClS5fQs2fPBtpiSZIkSY0yFWpyCCRYRE+SJElS49YoirclSZIkFZuBhSRJkqTcDCwkSZIk5WZgIUmSJCk3AwtJkiRJuRlYSJIkScrNwEKSJElSbgYWkiRJknIzsJAkSZKUm4GFJE2DP/74I+ywww6hY8eOYcUVVwybbrppGDx4cPzdfvvtFzp16hRWWmmlsPrqq4enn376b99v3333Dc2aNQujRo2aDlsvSVLdm6ke3lOSmoRu3bqFLbfcMgYEl19+eTjwwAPDc889Fy6++OIw11xzxde88847YeONNw4//PBDmGGGmvtyBgwYEGaeeebpvPWSJNUtRywkaRq0aNEibLXVVjGowJprrhmGDBkS/56CCowePXqy7zNy5MjQu3fvcNFFF9XzFkuSVL8csZCkOnDppZeG7bffvurnk046Kdxzzz3h559/Dv379691tOKggw4K5513Xphjjjmm49ZKklT3HLGQpJwYcaC+ok+fPlXPnXPOOeGLL74Id999dzjhhBPC+PHjJ/l31113XVhooYVC586dp/MWS5JU9wwsJCmHCy64INZIPPbYY6Fly5aT/H6TTTYJY8eODR988MEkv3v22WfDAw88EBZZZJH4AEXf1GVIklQ0pkJJ0jSiLuKOO+4ITz31VFVdxYQJE8JXX30Vllhiifjz66+/Hr777ruw2GKLTfLvb7vttmo/U6/x/vvvV6vRkCSpKAwsJGkafP311+G4446LAcNGG20Un2vevHkchejatWss2p5pppnCbLPNFu69994w99xzx9eceuqpoX379qF79+4NvAeSJNUtAwtJ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8ssvDx999FGYd95548+vvPJKLPI+5ZRT6mdLJUmSJBV/xGKTTTaJ082mguvWrVuHgQMHxqlmmSXqqaeeimtaSJIkSWp6pjiweOONN+LidGussUZ49913wzXXXBOngmW9CVbFZorYm266qX63VpIkSVKxU6FYnO7KK68ML7/8cth3331jTcWLL74YC7d5EFxIkiRJapqmunh77bXXDm+++WaYe+65w8orrxxeeOEFgwpJkiSpiZviEYs///wzpj/997//DSuuuGI4+eST42rc3bt3DzfeeGMs5m7Tpk39bq0kSZKkYo9YHHDAATF4mG222UK/fv3CMcccEzp27BieeeaZsMUWW4S11lorXHXVVfW7tZIkSZKKHVg88MADoX///uGcc84JTz75ZHjkkUeqBR2vvvpqrLmQJEmS1PRMcWBBmtMTTzwRxo8fH0cpmG42a/755w+33357fWyjJEmSpEqpsSANas899wzHHntsaNeuXbj77rvrd8skSZIkVV5gsemmm4aRI0eGH374wYXwJEmSJE37dLPNmjUzqJAkSZI0bYEFsz5RnP13xo4dG84999xwxRVXTMnbSpIkSWpKqVC77LJL6NKlS2jVqlXYdtttw2qrrRbat28fWrRoEX7++efw8ccfh0GDBoVHH300bL311uH888+v/y2XJEmSVKzAgulk99prr3DPPfeEu+66Ky6UN3r06Kr0qGWXXTZsvvnm4Y033gjLLLNMfW+zJEmSpKIWbzdv3jwGFzxAYPH777/HaWdnnnnm+txGSZIkSZUSWJQjLYqHJEmSJE3VrFCSJEmSVBMDC0mSJEm5GVhIkiRJys3AQpIkSVLDBBajRo0K1113XejRo0f46aef4nNvv/12+Oabb/JvkSRJkqTKnxXq/fffD5tsskmcEWrIkCHhoIMOCvPMM08YMGBAGDp0aLj55pvrZ0slSZIkVc6IxbHHHhv23Xff8Pnnn8eVt5OtttoqvPDCC3W9fZIkSZIqMbBgde2DDz54kucXWGCBMGLEiLraLkmSJEmVHFiwAveYMWMmef6zzz4L8803X11tlyRJkqRKDiy22267cMYZZ4QJEybEn5s1axZrK0488cTQpUuX+thGSZIkSZUWWFx44YXhl19+CfPPP3/4/fffwwYbbBCWWGKJMMccc4Szzz67frZSkiRJUmXNCsVsUE8++WQYNGhQnCGKIGOVVVaJM0VJkiRJapqmOrBI1l133fiQJEmSpKkOLC677LIan6fWgulnSYtaf/31w4wzzlgX2ydJkiSpEgOLiy++OHz//ffht99+C3PPPXd87ueffw4tW7YMs88+e/juu+/CYostFp599tmw4IIL1sc2S5IkSSp68Xbv3r3D6quvHhfI+/HHH+ODqWbXWGONcOmll8YZotq2bRuOOeaY+tliSZIkScUfsejZs2fo379/WHzxxaueI/3pggsuiNPN/u9//wvnnXeeU89KkiRJTchUj1gMHz48/Pnnn5M8z3Np5e327duHsWPH1s0WSpIkSaq8wGKjjTYKBx98cHjnnXeqnuPvhxxySOjcuXP8+YMPPgiLLrpo3W6pJEmSpMoJLK6//vowzzzzhFVXXTU0b948PlZbbbX4HL8DRdwspCdJkiSpaZjqGgsKs1kg75NPPolF21hqqaXiIzuqIUmSJKnpmOYF8pZeeun4kCRJkqRpCiy+/vrr8OCDD8apZcePH1/tdxdddFFdbZskSZKkSg0snn766bDddtvFRfBIh1p++eXDkCFDQqlUCqusskr9bKUkSZKkyire7tGjRzj++OPjzE8tWrSIa1oMGzYsbLDBBmGXXXapn62UJEmSVFmBxX//+9+wzz77xL/PNNNM4ffff4+zQJ1xxhnh3HPPrY9tlCRJklRpgcVss81WVVfRrl278MUXX1T97ocffqjbrZMkSZJUmTUWa665Zhg0aFBYZpllwlZbbRWOO+64mBY1YMCA+DtJkiRJTc9UBxbM+vTLL7/Ev/fq1Sv+/a677gpLLrmkM0JJkiRJTdRUBxbMBpVNi7r66qvrepskSZIkVXqNBYHFjz/+OMnzo0aNqhZ0SJIkSWo6pjqwYM2Kv/76a5Lnx40bF7755pu62i5JkiRJlZgKxUrbyeOPPx5atWpV9TOBBgvnLbLIInW/hZIkSZIqJ7DYYYcd4p/NmjULXbt2rfa7mWeeOQYVF154Yd1voSRJkqTKCSwmTpwY/1x00UXDG2+8Eeadd9763C5JkiRJlTwr1Jdfflk/WyJJkiSp6QQWoJ6Cx3fffVc1kpHccMMNdbVtkiRJkio1sGBRvDPOOCOsttpqoV27drHmQpIkSVLTNtWBBQvi3XjjjWHvvfeuny2SJEmSVPnrWIwfPz6svfba9bM1kiRJkppGYHHggQeG22+/vX62RpIkSVLTSIX6448/wjXXXBOeeuqp0KlTp7iGRdZFF11Ul9snSZIkqRIDi/fffz+stNJK8e8ffvhhtd9ZyC1JkiQ1TVMdWDz77LP1syWSJEmSmk6NRTJ48ODw+OOPh99//z3+XCqV6nK7JEmSJFVyYPHjjz+GjTfeOHTs2DFstdVWYfjw4fH5Aw44IBx33HH1sY2SJEmSKi2wOOaYY2LB9tChQ0PLli2rnv/nP/8ZBg4cWNfbJ0mSJKkSayyeeOKJmALVoUOHas8vueSS4auvvqrLbZMkSZJUqSMWv/76a7WRiuSnn34KzZs3r6vtkiRJklTJgcV6660Xbr755mpTzE6cODGcd955YaONNqrr7ZMkSZJUialQBBAUb7/55pth/Pjx4YQTTggfffRRHLF46aWX6mcrJUmSJFXWiMXyyy8fPvvss7DuuuuG7bffPqZG7bTTTuGdd94Jiy++eP1spSRJkqTKGrFAq1atwimnnFL3WyNJkiSpaYxY9OvXL9xzzz2TPM9zN910U11tlyRJkqRKDiz69OkT5p133kmen3/++UPv3r3rarskSZIkVXJgwcJ4iy666CTPL7zwwvF3kiRJkpqeqQ4sGJl4//33J3n+vffeC61bt66r7ZIkSZJUyYHF7rvvHo488sjw7LPPhr/++is+nnnmmXDUUUeF3XbbrX62UpIkSVJlBRZnnnlmWGONNeJaFrPOOmt8bLbZZqFz585TXWPxwgsvhG233Ta0b98+LrR3//33V/v9vvvuG5/PPrbYYoup3WRJkiRJjWm62VKpFEaMGBFuvPHGcNZZZ4V33303BhYrrLBCrLGYWqyBseKKK4b9998/roVREwIJZqJKmjdvPtX/H0mSJEmNLLBYYokl4krbSy65ZHzkseWWW8bH5BBItG3bNtf/R5IkSVIjSoWaYYYZYjDx448/hunlueeeiwXjSy21VDjkkEOm6/9bkiRJUj3VWJxzzjnhX//6V/jwww9DfSMN6uabbw5PP/10OPfcc8Pzzz8fRzgoGK/NuHHjwpgxY6o9JEmSJDWiVCjss88+4bfffou1EbPMMkusscj66aef6mzjsrNMUcfRqVOnsPjii8dRDIrHa1vAr1evXnW2DZIkSZLqIbC45JJLQkNZbLHF4qrfgwcPrjWw6NGjRzj22GOrfmbEYsEFF5yOWylJkiQ1PVMdWHTt2jU0lK+//jrWWLRr126yxd7OHCVJkiQ18hoLfPHFF6Fnz55xsbzvvvsuPvfYY4/F2aKmxi+//BKnrOWBL7/8Mv596NCh8XfUcrz66qthyJAhsc5i++23j7NSbb755tOy2ZIkSZIaS2BBATX1Dq+99loYMGBADADw3nvvhdNOO22q3uvNN98MK6+8cnyAFCb+fuqpp4YZZ5wxvP/++2G77bYLHTt2DAcccEBYddVVw4svvuiIhCRJklT0VKiTTjopLo5HEDDHHHNUPc/K25dffvlUvdeGG24Y18aozeOPPz61mydJkiSpCCMWH3zwQdhxxx0neZ61Jn744Ye62i5JkiRJlRxYzDXXXGH48OGTPP/OO++EBRZYoK62S5IkSVIlBxasLXHiiSeGESNGhGbNmoWJEyeGl156KRx//PFxjQtJkiRJTc9UBxa9e/cOSy+9dFwbgsLtZZddNqy//vph7bXXjjNFSZIkSWp6prp4m9W2r7322jhzE/UWBBfM5LTkkkvWzxZKkiRJqpzAgpSn888/Pzz44INh/PjxceVrppedddZZ63cLJUmSJFVOKtTZZ58dTj755DD77LPHIu1LL700HHbYYfW7dZIkSZIqK7C4+eabw5VXXhnXlrj//vvDQw89FG677bY4kiFJkiSpaZviwGLo0KFhq622qvp5k002ibNCffvtt/W1bZIkSZIqLbD4888/Q4sWLao9N/PMM4cJEybUx3ZJkiRJqsTi7VKpFPbdd9/QvHnzquf++OOP0L179zDbbLNVPTdgwIC630pJkiRJlRFYdO3adZLn9tprr7reHkmSJEmVHFj069evfrdEkiRJUtNZeVuSJEmSyhlYSJIkScrNwEKSJElSbgYWkiRJknIzsJAkSZKUm4GFJEmSpNwMLCRJkiTlZmAhSZIkKTcDC0mSJEm5GVhIkiRJys3AQpIkSVJuBhaSJEmScjOwkCRJkpSbgYUkSZKk3AwsJEmSJOVmYCFJkiQpNwMLSZIkSbkZWEiSJEnKzcBCkiRJUm4GFpIkSZJyM7CQJEmSlJuBhSRJkqTcDCwkSZIk5WZgIUmSJCk3AwtJkiRJuRlYSJIkScrNwEKSJElSbgYWkiRJknIzsJAkSZKUm4GFJEmSpNwMLCRJkiTlZmAhSZIkKTcDC0mSJEm5GVhIkiRJys3AQpIkSVJuBhaSJEmScjOwkCRJkpSbgYUkSZKk3AwsJEmSJOVmYCFJkiQpNwMLSZIkSbkZWEiSJEnKzcBCkiRJUm4GFpIkSZJyM7CQJEmSlJuBhSRJkqTcDCwkSZIk5WZgIUmSJCk3AwtJkiRJuRlYSJIkScrNwEKSJElSbgYWkiRJknIzsJAkSZKUm4GFpNyOPPLIsMgii4RmzZqFd999t+r5zz//PKy99tqhY8eOYfXVVw8fffRRjf/+mWeeCf/4xz/CsssuG5ZbbrlwwgknhIkTJ07HPZAkSXkZWEjKbeeddw6DBg0KCy+8cLXnDz744NCtW7fw2WefhRNPPDHsu+++Nf77ueeeO9x5553h448/Dm+99VZ4+eWXw8033zydtl6SJNUFAwtJua2//vqhQ4cO1Z777rvvwptvvhn22muv+HOXLl3CsGHDwuDBgyf59yuvvHJYbLHF4t9btGgRVlpppTBkyJDptPWSJKkuGFhIqhcEEe3atQszzTRT/Jk0qYUWWigMHTp0sv9uxIgR4d577w3bbLPNdNpSSZJUFwwsJDUaY8aMCdtuu22ssVhttdUaenMkSdJUMLCQVC8WXHDBMHz48PDnn3/Gn0ulUhytYNSiJmPHjg1bbLFF2H777cOxxx47nbdWkiTlZWAhqV7MP//8YZVVVgm33npr/Ll///6xDmOJJZaY5LW//PJLDCp49OzZswG2VpIk5WVgISk3Zn8iaPj666/D5ptvXhU89O3bNz6Ybvacc84J/fr1q/o3Bx54YHjwwQfj3y+99NLw+uuvhwEDBsTCbR5nn312g+2PJEmaev9XVSlJORA81GSppZYKr7zySo2/u+6666r+fsopp8SHJEkqLkcsJEmSJOVmYCGpEAYOHBhniurUqVNYc801w3vvvVfj6ygQZ2YpRktYyfs///nPdN9WSZKaIlOhJDV6P//8c9hzzz3DCy+8EJZbbrnw4osvxp8//PDDaq9j5qkdd9wxnHTSSWGXXXaJz40cObKBtlqSpKbFEQtJjd4XX3wRWrduHYMKrLfeenFk4u233672uqeffjo0b968KqhAmzZtpvv2SpLUFDVoYEHvIykL7du3j6vy3n///ZP0Pp566qlx9d5ZZ501bLLJJuHzzz9vsO2V1DCWXHLJ8OOPP4aXX345/sxsUqx7MWTIkGqv+/jjj8N8880Xdtttt7DyyivH0Yv//e9/DbTVkiQ1LQ0aWPz6669hxRVXDFdccUWNvz/vvPPCZZddFq6++urw2muvhdlmmy1OZfnHH39M922V1HBatWoV7r333tCjR4+w6qqrhieeeCLWT8w0U/VsThbje+aZZ8K///3v8M4778Trxa677tpg2y1JUlPSoDUWW265ZXzUhNGKSy65JC6WxUq8uPnmm2NaAyMb9EhKahxGX1U/79vqkP/394022ig+MG7cuNC2bdsYXGSxqjcjFSllau+99w6HHnpomDBhQph55pnrZyMlSVLjrrH48ssvw4gRI2L6U7bXco011qh1XvzU4BgzZky1h6TiGz58eNXfzzzzzNC5c+dJVvGmo4JF+r755pv486OPPhqWWWYZgwpJkpryrFAEFTUVXvJz+l1N+vTpE3r16lXv2ydp+qLeitmgSHdaa621wvXXX1/1PHVa3bt3j+mSpE5uvfXWcdSTzog777yzoTddkqQmodEGFtOKHOxjjz226mdGLBZccMEG3SZJ+V177bU1Pn/GGWdU+3mzzTaLD0mSNH012lQo8qdrmoOen9PvasJUk3POOWe1hyRJkqQmGlgsuuiiMYBgXvrs6AOzQ5EGIUmSJKnxaNBUqF9++SUMHjy4WsH2u+++G+aZZ544u8vRRx8dzjrrrDiHPYEGU0iSS73DDjs05GZLkiRJakyBxZtvvlk1fSRSbUTXrl3DjTfeGE444YS41kW3bt3CqFGjwrrrrhsGDhwYWrRo0YBbLUmSJKlRBRYbbrhhnLmlNqzGTWFmeXGmJEmSpMal4maFklQ5fn++7t9z1g3q/j0lSVIjLt6WJEmSVBwGFpIkSZJyM7CQJEmSlJuBhSRJkqTcDCwkSZIk5WZgIUmSJCk3AwtJkiRJuRlYSJIkScrNwEKSJElSbgYWkiRJknIzsJAkSZKUm4GFJEmSpNwMLCRJkiTlZmAhSZIkKTcDC0mSJEm5GVhIkiRJys3AQpIkSVJuBhaSJEmScjOwkCRJkpSbgYUkSZKk3AwsJEmSJOVmYCFJkiQpNwMLSZIkSbkZWEiSJEnKzcBCkiRJUm4GFpIkSZJyM7CQJEmSlJuBhSRJkqTcDCwkSZIk5WZgIUmSJCk3AwtJkiRJuRlYSJIkScrNwEKSJElSbgYWkiRJknIzsJAkSZKUm4GFJEmSpNwMLCRJkiTlZmAhSZIkKTcDC0mSJEm5GVhIkiRJys3AQpIkSVJuBhaSJEmScjOwkCRJkpSbgYUkSZKk3AwsJEmSJOVmYCFJkiQpNwMLSZIkSbkZWEiSJEnKzcBCkiRJUm4GFpIkSZJyM7CQJEmSlJuBhSRJkqTcDCwkSZIk5WZgIUmSJCk3AwtJkiRJuRlYSJIkScrNwEKSJElSbgYWkiRJknIzsJAkSZKUm4GFJEmSpNwMLCRJkiTlZmAhSZIkKTcDC0mSJEm5GVhIkiRJys3AQpIkSVJuBhaSJEmScjOwkCRJkpSbgYUkSZKk3AwsJEmSJOVmYCFJkiQpNwMLSZIkSbkZWEiSJEnKzcBCkiRJUm4GFpIkSZJyM7CQJEmSlJuBhSRJkqTcDCwkSZIkVXZgcfrpp4dmzZpVeyy99NINvVmSJEmSyswUGrnlllsuPPXUU1U/zzRTo99kSZIkqclp9K10Aom2bds29GZIkiRJKmoqFD7//PPQvn37sNhii4U999wzDB06tKE3SZI0HfTr1y+mwN5///2T/O7LL78Mq666alhppZXC8ssvH3bZZZfw888/N8h2SpIKEFisscYa4cYbbwwDBw4MV111VbyRrLfeemHs2LG1/ptx48aFMWPGVHtIkoplyJAh4dprrw1rrrlmjb+nw2nQoEHh3XffDR9++GH8mbo8SVLDadSBxZZbbhl7oTp16hQ233zz8Oijj4ZRo0aFu+++u9Z/06dPn9CqVauqx4ILLjhdt1mSlM/EiRPDgQceGP7zn/+E5s2b1/ganp911lnj3//666/w66+/xtENSVLDadSBRbm55pordOzYMQwePLjW1/To0SOMHj266jFs2LDpuo2SpHwuuuiisM4668RUp8kZP358TIWad955Y9psr169pts2SpIKHlj88ssv4Ysvvgjt2rWr9TX0Ys0555zVHpKkhqmF4LrNiDONfzqH/g5pTf379w89e/b829fOMsssMRVq5MiRcSryvn37TvM+SJIqPLA4/vjjw/PPPx9zbV9++eWw4447hhlnnDHsvvvuDb1pkqQpqIWYeeaZw4knnlht2vDJefHFF+N7LrnkkmGRRRYJr776aujWrVuss5tcgLHffvuFW265ZZr3Q5JU4YHF119/HYOIpZZaKuy6666hdevW8SYz33zzNfSmSVKTN6W1EJ07d56i0QoccsghYfjw4TG44EHAcs0118Tns7766qvw22+/VW3HPffcE+vxJEkNp1GvY3HnnXc29CZIknLWQtSVU089Nc7+1L179/D++++HU045pSqwWGWVVcJll102XbZDklTAwEKS1DilWogXXnihXv8/zz33XNXfzzjjjKq/b7vttvEhSWo8DCwkSVMtWwuBESNGxFoI0pjK05YkSU1Do66xkCQ1TlNaCyFJajoMLCRJdV4LcfXVV1f9TFH1WmutFcaMGRM6dOgQ9t577wbdPklS/TAVSpJUb7UQoNBaklT5HLGQJEmSlJsjFpKkBvXBBx/Uy/uusMIK9fK+kqSaOWIhSZIkKTcDC0mSJEm5GVhIkiRJys0aC0nSFHvkkUfq/D0XWmihOn9PSdL054iFJEmSpNwMLCRJkiTlZmAhSZIkKTcDC0mSJEm5GVhIkiRJys3AQpIkSVJuBhaSJEmScjOwkCRJkpSbgYUkSZKk3AwsJEmSJOVmYCFJkiQpNwMLSZIkSbkZWEiSJEnKzcBCkiRJUm4GFpIkSZJyM7CQJEmSlJuBhSRJkqTcDCwkSZIk5WZgIUmSJCk3AwtJkiRJuRlYSJIkScrNwEKSJElSbgYWkiRJknIzsJAkSZKUm4GFJEmSpNwMLCRJkiTlZmAhSZIkKTcDC0mSJEm5GVhIkiRJys3AQpIkSVJuBhaSJEmScjOwkCRJkpSbgYUkSZKk3AwsJEmSJOVmYCFJkiQpNwMLSZI03R155JFhkUUWCc2aNQvvvvtuja955ZVXwkorrRQfyy23XDj44IPDuHHjpvu2SpoyBhaSJGm623nnncOgQYPCwgsvXOtrVlxxxfDGG2/EwOODDz4I3333Xbjyyiun63ZKmnIzTcVrJUmS6sT666//t69p2bJl1d/Hjx8ffv/99zjCIalxcsRCkiQ1WkOGDIkjF/POO29o1apVOPTQQxt6kyTVwsBCkiQ1WtRhvPfee2HEiBGxvmLAgAENvUmSamFgIUmSchda4/rrrw9LLrlkWHzxxcNBBx0UJkyYUGfbMPvss4fddtst3HbbbXX2npLqloGFJEnKXWj95Zdfhn//+9/hxRdfDIMHDw4jR44M11xzTa7/L++TghNqLO67777QqVOnXO8pqf4YWEiSpL8ttO7QocNkX3PvvfeG7bbbLrRt2zaObHTv3j3ccccdtb6eqWN5z6+//jpsvvnmYYkllojPH3jggeHBBx+Mf3/mmWfCyiuvHGss+LNNmzYxeJHUODkrlCRJym3o0KHVRjRIneK52vTt27fG56+77rqqv3fr1i0+JBWDIxaSJEmScjOwkCRJuS200ELhq6++qjZNLM9JajoMLCRJUm5dunSJtRFMC1sqlcLVV18dZ3GS1HQYWEiSpMmakkLrxRZbLPTq1Suss8468ffzzTdf/HeSmg6LtyVJ0mRNSaE1WLuCh6SmycBCkiRNFwff8mW9vG/fvRetl/eVNHVMhZIkSZKUm4GFJEmSpNwMLCRJkiTlZmAhSZIkKTeLtyVJ0iSaHfRanb9nt/Xnr/P3lNR4OGIhSZIkKTcDC0mSJEm5GVhIkiRJys3AQtPN559/HtZee+3QsWPHsPrqq4ePPvqoxtddf/31YckllwyLL754XMF1woQJ0/U9JWly6uu64/Ws8WmK962men43xWNdHwwsNN0cfPDBoVu3buGzzz4LJ554Yth3330nec2XX34Z/v3vf4cXX3wxDB48OIwcOTJcc8010/U9JWly6uu64/Ws8WmK962men43xWNdHwwsNF1899134c033wx77bVX/LlLly5h2LBh8UuUde+994btttsutG3bNjRr1ix079493HHHHdPtPSVpcurruuP1rPFpivetpnp+N8VjXV8MLDRd8GVq165dmGmm/5vhmC/PQgstFIYOHVrtdfy88MILV/28yCKLTPKa+nxPSZqc+rrueD1rfJrifaupnt9N8VjXFwMLSZIkSbkZWGi6WHDBBcPw4cPDn3/+GX8ulUoxIid6z+Lnr776qurnIUOGTPKa+nxPSZqc+rrueD1rfJrifaupnt9N8VjXFwMLTRfzzz9/WGWVVcKtt94af+7fv3/o0KFDWGKJJaq9jhzEBx98MIwYMSJ+Ca+++uqw2267Tbf3lKTJqa/rjtezxqcp3rea6vndFI91fTGw0HTTt2/f+GDatXPOOSf069cvPn/ggQfGLxUWW2yx0KtXr7DOOuvEL998880XZ1WYnu8pSZNTX9cdr2eNT1O8bzXV87spHuv60KxEeFTBxowZE1q1ahVGjx4d5pxzzgbbjmYHNavz9+y2frdQH/ru3bde3rfp2LYe3nPzUD8Or5N3GX1VqBezLFv37znrBnX3XhOa1f33eoZu9fO9nrFv3XyvH3nkkVDX6mvYf4UVVqiX920qmh30Wp2/Z7f15w/1oe/ei9bL+0oKU9WWdsRCkiRJUm6FCCyuuOKKOP1WixYtwhprrBFef/31ht4kSZIkSUUKLO66665w7LHHhtNOOy28/fbbYcUVVwybb755XHhEkiRJUuPQ6AOLiy66KBx00EFhv/32C8suu2yslm/ZsmW44YYbGnrTJEmSJBUhsBg/fnx46623wiabbFL13AwzzBB/fuWVVxp02yRJkiT9P/+3zngj9cMPP4S//vortGnTptrz/PzJJ5/U+G/GjRsXHwkV7KmivUGNr4e3/L0e3rQxfFaFN6Ee3vP3UD/q5liPqafNm+XXun/PCWMa95GeYXz9fK9nrKPv9W+//Rbq2i+//BLqg9eynMbX/Rdw/O9jQ33wWEv1J32/pmQi2UY93ey3334bFlhggfDyyy+HtdZaq+r5E044ITz//PPhtdcmnQrv9NNPj/MBS5IkSaobw4YNi4v8FXbEYt555w0zzjhjGDlyZLXn+blt27Y1/psePXrEYu9k4sSJ4aeffgqtW7cOzephzvmGjB5ZLp6D3JDrc0xvTXG/m+I+N9X9dp+bxj431f1uivvcVPe7Ke5zJe93qVQKY8eODe3bt//b1zbqwGKWWWYJq666anj66afDDjvsUBUo8PPhh9e8sFfz5s3jI2uuueYKlYoTt5JO3inVFPe7Ke5zU91v97npaIr73RT3uanud1Pc50rdbxbImxKNOrAAow9du3YNq622WvjHP/4RLrnkkvDrr7/GWaIkSZIkNQ6NPrD45z//Gb7//vtw6qmnhhEjRoSVVlopDBw4cJKCbkmSJEkNp9EHFiDtqbbUp6aKdC8WDSxP+6p0TXG/m+I+N9X9dp+bjqa4301xn5vqfjfFfW7K+12YWaEkSZIkFUOjXiBPkiRJUjEYWEiSJEnKzcBCkiRJUm4GFo1UUyp9+eWXXxp6EyRJmmIsgCZpUgYWjTSgaCoXrVtuuSXsvffe4ZtvvglNSZ8+fcKJJ54YF3xsSj7++OOG3gRJyuX+++8PCy+8cHjuuecaelOkRsfAopFp1qxZuOeee8IiiywSPvnkk1DpRo4cGdcn6dmzZ5MKLlgN/vzzzw+9e/duMsHFMcccE/bdd9/wwgsvNPSmqJ41lXO6pk6hv/76K/zxxx+hqe33Rx99FN55553QFGyzzTahS5cucZ2t559/vqE3R9NZU8oomRYGFo0MiwG+8sor4bLLLgtLL710qHTHH398bGwOHTo0nHTSSWH48OGhKVyUDjnkkNCvX7843/XZZ58dxo8fHyrdgQceGMaNGxfOPffcJnMzrq2BXck3JvZthhn+79by8MMPh1tvvTVe0yr5HGef6RR69NFHQ9euXcNqq60WO0seeuihUMnSfg8YMCDssMMOcf+//fbbUOnf6Zlmmil2AG666aZh5513DoMGDQpN7XpWydewrLSfdICOHj06jB07Np7zTbHzZEoZWDQib7/9dthqq63Ciy++GNZdd92K/+JOmDAh/rnZZpuFTp06hZdeeinejPkCV6rsMd1uu+3CmWeeGYOLyy+/PPZ0VioCiuWWWy7cd999Mc3vkksuqfg0Am48qYH92GOPhQcffLCqocmNqZIbmjjuuONiMEnnQffu3eOfv/32W6hE7DPHd5dddomjzccee2wcmTvhhBPCu+++GypVCqb22muvOCJ55JFHhvbt24em4NVXXw077bRT+PHHH2PnGPftpnI9u+CCC8LJJ5/cJEbmOMdJfdtggw3CeuutF3bcccfw6aefxs/C4KJmBhaNCL32LVu2jHno6QZdyY3NmWeeOdx5551h++23D19//XXc9/79+8eRi0pNi+KY8mA/V1999fDZZ5+Ftm3bxkZXpaZFsU9pFVJuwttuu20YOHBg3F+CyUrvtafBRcOLRtf+++8fb06VWGuSDSree++98P7778eAiob1HnvsEd54441w2GGHVWRw8cMPP8TGFuf0WWedFff3v//9b+woWmmllUIl4ngz8caVV14ZA6hDDz00Hn+uaRdddFHo27dvqER8r2lobrLJJvHc5jvdunXrGGRUcppnup5xrOkYmm+++eL1vNI7AT///PMYONI5ss8++8R2yhprrBE+/PBDg4vasPK2Go+BAweWVl555dIKK6xQ+vzzz+Nzf/31V6kSffrpp6U2bdqUrr766tJvv/0Wnzv77LNLa665Zqlr166l4cOHlyrRRx99VJpzzjmr9vvbb78tXXzxxaUZZpihdMYZZ5QmTJhQqkQnnHBCqV27dqVevXqVjjjiiNLcc89d2mijjUovvPBCqZJMnDix6u8ffvhhaZVVVim99dZbpa+++qr0ySeflDp16hQf33zzzSSvrwR33HFHaeutty7ts88+VdeucePGlS699NLSGmusUdpvv/1Kv/76a6mSjB07trTqqqvGa/b//ve/0gILLFA66KCDqn7/5JNPxucr0bbbbhuP9dChQ0uHHXZYacMNNyx17Nix1LJly/g9rzSjR4+O3+kePXpUPff999+Xdtppp9K8885bcdezrFtuuaU033zzld5+++2q58aPHx+/z5V433rxxRdLd999d+n000+veu6LL74o7bDDDqU55pij9MEHH1R0G21aGVg0kNSYeO+990pPPfVU6bbbbqtqXD/99NOlzp07l9Zbb73S4MGDK/bEffXVV0vzzz9/6d133632udC4nn322eONediwYaVK89JLL5WWWGKJeCPOuuCCC0rNmjUrXXLJJbEhVkk4z9u2bVt64oknqp7773//W1p00UVL66+/fryAV5rrr7++tOWWW5Z23XXXeNNN33m+5xz/nXfeuVRpOG9pXC644IKxoV3+O4KLtddeu7T99tuX/vjjj1JRlQeDXKeWXXbZ0o033hiP7YEHHlj6888/qxoiu+++e+nxxx8vVRo+h/PPP7+02mqrxY4RGte33nprPMdpjG222Wax4VlJfv7559KSSy5Zuummm6rdm0eOHFlaaaWVSssss0zpmWeeKVUijulee+0V/06j+rLLLov7S0fof/7zn4q6b40aNaq08cYbx3vyvvvuW+13dBIQXMwzzzzV2i/6PwYWDXhT6t+/f2xsbbDBBrHnnkCCAAMPPvhgadNNN429P/TsV+L+c2GiZ+uhhx6KP6cbMZZaaqn42Rx88MEV1xPy+uuvx4vVK6+8En/ONkC4UPG7c889t1RJ6KmnsTlo0KD4c2ps0KM/66yzlnbcccfSY489Viqy1MDgz59++ql05JFHltq3b19aa621ql7z+++/xz/5ntMALXrgXFOHBzfkU089tbTQQgvFUars95eGB6OSdBoUtbMkXb/oEDrppJOqGlOnnXZa/O5ut9121V5/8sknx4ZXeUdCUff7tddeK11xxRWlCy+8sKp3nmtXeeC0//77l/bcc8+Ku35jk002iZ0G2c+Gx2677RbPgcUWW6yqo7DoxzsbRHPM2b+ePXvGQLpLly4xsCSQ5vrOyE0l4fxm9JWRqK+//rra77788svYAcx+cw2otJHnPAwsGggXZ05WejVB1Jt6q5NHH3009gRxAaMhVuQTt7ZtX3fddeM+8iVNaJTR88WNuvzLXNT9Lm9E0ZAmaHz//fer9YQdcMABpSuvvLL08ccflyrpWNOo4ny/6KKLqoIpHjS0SQuaccYZYyO0EqSGJmkxpEs0b948jsJlDRgwoLT44otXpUMVUfacZl85xqR7YcyYMXHf//GPf8Q/s50G2dGbogYX9957b2muueYqde/ePV7LQUojaV6zzDJL7MmlEXbooYfGlIlK6dVkv0lhZMSJji9GHI8//vhqr+FaznO8LqWKFFU6T7k280juueeemLL8r3/9q9rrDz/88DgqW/Q03uz38rvvvouPhPsynSWMUKROT+5Xq6++eqHT/dKxZiSVzpHsaDujrNmOoPTaIUOGFL5zqD4YWDSQ6667rrTFFlvEv/PlpIeDqD9JFzFqLtLNuqjSl5ALLvt47LHHlu6///6qIIIGFmkT5GaTJnTiiSfGn7MXsyLvN8Pi9Gyecsoppc8++6yqt5M0gXXWWSemvtFzz2uWXnrpmMNbCTckGlo0slPKCw2tmWaaqXTnnXdWvYbAgnOCzyPb+CyqG264odSqVauqGxM3Ws7nhRdeOB5/zmka4ZtvvnkMLIvasM4Gj+wX6RD03HXo0CE2OFLdAec0dRW8pvz4FqGjpKYAiMZyqg0rRyODhhefB0EVaXBFblxnjxmNR2pH6PjAO++8E1NWjz766Gq1JNTH0ZvN7yvBfffdFzvAuE/RU881nOC4d+/epRVXXDF+j+kwoc6E735KXy6q7PeS0UW+vxxP7skpZTWbxkinJ20ZHkX4TtckbTfZE4w4cqy5L91+++3xeWrkqAckBa7onZ3Tg4HFdFL+haOANeXtcTPu1q1b1c2LFCkuVEX9ktaE0Rd6bin0ozFNbx/51qAhzdAyN2NSRwiy3nzzzVIlIL2H3nguVuwzvVwEUHj22WdL//znP+NIFb0hFDZni+KKnovLTZebEQ0t8o9BUMn+kuL273//O96UeV0694seXHDekmdNil8KEGloEFxwHrRu3To2vMjPTakSRQ0ucM4558R94vv98MMPl/r06ROPLwFF6iBhxILvdE0N8caOkaVyDzzwQGxsETyma3R5uk8631PqW9FQK1JeA8MxZr/TqASpbozYZAMPPgc6wyqlF5e0Vc5v0tkIKgisqI1iBIprFef8NttsE3vraXhWysgUSGekBpKOII43wQUpyimlj+sXGRekA3HNS+mtRb2eEVQw4QBtM851AiXaZmlEkppQ2imcD3SaqXYGFtO5kclQMp5//vnY28OJnO3xwSGHHBJzNenxqwQjRowo9evXr3TVVVfFn0n/OOussyZJ/aIBRs99uikXVWpssB8EjNdcc038mQsvKVCkflHgmC7ADLWSElXk4fNsEMzMIaQ90TghNYTePm7G6biy79QTURjH80W9IdW2vTQuOMY0plNwwY2ZxjY359ToLlrDM5uuCEajGHmh5zaLwJnvNrOppFFJvvtFCxoZPWWkiR7K7LHmWkbjoqZZvRh9zBawFrFziNovJlQoP97sG2m5XK8YneLalo4pjS9qiop8DSvHaON5550Xe+2zOfc0oknVfeONN6qe/+WXXwo9GUFN92zSnVJmAQ1tRmPSPTx1GtABynmQAusi1tPwHaWTgAwCjnc6ntR4HnXUUZN8N+gcLfqoVH0zsJiO6K1dZJFFYgOLLyA9eQypp9kliILpGeGmVeQc+yxm/iGAYmgxXaTSRSkFF+QjVxouQPRg0cOXCpZBsMhNiYYnDe8iNSynBOlu9M6nIeSUHkQgwX6nxhgX7qwi3pCygVR5kJGCC0aiqDcAKRR85+n1S7UmRcHNlGLcLG7G5NiniQZS3QwYleHflBewFim4ICj84Ycf4t+z12NSGwk4+vbtW3VsUwDBCCTXtSJj6tBUhEs6U2owkw5CDzYjz4w4ZhFUbLXVVjGILDqOJQESo+fUx5TXkNApSF0YnX+kcFaC8usX9232n/sTRfncw1NQwT2M6dG5Zmf/XZG+2+Xo3KKOgvOdugn2PTtd9COPPFKVxlxp9+z6YGAxHdHApLGRZkHiJKbYa+aZZ465e8yNTQO8UtJhUq8Pc5kzMpNyc9NNmIZJSp249tprS5WE4JFjzb4xg0r5jZvca455mgWsUs5vZr9hnnPykrPo5aUXlFlEymuGitirmz2/uQlxU8reZPk7+cisV8J5kGou2HfqDWigFSmgpqGZeuJTYxtMLcsoTFpzJzUu+M6Xz45UVKR+UIhMz2xCGivH8PLLL4+9l4xqMBJFRxEzoBURNVDZzh/OVe5JzIqTGlN8j7mmnXnmmbF2hMZWpRRql+MaxnebkVVG0rMYuWDUhvOg6LM/lQdNCfvN1LIEFdn7M+c7a00xilHka3i2foqOTtKU6RQony6a7zb36zQCq79nYFFPavuicbPlS5nQ40UeJzcoouJKyU3N4kJEA4SeLmbTyKKHixsai8ZVGhpg1JMwakEaXPacILig2K/Is2iUoweLQJHeXHqrszNrgBEa6miyC0tVwj5zbEmPIHDKBhd8t0knoCHGaE3CMSePtyjD6dnUHlIXCR5TI5KGCA0QUvzSuUwPN7nI5b3aRcV5TBBIDRQdQdmUVYIqpkvm+FNzUNROIRpWNJ5oRFKAna5RdIpwDpOymIIL1tsh1ZHAip775ZdfvrD7PSU1NtRVUEtSnkVAqhzT7FYKUrvIlmDUmesYNXB0EjFlcEIQxcgUKZBFHKHIzkiXRhvTfpCyTB0cmQZZaXIKRjI0ZQws6rkH96677qo2tzMXJ1IhaGQVMa98ctIXlgYTebjZHFQuwPRi0oNbHlwUsbejpu0nzYcZvkihSI0xclUJLKgzoIen6Pua1HbecuEmNYYZcQgmy2e4Ingu4g2pJtlVpbkZM6MXwUVCuhc9fjRAyj+vIqZ+0dDkfKaxwc03jVJwjaOAk8kJCDIoxl9uueWqamcq4ZznPKb4nAY153XCdY4CXtKjijx1MBh9YLprjiPf03TMaXAx6rbLLrtUBRd0BHF/I6Ao+toF6fykg4+0Rjr5GK1J31nOb4p4CS5IEapUdAxQhJ7qDDifSe3j+0xHEfUG3MfoWChaXRzpXNl7Ed9ZpksmQKJjM53DaXIR0nkJrEiHos1SKTOcTS8GFvWIIWR6c2hwMJNISgGh92fvvfeumJtudj8YPqYXj15r/iTXujy4oFeEAt5K2296NaihYSiVi1Xq4UjBBY0xzoOiH/PszYS0PuoFmDkkrcnBTYchZUbmagouULTgovwGys/pOKYiV3p6aVBz/Nl/RquoLSnqjFcEwmkGMyaYSIWM5J/Te08jI/XY8icNb27InPtFK+YkzYGG5ZQGF9mRi6LLntvMakYtDcEFs9aVBxfZkYtKW6yWxUkJkCnaJUCmNix9ZwkuqCei974SFqytLSAgqJptttmqMgio+yQNipmvaLPQe1+07zYdO3TmMsLI8WS0lewJrlXsFyNyBFApxZPvOB1jzFjI5CPlaXD6ewYW9YweLW5CDKdyojI9Gw0Q5vOnl6uSLs6khKQiL1K6GJUh+udLm+0V4ctK2gBDkUVrZKftzTYSaYDRq0GKACkFNMLIzaX3IzW8qLng4sasKuWFy0WSPV4saEeeMQEEjWh661MxI8EFs6nw/B577FHofc7i5pNW2U2pEhx7bsScE4xI0vgiiKSHt2g9ewnnMd9Tar5YDI10H65lCQ2OFFzU1tAqSiBFLzSNZlI8/q5nMgUX7Du9+5UgncsPPvhgTGGjF5frNsEFU8dmgwsaYUzDmU2PK6LsuUk6H7UxrC0Fvsvcn+m9z85mdvPNN8eOg0qa+ao8vYfrG7MjMdVsunYV+bsN9oMFSqmDY5IB7tNpVAYc9zRzYTq2qTNscp+BamdgUccXZ3ptGXZjWtlsTy0XL1JEmGWCRgcXbobZihL1l2MYPLtQDAt/MUvG+eefX9XwoPeeIVRGKLI55vTw0otfRGmBoHTM2W9utGkmGAIIerYoeuTPY445pqpHm9eWT+FYVOTaExy+/PLL8WfObVYcZpSKYeZ0UaagNbtGS9HQCZBmcGIVZRqTqVHF6BOTEjA7ULnsVNFF/Y7TCcDx5FqVbsSc82n/+Y4TQNPLW/T5++mRplHN9erv1tDhus75T9BV1OtYTbPY0ZimIU0qK6lQXLPLgwtqTTjeRV0kjNmM6MEG1ySuUVy70pTvdAQxTTQjE3QCcQ2nxz59h1NefiXgGPPd5rqWTU9m3SEmFknf86Jev7IBEMeZCQfo3OX4pkU80zWNDl+CC+qMsud20To+GwsDizrEl5NGNDmJfGGJkMtnfuFmzHAiN7GiFiwTVNCDSQFqivC5SHNTovePBjR5mBRv8oVmES0+Dy7URcYCOewHvTnZBiRpQNyQ2G/S3tLsMfxJPjoBZJGL/Njf7IJA9GYTRKbpB0mHoteeEQyCLD6DNHLBhb2m1YuL1GtPzyX5uHQKpGFx0kH4DFIvZ203oiLemNI2MxsSoy4s5kdPbXYK4ZQOw/efgkcaJ0WUbTSRX09gwePv0h9oYHJ+VAq+y4wuZnF/Sgt7ptmCKN4t6n7TG8/1iRmsUtob1yfuWYw0MqrKZ5CmVSZ1mX0nuE5rERXx+5ykbc/uA+le1IGRBsb3nFoxvtukAmXX2ymq7L6mtgjZI4zKlc/mxYxntFuYVKVIIzKNkYFFHaGIjaCChsaPP/4YC5/ISSQ9JE2zmhpW3MyKnqdKUMGIBD31KcJP+8dnQM9AaoySEsUFm8ZJ+VSjRUKBFz23HGf2P0m5mfR8ceNKc7kz5MpnxEWsqD2bHMMWLVrEXsrswoU0OgiWyFdlH1MAzbk+wwwzxM+IKRmTIt2Q6bFL5yn7zDSEqaAvq1LSu5LaAj8aXUy/SMCYai6Qbr7MmlTUG3E6L2lQUQ/ELEcca3Kviz4KMzXosaXBXV6ATu0BnwcPPqOiI2AkNZMZrdKKyqlnng4zaiJTUMnIFR2A3MeLfN8q/27TAcYjYSSK9gudJ4y0M8MZf6djtMizVKbvNvchpnXnOKfJRdhP6j3LR6Co/XT2p/wMLOoIvV00nLN1AzTKdt9999IGG2xQtchQkRpYf3eBYmiR2TIILrI3JGoL6OVJaJDR6130YCoFEQQMrEJ6+umnV/sdPfYc6xRo/Otf/4pBVtFnTWG2GIaPSeErzy+m2I9CR25OadSOni9SRYrY2CRNgu8x+0RjghsRPXqsv0FwTCpFUuQUgcl9rxmZY8SJPxMWR2Pkjc8mTbzA5BTMnJIU8XinFaXTQp3sNyuJE0wyctFUggsaluwz+569XlFXw3E+7rjjCrs+R/n5TaoX0yNngwuQwsx1jhRHXk8HA6mP2bTGIsq2OegQ4ziTxrfqqqvGVM+Uss01nM+DTAO+D9TOFW2UuXyfSUln1Ik2SZrFLju5CPWvRT++jZGBRR0hImY2mNQznRodXMT4knLzqhTZBhVFUeXBBY0z0kYYtSBPNxW3VsrFmVQAakkILrIjFwQcBFTk51KwTv59JcwgkoILZvoiuMiOvlx66aVxaJnePRqWpE7Q2KypyL0o6KVlhIbgIjWyGJWjYc3NiKApK5smVvRzmzVGGJlgZhwKdbMFygQX9OozQQPnOXnYRS5uTPtN44JgOIvgid5rRi6Kfu2qaZ/plSe9iTTG1Hik84fjyjWd+hpSRU4++eQYWNQ0s1tjl/aLEbU0ukjgSAcX92Wu0dnggvsXefac18zwR3pQJa3Pwb2KkWRSfqgpYlIGJiEgHao8LYhOhXTtLmpwQbob+0vGRPl1KgUXdBaxyKHBRd0ysMhxceZGm246NLwoXqWXI4tiXW5QfzeVYWOXzZUvxz6n4CL1aFPASyOT6WbTNKRFlfabdTm4CaWVOtPIRfaY0zBjdglmmCnyftd0rDnHKdjOBhd8HqR6MQUnDVIaJinwLNLoHCkP3GwTRl5IYyTASGkQNEaom+FmREoc+0nwQYF+JaC3mtlxmKCAhhgjbnSKMFqTkCZASgwjVUWbdrI2jDTSoCxvXPG9ZlpKzoNKGLlI30fObRrUfF9nnnnmOBU2M0KlfWaGLNIfSRchiCzyvhMskNLD7G0Ei5zPaXIJ7t0U6/JZpEkoOL+ZjIHRK653RZatbSP1iRGK7AraYG0O9j+1Y8ob4EXpGKop+Ce9jwwCgoaagiSuWz179ozX/qKmKjdWBhY55r0m2meIOOWe33TTTfFCzclKI4QvM4XaNMaKunhS+crQzz33XExtolcrW8yZggvSo7L5m0WfljA7rSiF2Eyhmo4lvdkpuChPCUmpb0WUvfgyPJ7dF262TDHLaFTqzSdo5txn9CI1MotyQwKpa8wSUn6usrYB+0kglYIL6kqYspDZYhjBodivqOd49jgzskYQxZTR2amjCaS4zmWnjM4q0nGuDXVBzG5Fjn0WDXDyzcmxL3KueRadI/TE02vNPtERRCcII3FpUTxSnjj3qacpv/4XEWlP1IExyUB5wzoFF1zbmRmrUmS/24zQ8D3luk1qUHouIZAs8tTJTJ5CcFReL0H6E6NPNX0m1AbymRBIpdRl1R0Di2nA+hOkuTCEmC1opRFKrwg3ZIKJjh07xjQRRjaKiHm76a1jnQbwZ5rdiQYV+8hFOxtccAGn177o6SFZ5N6yaBA3pfKUABreqaD7+OOPLxVddpSB4JHRCNICCBhTw4tGKDepbD1JpTQ2KexjgbfJBRc0xujhJP0x7WuRe+1TGgDnN50CjFhw3UrT6DJLDt97Ao9KSQMi1SM7ikyxKtczOk5InQEdKHynmYyjUpAWwqyFHPPU0GL0lbULymeFKrr03STli2wCgkca1uWTLhBcUNBN4FHUe3Vt13C+u4zGgZGb7MyMqUOE2e3STIZFlQqus52a1I/wnabTK3tOcM8mkEpBluqegcU0Dp2nlbPTxTkbDZP+RCOc/FWmbCwqLsjkWVPESI89aU2kQICbL8Pn5GJnUyWYoo4Cz0rpBeC4cnEmvx5clOjt4BygAcpUhVzIaYTTg00vfpFSgLKy5zDBEj2bTM/HcDk3Jc6FFGSmgm7S/Irc8MoGQTS2WF2aNJA0lW42uKBhXdP3uWiBFHnmpAmAmglmR8miQc05n3o1SZEirZFpGIuab50dhSBtj9FVOkFI90oIogmomBmKoJk0KL7rlSBdkxiZoxc3BcLpGDMSxzoWBFaVhkCS9D0a0KRq0tAsDy4o7GWShkqpiUvXaDpEaGCDazfpb8zwlkVAyf2saGiTZKdxJ/WYa/d9990Xf2ZEjusW3+t0vSPwoAOUUdhUzK26Z2Axlbix8mVl+DTJNiSLunBQubRP9OwxasF89gyZZoeLGUbkS0xayP3331/1fKUEFeAGTODETYl956JM7yaF+jS2+Vzo+SGgKHIDu/yGRA9WyrtOU/ZRlE4Dm2AqTUPKZ1P0xiZSfj3fX9LamHwgTROdGqTUUzBSl+0VKxo6BDiXyaunKJeRuPLGM4XM6623XtV3nGOcOhRQtOOdrmWMNjIjDg1Lrms0shl5PuSQQ6pey+8IpDgHijwLUm2dG3x36b2nIySL7/JSSy1V6HqK8n0nZZXvc3b6UK7XjMCSWZBmsmOkjgCraOf15JBNQTuF725KZaXjhPU46BDiOsYoDSlwfB5FGnHl+DJqnOq/sp09BIekJqd7F9c27luMXBBMUGdCZ2glFeU3RgYW04BpRvlCZguGONk5wblJFb3oC9mLLCMXDKfyRc42MEAqGBcq8usrtTCfoIkcXNKdCCjpwQa9+fRsVtINiQsyx5l9ZcQti5nNCCJTLnaRe+2zuNmyX6lmhAYJtVHlwQWNTmYQKvrx5jrFqCLHOdvATI0Lgig+D65xLA7Ia4tYkF8+SsPoDFNppt5qgkmOKb2cjMpVghQgp+NFoMDx5Bqe6iUIqBiNYRYo0qA47/k7IzhFT2FN5yfXbBZ5o4eelOTsyBTXcBrWfMfJw+d7kDpLiiqbOUGtAenIHE8C6SwCKHr26Tjiwehk0eri0jEmlZFrNPVf2eCR7AIW8GXaYFCYzfeA+zXfBTJKVL8MLKYBhY3MA03hdurto2ePITaeL3L6UxZzmKeCKL7EBBcMm5Y3OHmOL23RZQu1KQYjgEw1NAybpl6OdBHn+NPrW2kLpZEOxM2WSQjKp+EjP7sSakmy6Jmmt5ZGdHlwwVTJ2bSopCg34ZrOcW6s9NwylSojE+Wrh9PYJP+YRjjneNEaHuW4Nvfp0yc2NgiSslJwQQOFVM8iI92DGcrSDDd0gLBfaaIB7k3PPvts/B3nNKM1PE+PNb25lVBfgIEDB8ZjTacAqU0EUlzPsvctzm1GIJn5qhJGaZJUA8hIDSNvHP8pmbWuSCMW2WsR05xzrAkWy4MLzu/sqLumHwOLHBdxcnHpEWC6MoqiWIilUobYKFSlocXUqSm4oHiXhgg9QdQXEGBRU0GPX6XkprJPqVC7tpQubsD0CNHoJPgqqsn1vJPyxXGl0ZWCC25aNMyyxc1F3+cUTDKLG/UiNDSywQUpMTRKCDYr7TjTg03qALUz5cFFWj2+qA2P8tEVjiXnLQW6TItd3ovLqBUpEjTKizoqc/TRR8d7Eucs9yFGUynAJ0WTyQb4TlNHkYILjj8zP9GzW/SVpbMYVeT6DBqbjKgTSCB7bLm+F3F9jtq+24zSUBeX0rEZfeJcJ3BMnweKOovdtAQXpEUxg6emLwOLWmQvQLX9nUI3ekU4oUkpKHJObjkuPiwCxygFRZvZ4IIRihlmmCEGGKQQFHm9hvLGE/vKdKKpN5MhcnruCSQZnaKBwgwq9NwXuacre0Niuj4WT7rooouqphsFCwfREGORQ0bjKIQjsCjyomjZfS7/TjMqxf5RS5SCC0YfaZwVsWFdfpw5h0l9IHWA1JjUuGQiCjoMrr766vgcHSUsjFZU6XiWT/lMXjYjF/Ti0ptbHlyk2aCKjKCC6zJBBp1d2VW0qQ2iKJ9zvFJG1ctxzPn+krLLPYtifFJ+0jnBSA0jGpUg+91mdIrvLJ0gTJGcpkcmyGBGP4rWGYEtspo6SP4uuKCejHOg0rIKGjsDizLpAsQFmd6M8p677GsqSU37RHBB7QSFnjQ+UnDBXOjkqNIjUNPnU1TsL8XJ7CtBIr1czAREKgE3Y3K08c4771RMkT5pTcySw1z2zBZDShCpUAn7zM2KaYWvuOKKqueL1tDm2KZiTW66rDdDgFh+/nNsGXncYostJlk0qWj7nEWOeWpkETByTGlkp8JderMpcCRdhh7OogaP6TgyE87uu+8eg+L0vU3BBWmbjDYytXClyKapMYpMilO29zp9LtSaFHkK9NrQuZX2lbWGOPakd9HxlRqkBI+c+3SiFPm7XI50RUZl2G/2j4lFuJanUSg+F35H3VzqPCgSRhrT1NBTGlxkR+CKXjdURAYWGeniS14e6QGkOfGFZTEh8o4rHTOlMO1c9iZFg4xVSOmhZ+7nFPkzcpHtGagUzHJFKtTcc88dZ5xIiwDSY0+vblHzzGtCETbpHy+99FL8mXoSAknOeRonCQ0zGtvZXv4ioV6ABibf55QGwyxXTDmandcdpI3Q40vDu+g599njzLojaYSNGzD7lz2eND5odJICWPS1OfgOMyrBNLo0IumtJS0odYwQXDCdMp/BxRdfXKoU2UZXWkWdhnW2E4QRV4IO1uapFDQc6QBihD193ylcZuSCFMd0H6NHn+C5kqYZ5TvNdSx7PJlkg3sVRevp2DNCxRomRbt/0d5gFkbuyXT6TElwQacB1/VKHZUrAgOLMsz1TNTLDYeePHp0uQGxaFSlj9DQq5lmyyi/ANGjycJ/FH2Wr3BZ5P0mFYRpZBmhSPm2HPfU2E4XMVILaJymXu8iKr8g04gsT20i75iidabSzV6YOf7kq3JzKtKq4vTQcaOhgJFjSApfWn2X7zS9msxzntCrSboItTNFuwnXhoX8tt9++/h3AuXsbFec86nxlVXUfWfNAkZc0v7Rc0kPPbUF1B+kdCca2JdccklFpa+Wf8dJiyIthg4h5vunaJ9ce2a4K/KIa02j64wus6+p44tjSwcJDWw6iJhCmZHZSqmBTOjgo72STUfmu0vnKPdrOgRTWlT6Thftu03gSK0n95/yCVSy0n5xP+e6XuRzvOgMLDI4WSlmzBZ+MaSYFker1FQoGh4MHdOgpleH1Cd6rLMNzlSsTkpM0b+w2dmfSP2hx4feLeoraHBk0cDkM6FxWim1JDS6KODk5sOweXkBOhdmaiso+MwiN59GWlECSwIIUp7Sgkkp55ZRGQJpbkSMXNCzxw2YKTdZs4XRynTjKtpNuKYbLo0svtPUz3Ael0+hS9BYCfUFeOaZZ2IACQJjUru4fnMu07Bkbv80+ly0Y1vbdax85rbsOcA5TSBBWhTpfQTRlZIGRRCZerFBQJldrJViZlKA6BBiBKfoE4zU1O5glJkJJ0jvy96v6QDjO8/IDQFXttamKLLnMZ0fdI6wenqaiXNywUWROr8qkYFFBicjX8KHH3449nxwEmcLv8gxr6l3r4jKF42icDfdpAismMM+mxZF45oC9UqpqWDomB4Q0rwo0iaPk55c8u5T4ESDm0CKUZwiF2pnG1BMvUhDg5sygRL1I/TmZ4NFznGCSGppylNiipKvSuDESCOpMFkEEBxPjjVBBAEzo1ZMG0zRMsc73aCLvF4F53fqqaSBzQxvfB7Z9WY477fddts4QlNJnSWc22B0lQ4TjiPXdnqv+QwIHCtlf+kc2W+//Sa5LmfPXWpJCCwIMipl8VKCBI4lwURaW4nAmYlFSF2uNNnjScdO6gjgWkXgzP2aGb6yKZ308jPCTKcZ130U6bxP28qsZUwNTFDMMef+Nbm0qOy/VcMwsChz6KGHxl4Pemb5e2pkcBNmOJWegSI3OLKYHYP8eQq+sjccLlwMo7NKJcPJ7DdzQldK2gD7R0OS3qw0Wwo56ORyss8EF2n9CorGij5CUz5NLiNUyV133RUb2dyceJ5ggv2nziB7nqfgpCgXbBappCHJTFYpQKLnkhEa9plGCGlgNExSkTZpUEnR6guyx4rvKTdgOgbYN44dATQBFSOyLPxI3QV5yASQRV/8LsluPw0vGlSpscU+co6T6lr0qVXTfjLCzIgMDemaRl+y5wQBdtH3O7tPHF96sEnZ5PrFwrQ0ohlVZbpZGtaVcE6XI02V4InrVuokoBOUz4J7F99vRiS59lF3wnnBiEZRF4AkJZlRZ2bmY4ZGrtvcn6j5+7vgQg2nyQYW6YLDBYqbb2pUkDZBY5oevuwc1zTIuIiTq1op+8/UezRAyEdMQ6WpkcFQKjOrcJGmCDK7ynjRb8b0XjIqRbE6ARUNzHThpVePz4SGddEDCkZZSAdgatHUw0eueXmPHuc8KSL0arKWA4WuldBrT3BB+gdBJDdjbrDZVVcJtPhMsqlSRWyMZLeXUUWKWJkBZpZZZonfXwJprm/0WnJdY30SGiEEXek4FzktqKZzlOsYo1N0FvCdZ4Vlrt/lqY5FxblLATrBEvtf2/Er8nGtSfb4EUgw2sZ1nPOcz4KVtjnvb7755lIlyJ7bpDRyr2Y2N2buI12V/U73azo9U+cYnSipTcP1L02vXLRrG20UprzPfg5cwxldZuQitUuKtl+VrkkGFukkpNHF9KKMTtArn7583Jy5KRH106PPl5RGV6UVftHgoJHJhTi7gE75zahSbk4MqZJzmq0dYGEwLsZphIKZcshNJRe/yLNe3XrrrTGtj8ZjOrbUHNCQppiTUZosUinYX3q700W8aL32tQUX3IRIe2Oud7B/XANonDFjEAWQlYDrF7OZMbsTnQJpxWF6c7N5+AScdCSk62BRjzOz+9TUoEjPPfHEE7GTiBoqUv4q5frN/tEbnTpAKmXE6e+QoklBMvfk1OnDqBupYKk2jIY2nwsjk2QZVMpnwneWlLbs6uG0X+go4vPI3qOzNXCkMNMA5zpYRIzKUBeWFvXL1kemjrIipylXqiYZWGRnfyK3niE1LkjMGJNWJWUInZkmiPaZLYlhuCJLFx4uyNl9oZHF0Cm9Hyykk/AFroSLctoHGs7Mb53NMQfTjzIFYSroJH2E413kFVkpyOXc5hwunyaZOiEuyDRCswW75ce6yCMVNTVIyM+lEUKxdrLNNtvEjoVK2FcalwTI2Q4C3HPPPfF4U0eTai6yirrv1MUwskZa2+RwjjMFZeo4qBT0RpNDT6ORzqFUrFoJ1+zacE1OGQWkwzDjG9d1zoMbbrihWmdR0Qu1s0jl5DvcvHnzqimis1PjkyrEoq4p/Qt0ENEhSkdakQNqjiOdvMxUmb0n0ylEZzAjVkVvm1WiJhdY8IXkokyPdCrs5OLEqAUpP0W90daEgIFZUlKPFo0Magl4kP7D71IqBA1OAqtUd1BUNR0/VkgnFYZ0HxoZ2UCLnE2KORml4EZNLQmpE0UuXOXYpilVk2yvNMFVWiCtyAHUtKRFsRAg08xy02U2qEpI+WLb6Z1lhCqtP8L5nY45IxZ8t1l1u3wGoaKiEUWv/R577FH1XKU2qtN+ERxxryKoAvcxAmZS/Pr37191Llfq55AwGQHnOec7E48wqxl1gkWZWGJaEDgRQNDpVT5CxShGTWuyUEOZzpXGLu0L92c6C9Lq6FzH6CyhloZjzmgM1zBGYriWF3n690rWJAILTtrUcEgnIj0eXIzpxUsr0maHGGl0F1X6kjKVKr3xpP6kGYDIv2ZUhhsSvyPYSMOM9ABxgUoLDRVNOsYcU1KBaFxzM6aGhsWi2LeUDpNwkaaHn/QgZpBJU9kVeTYgjjM9PTWNQqTnUn0NF+0093tTCC4YgeQGzXcjNcSKlgpUWxBEfRApm+VFjYxEst8c7zSDTtGk85b8aha4A/nVadS5UmVnxqFzhBooCncvuOCCquCCexl59aSHFHXF9CmVzmkCaTqA6CAgHYZz+5ZbbikV3eQ6ONJoM7U16bxIf5LOWfSUOEajSMtmQgn2k+nfCRY5p3v27BmDSH5PIE3BvilQjVfFBxbZCy2pIZys9HgwzSKpThT00eORvowU8zKzArMQFLEXs3ybGSamoI3GM70dWcx+VR5cMIxcxB77tN/02DN0yjEkrSk9T0oQebdcnGoLHirhpkyKE/P1JzXdZGiQUU/BjYqeoKLeiKYFw+aMTKabcJGDCkbiaEzSEUIqDOc4NTXcmFP6Aw1PrnXUXDBCyxTaBNtFPOakhNCIJEhKdVLUkVBnUKkLmKa0XQru2VeCRo4jDS9qadIxJs2PFCFSY4ounZvZWdomh3t1KtIvsux3m+PIPfuaa66p9ppUN0XnX03f4aJdz9I+UPNHLRzTfzMqwfeZCSjIIqCjkNfRocDvSQerlEl0KlVFBxY0IJmejS8sxYpceFOOPSMSaXaULIbYijr7U7ow0avHBSitucGNl4sRoxTljWeCC/aXHv6iNqzTxYmgguJVejeyKT6MTDFtLPnW5JzS85ed5Sp9bkVsbJVjRIZeXEYuakOAmRZ9LO/5akqKdhPOImhm1IXea2ZN4e+kybz22mtx/QZGZZjbngU+eQ0pBdyU6fGe0gZbY5G+n1yTKbano4SURa5xNL64hhFQ0zlSaecx+04eOdN/gyljuV7TKZZ+n0biWYOlKKkvtUnH7+mnn47HdHL589mCZUYwKiWoIGWRDgA6faihYUSKgDK9hvOe7zcjlJWAtCfOZ6YKTlN/p2J89p/golKmum8qKjawYJiMxjS9sgQRpAMwpShpH+nilVJ/qLcgR3Pvvfeutmx8kaSLDilP5I5zk8lOo0mPDo1uLtjlszzxO+a4L8qKyrXlXLPgWZp+L2EKPo4xM3zR45mCC15bvuJ0JaDxxTlMYys7b312QUR+x9SF6flKa4xVOmqnuOESLIM1KjjHU14yx5hePXq2ybtOHQbMHkMjpWh1FilVj1EZZuyj44AAmjQYUlhJ/aOxzbWvEmQbmRwrgkE6fjiuKW03fWc5FypltCbt07333luabbbZ4j07LXZY/prafi460voIKlItIFkW6f5FuyTtL/VxdChUwv4zOsM+csxTelPaL6YS5vNgRM4i7eKoyMAi5d6edtpp8Wd6ezhxaXCX31QZTiZSZoaB448/vtAnL9tO8ECRU03ztdNTT6OaG1F5ylRNM8YUSVosiiAy7Rt1BPTsEFwSPPGgMcYNmosYxV8pBayScDNiBhEKW7NBMucEF2jOgyL31jdl3HAJEFIdFJ0H5BunlAl6rsvPab7bBNwsKlW0xjfBP0HU7bffHveLdAi+5xSzEmgQYDApA9d3vt9FDJTT9pLKlmZxoyA3XcOpg2JKVRpYdI6ljiGONZ1hTEPK97lo+10TGpJppqus7AKuRUxRrg0jy2kRRzq9OL4EkWmkne8swQbnfOocKx9hL/Jxz45QMcEEaelp1CJbP8LIa9HXlWpKQiWmP5FjzvB/Qv4eBU+cuDQ2k/QFrYSZYUhvIAWCRkcW+8bweFq3gJlxqKtgRcsi7285CveYMjd7kaVBlaYX5bzYeOONY40FKSPkmRd1bu+/Q8ODwnWCKubw55jTU83MVyyQVgmLojUVNTUaWGWXNBFWz2Zef3qtwfeZNAkKtNO/YySPwJrjX6Rix3RtohaIDh+u6Ywqkx5BsEE6FH9PDWwWwCtypxCNKdJyWfSN9K7sRBM8R1DB7HVp5iO+u6Tt0lFUxLTd2hAgkwKU7mnUEFEjxLWr6DMWlqPBzHFmhfjbbrutqoHNuUDqE8FESt1mwT9eSypgdirdogUVaXsZhSyfkZCRC9pohx566CTBRdHSN5u6igosuHGSe8vc9FyIKdJM6AlKIxdpVc7Uu1UJkT89VvRo0LBISI04+uij4wIzNDDJVQQNTdJl6B2qFIzC0EtPL0/5sUyNFG5aNKwp3m8KuDnxHaBRyaxXNDhTMOGIRbFwzaKRBYIK6qb4XhM0JNSRMQpHD3YWwUX5eiaNVfreltd70YNP7zxpT127do3pQIzMVtJ0yewTqU40rkjTzSItiIYm32VqLriWV8Kirel4p+sSHUQ0nqkfYDphggr2lVpJRpkr6Z7FpAu0R0jLZT/TGhUpvZH9Tx2CfC50GpK2XdQOoXSsH3744djJx7ToZIrQQZDWYUnBBetyZKcPLnLbrCmqmMCCIUJ6aLkA8cVjpgh6ubLBBUON5OfyZU7DjZWCGyy9eBTlUuhE44OCTvLp6fWgcHPhhReuWgSPLzYr11YKRifmn3/+OCtObStmH3fccXFUp8i1JHWhqDempoqAgZG2NKsbgTEzP9HQZHYkev8450lzK/JKzGl7mcGK0QkaUUcddVRV+iqpQQQY7DeNDx4slFV0qeODexgpvKQCMUpRHgxyz+Ic4DizYFiRR2iy6ADjvsTxJ+WJBjSjFqQFpdm/6KWnZz876UYlIFhm5kbqhegQTZ2epL+Ruk3qH/d2FvPMThVd1Gs4gQOpmxSok4bODI6k5jIzZRqVSOtycK4XdT+buooJLJ5//vkY5WaDiNqCC2ovOHGzPQSVgGFUpmMkgODLS69XCh7oAaS3i7UaKhVFf8xzzcU6ewPiwsxFivqT8mLASle0xqVqRnoMPbZpjQrSG2l4MOkC17i0yGPR09zoxWXkkVli6ASgcJkFPbPfZzoGCDjoSKmkzhEmWyA9hnoYgidS3GoaaSrq7H21SWvqnHXWWVXnbvlIFCMYjGSkNUyKLvXQEyzSGchIDMEFWQc0rEnVbdeuXXwwmyXf86Ifd1L26CBJ6V2kMPLdpkOQ1HWyDVJwwcK1RZ8+uCmrmMAiKzsDTk3BBTn25GtW4olLbyYzStDLWd4rxo2aERv+Xkn1FQk3JIIpgisaHaQM0ECht6dt27aFTxtQ0wsE0+gD1yzSnMirTzdfvuN0JpDix6QFRU9zYx+pM0gNTJBrzX5TF5adUpR9LHoaVDYNqHy6VBqbBBfcv1JwwQxflbq6NOcwwQUjF9nPggYm9246hVJQXVR8R1knKovjSfobkxEQNBFcMNsT6UJ8H0iJIsAs6ro75YEFCzvyvWW/Ob8JogmyKM6mY4QRG+spiq8iA4usbHBBvUFT7MllNhUCCupOKrVgOSv1/jDMykWaXOxK6tlU5aOhRRpItiFBjRg1BpNrUBd1pAI0NgggKErPXqNJgaK3Os3yV+R9TNK+kQZEBwiNKlJdsgX2BBekszI6QwOMhnfRZvWqTU0BUpr+nU4/erN5kBLE1OlFH2kmqGDf0npSjNKkhVqZFYoaC1L+2E/Sl0mPSgXdSdHPe7afNbZAmhuzcaa05D333DOmsjOzW1NPVa4EFR9YgBsxs+TwpSa3rymh6IsUsTZt2jSpHvuiX4TVdKV6CWY5o6CXfPuEBiizplQqUiWy+0cDnO8yDY5DDjmkVEmYKphZvagpoGaCIIK6kmeffbbqNdyvGLEh1a1S1t2hk4d7cXnvPeihp3YmrbPD6AXpy5WwzxRpU5BNLQWjMKwszX5edNFF8fm0Hglpf7ymfIbHSsLMdsccc0xVgE3wzOhUU5lYpdI14z+hCRg9enS4//77w1prrRU6duwYmoJPP/00dO/ePcw999zh7LPPDssss0xoKjitmzVrNsnfpaJ46KGHwn333RcefPDBsPrqq4euXbuG//73v+GTTz4JF198cWjfvn0oqvSd/OOPP+LPLVq0iM/17t077vf+++8funXrVvX6XXbZJSy00ELh/PPPj/+u6N/nDz74IHTp0iX861//CgcddFD466+/wrzzzhtmn332sOqqq4bjjjsurLfeelX3rhlnnDH+rlIcf/zx4corrwxXX3112Geffaqe/+mnn8JKK60Uvv7663DeeefF11WKzz77LPTo0SNMmDAhHHnkkfGYX3PNNeH3338PAwcODNtvv324995747EeMmRIPN9nmGGGUGQ13XvZ/5122ike67333jte026++ebw4YcfhgUWWKDBtlV1p8kEFk21gfndd9+F5s2bh1atWjX0pkiaymvUL7/8Er755pvY0OSGPGjQoNgQufvuu8POO+8ciryPBBDXX399+P7778OBBx4Y9tprr7i/xxxzTPjoo4/C8ssvHzbeeOPw0ksvhdtuuy28/vrrYemllw6V4K233oqNyF69eoURI0aEDTbYIGyzzTZh6623jsd1s802i51C/Fmp992TTjopXHjhhfEcSMHFmDFjwqmnnhoWX3zxeOyXXXbZUGmdfUcffXSYOHFiuPTSS8OSSy4Zn7vooovCEUccEVZcccVqnxevK1JwkbadYLimNkf6/Y8//hi22mqreE3jccstt8SAUpWhSQUWklQk6UY8bty42KN3++23x4Y2AcZMM80UiiTbYHr++edjQ3rPPfcMv/76a9yvww8/PJx11lnhzz//DP369YvB02+//Rbmm2++2PCi0VV0NCLnnHPOuE/0ytMrTUA1yyyzxB78li1bhg033DCOaOywww7hP//5T3yuqNIx55x99dVXY+DI6NsWW2wRG8wnnnhiuOCCC8K5554bR2o4L8gsePnllwu935Pz+eefx3MdPXv2rBqZKmIgUdOxZvSlf//+MVjM7lvC95trF6OVfPcZoZlrrrkaZJtVPwwsJGk6q60BUVPvbm09vukGXRRpP4YPHx7uvPPO+Hd6b0EQQUoQjZHTTz89tG7dOj7/888/xzSpWWedNRTd0KFD42gEPdOkgIDGFYHErrvuGo499th4TA8++ODQqVOnsOOOO8bAo+gGDBgQ95cRCAImUroYkaDxSaOS9DZS4OaZZ57Ye/3AAw+ElVdeOVQyggvSoXDKKaeEddddN1QCjinH+rTTTosjEiussELV9z57zStyAKW/Z2AhSdNR9qb69NNPxwYnjarlllsuLLHEErUGEunfpUt2Y0/rTNub3d8vv/wyNiqpJ6BBddRRR1W9/q677orBBWlRhx12WHxdkdV0HAmcXnvttZhXzmfy7bffhn/+858x7Wu77baLPfWkfb3xxhtVwVWRcbw7d+4cayU4pgRSBBqMQBE0kQ7G5/Dxxx/Hz4p6wLZt24amgOCCtL+RI0fGdDCCySIjaCSYIL2PGqnsfpLyBQOKpsEjLEnTUbqxnnDCCbFAmRSYq666Kmy00Uax0VlbwJD+XRGKl1MDgiLU6667Lrz55pvx+UUXXTRcfvnl4YcffogNEUYkEhrYN9xwQ7jkkktiQ4ve+yJLx4iiXVKgcNNNN8Wat1SYTgE+IxSkAJEec+utt8bGdiUEFanGb/z48XG0Aow+MRJDQPnFF1/ElD5QS8HkIk0lqACNbUZr1l9//RhYFh21YHPMMUccsWDkie8wQSX7x3cbBhVNg0dZkqYzagiYCSX1TpNzzo2Z0YuiS0EFgcPmm28ec65pYKaRlkMPPTQGFwQRffv2jYWeCalCpFMwA1aR0rxqwwxeFJwTPDADEsEGdQXDhg0LDz/8cHwNNRak//A5vfLKK2GVVVYJlYIAiUCK+qCEtDZmQGK05t133w1NGcEUBexpZK9I0vd57Nix8U/qhtgP6qbWWGONOJsdASPn/T333BNHJNU0FP/KLUkFQ6ObtJg111wzFqv++9//jo1splWlwJWbdbt27UIR0bigQc1MRzSoqSkonxqX4IK0GFJkaKCQJkNRM+jRLrqUBjXzzDPHz4HP5JxzzompTgQSFK0+9thjsYAdpMA19lGov1PTbEbzzz9/WHjhhWMQSSMzzfJEYTa99PRwKxSuNz8d68cffzw+9thjjzirE6NunOPMZsb1jePNBAzrrLNOxYzC6e8V50yWpAKqqSeSOezJJ2fKVVIHSImgvoDXsnYFvXvMBFVEBAxMGUpjo0+fPlVBBekRzIREPj0oVma/KfRkZiCmGq0U9MaDOhFmd6IRRoOL9C5GJ+i1J/3tjjvuiK+rlKDiqaeeilMjb7nlljEFjnOY9K/3338/rtnBSB1pcSeffHJ8jqBLxcOxplaG9SgIGEhxY4SRKZI53gTRKYhkxi9G6JrK+mH6vwuCJKke/PXXX1V///DDD6v+fu6555batm0bV16+6qqrqp7/6aefSptttlnp9NNPLxXVhAkTSuutt17pP//5T9VzAwcOLB199NGlOeecs7TooovGlYXTqru9e/cuzT333KUffvihVAk+/fTT0hJLLBFXE2bVcGy88calAw44oGrFbX7H6tOspM7q0pVgwIABpTnmmKN08MEHl04++eRS+/btS1tssUVp/PjxpU8++aS0+eablxZbbLHSIossUlp++eVLb7/9dkNvsqbRO++8E49vv379qj0/ZMiQqr9znh900EGl+eabz2PdxBhYSFI9BxWnnnpqabnllis9/vjjVc9tv/32sSE2aNCg0ldffVX64osvYuNrtdVWi43zoho9enRp6aWXjo0KGpQEDksttVSpS5cupUsvvbR0/fXXVzW8swFVpRg2bFjppptuKrVp0yYGULfddlvpo48+Ku25556le++9t+p1V199denjjz8uVYKhQ4eWVlhhhbhPIGgkaD7hhBOqgisCqG+//TZ+Fj/++GMDb7HyePjhh0srrrhi6ffff4+B44033ljq3Llz/J7vvvvu8TU33HBD6dBDD62Yc1xTzulmJake9ejRI6aAkGfOlJIdOnSIz5NnzxSjzBpEXQVFvuRZP/fcczE3n3Qp5vkvomeeeSYWbi+wwALhp59+iilPzAxELQEpUdQWUENy4403xtfXNsVukbG6MDN/MfsRx5dCXWoOSBPh+FYSUl1I+XrxxRfjJATMcMbUo9dcc038PbOdMZ0ya1io+JhogKlySWUjtY3vOd9nirZZm4aZzfi+kxZZqQsdqnYWb0tSHco2kpn1hpoJculpbNHA/Oqrr+L0okzFyDoWTLn5/fffx6k2uTETXBRt8bty7Nv//ve/OBsUxbusW5EQLLVq1SosuOCChVmToza1BX88T+45s1+x4jT1FMwABgr2KdIvsvJAkCCKKYTfeuutsN9++8WggtmA8N5778UphE866aSKWD29qUnHmg4BrkvUBzGL3UcffRTPbYKLfffdNy6Gx/TRHHeuXVzHDCqapuLeuSSpETe4GJGYbbbZYuOa3mp69mhc0tvHtLIUM7JuQfmquxRwFzmoSAgceGSxpsGZZ54ZXnrppXD22WcXLqBIsx1RaM4sVgQVr7/+epzhKNuI4nnOBRphBJQ8rrjiijjFcNHXLEjnOMXoNC6ZdIAZgVivgEYmq4inkQowEQFBZps2bRp0uzXtx/rRRx+Nxfgcx1VXXTVOzECRfrlLL700BpmMTKrpKv7dS5IaWVDB6tEEEjS+FllkkbDaaqvFKWSZarR3795hk002ic+zbgEpIkWddnJqEESxZgcNTaZaTavxFgnHhpmtmFaTY0yqBw3pF154YZIAsXzqVabUpWeXYLPI2C/WGmEGIBqYjEgwEnHIIYfEIJqfn3322TBq1Kg4GnfttdfGP5vS4neVgmPNeitdunSJx3fllVeO61OwcjyzepEOBWaIYvSV7/aTTz45SYeCmhYDC0mqA6khOXjw4Djd6MUXXxx7sbnR0hCjF4/53FkwjMYm0zE2lZxzVp5mJV6m2KXRyQhOUZESwmjUKaecEveLOhGCihRAlOO5FHQWPagAwSFBFdOIphXEsfbaa8d6IlJhWIuExiWjFAQV1BapOB0jKUWRkTmuYz179oxr7YCAslevXvGaRqcIa1aQ3sl6FdTYFPm7rbph8bYk1REamaSBzDPPPOHuu++OQUQ2B//333+PqQLcnAk+aKQVtUB7atGbzedBfUXRG18cW1YYJlikGJuVpFFbcFEJ0r5feeWVsdeanmzO3ZR/ny1IZ0IC1i/h37gIXuOXzlvqZEjDnGuuuapqhaj7ojCf4CK9jmsY6X3UUlE/k039lCrzCihJ0xmLgTE7DjddRi0YraDhRcFjuklTyP3Pf/4zpokwUw6/5/mmgBmRihxUZFFfQc45dTLklaeF7mh01bQgYiVIvdkEiKSDcV7zHMFDCipI7QOfC6NxBhXFwHnLNesf//hHLLInwMgGC9RWJJzfTEzArE8ffvhhrJuCQYUSAwtJmgblg730xpNHf+ihh8ZZnkgXAT2AqbFJjvLBBx8cZ4WiMUbjrKmMWFTCsabBxbGkp7Zr165xGl0KtKkjIL88NdJYXZvRqUr8DJguOc0AlUYx+JNzmc8hzX6l4uCcvuWWW8KQIUNigMEECyNHjowBNIEGI7EXXnhhPLfTiBwjrgsttFBFTDShumUqlCRNpWzKC0EEoxNcSumlZd0GbsSsXcEsOUw5WpMir1PRFBEskFvOMaNYmTUq6Jkn7YciVgq5KcrnTxpmX375ZZxqt6hS0DB69Oh4rtOAJIgCNSU0PBm14bPgd3369ImzXhE0L7bYYg29+ZpKTI1NehMTTXCOs64ONTPUyXANO/LII8Nuu+0W16tgJIMAkhGqos9yprpnYCFJ0xhUUMDKDEekNnGDpcBxqaWWij26N910U3xsuOGG4bLLLmvozVaOxjUpH6w/QZ45DeqPP/44jBgxIqZAUYRPL+8ZZ5wRi7lpdNH7y+hU0febOgoalZ9//nk8j0l/YSYoRico2mW/eR0917yG70KR97upFmpzTSOYOPXUU2MRNh0lTDG73nrrxXOe1KennnoqXsc4v6nBOP300+PaFVI5AwtJmgbMCkTqxwUXXBB/ZjYcRivSbCkEFzQwKe498cQTw7HHHtvQm6xp8Pbbb8fH8OHDq2bGYXpZgkpmw6GQm+CCxcEoYqaBRkOs6B566KFYD8R5vuiii8aGJtMnn3zyyVVpftQM8blQS0EjlCmUVYyOEa5VBIjUPqVAg5nbuKYRRPB3rl8cV9KhGLlIQQejci1atGjoXVFjRWAhSZpyjz76aKlTp06lV155Jf788MMPl2afffbSMsssU1pggQVKH3/8cXx+xIgRpTvuuKP0559/NvAWa1pw/Dp37lyabbbZSv/617+q/e75558vbbnllqUVV1yx9MEHH5Qqyeeff15aeeWVS1dffXX8edSoUaW2bdvGc37xxRcv9e3bt6E3UTl89tln8Tgut9xypQceeKD0ySefVP1uo402Kp1wwgnx72eeeWbpH//4R+m4444rDR8+vOo1EydObJDtVjFYvC1JU4nZjbbYYouYHkNPLgufnXfeebGugtoJph8lZ5lePvKSm9LsT5WE47f//vvHlA9655kRKWGlaXrvmQ2H9RwYraiUBADWG2H/tttuuzgD1Oqrrx7XprjzzjvDfPPNF2tNWElcxRyxoAaMVD5msCOliZE4Jp1Ii3hSN8ZsT6RBcQ4wevWf//ynahKKlEYl1cRUKEmajNrWJqCRSQNsm222iQEGjS1uxptuumn46KOP4oJhzPefzWdW45aOFcec6YNTsfIjjzwSaygIKKmboYA1oYCVmZIqbbVhGpmkOB199NEx3YkUGWYJYgVmaikWWGCBWIPBd0DFwvFMqXysubP77rvHQm3WHqGG4plnnompUPvtt198PemeO++8s6lumiKOWEjSFAQVrFHxxRdfVP2O3ORvvvkmBhHMjJNWqm3btm3s2b3//vvjcwYVxQoqBg4cGHttyS2nLobAYeutt4555gQb++yzT+ztTdZaa61CBxWpF5qi9KFDh1Y9T1DB7z744INYrEtQAb4PBBv0YhtUFBOBMbOaERx+8sknsQifxTqZCnullVaKr8muQXL88ccbVGiKOWIhSX+DRiXTjTLPO1My8vjXv/4Vf8fsOEzJedRRR8VePlKe6PFLi6VV6krMlYgRJmY9Ii2E2Y2YNnaWWWaJa1Qw29e9994brrrqqhhA0ltPqlQRcZ4yFTIrh2PAgAGx8Ug6F6M0pPbRi03RNs+/+OKLYZdddolrF9x+++1xccciT6Wr/zdy0bt37xg8E0wTMIIF8ZwyWNPKwEKSymQDghtuuCFOw3jxxRfHRheNMHpxyUFn0ahnn3021lewbgENMRqnLH5nUFEc3AbJN6c2hpQP1qWgkU2KE4HGRRddVDXyxBSzzOF/5ZVXxmlWi4ZUl2WWWSamdVEfxFTJBMoEEKT0cf4OGjQoTp/MjGaMZHCeMyMUoxakRDmlbOVg9O3ss88Or7/+ejz/qRuC6+xoWhlYSFItGHlgwS96punFBtM00rgi3Ym6CoobaYQyvSxpUDRAmcbRFWmL5ZdffokralOkzfFcZ511YgrUNddcE3/PFJwUMdMgT/UHRW5Msm+cq0yF/Oqrr8bgIenbt2987L333jHIYkQOBMumP1VucPHOO+/EtUq4rknTyu40SSpDA4p8c1ZSJh2GlIGEYsfDDjsszuNOESsYoSBvORX+GlQUC8eMufkZtSDljfQ2Gt6MSoAUOGZBImUERQ0q0mJoBMCkcjVv3jyuVcECgATDCbn2jF6koIpgiodBRWXifGC9kiWXXDKOTPE9kKaVgYUkZYpYQY81aS40JGlEMnLx2WefVf1+9tlnj0W7zKrCa7NMf2r80kA9wUQ6ZvPOO2+cBYc8cwpVaVSnAPG6666LeecsfFh07CuF16T03XPPPXFF7ffeey+8//771V7H7GZ8Tkw9qqYRXJD6duutt1bEAo9qON4BJTV52XoIClsp0GUl5TXWWCM8/vjj4c033wynnXZaVeOLVJiXXnopzqrCaIWKOfsTRcoUJZP+RCrUQQcdFIuWWYPkkksuiSMWjE5ddtllcZrZIs/+BPabc5n9JmBmelGKsfmT5/gdqyun1C9GNFxhuekg5bOoExKo8bDGQlKTll1ngikY6bE766yzYq5xmvnmhRdeiOkx9OStssoqsSebhcMILpg1yLUqioXjSZobC9tRX0BgyfFloTCKmamhYbFDenEJJlhEjGLmovv8889jEEWdEL3TqUCXHPutttoqpv9R2M3IDNMlk+pnobakqWFgIUkhhKuvvjoWLZJj/49//KPqeaYWZTYc0qJojJIixeJS2267bQwmWBSP4ELFQOOZwIEVpI888sj4HIEDMySRFsSsOKzbwIgVNQWkSxW9157bPPvDGgXM8sRMVwRO2dE6nu/atWt44oknYkBBcMGsWJI0NUyFkqQQYhrIDjvsEIMK6ilIfVl33XVjY5N5/KmpePLJJ+Mief3794+55zTYDCqKg8UM99xzzzijFwscJgQWFGs/99xzcV5/GtmpUJl0oCJLo2lMOsA5TWDM7D+pED2tt0IKDFMrc84vvfTSBhWSpomBhST9//nFNLZIhyHfnJQR0kBYRIyZc+jxXXvttWMhN4FF9+7dq63ArMaPWW9Y6I6gkOPIStoJNTRMHcyI1eWXX15VzF/UFLeUjPD777/HvzPywnoVFKUzfSz7SC1JNrig1oJ1WVz8TtK0ck5ESU1Kyisvr4vYcsstY4Pr7rvvjkW85Nx36tQpzpxDUJEWvaNHl1l1dtttt6rGm4qB0SUK8xmFYFpNGteHHHJIaNmyZfx9z54942t23XXXQs/ulS1QT4EE5y8F6QQXpEExA9YFF1wQV5BfccUVq/bXRdEk5WGNhaQm45FHHomrJjMTTm1BBysTU1MBAoltttkmNjwJMGispcCEnmBW4lbjblxTsPztt9/G6WRJf6K2grqYww8/PPbYE0Qw81OlHUtW0Cb4Pemkk+IoDQvevfHGGzENilE4RiZYr4JibSYrWGGFFRp6kyVVgOJ2yUjSVFp22WXjStr33ntvjb8nYCCoYOpRghBGLb755ptwxx13xEYqjdXUo1v0gt6mEFSQzkbBPSNQ1FD06NEjvP7663FUgtEKipl5DT33BIqVgvOXKXJJ7zr11FPjKuIs8kfRNkEFnw8jF5deemlci8V1CyTVFQMLSU0Cow8UrtLIHDRoUFXueU1YDI1CbaYafeutt2IaCSsTZ1Onipp73xRwbDh++++/f0z1oRifqYRZFI7GdpommOCCc4Jgs4iBRTp/WVcli3oKzuGddtop/PDDD3EVbRa8Y9QCt9xyS5xWl/Q/UsKorZCkumAqlKQmhRSQffbZJ6ZDrbfeerWuQUFhNgXd2fQnFQMNbYrrWUH77LPPjqNOHOvFF188Th/cqlWrmP7DDGCkRf3444+hXbt2oYjYdmZxYjYrguaEQvTVVlstLvjIGhWMYBAgU7hOChQLA7IYoGuwSKpLjlhIalJIAWHWp+OOOy589913tTaqWBytPP1JxcCq0qnxTOE9PfMseMgoBtPNMmJ19NFHV41cFDWoALUhBMrUjDASAUbXSHm68MILY/ofBetphfiLLroojuAwCQEMKiTVJWeFktRkpN7ZvfbaK3zyySdxBeadd955siMSNrwav5p63RmNoA7m5ptvjgveMXIB0ttobHfs2DGmQRUdEwuQ3jXbbLPFBe44j6mloLbiv//9b1yT46ijjor7S1of6WCs18HnIEl1zRELSU1GanwySw691OTYI00/q+IGFaxBcuutt8ZZv7LF9RQyf/311+Gnn36KP1O8vcUWW8SpV4vWuE5raySMTLD/TDhwxhlnxHVWCJpTMMVnQfE6s1/deOONcd0ORmsoWpek+mCNhaQm2RCdMGFCXACPxe9YFE/FxboiTBtLwPjpp5/GQmVWkWaK2ccffzz26HPcWU2bhvVrr70WlltuuVBEQ4cODffff3848sgjq4IN1qA477zz4uxWpPoxNfJ1110Xi9cZjUvnOwH0TDOZqCCp/niFkVQxUiNrcgEFD15HzvkxxxwTi7kp7l1ggQWm+/Yqn9QvxqKGjD4xCxKzIXXp0iXWVzCt8Oabbx7rLN588834JyMWpEIVEUHClVdeGafIZeYnZrrifKdwm3qKu+66K2y44YYx7enAAw+M5/jee+8d/y2LAkpSfTOwkFRxQcWjjz4aG5E8x1oUaXanJL2ORti5554bFxNjBWYVQwoSmUqVY8zCd9RUMCKx6qqrxiJtRi0INOjdZ6E4HpMLPIuAEYcjjjgiBhXUSpACxQxYFGSTBkbaE1gUj9dSc0FxOqNykjQ9mAolqaKceOKJMbd8+eWXj8WrTDlK8SqNzJoapyx+x2J49ASnFbfV+PXv3z+cfPLJsSeeQvw777yz2jFmxW2mWZ199tljOhTBR6VgKmSK0Qmgvvjii7h/nTt3jjUXKdUpLZK34447xtW1JWl6KG7XjSSV6devX+y5ZQRi4MCBMbeenHpmzCmXRjBImeF1BhXF8cEHH8Q0IOoq6MFndica2jyfLLnkkrH2glGKIi5+NzlMhdyzZ8+Y5kVa1zvvvBOfJ6gguAABFSuNG1RImp4csZBUWCm1Jf3JKsu//vprHH0g35y1DPr06RPTnGhcsjgaaVG1cbGwxu/9998PTzzxRFyDhIJlsIo0hfgc22uuuSZ06tSp6vUULac1HCpNGrl444034sgEo3VwQUdJDcURC0mFRBCQ8uUpwMbw4cPDwgsvHHtwKV4955xzYlBB4MEsOQ8//PAkU3ZmGVQ0Tqn/i/QeVpdmtOLjjz+u+j1Tq3LMWbPh0EMPDW+//XbV7yo1qEgjF6ecckpYffXV4+gMI28wqJDUUAwsJBUOwUEKAsizp1CXRuc222wTTj/99FjAS8919+7d42sYrSCoIB+9yMW7TRXHmrUZWPSNWgrqCZhWNqU6ZYML0qHouR8/fnxoClJwQerXyy+/HH788ceG3iRJTZh3WEmFk4KDDz/8MAYNjFiQU86sOMzdT2OLGYJ+++23WMTL6trMIMQiYireSAWL25HSxnFddNFFY8E9a1SwbgNpUel1BBfDhg0LV111VZwNqangc2F0jvqi1q1bN/TmSGrCrLGQVEjM5X/44YfHgIJCbRqcYL0CRiso5GZ1bQKMVq1ahaeffjqmxZh/Xiwct8ceeyzWx1x88cVxFiiKlEl72n777ePP9NgzamUqmyQ1LEcsJBXSrLPOGtcuGDJkSOylTlZbbbW4WNorr7wSLr300th7/dxzz8WgghlzDCqKY9y4cfHYXXLJJTHNh9m9CCp4nkLtBx54IAaKFO0/88wzDb25ktTkOWIhqdGrbWGzF154IZx11llh6NCh4aabbgprrLFGTIvJFnb/3Xuocfvqq6/isaV2hkCR6WVBDQXpThTs77PPPrE4n8J9SVLDMbCQ1KhlAwIKc7lkMfqQ5uenp/o///lPDC4YnWAUwyCimNJ0v99//32cNphRCUamqJXp1atXPM6kQzGNMBi5IBXK9DZJahz+b4lOSWqEsiMP//73v2PqC7n1HTt2DFtssUXMrWeGIAIJ1q447LDDYsNz3XXXbehN1zQGFffff38MIqipoDaG2oljjjkmLvZGQEnaE+cE084SVMAgUpIaB6/GkhqtVIzLbE59+/aNufbUTjBaQaBBYxPMBkVQ0bJly3DDDTc08FZrWo/1U089Ffbaa6+Y2vTWW2/F48ooxYsvvhhnfOIYH3300XHE4sYbb6z2byVJDc8RC0mNGoudMaUoK2lvtNFG4fHHH49rGey6667hiiuuiMW8Z555Zth4441jD/cqq6zS0Jusv1HTCuekNXFcu3XrFkcoWFn7nnvuCfvtt1/YZZdd4mtIjaLGgtqKtdZaq4G2XpJUGwMLSY3a0ksvHbbbbrs42xPrVdDQvPDCC8Puu+8edtttt3D22WfHRcFIheI1sMai8UrHZtSoUXF9Ciy22GIxrYnnNttss1hjsfLKK8cFDwkeQYpUWquEkSprKiSp8fHOK6lRrVlAjcQJJ5wQxo4dG58jvenYY48Nc8wxRxy12GmnnWKqDI1Mai023HDD8O2331atwAyDisYdVLCw4bbbbhs22GCDGCikmZ7mm2++ePyZ3WuHHXaoCioo5ObYs0aJhdqS1Hh595XUKDBd6B577BEeeeSRuILw6quvHiZMmBB/R7oTf3/vvffC6NGjY+/2H3/8EdevYASD3mwarNngQo0zqOAYksbUqVOncN5554X1118/9O/fP/Tu3bsqoCR4SGlu4HfU1rCCukGFJDVeTjcrqcFRmM0q2nfffXecBWjEiBFxJILVtUlvSvn4FG+ff/75cdYnggqmIaXIl8ZmTXn7alwGDx4cVlhhhTizEwX5+P3338PWW28daywYsXrwwQdjkTZrUpAiRZDBInkUdpMeJUlqvByxkNSgGG045JBDwoABA8KOO+4YU5wWWGCBuMpyv3794nSyrKTNQmh777137NWmMUoD9Y033ohBBY1Pg4rGP2LBjF2ktM0777xVz7NOBUX5rIqO7bffPo5OMGI155xzxpGNV1991aBCkgrA4m1JDYZeamZ5omf6f//7X9Xze+65Z0yJoWFJgEGNxTfffBP69OkTjjrqqPhIaJCmlBk1XqRBMSrFKNPtt98efvnll3DyySeHH374IaZE9ezZM7Ro0SK+doklloiLHUqSisVUKEkNipGIc889N7z22mtxlqdBgwbFlBlGMBZddNH4Goq1CUA++uijar3dpj8VD2luzOTFNMLrrLNOuOOOO+JI1WWXXRZ/n25J6bh6jCWpOAwsJDWaxiaF2xRnv//++zEdit5tZoW65pprYnH3ww8/HOaff/6G3lzVQTBJQTZF2xxnUtrg6JMkFZs1FpIaXNu2bWMqDFOQMkpBLzYIKmhs3nvvvTFdiulIVXzt2rWLxzvN8sSIFQgqnNlLkorLEQtJjW7k4vXXX4+rLR9//PFxcbwvvvgiTlNKw9PUmMo73u+8805cOb1Xr14NvUmSpBwMLCQ1usYmaTJMI0utxVxzzRUXVJt55plNlanQ481K2l9//XW48847Q+vWrRt6kyRJ08jAQlKjbGyeeOKJ4fvvvw8PPPCAQUWFGzlyZPyzTZs2Db0pkqQcDCwkNUo///xzaNWqVZym1KBCkqTGz8BCUqNGMS/BhSRJatwMLCRJkiTlZjegJEmSpNwMLCRJkiTlZmAhSZIkKTcDC0mSJEm5GVhIkiRJys3AQpIkSVJuBhaSJEmScjOwkCRJkpSbgYUkSZKk3AwsJEmSJIW8/j8MxsxprbvuWgAAAABJRU5ErkJggg==",
      "text/plain": [
       "<Figure size 800x800 with 1 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "import matplotlib.pyplot as plt\n",
    "import numpy as np\n",
    "\n",
    "# Matched lengths of classes, labels, palette\n",
    "class_values = [\n",
    "    10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 100\n",
    "]\n",
    "\n",
    "class_labels = [\n",
    "    'Tree cover', 'Shrubland', 'Grassland', 'Cropland', 'Built-up', 'Bare / sparse vegetation',\n",
    "    'Snow and ice', 'Permanent water bodies', 'Herbaceous wetland', 'Mangroves',\n",
    "    'Moss and lichen'\n",
    "]\n",
    "\n",
    "class_palette = [\n",
    "    '006400',  # Tree cover - dark green\n",
    "    'ffbb22',  # Shrubland - yellow-orange\n",
    "    'ffff4c',  # Grassland - light yellow\n",
    "    'f096ff',  # Cropland - pink\n",
    "    'fa0000',  # Built-up - red\n",
    "    'b4b4b4',  # Bare / sparse vegetation - grey\n",
    "    'f0f0f0',  # Snow and ice - white/light gray\n",
    "    '0064c8',  # Permanent water bodies - blue\n",
    "    '0096a0',  # Herbaceous wetland - teal\n",
    "    '00cf75',  # Mangroves - greenish\n",
    "    'fae6a0'   # Moss and lichen - beige\n",
    "]\n",
    "\n",
    "counts_2018 = result18.reduceRegion(\n",
    "    reducer=ee.Reducer.frequencyHistogram(),\n",
    "    geometry=marion.geometry(),\n",
    "    scale=10,\n",
    "    maxPixels=1e10\n",
    ").getInfo()['classification']\n",
    "\n",
    "counts_2024 = result24.reduceRegion(\n",
    "    reducer=ee.Reducer.frequencyHistogram(),\n",
    "    geometry=marion.geometry(),\n",
    "    scale=10,\n",
    "    maxPixels=1e10\n",
    ").getInfo()['classification']\n",
    "\n",
    "def plot_side_by_side_histogram(counts1, counts2, class_values, class_labels, class_palette, title1, title2):\n",
    "    labels = []\n",
    "    colors = [c if c.startswith('#') else '#' + c for c in class_palette]\n",
    "\n",
    "    counts_1 = []\n",
    "    counts_2 = []\n",
    "    for i, val in enumerate(class_values):\n",
    "        counts_1.append(counts1.get(str(val), 0))\n",
    "        counts_2.append(counts2.get(str(val), 0))\n",
    "        labels.append(class_labels[i])\n",
    "\n",
    "    total1 = sum(counts_1)\n",
    "    total2 = sum(counts_2)\n",
    "    perc1 = [c / total1 * 100 if total1 else 0 for c in counts_1]\n",
    "    perc2 = [c / total2 * 100 if total2 else 0 for c in counts_2]\n",
    "\n",
    "    x = np.arange(len(labels))\n",
    "    width = 0.35\n",
    "\n",
    "    fig, ax = plt.subplots(figsize=(8,8))\n",
    "    bars1 = ax.bar(x - width/2, perc1, width, label=title1, color=colors)\n",
    "    bars2 = ax.bar(x + width/2, perc2, width, label=title2, color=colors, alpha=0.6)\n",
    "\n",
    "    ax.set_xticks(x)\n",
    "    ax.set_xticklabels(labels, rotation=45, ha='right')\n",
    "    ax.set_ylabel('Percentage (%)')\n",
    "    ax.set_title('Landcover Change: 2018 vs 2024')\n",
    "    ax.legend()\n",
    "\n",
    "    def add_labels(bars):\n",
    "        for bar in bars:\n",
    "            height = bar.get_height()\n",
    "            ax.annotate(f'{height:.1f}',\n",
    "                        xy=(bar.get_x() + bar.get_width() / 2, height),\n",
    "                        xytext=(0,3),\n",
    "                        textcoords='offset points',\n",
    "                        ha='center', va='bottom', fontsize=8)\n",
    "    add_labels(bars1)\n",
    "    add_labels(bars2)\n",
    "\n",
    "    plt.tight_layout()\n",
    "    plt.show()\n",
    "\n",
    "plot_side_by_side_histogram(counts_2018, counts_2024, class_values, class_labels, class_palette, '2018', '2024')\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "id": "272d1cf9-5736-425f-989b-5f58adf55e8a",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.13.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
