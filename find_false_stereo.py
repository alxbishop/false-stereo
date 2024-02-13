# %% Libs

import up42
import geojson
from pathlib import Path

from datetime import datetime
from shapely.geometry import shape
from itertools import combinations

# STATED THEORY IS THAT AS LONG AS THE ACROSS TRACK INCIDENCE ANGLES ARE  DIFFERENT OR IF
# THE ALONG TRACK ANGLES ARE DIFFERENT THEN THE IMAGES CAN BE CONSIDERED FOR FALSE STEREO.
        
# this script does not seem to be producing reversed ordered duplicate outputs, I assume this is because
# with what was the previous 'current' scene set as 'reference' scene, it is not passing overlap validation. 

# %% ================================== Fuctions 
def calculate_overlap_percentage(geom1, geom2):

    intersection = geom1.intersection(geom2)
    area1 = geom1.area
    area2 = geom2.area
    overlap_percentage = (intersection.area / min(area1, area2)) * 100
    return overlap_percentage

def write_geojson_output(output_feature_collection:dict, output_name:str):

    output_dir_name = Path.cwd()/f'./output/{aoi_file.stem}_{search_collection}'

    try:
        Path.mkdir(output_dir_name)
        print(f'Output folder created at {output_dir_name}')
    except:
        pass

    with open(f'{output_dir_name}/{output_name}.geojson', 'w') as tav:
        geojson.dump(output_feature_collection, tav)

