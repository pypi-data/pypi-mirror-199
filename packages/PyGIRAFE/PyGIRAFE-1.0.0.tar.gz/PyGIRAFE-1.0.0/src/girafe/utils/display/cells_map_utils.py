import numpy as np
import scipy.ndimage as ndimage
import matplotlib.pyplot as plt
from matplotlib import patches
import matplotlib
from shapely import geometry
import PIL
from PIL import ImageDraw
import math
import scipy.stats as stats
# from matplotlib.colors import NoNorm
import matplotlib.cm as cm
import networkx as nx
from girafe.utils.graphs.utils_graphs import welsh_powell
from girafe.utils.display.colors import BREWER_COLORS
import matplotlib.colors as plt_colors
from shapely.geometry import MultiPoint, LineString, Point
import cv2
import hdf5storage
from read_roi import read_roi_file, read_roi_zip
from PIL import Image, ImageEnhance


class CellsCoord:

    def __init__(self, coords=None, pixel_masks=None, nb_lines=None, nb_col=None,
                 from_matlab=False, invert_xy_coord=False): # from_suite_2p=False, from_fiji=False
        """

        Args:
            coords: list of array of 2 lines (x & y) and n columns, n being the number of coordinate to set the contour of
            the cell. if None, then pixel_masks must be not None
            pixel_masks: a list of list of tuples of int representing the coordinates of the pixels in a given cell.
                len(pixel_masks) == number of cells.
            nb_lines: If None, set it using the max coordinate in coords
            nb_col:If None, set it using the max coordinate in coords
            from_matlab: Means coordinates have been computed on matlab and indexing starts at 1 so
            invert_xy_coord: if True, invert the xy coords
        """

        if coords is None and pixel_masks is None:
            raise Exception("Coord or pixel_masks must be given to instanciate CellsCoord")

        # dict of tuples, key is the cell #, cell center coords x and y (x and y are inverted for imshow)
        self.center_coord = dict()
        self.cv2_contours = None
        # shapely polygons
        self.cells_polygon = dict()
        # first key is an int representing the number of the cell, and value is a list of cells it interesects
        self.intersect_cells = dict()
        # for garbage collector issue only
        self.cell_contour = None
        self.invert_xy_coord = invert_xy_coord
        self.from_matlab = from_matlab

        # contour coords
        self.coords = coords

        # ---------------------------
        # we clean coords if not None
        # ---------------------------
        if self.coords is not None:
            for cell, coord in enumerate(self.coords):
                if from_matlab:
                    # it is necessary to remove one, as data comes from matlab, starting from 1 and not 0
                    coord = coord - 1
                # in case it would be floats
                coord.astype(int, copy=False)
                if invert_xy_coord:
                    # invert xy lines
                    coord = np.flipud(coord)
                self.coords[cell] = coord

        self.pixel_masks = pixel_masks
        self.original_pixel_masks = pixel_masks

        # ---------------------------
        # we clean pixel_masks if not None
        # we change the structure of so each element
        # is an np.array of 2d with 2 lines and n columns
        # n being the number of pixels
        # ---------------------------
        if self.pixel_masks is not None:
            tmp_pixel_masks = self.pixel_masks
            self.pixel_masks = []
            to_substract = 0
            if from_matlab:
                to_substract = 1
            for pixel_mask in tmp_pixel_masks:
                pix_array = np.zeros((2, len(pixel_mask)), dtype="int16")
                for index_pix, pix in enumerate(pixel_mask):
                    if invert_xy_coord:
                        pix_array[0, index_pix] = int(pix[1] - to_substract)
                        pix_array[1, index_pix] = int(pix[0] - to_substract)
                    else:
                        pix_array[0, index_pix] = int(pix[0] - to_substract)
                        pix_array[1, index_pix] = int(pix[1] - to_substract)
                self.pixel_masks.append(pix_array)

        # --------------------------------------------
        # Number of lines and columsn (height & width)
        # of the Field Of View (FOV)
        # --------------------------------------------
        if (nb_lines is None) or (nb_col is None):
            # in that case we take the maximum coordinates to fix the size of the FOV adding some padding
            self.nb_lines = 0
            self.nb_col = 0
            padding = 2

            if self.coords is not None:
                for cell, coord in enumerate(self.coords):
                    self.nb_col = max(self.nb_col, np.max(coord[1, :]) + padding)
                    self.nb_lines = max(self.nb_lines, np.max(coord[0, :]) + padding)
            else:
                for pixel_mask in self.pixel_masks:
                    # raise Exception("TOTO")
                    self.nb_col = max(self.nb_col, np.max(pixel_mask[1, :]) + padding)
                    self.nb_lines = max(self.nb_lines, np.max(pixel_mask[0, :]) + padding)
        else:
            self.nb_lines = nb_lines
            self.nb_col = nb_col

        if self.coords is not None:
            self.n_cells = len(self.coords)
        else:
            self.n_cells = len(self.pixel_masks)

        # -----------------------------------------------------------
        # Using pixels_masks to build contour coords if doesn't exist
        # -----------------------------------------------------------
        if self.pixel_masks is not None:
            if self.coords is None:
                # first we build self.coords from self.pixel_masks
                self.coords = []
                for cell, pixel_mask in enumerate(self.pixel_masks):
                    # we use pixel_masks to build the coords, using convex_hull
                    use_convex_hull_method = True
                    if use_convex_hull_method:
                        list_points_coord = list(zip(pixel_mask[1], pixel_mask[0]))
                        convex_hull = MultiPoint(list_points_coord).convex_hull
                        if isinstance(convex_hull, LineString):
                            coord_shapely = MultiPoint(list_points_coord).convex_hull.coords
                        elif isinstance(convex_hull, Point):
                            coord_shapely = MultiPoint(list_points_coord).convex_hull.coords
                        else:
                            coord_shapely = MultiPoint(list_points_coord).convex_hull.exterior.coords
                        self.coords.append(np.array(coord_shapely).transpose())
                    else:
                        # other method
                        binary_img = np.zeros(( self.nb_lines, self.nb_col), dtype="uint8")
                        for x, y in zip(pixel_mask[0], pixel_mask[1]):
                            binary_img[x, y] = 1
                        contours, _ = cv2.findContours(binary_img, mode=cv2.RETR_EXTERNAL,
                                                       method=cv2.CHAIN_APPROX_SIMPLE)
                        # contours, _ = cv2.findContours(binary_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                        if len(contours) == 0:
                             raise Exception(f"CAREFUL: No contour for cell {cell} in cells_map_utils")

                        biggest_contour = contours[0]
                        biggest_area = cv2.contourArea(contours[0])
                        if len(contours) > 1:
                            for contour in contours[1:]:
                                area = cv2.contourArea(contour)
                                if area > biggest_area:
                                    biggest_area = area
                                    biggest_contour = contour

                        contour = biggest_contour
                        area = cv2.contourArea(contour)
                        print(f"Area {area}")
                        if area < 10:
                            continue
                        # the bigger espilon, the less detailed contour
                        epsilon = 0.04 * cv2.arcLength(contour, True)
                        contour = cv2.approxPolyDP(contour, epsilon, True)
                        # xy = []
                        coord = np.zeros((2, len(contour)))
                        for c_index, c in enumerate(contour):
                            # xy.append([c[0][0] + 0.5, c[0][1] + 0.5])
                            # xy.append([c[0][0], c[0][1]])
                            coord[0, c_index] = c[0][0]
                            coord[1, c_index] = c[0][1]
                        self.coords.append(coord)

        # ----------------------------------------------------------------------
        # Going through contour coords and building polygons and centers of mass
        # ----------------------------------------------------------------------
        self._build_polygons_and_center_of_mass()

        # --------------------------------------------------------------
        # building the intersections dictionnary using coords
        # --------------------------------------------------------------
        self._build_interesect_dict()

        # TODO: build contours using cv2 method, not only using cv2 format
        self._build_cv2_contours()

    def _build_polygons_and_center_of_mass(self):
        """
        Going through contour coords and building polygons and centers of mass
        Returns:

        """
        for cell, coord in enumerate(self.coords):
            if coord.shape[0] == 0:
                print(f'Error: {cell} coord.shape {coord.shape}')
                continue

            self.build_cell_polygon_from_contour(cell=cell)

            # poly = MultiPoint(list_points).convex_hull

            use_centroid = True

            if use_centroid:
                self.center_coord[cell] = self.cells_polygon[cell].centroid.coords[0]
            else:
                bw = np.zeros((self.nb_lines, self.nb_col), dtype="int8")
                # we could use morphology.binary_fill_holes to build pixel_mask from coord
                # but let's keep pixel_mask to None if not passed as argument
                # morphology.binary_fill_holes(input
                bw[coord[0, :], coord[1, :]] = 1
                c_x, c_y = ndimage.center_of_mass(bw)
                self.center_coord[cell] = (c_x, c_y)

            # if (cell == 0) or (cell == 159):
            #     print(f"cell {cell} fig")
            #     fig, ax = plt.subplots(nrows=1, ncols=1,
            #                            gridspec_kw={'height_ratios': [1]},
            #                            figsize=(5, 5))
            #     ax.imshow(bw)
            #     plt.show()
            #     plt.close()

    def _build_interesect_dict(self):
        """
        building the intersections dictionnary using coords
        Returns:

        """
        # reseting it
        self.intersect_cells = dict()
        for cell_1 in np.arange(self.n_cells - 1):
            if cell_1 not in self.intersect_cells:
                if cell_1 not in self.cells_polygon:
                    continue
                self.intersect_cells[cell_1] = set()
            for cell_2 in np.arange(cell_1 + 1, self.n_cells):
                if cell_2 not in self.cells_polygon:
                    continue
                if cell_2 not in self.intersect_cells:
                    self.intersect_cells[cell_2] = set()
                poly_1 = self.cells_polygon[cell_1]
                poly_2 = self.cells_polygon[cell_2]
                # if it intersects and not only touches if adding and (not poly_1.touches(poly_2))
                # try:
                if poly_1.intersects(poly_2):
                    self.intersect_cells[cell_2].add(cell_1)
                    self.intersect_cells[cell_1].add(cell_2)
                # except shapely.errors.TopologicalError:
                #     print(f"cell_1 {cell_1}, cell_2 {cell_2}")
                #     print(f"cell_1 {poly_1.is_valid}, cell_2 {poly_2.is_valid}")
                #     poly_1 = poly_1.buffer(0)
                #     poly_2 = poly_2.buffer(0)
                #     print(f"cell_1 {poly_1.is_valid}, cell_2 {poly_2.is_valid}")
                #     raise Exception("shapely.errors.TopologicalError")

    def save_coords(self, file_name):
        """
        Save the coords in the file_name given. Is pixel_masks info is available, coord
        will be save in Suite2p format, other as list of 2array (list of 2*n_points_in_contours)
        Args:
            file_name: npy extension will be added

        Returns:

        """
        # print(f"self.original_pixel_masks {self.original_pixel_masks}")
        # suite2p format by default if possible
        if self.original_pixel_masks is not None:
            stat = [{'ypix': np.array([int(pix[0]) for pix in pixels]),
                     'xpix': np.array([int(pix[1]) for pix in pixels])} for pixels in self.original_pixel_masks]
            file_name = file_name + "_suite2p.npy"
            np.save(file_name, stat, allow_pickle=True)
        else:
            file_name = file_name + "_caiman.npy"
            # TODO: to test
            np.save(file_name, self.coords, allow_pickle=True)

    def remove_cells(self, cells_to_remove):
        """
        Remove cells, identified by their indices.
        Return a new CellsCoord instance
        Args:
            cells_to_remove: list of integers

        Returns: CellsCoord instance

        """
        if self.original_pixel_masks is not None:
            list_to_change = self.original_pixel_masks
        else:
            list_to_change = self.coords

        new_data = []
        for cell_index, data_cell in enumerate(list_to_change):
            if cell_index not in cells_to_remove:
                new_data.append(data_cell)

        # if invert_xy_coord
        if self.original_pixel_masks is not None:
            return CellsCoord(pixel_masks=new_data, from_matlab=self.from_matlab,
                              invert_xy_coord=False)
        else:
            # from_matlab and invert_xy_coord are False because the coords has already been transformed
            #
            return CellsCoord(coords=new_data, from_matlab=False, invert_xy_coord=self.invert_xy_coord)

    def replace_cells(self, cells_to_replace, cells_to_replace_by, cells_coord):
        """
            Extract cells from a CellsCoord instance to replace cells in this one
            Args:
                cells_to_replace: list of int, representing the indices of the cells in self
                cells_to_replace_by: list of int, represents the cell index in cells_coord
                cells_coord: instance of CellsCoord, from where to extract the cells

            Returns: Online modification, the self instance is modified

        """

        for index, cell_to_replace in enumerate(cells_to_replace):
            cell_to_replace_by = cells_to_replace_by[index]
            contours = cells_coord.coords[cell_to_replace_by]
            if cells_coord.pixel_masks is not None:
                pixel_mask = cells_coord.pixel_masks[cell_to_replace_by]
                original_pixel_mask = cells_coord.original_pixel_masks[cell_to_replace_by]
            else:
                # we build pixel_mask, using shapely polygon
                # solution from https://stackoverflow.com/questions/50847827/how-can-i-select-the-pixels-that-fall-within-a-contour-in-an-image-represented-b
                # there might be some more efficient way to do it, including with opencv
                polygon = cells_coord.cells_polygon[cell_to_replace_by]
                minx, miny, maxx, maxy = polygon.bounds
                minx, miny, maxx, maxy = int(minx), int(miny), int(maxx), int(maxy)
                box_patch = [[x, y] for x in range(minx, maxx + 1) for y in range(miny, maxy + 1)]
                pixels = []
                for pb in box_patch:
                    pt = Point(pb[0], pb[1])
                    if polygon.contains(pt):
                        # we need to revert
                        pixels.append([int(pb[1]), int(pb[0])])

                # other solution:
                # img_mask = cells_coord.get_cell_mask(cell=cell_to_replace_by,
                #                                      dimensions=(cells_coord.nb_lines, cells_coord.nb_col))
                # where_pixels = np.where(img_mask)
                # pixels = [(p[0], p[1]) for p in zip(where_pixels[0], where_pixels[1])]

                # list of tuple of int
                original_pixel_mask = pixels
                pix_array = np.zeros((2, len(pixels)), dtype="int16")
                for index_pix, pix in enumerate(pixels):
                    pix_array[0, index_pix] = pix[0]
                    pix_array[1, index_pix] = pix[1]
                pixel_mask = pix_array

            self.coords[cell_to_replace] = contours
            if pixel_mask is not None and self.pixel_masks is not None:
                self.pixel_masks[cell_to_replace] = pixel_mask
                self.original_pixel_masks[cell_to_replace] = original_pixel_mask

        self._build_polygons_and_center_of_mass()
        self._build_interesect_dict()
        self._build_cv2_contours()

    def add_cells(self, cells_to_add, cells_coord):
        """
        Extract cells from a CellsCoord instance to add them in this one at the end of list
        Args:
            cells_to_add: list of int, representing the indices of the cells in cells_coord
            cells_coord: instance of CellsCoord, from where to extract the cells and insert them in self

        Returns: Online modification, the self instance is modified. Return the indices of the cells added
        in the map.

        """
        added_cells_index = []
        for cell_to_add in cells_to_add:
            contours = cells_coord.coords[cell_to_add]
            pixel_mask = None
            if cells_coord.pixel_masks is not None:
                pixel_mask = cells_coord.pixel_masks[cell_to_add]
                original_pixel_mask = cells_coord.original_pixel_masks[cell_to_add]
            else:
                # we build pixel_mask, using shapely polygon
                # solution from https://stackoverflow.com/questions/50847827/how-can-i-select-the-pixels-that-fall-within-a-contour-in-an-image-represented-b
                # there might be some more efficient way to do it, including with opencv
                polygon = cells_coord.cells_polygon[cell_to_add]
                minx, miny, maxx, maxy = polygon.bounds
                minx, miny, maxx, maxy = int(minx), int(miny), int(maxx), int(maxy)
                box_patch = [[x, y] for x in range(minx, maxx + 1) for y in range(miny, maxy + 1)]
                pixels = []
                for pb in box_patch:
                    pt = Point(pb[0], pb[1])
                    if polygon.contains(pt):
                        # we need to revert
                        pixels.append([int(pb[1]), int(pb[0])])

                # other solution:
                # img_mask = cells_coord.get_cell_mask(cell=cell_to_add,
                #                                      dimensions=(cells_coord.nb_lines, cells_coord.nb_col))
                # where_pixels = np.where(img_mask)
                # pixels = [(p[0], p[1]) for p in zip(where_pixels[0], where_pixels[1])]

                # list of tuple of int
                original_pixel_mask = pixels
                pix_array = np.zeros((2, len(pixels)), dtype="int16")
                for index_pix, pix in enumerate(pixels):
                    pix_array[0, index_pix] = pix[0]
                    pix_array[1, index_pix] = pix[1]
                pixel_mask = pix_array

            added_cells_index.append(len(self.coords))
            self.coords.append(contours)
            if pixel_mask is not None and self.pixel_masks is not None:
                self.pixel_masks.append(pixel_mask)
                self.original_pixel_masks.append(original_pixel_mask)

        self.n_cells = len(self.coords)
        self._build_polygons_and_center_of_mass()
        self._build_interesect_dict()
        self._build_cv2_contours()

        return added_cells_index

    def _build_cv2_contours(self):
        """
        Change coords to cv2 format
        Returns:

        """
        self.cv2_contours = []
        # list of array, each array has a shape of n_points*1*2
        for coord in self.coords:
            coord = coord.transpose()
            # print(f"coord.shape {coord.shape}")
            # print(f"coord {coord}")
            cv2_array = np.zeros((len(coord), 1, 2), dtype="int32")
            for coord_index, coord_xy in enumerate(coord):
                cv2_array[coord_index, 0, 0] = int(coord_xy[1])
                cv2_array[coord_index, 0, 1] = int(coord_xy[0])
            self.cv2_contours.append(cv2_array)

    @property
    def coord(self):
        """
        Return the coords. The coords attribute used to be call coord, so we make a property
        Returns:

        """
        return self.coords

    def build_raw_traces_from_movie(self, movie, without_overlap=False, buffer_overlap=1):
        """
        Return a 2d array representing the fluoresence signal raw trace for each cell
        Args:
            movie: 3d array n_frames x len_y x len_x
            without_overlap: (bool) if True, means the trace will be build only from the pixels from this cell
            buffer_overlap: indicate from how much pixels increasing the size of overlaping cell

        Returns: A 2d array (n_cells * n_frames) of float

        """
        buffer_overlap = max(0, buffer_overlap)
        raw_traces = np.zeros((self.n_cells, movie.shape[0]))
        for cell in np.arange(self.n_cells):
            tmp_buffer_overlap = buffer_overlap
            while True:
                mask = self.get_cell_mask(cell=cell,
                                          dimensions=(movie.shape[1], movie.shape[2]),
                                          without_overlap=without_overlap,
                                          buffer_overlap=tmp_buffer_overlap)
                n_pixels_in_cell = np.sum(mask)
                if (n_pixels_in_cell > 2) or tmp_buffer_overlap == 0:
                    break
                tmp_buffer_overlap -= 1

            # print(f"n_pixels_in_cell for cell {cell}: {n_pixels_in_cell}")
            if n_pixels_in_cell > 0:
                raw_traces[cell, :] = np.mean(movie[:, mask], axis=1)
        return raw_traces

    def build_cell_polygon_from_contour(self, cell):
        """
        Build the (shapely) polygon representing a given cell using its contour's coordinates.
        Args:
            cell:

        Returns:

        """
        coord = self.coords[cell]
        # make a list of tuple representing x, y coordinates of the contours points
        coord_list_tuple = list(zip(coord[0], coord[1]))

        # buffer(0) or convex_hull could be used if the coords are a list of points not
        # in the right order. However buffer(0) return a MultiPolygon with no coords available.
        if len(coord_list_tuple) < 3:
            list_points = []
            for coords in coord_list_tuple:
                list_points.append(geometry.Point(coords))
            if len(coord_list_tuple) == 1:
                self.cells_polygon[cell] = geometry.Point(coord_list_tuple[0])
            else:
                self.cells_polygon[cell] = geometry.LineString(list_points)
        else:
            self.cells_polygon[cell] = geometry.Polygon(coord_list_tuple) # .convex_hull # buffer(0)

        # self.coords[cell] = np.array(self.cells_polygon[cell].exterior.coords).transpose()

    def get_cell_mask(self, cell, dimensions, without_overlap=False, buffer_overlap=1):
        """
        Return the mask of the pixels of the cell
        :param cell:
        :param dimensions: height x width
        :param without_overlap: if True, means with return only the pixel belonging to this cell
            buffer_overlap: indicate from how much pixels increasing the size of overlaping cell
        :return: binary 2d array (movie dimension), with 1 for the pixels belonging to the cell
        """
        poly_gon = self.cells_polygon[cell]
        img = PIL.Image.new('1', (dimensions[1], dimensions[0]), 0)
        if (self.pixel_masks is not None) and (not without_overlap):
            img = np.array(img)
            pix_array = self.pixel_masks[cell]
            for index in np.arange(pix_array.shape[1]):
                img[pix_array[0, index], pix_array[1, index]] = 1
            # if without_overlap and (cell in self.intersect_cells) and (len(self.intersect_cells[cell]) > 0) \
            #         and (pix_array.shape[1] > 1):
            #     for overlaping_cell in self.intersect_cells[cell]:
            #         overlaping_poly_gon = self.cells_polygon[overlaping_cell]
            #         # increasing the size of the cell of 1
            #         if buffer_overlap > 0:
            #             overlaping_poly_gon = overlaping_poly_gon.buffer(buffer_overlap)
            #         if isinstance(poly_gon, geometry.Point):
            #             pass
            #         elif isinstance(overlaping_poly_gon, geometry.LineString):
            #             ImageDraw.Draw(img).polygon(list(overlaping_poly_gon.coords), outline=0,
            #                                         fill=0)
            #         else:
            #             ImageDraw.Draw(img).polygon(list(overlaping_poly_gon.exterior.coords), outline=0,
            #                                         fill=0)
                    # pix_array = self.pixel_masks[overlaping_cell]
                    # for index in np.arange(pix_array.shape[1]):
                    #     img[pix_array[1, index], pix_array[0, index]] = 0
        else:
            if isinstance(poly_gon, geometry.Point):
                img = np.array(img)
                img[poly_gon.x, poly_gon.y] = 1
            else:
                if isinstance(poly_gon, geometry.LineString):
                    ImageDraw.Draw(img).polygon(list(poly_gon.coords), outline=1,
                                                fill=1)
                else:
                    ImageDraw.Draw(img).polygon(list(poly_gon.exterior.coords), outline=1,
                                                fill=1)
                if without_overlap and (cell in self.intersect_cells) and (len(self.intersect_cells[cell]) > 0):
                    for overlaping_cell in self.intersect_cells[cell]:
                        overlaping_poly_gon = self.cells_polygon[overlaping_cell]
                        if buffer_overlap > 0:
                            overlaping_poly_gon = overlaping_poly_gon.buffer(buffer_overlap)
                        if isinstance(overlaping_poly_gon, geometry.LineString):
                            ImageDraw.Draw(img).polygon(list(overlaping_poly_gon.coords), outline=0,
                                                        fill=0)
                        else:
                            ImageDraw.Draw(img).polygon(list(overlaping_poly_gon.exterior.coords), outline=0,
                                                        fill=0)
        return np.array(img)

    def match_cells_indices(self, coord_obj, path_results, max_dist_bw_centroids=3, plot_result=True, plot_title_opt="",
                            take_the_biggest=False, min_cell_area=0):
        """

        Args:
            coord_obj: another instanc of coord_obj
            path_results:
            max_dist_bw_centroids:
            plot_result:
            plot_title_opt:
            take_the_biggest: if True, then we don't take the closest cell that match, but the biggest in the range
            (max_dist_bw_centroids)
            min_cell_area: if min_cell_area > 0, then we take the closest cell among
            the one with area > min_cell_area, if no cell are > min_cell_area, then we take the closest one

        Returns: a 1d array, each index corresponds to the index of a cell of coord_obj, and map it to an index to self
        or -1 if no cell match

        """
        # TODO: Add option so that if a cell is mostly overlap by a bigger one and no close centroid is found, then we
        #  match them
        other_to_self_mapping_array = np.ones(len(coord_obj.coord), dtype='int16')
        other_to_self_mapping_array *= -1
        cells_to_link = list(range(len(coord_obj.coord)))

        distances_dict = dict()
        for cell in np.arange(len(coord_obj.coord)):
            c_x, c_y = coord_obj.center_coord[cell]
            distances_array = np.zeros(len(self.coords))
            # areas = np.array([self.cells_polygon[cell_index].area for cell_index in range(len(self.coords))])
            for self_cell in np.arange(len(self.coords)):
                self_c_x, self_c_y = self.center_coord[self_cell]
                # then we calculate the cartesian distance to all other cells
                distances_array[self_cell] = math.sqrt((self_c_x - c_x) ** 2 + (self_c_y - c_y) ** 2)
            distances_dict[cell] = distances_array

        while len(cells_to_link) > 0:
        # for cell in np.arange(len(coord_obj.coord)):
            cell = cells_to_link[0]
            cells_to_link = cells_to_link[1:]
            c_x, c_y = coord_obj.center_coord[cell]
            if np.min(distances_dict[cell]) <= max_dist_bw_centroids:
                if min_cell_area > 0:
                    args_sort = np.argsort(distances_dict[cell])
                    arg_indices = np.where(distances_dict[cell][args_sort] <= max_dist_bw_centroids)[0]
                    areas_sorted = np.array([self.cells_polygon[args_sort[arg_index]].area
                                             for arg_index in arg_indices])
                    if len(np.where(areas_sorted > min_cell_area)[0]) == 0:
                        # means there is not cell in the are that is superior to the min cell_area
                        dont_match_in_that_case = True
                        if dont_match_in_that_case:
                            other_to_self_mapping_array[cell] = -1
                        else:
                            closest_cell = np.argmin(distances_dict[cell])
                            # then we take the closest
                            # first we make sure the cell that we want to match is not already matched
                            if closest_cell in other_to_self_mapping_array:
                                matched_cell = np.where(other_to_self_mapping_array == closest_cell)[0][0]
                                distance_matched = distances_dict[matched_cell][closest_cell]
                                if distance_matched < distances_dict[cell][closest_cell]:
                                    cells_to_link.append(cell)
                                    # then we modify the distance between the cell to make sure in the next iteration
                                    # it is not picked
                                    distances_dict[cell][closest_cell] = 10000
                                    continue
                                else:
                                    other_to_self_mapping_array[cell] = closest_cell
                                    cells_to_link.append(matched_cell)
                                    # then we modify the distance between the cell to make sure in the next iteration
                                    # it is not picked
                                    distances_dict[matched_cell][closest_cell] = 10000
                                    continue
                            else:
                                other_to_self_mapping_array[cell] = closest_cell
                        continue
                    """

                        close_cells_to_pick_from = args_sort[arg_indices[np.where(areas_sorted > min_cell_area)[0]]]
                        closest_cell = np.argmin(distances_dict[cell][close_cells_to_pick_from])
                        closest_cell = close_cells_to_pick_from[closest_cell]
                    """
                    closest_dist = -1
                    closest_one_index = 0
                    close_cells_to_pick_from = args_sort[arg_indices[np.where(areas_sorted > min_cell_area)[0]]]
                    for cell_index in close_cells_to_pick_from:
                        # if distances_dict[cell][cell_index] > max_dist_bw_centroids:
                        #     continue
                        distance = distances_dict[cell][cell_index]
                        if closest_dist == -1 or distance < closest_dist:
                            closest_dist = distance
                            closest_one_index = cell_index
                    # the_one = chosen cell
                    if closest_dist == -1:
                        # then we take the closest, should not arrive
                        the_one = np.argmin(distances_dict[cell])
                    else:
                        the_one = closest_one_index

                    # first we make sure the cell that we want to match is not already matched
                    if the_one in other_to_self_mapping_array:
                        matched_cell = np.where(other_to_self_mapping_array == the_one)[0][0]
                        distance_matched = distances_dict[matched_cell][the_one]
                        if distance_matched < distances_dict[cell][the_one]:
                            cells_to_link.append(cell)
                            # then we modify the distance between the cell to make sure in the next iteration
                            # it is not picked
                            distances_dict[cell][the_one] = 10000
                            continue
                        else:
                            other_to_self_mapping_array[cell] = the_one
                            cells_to_link.append(matched_cell)
                            # then we modify the distance between the cell to make sure in the next iteration
                            # it is not picked
                            distances_dict[matched_cell][the_one] = 10000
                            continue
                    else:
                        other_to_self_mapping_array[cell] = the_one
                        continue

                elif take_the_biggest:
                    args_sort = np.argsort(distances_dict[cell])
                    arg_indices = np.where(distances_dict[cell][args_sort] <= max_dist_bw_centroids)[0]
                    biggest_area = -1
                    biggest_one_index = 0
                    for arg_index in arg_indices:
                        cell_index = args_sort[arg_index]
                        # if distances_dict[cell][cell_index] > max_dist_bw_centroids:
                        #     continue
                        area = self.cells_polygon[cell_index].area
                        if area > biggest_area:
                            biggest_area = area
                            biggest_one_index = cell_index
                    if biggest_area == -1:
                        # then we take the closest
                        other_to_self_mapping_array[cell] = np.argmin(distances_dict[cell])
                    else:
                        other_to_self_mapping_array[cell] = biggest_one_index
                else:
                    other_to_self_mapping_array[cell] = np.argmin(distances_dict[cell])
            else:
                other_to_self_mapping_array[cell] = -1

        if plot_result:
            fig, ax = plt.subplots(nrows=1, ncols=1,
                                   gridspec_kw={'height_ratios': [1]},
                                   figsize=(20, 20), dpi=300)

            fig.patch.set_facecolor("black")
            ax.set_facecolor("black")

            # dark blue
            other_twin_color = list((0.003, 0.313, 0.678, 1.0))
            n_twins = 0
            # red
            other_orphan_color = list((1, 0, 0, 1.0))
            n_other_orphans = 0
            # light blue
            self_twin_color = list((0.560, 0.764, 1, 1.0))
            # green
            self_orphan_color = list((0.278, 1, 0.101, 1.0))
            n_self_orphans = 0
            with_edge = True
            edge_line_width = 1
            z_order_cells = 12
            z_order_links = 20
            links_line_width = 3
            # orange
            links_color = [0.99, 0.698, 0.298, 1.0]
            z_order_center = 15

            for cell in np.arange(len(self.coords)):
                xy = self.coords[cell].transpose()
                if with_edge:
                    line_width = edge_line_width
                    edge_color = "white"
                else:
                    edge_color = "white"
                    line_width = 0
                # allow to set alpha of the edge to 1
                if cell in other_to_self_mapping_array:
                    # light blue
                    face_color = self_twin_color
                else:
                    # green
                    face_color = self_orphan_color
                    n_self_orphans += 1
                face_color[3] = 0.8
                face_color = tuple(face_color)
                # drawing the cell
                cell_contour = patches.Polygon(xy=xy,
                                               fill=True, linewidth=line_width,
                                               facecolor=face_color,
                                               edgecolor=edge_color,
                                               zorder=z_order_cells)  # lw=2
                ax.add_patch(cell_contour)
                ax.scatter(x=self.center_coord[cell][0], y=self.center_coord[cell][1],
                           s=20, color="white", marker='o', linewidths=None,
                           edgecolors=None, zorder=z_order_center)
                with_cell_numbers = True
                if with_cell_numbers:
                    # c_x_c = self.center_coord[cell][0]
                    # c_y_c = self.center_coord[cell][1]
                    # ax.text(x=c_x_c, y=c_y_c,
                    #         s=f"{np.round(self.cells_polygon[cell].area, 1)}", color="black", zorder=22,
                    #         ha='center', va="center", fontsize=4, fontweight='bold')
                    self.plot_text_cell(cell=cell, cell_numbers_color="black", ax=ax, text_size=6,
                                        text=f"{cell}\n({int(np.round(self.cells_polygon[cell].area, 0))})")

            for cell in np.arange(len(coord_obj.coord)):
                xy = coord_obj.coord[cell].transpose()
                if with_edge:
                    line_width = edge_line_width
                    edge_color = "white"
                else:
                    edge_color = "white"
                    line_width = 0
                # allow to set alpha of the edge to 1
                if other_to_self_mapping_array[cell] >= 0:
                    # dark blue
                    face_color = other_twin_color
                    n_twins += 1
                else:
                    # red
                    face_color = other_orphan_color
                    n_other_orphans += 1
                face_color[3] = 0.8
                face_color = tuple(face_color)
                cell_contour = patches.Polygon(xy=xy,
                                                    fill=True, linewidth=line_width,
                                                    facecolor=face_color,
                                                    edgecolor=edge_color,
                                                    zorder=z_order_cells)  # lw=2
                ax.add_patch(cell_contour)
                ax.scatter(x=coord_obj.center_coord[cell][0], y=coord_obj.center_coord[cell][1],
                           s=20, color="white", marker='o', linewidths=None,
                           edgecolors=None, zorder=z_order_center)

                circle = plt.Circle((coord_obj.center_coord[cell][0], coord_obj.center_coord[cell][1]),
                                     max_dist_bw_centroids, color=face_color, fill=False, zorder=18)
                ax.add_artist(circle)
                # then we plot a line to link it to it mats if it exists
                if other_to_self_mapping_array[cell] >= 0:
                    c_x, c_y = self.center_coord[other_to_self_mapping_array[cell]]
                    c_x_c, c_y_c = coord_obj.center_coord[cell]
                    line = plt.plot((c_x, c_x_c), (c_y, c_y_c), linewidth=links_line_width, c=links_color,
                                    zorder=z_order_links)[0]

            fontsize = 12
            plt.text(x=190, y=180,
                     s=f"{n_twins}", color=self_twin_color, zorder=22,
                     ha='center', va="center", fontsize=fontsize, fontweight='bold')
            plt.text(x=190, y=185,
                     s=f"{n_self_orphans}", color=self_orphan_color, zorder=22,
                     ha='center', va="center", fontsize=fontsize, fontweight='bold')
            plt.text(x=190, y=190,
                     s=f"{n_twins}", color=other_twin_color, zorder=22,
                     ha='center', va="center", fontsize=fontsize, fontweight='bold')
            plt.text(x=190, y=195,
                     s=f"{n_other_orphans}", color=other_orphan_color, zorder=22,
                     ha='center', va="center", fontsize=fontsize, fontweight='bold')
            ax.set_ylim(0, self.nb_lines)
            ax.set_xlim(0, self.nb_col)
            ylim = ax.get_ylim()
            # invert Y
            ax.set_ylim(ylim[::-1])
            # xlim = ax.get_xlim()
            # ax.set_xlim(xlim[::-1])
            plt.setp(ax.spines.values(), color="black")
            frame = plt.gca()
            frame.axes.get_xaxis().set_visible(False)
            frame.axes.get_yaxis().set_visible(False)
            save_format = "png"
            fig.savefig(f'{path_results}/cells_map_matching_{plot_title_opt}.{save_format}',
                        format=f"{save_format}",
                            facecolor=fig.get_facecolor())
            plt.close()
        return other_to_self_mapping_array

    def plot_cells_map(self, path_results, data_id=None, use_pixel_masks=False, title_option="", connections_dict=None,
                       background_color=(0, 0, 0, 1), default_cells_color=(1, 1, 1, 1.0),
                       default_edge_color="white",
                       dont_fill_cells_not_in_groups=False,
                       link_connect_color="white", link_line_width=1,
                       cell_numbers_color="dimgray", show_polygons=False,
                       cells_to_link=None, edge_line_width=2, cells_alpha=1.0,
                       fill_polygons=True, cells_groups=None, cells_groups_colors=None,
                       cells_groups_alpha=None,
                       cells_to_hide=None, img_on_background=None,
                       real_size_image_on_bg=True,
                       cells_groups_edge_colors=None, with_edge=False,
                       with_cell_numbers=False, text_size=6, save_formats="png",
                       save_plot=True, return_fig=False, ax_to_use=None,
                       verbose=False,
                       xkcd_mode=False,
                       use_open_cv_approx_for_contours=False,
                       epsilon_factor_for_open_cv_approx=0.001,
                       use_welsh_powell_coloring=False, dpi=300, adjust_brightness=False, max_saturation=0.001):
        """

        Args:
            path_results (str): where the save the file
            data_id (str): use for the name of the file resistered
            use_pixel_masks:
            title_option:
            connections_dict: key is an int representing a cell number, and value is a dict representing the cells it
            connects to. The key is a cell is connected too, and the value represent the strength of the connection
            (like how many times it connects to it)
            background_color (list): 4 float between 0 and 1 representing the RGBA value of the color
            default_cells_color: 4 float between 0 and 1 representing the RGBA value of the color
            default_edge_color: 4 float between 0 and 1 representing the RGBA value of the color
            dont_fill_cells_not_in_groups (bool):
            link_connect_color: color or a dict, key is an int representing the cell, value is the color of the link
            from this cell
            link_line_width:
            cell_numbers_color:
            show_polygons (bool):
            cells_to_link:
            edge_line_width:
            cells_alpha:
            fill_polygons (bool):
            cells_groups (list): list of list, each list represent a group (len(cells_groups) == n_groups), each list
            contains int representing the cell indices
            cells_groups_colors (list): same length as cells_groups, define a color for each group (color should be a
            list of 4 float (RGBA value betwwen 0 and 1)
            cells_groups_alpha(list): same length as cells_groups, contains float values, representing the alpha of
            each color group, if None the one given in cells_groups_colors is used
            cells_to_hide:
            img_on_background:
            real_size_image_on_bg: if True, the size of the figure will respect the original size of the background
            image
            cells_groups_edge_colors:
            with_edge:
            with_cell_numbers:
            xkcd_mode(bool): Turn on xkcd sketch-style drawing mode
            text_size:
            save_formats (str or list): format of the figure: could be "pdf or like ["png", "pdf"]
            save_plot (bool):
            return_fig (bool): return the figure object
            ax_to_use: if matplolib axe is given, then no new figure is created, but this axe is used
            use_open_cv_approx_for_contours: if True, use open cv to approximate the contours as a polygon
                if pixels mask is available, otherwise use convex_hull approximation or the contours already known
            epsilon_factor_for_open_cv_approx: used if  use_open_cv_approx_for_contoursis True,
                indicate the approximation accuracy use to approximates a curve or a polygon with another
                curve/polygon with less
                vertices so that the distance between them is less or equal to the specified precision. It uses the
                Douglas-Peucker algorithm <http://en.wikipedia.org/wiki/Ramer-Douglas-Peucker_algorithm>
                (using open cv package). A smaller value means more detailed contour (0.001 means very details,
                0.05 not much)
            verbose: if True, some informations will be printed along the way
            use_welsh_powell_coloring: if True, use welsh powell algorithm to color all cells that intersect with
        different color. In that case, cancel cell_groups arguments.
            dpi:

        Returns:

        """

        if use_pixel_masks and (self.pixel_masks is None):
            print(f"No pixel_masks available in plot_cells_map() and use_pixel_masks argument set to True")
            return
        if xkcd_mode:
            plt.xkcd()
        cells_center = self.center_coord
        n_cells = len(self.coords)
        if cells_to_hide is None:
            cells_to_hide = []

        if use_welsh_powell_coloring:
            if verbose:
                print("Welsh Powell coloring:")
            isolated_cell_color = default_cells_color
            isolated_group = []
            cells_groups_colors = []
            cells_groups_edge_colors = []
            cells_groups_alpha = []
            cells_groups = []

            # building networkx graph
            graphs = []
            cells_added = []
            for cell in np.arange(n_cells):
                if cell in cells_added:
                    continue
                # welsh_powell
                n_intersect = len(self.intersect_cells[cell])
                if n_intersect == 0:
                    isolated_group.append(cell)
                    cells_added.append(cell)
                else:
                    graph = nx.Graph()
                    cells_to_expend = [cell]
                    edges = set()
                    while len(cells_to_expend) > 0:
                        if cells_to_expend[0] not in cells_added:
                            cells_added.append(cells_to_expend[0])
                            n_intersect = len(self.intersect_cells[cells_to_expend[0]])
                            if n_intersect > 0:
                                for inter_cell in self.intersect_cells[cells_to_expend[0]]:
                                    min_c = min(inter_cell, cells_to_expend[0])
                                    max_c = max(inter_cell, cells_to_expend[0])
                                    edges.add((min_c, max_c))
                                    cells_to_expend.append(inter_cell)
                        cells_to_expend = cells_to_expend[1:]
                    graph.add_edges_from(list(edges))
                    graphs.append(graph)
            cells_by_color_code = dict()
            max_color_code = 0
            for graph in graphs:
                # dict that give for each cell a color code
                col_val = welsh_powell(graph)
                for cell, color_code in col_val.items():
                    if color_code not in cells_by_color_code:
                        cells_by_color_code[color_code] = []
                    cells_by_color_code[color_code].append(cell)
                    max_color_code = max(max_color_code, color_code)

            for color_code, cells in cells_by_color_code.items():
                if len(cells) == 0:
                    continue
                cells_groups.append(cells)
                # cells_groups_colors.append(cm.nipy_spectral(float(color_code + 1) / (max_color_code + 1)))
                color_hex = BREWER_COLORS[color_code % len(BREWER_COLORS)]
                # putting it with value from 0.0 to 1.0
                color_rgb = plt_colors.hex2color(color_hex)
                # adding the alpha
                color_rgba = [c for c in color_rgb]
                color_rgba.append(cells_alpha)
                cells_groups_colors.append(color_rgba)
                cells_groups_edge_colors.append(default_edge_color)
                cells_groups_alpha.append(0.8)
            cells_groups.append(isolated_group)
            cells_groups_colors.append(isolated_cell_color)
            cells_groups_alpha.append(1)
            cells_groups_edge_colors.append("white")
            if verbose:
                print(f"Isolated cells: {len(isolated_group)}")
                print(f"Grouped cells: {self.n_cells - len(isolated_group)}")

        cells_in_groups = []
        if cells_groups is not None:
            for group_id, cells_group in enumerate(cells_groups):
                cells_in_groups.extend(cells_group)
        cells_in_groups = np.array(cells_in_groups)
        cells_not_in_groups = np.setdiff1d(np.arange(n_cells), cells_in_groups)

        if ax_to_use is None:
            if (img_on_background is None) or (real_size_image_on_bg is False):
                figsize = 20 * (self.nb_col / float(dpi)), 20 * (self.nb_lines / float(dpi))
                fig, ax = plt.subplots(nrows=1, ncols=1,
                                       gridspec_kw={'height_ratios': [1]},
                                       figsize=figsize, dpi=dpi)
                fig.subplots_adjust(bottom=0, top=1, left=0, right=1)
                plt.tight_layout()
            else:
                # then we want the figure to respect the size of the image on background
                height, width = img_on_background.shape

                # What size does the figure need to be in inches to fit the image?
                figsize = width / float(dpi), height / float(dpi)

                # Create a figure of the right size with one axes that takes up the full figure
                fig = plt.figure(figsize=figsize)
                ax = fig.add_axes([0, 0, 1, 1])

                text_size = 0.05
                edge_line_width = 0.1

            fig.patch.set_facecolor(background_color)
            ax.set_facecolor(background_color)
        else:
            ax = ax_to_use

        if img_on_background is not None:
            img_on_background = img_on_background - np.min(img_on_background)

            if adjust_brightness:
                print(f"Adjust image brightness")
                # Normalize the 16 bit image
                tmp_img_on_background_16bit = img_on_background * (2**16 / np.max(img_on_background))
                # normalize 8 bit image
                tmp_img_on_background_8bit = (tmp_img_on_background_16bit * (255 / 2**16))

                saturation = max_saturation
                n_pixels = tmp_img_on_background_8bit.shape[0] * tmp_img_on_background_8bit.shape[1]
                for factor in range(100):
                    use_factor = 1 + factor / 10
                    tmp_tmp_img_on_background_8bit = tmp_img_on_background_8bit * use_factor
                    sat_pixels = np.where(tmp_tmp_img_on_background_8bit > 255)
                    n_sat_pixels = len(np.where(tmp_tmp_img_on_background_8bit > 255)[0])
                    tmp_tmp_img_on_background_8bit[sat_pixels] = 255
                    prct_sat = n_sat_pixels / n_pixels
                    if prct_sat > saturation:
                        tmp_img_on_background_8bit = tmp_tmp_img_on_background_8bit
                        print(f"Final image saturation : {n_sat_pixels} pixels, "
                              f"{np.round(prct_sat*100, decimals=2)} % of pixels")
                        break
                tmp_img_on_background_8bit = tmp_img_on_background_8bit.astype(int)
                img_on_background = tmp_img_on_background_8bit

            ax.imshow(img_on_background, cmap=plt.get_cmap("gray")) #, vmin=0,
                     # vmax=np.max(img_on_background), interpolation='nearest') # vmax= 4096 math.pow(2, n_bits)-1

        if use_pixel_masks:
            cells_imshow_alpha = 0.2 if (img_on_background is not None) else 1
            bg_imshow_alpha = 0 if (img_on_background is not None) else 1

            self.add_cells_using_pixel_masks_on_ax(ax, cells_groups, cells_not_in_groups, cells_to_hide,
                                                   default_cells_color, cells_groups_colors, with_cell_numbers,
                                                   cell_numbers_color, text_size,
                                                   background_color, cells_imshow_alpha=cells_imshow_alpha,
                                                   bg_imshow_alpha=bg_imshow_alpha)
        else:
            self.add_cells_using_polygons_on_ax(ax, cells_groups, cells_not_in_groups, cells_to_hide, with_edge,
                                                edge_line_width, default_cells_color,
                                                default_edge_color, cells_groups_edge_colors, cells_groups_colors,
                                                cells_groups_alpha, cells_alpha, with_cell_numbers,
                                                cell_numbers_color, text_size, dont_fill_cells_not_in_groups,
                                                use_open_cv_approx_for_contours=use_open_cv_approx_for_contours,
                                                epsilon_factor_for_open_cv_approx=epsilon_factor_for_open_cv_approx)

        ax.set_ylim(0, self.nb_lines)
        ax.set_xlim(0, self.nb_col)
        ylim = ax.get_ylim()
        # invert Y
        ax.set_ylim(ylim[::-1])

        if connections_dict is not None:
            zorder_lines = 15
            for neuron in connections_dict.keys():
                # plot a line to all out of the neuron
                for connected_neuron, nb_connexion in connections_dict[neuron].items():
                    line_width = link_line_width + np.log(nb_connexion)

                    c_x = cells_center[neuron][0]
                    c_y = cells_center[neuron][1]
                    c_x_c = cells_center[connected_neuron][0]
                    c_y_c = cells_center[connected_neuron][1]

                    if isinstance(link_connect_color, dict):
                        color_to_use = link_connect_color[neuron]
                    else:
                        color_to_use = link_connect_color
                    line = plt.plot((c_x, c_x_c), (c_y, c_y_c), linewidth=line_width, c=color_to_use,
                                    zorder=zorder_lines)[0]
        # print(f"(self.cells_groups is not None) {(self.cells_groups is not None)} show_polygons {show_polygons}")
        if (cells_groups is not None) and show_polygons:
            # DISPLAY THE POLYGON THAT ENGLOB ALL THE CELLS IN A GROUP
            for group_id, cells in enumerate(cells_groups):
                points = np.zeros((2, len(cells)))
                for cell_id, cell in enumerate(cells):
                    c_x, c_y = cells_center[cell]
                    points[0, cell_id] = c_x
                    points[1, cell_id] = c_y
                # finding the convex_hull for each group
                xy = convex_hull(points=points)
                # xy = xy.transpose()
                # print(f"xy {xy}")
                # xy is a numpy array with as many line as polygon point
                # and 2 columns: x and y coords of each point
                face_color = list(cells_groups_colors[group_id])
                # changing alpha
                face_color[3] = 0.3
                face_color = tuple(face_color)
                # edge alpha will be 1
                poly_gon = patches.Polygon(xy=xy,
                                           fill=fill_polygons, linewidth=0, facecolor=face_color,
                                           edgecolor=cells_groups_colors[group_id],
                                           zorder=15, lw=3)
                ax.add_patch(poly_gon)

        # plt.title(f"Cells map {data_id} {title_option}")

        # ax.set_frame_on(False)

        # invert Y
        # ax.set_ylim(ylim[::-1])
        plt.setp(ax.spines.values(), color=background_color)
        frame = plt.gca()
        frame.axes.get_xaxis().set_visible(False)
        frame.axes.get_yaxis().set_visible(False)


        # ax.xaxis.set_ticks_position('none')
        # ax.yaxis.set_ticks_position('none')
        #  :param plot_option: if 0: plot n_out and n_int,
        #  if 1 only n_out, if 2 only n_in, if 3: only n_out with dotted to
        # show the commun n_in and n_out, if 4: only n_in with dotted to show the commun n_in and n_out,
        if ax_to_use is None:
            if data_id is None:
                data_id = ""
            if save_plot:
                if isinstance(save_formats, str):
                    save_formats = [save_formats]
                for save_format in save_formats:
                    fig.savefig(f'{path_results}/{data_id}_cell_maps_{title_option}.{save_format}',
                                format=f"{save_format}",
                                facecolor=fig.get_facecolor())
            if return_fig:
                return fig
            else:
                plt.close()

    def _get_contours_for_plt_polygon_using_cv2(self, cell, epsilon_factor=0.001):
        """
        Return coord as a 2d np array (n_coord, 2), columns representing x and y position.
        Contours are computing using open cv findContours method and then approxPolyDP
        Args:
            cell: cell index
            epsilon_factor: indicate the approximation accuracy use to approximates a curve or a polygon with another
            curve/polygon with less
            vertices so that the distance between them is less or equal to the specified precision. It uses the
            Douglas-Peucker algorithm <http://en.wikipedia.org/wiki/Ramer-Douglas-Peucker_algorithm>
            (using open cv package)

        Returns:

        """
        if self.pixel_masks is None:
            return None

        pixel_mask = self.pixel_masks[cell]

        binary_img = np.zeros((self.nb_lines, self.nb_col), dtype="uint8")
        for x, y in zip(pixel_mask[0], pixel_mask[1]):
            binary_img[x, y] = 1
        contours, _ = cv2.findContours(binary_img, mode=cv2.RETR_EXTERNAL,
                                       method=cv2.CHAIN_APPROX_SIMPLE)
        # contours, _ = cv2.findContours(binary_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) == 0:
            raise Exception(f"CAREFUL: No contour for cell {cell} in cells_map_utils")

        biggest_contour = contours[0]
        biggest_area = cv2.contourArea(contours[0])
        if len(contours) > 1:
            for contour in contours[1:]:
                area = cv2.contourArea(contour)
                if area > biggest_area:
                    biggest_area = area
                    biggest_contour = contour

        contour = biggest_contour
        area = biggest_area
        if area < 10:
            return None
        # the bigger espilon, the less detailed contour
        epsilon = epsilon_factor * cv2.arcLength(contour, True)
        contour = cv2.approxPolyDP(contour, epsilon, True)
        # xy = []
        coord = np.zeros((2, len(contour)))
        for c_index, c in enumerate(contour):
            # xy.append([c[0][0] + 0.5, c[0][1] + 0.5])
            # xy.append([c[0][0], c[0][1]])
            coord[0, c_index] = c[0][0]
            coord[1, c_index] = c[0][1]

        return coord.transpose()

    def add_contours_to_image(self, image_data):
        """
        Take a 2d or 3d array representing an image, and add contours on it
        Args:
            image_data:

        Returns:

        """

        cv2.drawContours(image=image_data, contours=self.cv2_contours, contourIdx=-1, color=(255, 0, 0), thickness=1)

        # return image_data

    def add_cells_using_pixel_masks_on_ax(self, ax, cells_groups, cells_not_in_groups, cells_to_hide,
                                          default_cells_color, cells_groups_colors,with_cell_numbers,
                                          cell_numbers_color, text_size,
                                          background_color, cells_imshow_alpha, bg_imshow_alpha):
        """
        Using pixel mask if it exists
        Args:
            ax:
            cells_groups:
            cells_not_in_groups:
            cells_to_hide:
            default_cells_color:
            cells_groups_colors:
            with_cell_numbers:
            cell_numbers_color:
            text_size:
            background_color:

        Returns:

        """
        if self.pixel_masks is None:
            return

        use_multiple_imshow = False

        background_color = [code for code in background_color]
        background_color[-1] = bg_imshow_alpha
        cmap_colors = [background_color]
        # 0 represents the background
        color_index = 1
        cells_displayed = []
        if not use_multiple_imshow:
            img = np.zeros((self.nb_lines, self.nb_col), dtype="int8")
        else:
            default_cells_color = [code for code in default_cells_color]
            default_cells_color[-1] = cells_imshow_alpha

        if cells_groups is not None:
            for group_index, cell_group in enumerate(cells_groups):
                for cell in cell_group:
                    if cell in cells_to_hide:
                        continue
                    if use_multiple_imshow:
                        img = np.zeros((self.nb_lines, self.nb_col), dtype="int8")
                        cmap_colors = [background_color]
                        color_index = 1

                    cells_displayed.append(cell)
                    pixel_mask = self.pixel_masks[cell]
                    img[pixel_mask[0, :], pixel_mask[1, :]] = color_index
                    face_color = list(cells_groups_colors[group_index])
                    face_color[-1] = cells_imshow_alpha

                    if use_multiple_imshow:
                        cmap_colors.append(face_color)
                        cmap = matplotlib.colors.ListedColormap(cmap_colors)
                        ax.imshow(img, cmap=cmap, interpolation='nearest')
                if not use_multiple_imshow:
                    cmap_colors.append(face_color)
                    color_index += 1

        for cell in cells_not_in_groups:
            if cell in cells_to_hide:
                continue

            if use_multiple_imshow:
                img = np.zeros((self.nb_lines, self.nb_col), dtype="int8")
                cmap_colors = [background_color]
                color_index = 1

            cells_displayed.append(cell)
            pixel_mask = self.pixel_masks[cell]
            img[pixel_mask[0, :], pixel_mask[1, :]] = color_index

            cmap_colors.append(default_cells_color)
            if use_multiple_imshow:
                cmap = matplotlib.colors.ListedColormap(cmap_colors)
                ax.imshow(img, cmap=cmap, interpolation='nearest')
            else:
                color_index += 1

        if not use_multiple_imshow:
            cmap = matplotlib.colors.ListedColormap(cmap_colors)
            ax.imshow(img, cmap=cmap, interpolation='nearest') #, origin='lower') alpha=cells_imshow_alpha,

        if with_cell_numbers:
            for cell in cells_displayed:
                self.plot_text_cell(cell=cell, cell_numbers_color=cell_numbers_color, ax=ax,
                                    text_size=text_size)

    def add_cells_using_polygons_on_ax(self, ax, cells_groups, cells_not_in_groups, cells_to_hide, with_edge,
                                       edge_line_width, default_cells_color,
                                       default_edge_color, cells_groups_edge_colors, cells_groups_colors,
                                       cells_groups_alpha, cells_alpha, with_cell_numbers,
                                       cell_numbers_color, text_size, dont_fill_cells_not_in_groups,
                                       use_open_cv_approx_for_contours, epsilon_factor_for_open_cv_approx):
        """
        Add cells to a matplolib ax using the polygons representation. Arguments give parameters to apply
        Args:
            ax:
            cells_groups:
            cells_not_in_groups:
            cells_to_hide:
            with_edge:
            edge_line_width:
            default_cells_color:
            default_edge_color:
            cells_groups_edge_colors:
            cells_groups_colors:
            cells_groups_alpha:
            cells_alpha:
            with_cell_numbers:
            cell_numbers_color:
            text_size:
            dont_fill_cells_not_in_groups:
            use_open_cv_approx_for_contours: if True, use open cv to approximate the contours as a polygon
            if pixels mask is available, otherwise use convex_hull approximation or the contours already known
            epsilon_factor_for_open_cv_approx: use for approximation of the contours if use_open_cv_approx_for_contours
            is True

        Returns:

        """
        z_order_cells = 12
        if cells_groups is not None:
            for group_index, cell_group in enumerate(cells_groups):
                for cell in cell_group:
                    if cell in cells_to_hide:
                        continue

                    xy = None
                    if use_open_cv_approx_for_contours:
                        xy = self._get_contours_for_plt_polygon_using_cv2(cell=cell,
                                                                          epsilon_factor=epsilon_factor_for_open_cv_approx)
                    if xy is None:
                        xy = self.coords[cell].transpose()
                    if with_edge:
                        line_width = edge_line_width
                        if cells_groups_edge_colors is None:
                            edge_color = default_edge_color
                        else:
                            edge_color = cells_groups_edge_colors[group_index]
                    else:
                        edge_color = cells_groups_colors[group_index]
                        line_width = 0
                    # allow to set alpha of the edge to 1
                    face_color = list(cells_groups_colors[group_index])
                    # changing alpha
                    if len(face_color) > 3:
                        if cells_groups_alpha is not None:
                            face_color[3] = cells_groups_alpha[group_index]
                        else:
                            face_color[3] = cells_alpha
                    face_color = tuple(face_color)
                    # TODO: a solution to explore to plot pixel by pixel and not using the polygon version
                    #  https://stackoverflow.com/questions/39753282/scatter-plot-with-single-pixel-marker-in-matplotlib
                    self.cell_contour = patches.Polygon(xy=xy,
                                                        fill=True, linewidth=line_width,
                                                        facecolor=face_color,
                                                        edgecolor=edge_color,
                                                        zorder=z_order_cells)  # lw=2
                    ax.add_patch(self.cell_contour)
                    if with_cell_numbers:
                        self.plot_text_cell(cell=cell, cell_numbers_color=cell_numbers_color, ax=ax,
                                            text_size=text_size)

        for cell in cells_not_in_groups:
            if cell in cells_to_hide:
                continue

            xy = None
            if use_open_cv_approx_for_contours:
                xy = self._get_contours_for_plt_polygon_using_cv2(cell=cell,
                                                                  epsilon_factor=epsilon_factor_for_open_cv_approx)
            if xy is None:
                xy = self.coords[cell].transpose()
            # face_color = default_cells_color
            # if dont_fill_cells_not_in_groups:
            #     face_color = None
            self.cell_contour = patches.Polygon(xy=xy,
                                                fill=not dont_fill_cells_not_in_groups,
                                                linewidth=0, facecolor=default_cells_color,
                                                edgecolor=default_edge_color,
                                                zorder=z_order_cells, lw=edge_line_width)
            ax.add_patch(self.cell_contour)

            if with_cell_numbers:
                self.plot_text_cell(cell=cell, cell_numbers_color=cell_numbers_color, ax=ax,
                                    text_size=text_size)

    def plot_text_cell(self, cell, ax, cell_numbers_color, text_size, text=None):
        """
        Plot the cell number on the cell
        Args:
            cell: integer
            ax: matplolib axis
            cell_numbers_color: color of the text
            text_size: text size (float)

        Returns:

        """
        fontsize = text_size
        if cell >= 100:
            if fontsize > 2.5:
                fontsize -= 2
        elif cell >= 10:
            if fontsize > 2:
                fontsize -= 1

        c_x_c = self.center_coord[cell][0]
        c_y_c = self.center_coord[cell][1]

        if fontsize < 0.5:
            fontweight = 'ultralight'
        else:
            fontweight = 'bold'

        if text is None:
            ax.text(x=c_x_c, y=c_y_c,
                     s=f"{cell}", color=cell_numbers_color, zorder=22,
                     ha='center', va="center", fontsize=fontsize, fontweight=fontweight)
        else:
            ax.text(x=c_x_c, y=c_y_c,
                    s=text, color=cell_numbers_color, zorder=22,
                    ha='center', va="center", fontsize=fontsize, fontweight=fontweight)

    def get_cell_new_coord_in_source(self, cell, minx, miny):
        coord = self.coords[cell]
        # coords = coords - 1
        coord = coord.astype(int)
        n_coord = len(coord[0, :])
        xy = np.zeros((n_coord, 2))
        for n in np.arange(n_coord):
            # shifting the coordinates in the square size_square+1
            xy[n, 0] = coord[0, n] - minx
            xy[n, 1] = coord[1, n] - miny
        return xy

    def scale_polygon_to_source(self, poly_gon, minx, miny):
        coords = list(poly_gon.exterior.coords)
        scaled_coords = []
        for coord in coords:
            scaled_coords.append((coord[0] - minx, coord[1] - miny))
        # print(f"scaled_coords {scaled_coords}")
        return geometry.Polygon(scaled_coords)


    def get_source_profile(self, cell, tiff_movie, traces, peak_nums, spike_nums,
                           pixels_around=0, bounds=None, buffer=None, with_full_frame=False):
        """
        Return the source profile of a cell
        :param cell:
        :param pixels_around:
        :param bounds: how much padding around the cell pretty much, coordinate of the frame covering the source profile
        4 int list
        :param buffer:
        :param with_full_frame:  Average the full frame
        :return:
        """
        # print("get_source_profile")
        len_frame_x = tiff_movie[0].shape[1]
        len_frame_y = tiff_movie[0].shape[0]

        # determining the size of the square surrounding the cell
        poly_gon = self.cells_polygon[cell]
        if bounds is None:
            minx, miny, maxx, maxy = np.array(list(poly_gon.bounds)).astype(int)
        else:
            minx, miny, maxx, maxy = bounds

        if with_full_frame:
            minx = 0
            miny = 0
            maxx = len_frame_x - 1
            maxy = len_frame_y - 1
        else:
            minx = max(0, minx - pixels_around)
            miny = max(0, miny - pixels_around)
            maxx = min(len_frame_x - 1, maxx + pixels_around)
            maxy = min(len_frame_y - 1, maxy + pixels_around)

        len_x = maxx - minx + 1
        len_y = maxy - miny + 1

        # mask used in order to keep only the cells pixel
        # the mask put all pixels in the polygon, including the pixels on the exterior line to zero
        scaled_poly_gon = self.scale_polygon_to_source(poly_gon=poly_gon, minx=minx, miny=miny)
        img = PIL.Image.new('1', (len_x, len_y), 1)
        if buffer is not None:
            scaled_poly_gon = scaled_poly_gon.buffer(buffer)
        ImageDraw.Draw(img).polygon(list(scaled_poly_gon.exterior.coords), outline=0, fill=0)
        mask = np.array(img)
        # mask = np.ones((len_x, len_y))
        # cv2.fillPoly(mask, scaled_poly_gon, 0)
        # mask = mask.astype(bool)

        source_profile = np.zeros((len_y, len_x))

        # selectionning the best peak to produce the source_profile
        peaks = np.where(peak_nums[cell, :] > 0)[0]
        threshold = np.percentile(traces[cell, peaks], 95)
        selected_peaks = peaks[np.where(traces[cell, peaks] > threshold)[0]]
        # max 10 peaks, min 5 peaks
        if len(selected_peaks) > 10:
            p = 10 / len(peaks)
            threshold = np.percentile(traces[cell, peaks], (1 - p) * 100)
            selected_peaks = peaks[np.where(traces[cell, peaks] > threshold)[0]]
        elif (len(selected_peaks) < 5) and (len(peaks) > 5):
            p = 5 / len(peaks)
            threshold = np.percentile(traces[cell, peaks], (1 - p) * 100)
            selected_peaks = peaks[np.where(traces[cell, peaks] > threshold)[0]]

        # print(f"threshold {threshold}")
        # print(f"n peaks: {len(selected_peaks)}")

        onsets_frames = np.where(spike_nums[cell, :] > 0)[0]
        pos_traces = np.copy(traces)
        pos_traces += abs(np.min(traces))
        for peak in selected_peaks:
            tmp_source_profile = np.zeros((len_y, len_x))
            onsets_before_peak = np.where(onsets_frames <= peak)[0]
            if len(onsets_before_peak) == 0:
                # shouldn't arrive
                continue
            onset = onsets_frames[onsets_before_peak[-1]]
            # print(f"onset {onset}, peak {peak}")
            frames_tiff = tiff_movie[onset:peak + 1]
            for frame_index, frame_tiff in enumerate(frames_tiff):
                tmp_source_profile += (frame_tiff[miny:maxy + 1, minx:maxx + 1] * pos_traces[cell, onset + frame_index])
            # averaging
            tmp_source_profile = tmp_source_profile / (np.sum(pos_traces[cell, onset:peak + 1]))
            source_profile += tmp_source_profile
        if len(selected_peaks) > 0:
            source_profile = source_profile / len(selected_peaks)

        return source_profile, minx, miny, mask

    def get_transient_profile(self, cell, transient, tiff_movie, traces,
                              pixels_around=0, bounds=None):
        len_frame_x = tiff_movie[0].shape[1]
        len_frame_y = tiff_movie[0].shape[0]

        # determining the size of the square surrounding the cell
        if bounds is None:
            poly_gon = self.cells_polygon[cell]
            minx, miny, maxx, maxy = np.array(list(poly_gon.bounds)).astype(int)
        else:
            minx, miny, maxx, maxy = bounds

        minx = max(0, minx - pixels_around)
        miny = max(0, miny - pixels_around)
        maxx = min(len_frame_x - 1, maxx + pixels_around)
        maxy = min(len_frame_y - 1, maxy + pixels_around)

        len_x = maxx - minx + 1
        len_y = maxy - miny + 1

        transient_profile = np.zeros((len_y, len_x))
        frames_tiff = tiff_movie[transient[0]:transient[-1] + 1]
        # print(f"transient[0] {transient[0]}, transient[1] {transient[1]}")
        # now we do the weighted average
        raw_traces = np.copy(traces)
        # so the lowest value is zero
        raw_traces += abs(np.min(raw_traces))

        for frame_index, frame_tiff in enumerate(frames_tiff):
            transient_profile += (
                    frame_tiff[miny:maxy + 1, minx:maxx + 1] * raw_traces[cell, transient[0] + frame_index])
        # averaging
        transient_profile = transient_profile / (np.sum(raw_traces[cell, transient[0]:transient[-1] + 1]))

        return transient_profile, minx, miny

    def corr_between_source_and_transient(self, cell, transient, source_profile_dict, tiff_movie, traces,
                                          source_profile_corr_dict=None,
                                          pixels_around=1):
        """
        Measure the correlation (pearson) between a source and transient profile for a giveb cell
        :param cell:
        :param transient:
        :param source_profile_dict should contains cell as key, and results of get_source_profile avec values
        :param pixels_around:
        :param source_profile_corr_dict: if not None, used to save the correlation of the source profile, f
        for memory and computing proficiency
        :return:
        """
        # print('corr_between_source_and_transient')
        poly_gon = self.cells_polygon[cell]

        # Correlation test
        bounds_corr = np.array(list(poly_gon.bounds)).astype(int)
        # looking if this source has been computed before for correlation
        if (source_profile_corr_dict is not None) and (cell in source_profile_corr_dict):
            source_profile_corr, mask_source_profile = source_profile_corr_dict[cell]
        else:
            source_profile_corr, minx_corr, \
                miny_corr, mask_source_profile, xy_source = source_profile_dict[cell]
            # normalizing
            source_profile_corr = source_profile_corr - np.mean(source_profile_corr)
            # we want the mask to be at ones over the cell
            mask_source_profile = (1 - mask_source_profile).astype(bool)
            if source_profile_corr_dict is not None:
                source_profile_corr_dict[cell] = (source_profile_corr, mask_source_profile)

        transient_profile_corr, minx_corr, miny_corr = self.get_transient_profile(cell=cell,
                                                                                  transient=transient,
                                                                                  tiff_movie=tiff_movie, traces=traces,
                                                                                  pixels_around=pixels_around,
                                                                                  bounds=bounds_corr)
        transient_profile_corr = transient_profile_corr - np.mean(transient_profile_corr)

        pearson_corr, pearson_p_value = stats.pearsonr(source_profile_corr[mask_source_profile],
                                                       transient_profile_corr[mask_source_profile])

        return pearson_corr

