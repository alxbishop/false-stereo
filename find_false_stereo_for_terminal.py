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


def write_geojson_output(output_feature_collection:dict, output_name:str, output_dir_name:Path):

    try:
        Path.mkdir(output_dir_name)
        print(f'Output folder created at {output_dir_name}')
    except:
        print(f'Folder already there {output_dir_name}')
        pass

    with open(f'{output_dir_name}/{output_name}.geojson', 'w') as tav:
        geojson.dump(output_feature_collection, tav)

    print(f'Files writting out folder {output_dir_name}')
    

def false_stereo_validation(search_results:dict, output_dir_name:Path):

    if len(search_results['features']) > 1:
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

                    print(f'-- VALID OPTION on ax  -- {reference_sceneId} and {current_sceneId} acquiered on different orbits')
                    stereo_list.append(f'{reference_sceneId}_{current_sceneId}')
                    print(f'{ref_along_angle}, {cur_along_angle}\n{ref_across_angle}, {cur_across_angle}\n')

                    build_feature_collection['features'].append(build_ref_feature)
                    build_feature_collection['features'].append(build_cur_feature)

                    write_geojson_output(build_feature_collection, f'{reference_sceneId}_pair_{current_sceneId}', output_dir_name)


                elif ref_across_angle < 0 and cur_across_angle > 0:

                    print(f'-- VALID OPTION on ax  -- {reference_sceneId} and {current_sceneId} acquiered on different orbits')
                    stereo_list.append(f'{reference_sceneId}_{current_sceneId}')
                    print(f'{ref_along_angle}, {cur_along_angle}\n{ref_across_angle}, {cur_across_angle}\n')

                    build_feature_collection['features'].append(build_ref_feature)
                    build_feature_collection['features'].append(build_cur_feature)

                    write_geojson_output(build_feature_collection, f'{reference_sceneId}_pair_{current_sceneId}', output_dir_name)

                elif ref_along_angle > 0 and cur_along_angle < 0:
                    print(f'-- VALID OPTION on al -- {reference_sceneId} and {current_sceneId} acquiered on opposite along track angles')
                    stereo_list.append(f'{reference_sceneId}_{current_sceneId}')
                    print(f'{ref_along_angle}, {cur_along_angle}\n{ref_across_angle}, {cur_across_angle}\n')

                    build_feature_collection['features'].append(build_ref_feature)
                    build_feature_collection['features'].append(build_cur_feature)

                    write_geojson_output(build_feature_collection, f'{reference_sceneId}_pair_{current_sceneId}', output_dir_name)

                elif ref_along_angle < 0 and cur_along_angle > 0:
                    print(f'-- VALID OPTION on al -- {reference_sceneId} and {current_sceneId} acquiered opposite along track angles')
                    stereo_list.append(f'{reference_sceneId}_{current_sceneId}')
                    print(f'{ref_along_angle}, {cur_along_angle}\n{ref_across_angle}, {cur_across_angle}\n')

                    build_feature_collection['features'].append(build_ref_feature)
                    build_feature_collection['features'].append(build_cur_feature)

                    write_geojson_output(build_feature_collection, f'{reference_sceneId}_pair_{current_sceneId}', output_dir_name)

                else:
                    print(f'Failed across track and along track validation\n')
                    # print(f'{ref_along_angle}, {cur_along_angle}\n{ref_across_angle}, {cur_across_angle}\n\n')
        
            else:
                print('Failed overlap validation\n')

        return build_feature_collection, stereo_list
    
    else:
        print('WARNING - -- - There not enough catalog search results for false stereo matching :(\n Better luck next time')


# %% ================================== Auth

def main(search_collection:str, startDate:str, endDate:str, cloudCover:int, aoi_file_name:str, limit:int):

    """
    :param collection: Run the tool on one collection at a time, 'pneo', 'phr', 'triplesat' ...
    :param startDate: 'year-month-day' '2022-01-01'
    :param endDate: 'year-month-day' '2022-01-01'
    :param cloudCover: 10
    :param aoi_file_name: This file must be located in the input for folder, only provide the name, 'name_of_file.geojson'
    :param limit: for 0 to 5000
    """

    up42.authenticate('./input/config.json')
    catalog = up42.initialize_catalog()


    aoi_file = Path.cwd()/f'input/{aoi_file_name}'
    # aoi_geom = up42.read_vector_file(aoi_file)

    # output_dir_name = Path.cwd()/f'./output/{aoi_file.stem}_{search_collection}'


    with open(aoi_file, 'r') as topo:
        data = geojson.load(topo)

    for feature in data['features']:
        aoi_id = feature['properties']['id']
        aoi_geom = feature['geometry']
        print(aoi_id)

        search_params = catalog.construct_search_parameters(geometry=aoi_geom,
                                                            start_date=f'{startDate}',
                                                            end_date=f'{endDate}',
                                                            max_cloudcover=cloudCover,
                                                            limit=limit,
                                                            collections=[f'{search_collection}'])

        search_results = catalog.search(search_params, as_dataframe=False)

        output_dir_name = Path.cwd()/f'./output/{aoi_file.stem}_{aoi_id}_{search_collection}'

        false_stereo_validation(search_results, output_dir_name)


if __name__ == "__main__":
    print("""This program has been designed to find false stereo catalog scenes for airbus products. 
You can use this tool on phr, pneo and spot.    
 - -  ONLY one sensor at a time !!! - -
 - - Please enter search parameters as prompted""")
    collection = input('.......Enter collection:')
    startDate = input('.......Enter startDate:')
    endDate = input('.......Enter endDate:')
    cloudCover = input('.......Enter cloudCover:')
    limit = int(input('.......Enter limit:'))

    print('These are the avaiable AOI files from the input folder:')
    for file in (Path.cwd()/'input/').iterdir():
        if file.suffix == '.geojson':
            print(f'   - {file.name}')

    aoi_geom = input('Enter aoi_geom from above list:')

    main(collection,startDate,endDate,cloudCover,aoi_geom,limit)

# %%