def false_stereo_validation(search_results:dict, output_dir_name:Path):

    if len(search_results['features']) > 2:
        print('There are enough catalog search results to continue')
        stereo_list = []
        features = search_results['features']

        for reference_feature, compare_feature in combinations(features, 2):

            build_feature_collection = geojson.FeatureCollection(features=[])

            ref_geom = shape(reference_feature['geometry'])
            ref_ordering_id = reference_feature['properties']['id']
            reference_sceneId = reference_feature['properties']['providerProperties']['acquisitionIdentifier']
            ref_incidence_angle = reference_feature['properties']['providerProperties']['incidenceAngle']
            ref_across_angle = reference_feature['properties']['providerProperties']['incidenceAngleAcrossTrack']
            ref_along_angle = reference_feature['properties']['providerProperties']['incidenceAngleAlongTrack']
            ref_acquisition_date = reference_feature['properties']['acquisitionDate']
            ref_cloud_cover = reference_feature['properties']['cloudCoverage']

            cur_geom = shape(compare_feature['geometry'])
            cur_ordering_id = compare_feature['properties']['id']
            current_sceneId = compare_feature['properties']['providerProperties']['acquisitionIdentifier']
            cur_incidence_angle = compare_feature['properties']['providerProperties']['incidenceAngle']
            cur_across_angle = compare_feature['properties']['providerProperties']['incidenceAngleAcrossTrack']
            cur_along_angle = compare_feature['properties']['providerProperties']['incidenceAngleAlongTrack']
            cur_acquisition_date = compare_feature['properties']['acquisitionDate']
            cur_cloud_cover = compare_feature['properties']['cloudCoverage']


            overlap_percentage = calculate_overlap_percentage(ref_geom, cur_geom)

            # Build output geojson features
            build_ref_feature = geojson.Feature(geometry=ref_geom, 
                                            properties={
                                                'id':ref_ordering_id,
                                                'scene_name':reference_sceneId,
                                                'overlap_percentage':overlap_percentage,
                                                'incidence_angle':ref_incidence_angle,
                                                'across_track_angle': ref_across_angle,
                                                'along_track_angle': ref_along_angle,
                                                'acquisition_date':ref_acquisition_date,
                                                'cloud_cover':ref_cloud_cover}
                                            )
            
            build_cur_feature = geojson.Feature(geometry=cur_geom, 
                                    properties={
                                        'id':cur_ordering_id,
                                        'scene_name':current_sceneId,
                                        'overlap_percentage':overlap_percentage,
                                        'incidence_angle':cur_incidence_angle,
                                        'across_track_angle': cur_across_angle,
                                        'along_track_angle': cur_along_angle,
                                        'acquisition_date':cur_acquisition_date,
                                        'cloud_cover':cur_cloud_cover}
                                    )
            
            if 80 <= overlap_percentage <= 100:

                if ref_across_angle > 0 and cur_across_angle < 0:

                    print(f'-- VALID OPTION on ax  -- {reference_sceneId} and {current_sceneId} acquiered on opposite side of orbits')
                    stereo_list.append(f'{reference_sceneId}_{current_sceneId}')
                    print(f'{ref_along_angle}, {cur_along_angle}\n{ref_across_angle}, {cur_across_angle}\n\n')

                    build_feature_collection['features'].append(build_ref_feature)
                    build_feature_collection['features'].append(build_cur_feature)

                    write_geojson_output(build_feature_collection, f'{reference_sceneId}_pair_{current_sceneId}')


                elif ref_across_angle < 0 and cur_across_angle > 0:

                    print(f'-- VALID OPTION on ax  -- {reference_sceneId} and {current_sceneId} acquiered on opposite side of orbits')
                    stereo_list.append(f'{reference_sceneId}_{current_sceneId}')
                    print(f'{ref_along_angle}, {cur_along_angle}\n{ref_across_angle}, {cur_across_angle}\n\n')

                    build_feature_collection['features'].append(build_ref_feature)
                    build_feature_collection['features'].append(build_cur_feature)

                    write_geojson_output(build_feature_collection, f'{reference_sceneId}_pair_{current_sceneId}')

                elif ref_along_angle > 0 and cur_along_angle < 0:
                    print(f'-- VALID OPTION on al -- {reference_sceneId} and {current_sceneId} acquiered on opposite side of orbits')
                    stereo_list.append(f'{reference_sceneId}_{current_sceneId}')
                    print(f'{ref_along_angle}, {cur_along_angle}\n{ref_across_angle}, {cur_across_angle}\n\n')

                    build_feature_collection['features'].append(build_ref_feature)
                    build_feature_collection['features'].append(build_cur_feature)

                    write_geojson_output(build_feature_collection, f'{reference_sceneId}_pair_{current_sceneId}')

                elif ref_along_angle < 0 and cur_along_angle > 0:
                    print(f'-- VALID OPTION on al -- {reference_sceneId} and {current_sceneId} acquiered on opposite side of orbits')
                    stereo_list.append(f'{reference_sceneId}_{current_sceneId}')
                    print(f'{ref_along_angle}, {cur_along_angle}\n{ref_across_angle}, {cur_across_angle}\n\n')

                    build_feature_collection['features'].append(build_ref_feature)
                    build_feature_collection['features'].append(build_cur_feature)

                    write_geojson_output(build_feature_collection, f'{reference_sceneId}_pair_{current_sceneId}')

                else:
                    print(f'Not valid option')
                    print(f'{ref_along_angle}, {cur_along_angle}\n{ref_across_angle}, {cur_across_angle}\n\n')
        
            else:
                print('Failed overlap validation')

        print(f'Files writting out folder {output_dir_name}')


        return build_feature_collection, stereo_list
    
    else:
        print('WARNING - -- - There not enough catalog search results for false stereo matching :(\n Better luck next time')


# %% ================================== Auth

up42.authenticate('./input/config.json')
catalog = up42.initialize_catalog()


# %% ================================== AOI

aoi_file = Path.cwd()/'input/Dhusamareb.geojson'
aoi_geom = up42.read_vector_file(aoi_file)


# %% ================================== Catalog search 

search_collection = 'phr'

search_params = catalog.construct_search_parameters(geometry=aoi_geom,
                                                    start_date='2022-01-01',
                                                    end_date='2023-01-31',
                                                    max_cloudcover=50,
                                                    limit=50,
                                                    collections=[search_collection])

search_results = catalog.search(search_params, as_dataframe=False)



# %% ================================== Run 

false_stereo_validation(search_results)


# %%