def _angle_to_point(point, centre):
    '''calculate angle in 2-D between points and x axis'''
    delta = point - centre
    res = np.arctan(delta[1] / delta[0])
    if delta[0] < 0:
        res += np.pi
    return res


def area_of_triangle(p1, p2, p3):
    '''calculate area of any triangle given co-ordinates of the corners'''
    return np.linalg.norm(np.cross((p2 - p1), (p3 - p1))) / 2.


def convex_hull(points, smidgen=0.0075):
    '''
    from: https://stackoverflow.com/questions/17553035/draw-a-smooth-polygon-around-data-points-in-a-scatter-plot-in-matplotlib
    Calculate subset of points that make a convex hull around points
    Recursively eliminates points that lie inside two neighbouring points until only convex hull is remaining.

    :Parameters:
    points : ndarray (2 x m)
    array of points for which to find hull
    use pylab to show progress?
    smidgen : float
    offset for graphic number labels - useful values depend on your data range

    :Returns:
    hull_points : ndarray (2 x n)
    convex hull surrounding points
    '''

    n_pts = points.shape[1]
    # assert(n_pts > 5)
    centre = points.mean(1)

    angles = np.apply_along_axis(_angle_to_point, 0, points, centre)
    pts_ord = points[:, angles.argsort()]

    pts = [x[0] for x in zip(pts_ord.transpose())]
    prev_pts = len(pts) + 1
    k = 0
    while prev_pts > n_pts:
        prev_pts = n_pts
        n_pts = len(pts)
        i = -2
        while i < (n_pts - 2):
            Aij = area_of_triangle(centre, pts[i], pts[(i + 1) % n_pts])
            Ajk = area_of_triangle(centre, pts[(i + 1) % n_pts], pts[(i + 2) % n_pts])
            Aik = area_of_triangle(centre, pts[i], pts[(i + 2) % n_pts])
            if Aij + Ajk < Aik:
                del pts[i + 1]
            i += 1
            n_pts = len(pts)
        k += 1
    return np.asarray(pts)


