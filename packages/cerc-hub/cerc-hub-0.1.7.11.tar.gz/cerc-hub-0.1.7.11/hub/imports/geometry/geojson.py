"""
Geojson module parses geojson files and import the geometry into the city model structure
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Guillermo Gutierrez Guillermo.GutierrezMorote@concordia.ca
"""

import json

import numpy as np

from pyproj import Transformer

import hub.helpers.constants as cte
from hub.helpers.geometry_helper import GeometryHelper
from hub.imports.geometry.helpers.geometry_helper import GeometryHelper as igh
from hub.city_model_structure.attributes.polygon import Polygon
from hub.city_model_structure.building import Building
from hub.city_model_structure.building_demand.surface import Surface
from hub.city_model_structure.city import City


class Geojson:
  """
  Geojson class
  """
  X = 0
  Y = 1

  def __init__(self,
               path,
               extrusion_height_field=None,
               year_of_construction_field=None,
               function_field=None,
               function_to_hub=None):
    # todo: destination epsg should change according actual the location
    self._transformer = Transformer.from_crs('epsg:4326', 'epsg:26911')
    self._min_x = cte.MAX_FLOAT
    self._min_y = cte.MAX_FLOAT
    self._max_x = cte.MIN_FLOAT
    self._max_y = cte.MIN_FLOAT
    self._max_z = 0
    self._city = None
    self._extrusion_height_field = extrusion_height_field
    self._year_of_construction_field = year_of_construction_field
    self._function_field = function_field
    self._function_to_hub = function_to_hub
    with open(path) as json_file:
      self._geojson = json.loads(json_file.read())

  def _save_bounds(self, x, y):
    if x > self._max_x:
      self._max_x = x
    if x < self._min_x:
      self._min_x = x
    if y > self._max_y:
      self._max_y = y
    if y < self._min_y:
      self._min_y = y

  @staticmethod
  def _create_buildings_lod0(name, year_of_construction, function, surfaces_coordinates):
    surfaces = []
    buildings = []
    for zone, surface_coordinates in enumerate(surfaces_coordinates):
      points = igh.points_from_string(igh.remove_last_point_from_string(surface_coordinates))
      # geojson provides the roofs, need to be transform into grounds
      points = igh.invert_points(points)
      polygon = Polygon(points)
      polygon.area = igh.ground_area(points)
      surface = Surface(polygon, polygon)
      surfaces.append(surface)
      buildings.append(Building(f'{name}_zone_{zone}', surfaces, year_of_construction, function))
    return buildings

  @staticmethod
  def _create_buildings_lod1(name, year_of_construction, function, height, surface_coordinates):
    lod0_buildings = Geojson._create_buildings_lod0(name, year_of_construction, function, surface_coordinates)
    surfaces = []
    buildings = []

    for zone, lod0_building in enumerate(lod0_buildings):
      for surface in lod0_building.grounds:

        volume = surface.solid_polygon.area * height
        surfaces.append(surface)
        roof_coordinates = []
        # adding a roof means invert the polygon coordinates and change the Z value
        for coordinate in surface.solid_polygon.coordinates:
          roof_coordinate = np.array([coordinate[0], coordinate[1], height])
          # insert the roof rotated already
          roof_coordinates.insert(0, roof_coordinate)
        polygon = Polygon(roof_coordinates)
        polygon.area = surface.solid_polygon.area
        roof = Surface(polygon, polygon)
        surfaces.append(roof)
        # adding a wall means add the point coordinates and the next point coordinates with Z's height and 0
        coordinates_length = len(roof.solid_polygon.coordinates)
        for i, coordinate in enumerate(roof.solid_polygon.coordinates):
          j = i + 1
          if j == coordinates_length:
            j = 0
          next_coordinate = roof.solid_polygon.coordinates[j]
          wall_coordinates = [
            np.array([coordinate[0], coordinate[1], 0.0]),
            np.array([next_coordinate[0], next_coordinate[1], 0.0]),
            np.array([next_coordinate[0], next_coordinate[1], next_coordinate[2]]),
            np.array([coordinate[0], coordinate[1], coordinate[2]])
          ]
          polygon = Polygon(wall_coordinates)
          wall = Surface(polygon, polygon)
          surfaces.append(wall)

        building = Building(f'{name}_zone_{zone}', surfaces, year_of_construction, function)
        building.volume = volume
        buildings.append(building)

    return buildings

  def _get_polygons(self, polygons, coordinates):
    if type(coordinates[0][self.X]) != float:
      polygons = []
      for element in coordinates:
        polygons = self._get_polygons(polygons, element)
      return polygons
    else:
      transformed_coordinates = ''
      for coordinate in coordinates:
        transformed = self._transformer.transform(coordinate[self.Y], coordinate[self.X])
        self._save_bounds(transformed[self.X], transformed[self.Y])
        transformed_coordinates = f'{transformed_coordinates} {transformed[self.X]} {transformed[self.Y]} 0.0'
      polygons.append(transformed_coordinates.lstrip(' '))
      return polygons

  @staticmethod
  def _find_wall(line_1, line_2):
    for i in range(0, 2):
      j = 1 - i
      point_1 = line_1[i]
      point_2 = line_2[j]
      distance = GeometryHelper.distance_between_points(point_1, point_2)
      if distance > 1e-2:
        return False
    return True

  def _store_shared_percentage_to_walls(self, city, city_mapped):
    for building in city.buildings:
      if building.name not in city_mapped.keys():
        for wall in building.walls:
          wall.percentage_shared = 0
        continue
      building_mapped = city_mapped[building.name]
      for wall in building.walls:
        percentage = 0
        ground_line = []
        for point in wall.perimeter_polygon.coordinates:
          if point[2] < 0.5:
            ground_line.append(point)
        for entry in building_mapped:
          if building_mapped[entry]['shared_points'] <= 3:
            continue
          line = [building_mapped[entry]['line_start'], building_mapped[entry]['line_end']]
          neighbour_line = [building_mapped[entry]['neighbour_line_start'],
                            building_mapped[entry]['neighbour_line_end']]
          neighbour_height = city.city_object(building_mapped[entry]['neighbour_name']).max_height
          if self._find_wall(line, ground_line):
            line_shared = (GeometryHelper.distance_between_points(line[0], line[1]) +
                           GeometryHelper.distance_between_points(neighbour_line[0], neighbour_line[1]) -
                           GeometryHelper.distance_between_points(line[1], neighbour_line[0]) -
                           GeometryHelper.distance_between_points(line[0], neighbour_line[1])) / 2
            percentage_ground = line_shared / GeometryHelper.distance_between_points(line[0], line[1])
            percentage_height = neighbour_height / building.max_height
            if percentage_height > 1:
              percentage_height = 1
            percentage += percentage_ground * percentage_height
        wall.percentage_shared = percentage

  @property
  def city(self) -> City:
    """
    Get city out of a Geojson file
    """
    if self._city is None:
      missing_functions = []
      buildings = []
      building_id = 0
      lod = 1
      for feature in self._geojson['features']:
        extrusion_height = 0
        if self._extrusion_height_field is not None:
          extrusion_height = float(feature['properties'][self._extrusion_height_field])
        year_of_construction = None
        if self._year_of_construction_field is not None:
          year_of_construction = int(feature['properties'][self._year_of_construction_field])
        function = None
        if self._function_field is not None:
          function = feature['properties'][self._function_field]
          if self._function_to_hub is not None:
            # use the transformation dictionary to retrieve the proper function
            if function in self._function_to_hub:
              function = self._function_to_hub[function]
            else:
              if function not in missing_functions:
                missing_functions.append(function)
              function = function
        geometry = feature['geometry']
        if 'id' in feature:
          building_name = feature['id']
        else:
          building_name = f'building_{building_id}'
          building_id += 1
        polygons = []
        for part, coordinates in enumerate(geometry['coordinates']):
          polygons = self._get_polygons(polygons, coordinates)
          for zone, polygon in enumerate(polygons):
            if extrusion_height == 0:
              buildings = buildings + Geojson._create_buildings_lod0(f'{building_name}_part_{part}',
                                                                     year_of_construction,
                                                                     function,
                                                                     [polygon])
              lod = 0
            else:
              if self._max_z < extrusion_height:
                self._max_z = extrusion_height
              buildings = buildings + Geojson._create_buildings_lod1(f'{building_name}_part_{part}',
                                                                     year_of_construction,
                                                                     function,
                                                                     extrusion_height,
                                                                     [polygon])

      self._city = City([self._min_x, self._min_y, 0.0], [self._max_x, self._max_y, self._max_z], 'epsg:26911')
      for building in buildings:
        self._city.add_city_object(building)
      self._city.level_of_detail.geometry = lod
      if lod == 1:
        lines_information = GeometryHelper.city_mapping(self._city, plot=False)
        self._store_shared_percentage_to_walls(self._city, lines_information)
      if len(missing_functions) > 0:
        print(f'There are unknown functions {missing_functions}')
    return self._city