def get_coords_extracted_from_fiji(file_name):
    """
    Extract coords from file_name, should be z .zip or .roi file
    Args:
        file_name: .zip or .roi file

    Returns: Array of len the number of contours made of array of 2 lines (x & y) and n columns,
    n being the number of coordinate to set the contour of
    each cell.

    """
    if file_name.endswith("zip"):
        zip_data = read_roi_zip(file_name)
        coords_loaded = np.empty((len(zip_data),), dtype=np.object)
        for roi_index, roi in enumerate(zip_data.values()):
            n_points = len(roi['x'])
            contours = np.zeros((2, n_points), dtype="int16")
            contours[0] = roi['x']
            contours[1] = roi['y']
            coords_loaded[roi_index] = contours
    elif file_name.endswith("roi"):
        roi = read_roi_file(file_name)
        coords_loaded = np.empty((1,), dtype=np.object)
        roi = roi[list(roi.keys())[0]]
        n_points = len(roi['x'])
        contours = np.zeros((2, n_points), dtype="int16")
        contours[0] = roi['x']
        contours[1] = roi['y']
        coords_loaded[0] = contours
    else:
        return None

    return coords_loaded


def get_coords_from_caiman_format_file(file_name, key_to_data=None):
    """
    Extract coords from file_name.
    Args:
        file_name: str: npz or .mat file
        key_to_data: key to use (from dict return when opening the file),
        if None, then assume there is only one

    Returns:  list of array of 2 lines (x & y) and n columns,
    n being the number of coordinate to set the contour of
    the cell.

    """
    if file_name.endswith(".npz"):
        data = np.load(file_name)
        # for now
        keys = list(data.keys())
        coords = data[keys[0]]
    elif file_name.endswith(".mat"):
        data = hdf5storage.loadmat(file_name)
        keys = list(data.keys())
        for key in keys:
            # if isinstance(data[key], bytes):
            #     print(f"key {key}, bytes type")
            if isinstance(data[key], np.ndarray):
                coords = data[key][0]
    else:
        print("Only npz and mat format are accepted for function get_coords_from_file_caiman_format")
        return None

    return coords


def get_coords_from_suite2p_format_file(is_cell_file_name, stat_file_name):
    """
    Extract coords from file_name.
    Args:
        is_cell_file_name: str
        stat_file_name: str

    Returns:  pixel_masks format is returned

    """
    # TODO: to finish
    pass


def compute_distance_from_center(center_dict):

    cell_indexes = list(center_dict.keys())
    n_cells = len(cell_indexes)

    dist_matrix = np.zeros((n_cells, n_cells), dtype=float)
    for cell_1 in range(n_cells):
        cell_1_center = center_dict[cell_1]
        c_1_x = cell_1_center[0]
        c_1_y = cell_1_center[1]
        for cell_2 in np.arange(cell_1, n_cells):
            if cell_2 == cell_1:
                dist_matrix[cell_1, cell_2] = 0
                dist_matrix[cell_2, cell_1] = 0
            else:
                cell_2_center = center_dict[cell_2]
                c_2_x = cell_2_center[0]
                c_2_y = cell_2_center[1]
                dist_matrix[cell_1, cell_2] = np.sqrt((c_2_x - c_1_x) ** 2 + (c_2_y - c_1_y) ** 2)
                dist_matrix[cell_2, cell_1] = np.sqrt((c_2_x - c_1_x) ** 2 + (c_2_y - c_1_y) ** 2)

    return dist_matrix






