# -*- coding: utf-8 -*-
#---------------------------------------------------------------------#
#   FLApy: A analyzer of Irradiance within Understory                 #
#   IA:Irradiance calculator/interpolation/change analysis            #
#   Virsion: 1.0                                                      #
#   Developer: Wang Bin (Yunnan University, Kunming, China)           #
#   Latest modification time: 2021-7-20                               #
#---------------------------------------------------------------------#

import numpy as np
#import naturalneighbor
import pyvista as pv
import pandas as pd
import os
import itertools
import miniball

from tqdm import tqdm
from scipy.optimize import curve_fit
from scipy.spatial import ConvexHull
from scipy.stats import entropy
#from libpysal.cg.kdtree import KDTree
from scipy.spatial import KDTree
from p_tqdm import p_map

class LAH_Analysis(object):
    def __init__(self, inArray = None, resolution = 10):#in xyzv
        _workspace = os.path.abspath(os.path.dirname(__file__))
        self.tempSFL = str(_workspace + '/tem./.temFile.vtk')



        self.inCandidateArray = inArray
        self.resolutionGrid   = resolution

        if inArray is not None:
            if len(self.inCandidateArray) < 30:

                raise OSError('The dimension of matrix cannot less than 30.')


    def lightInterpolation(self):
        self.givenPointsLocation = self.inCandidateArray[:, 0:3]
        self.givenPointsValue = self.inCandidateArray[:, 3]
        self.Xmin, self.Xmax = min(self.inCandidateArray[:, 0]), max(self.inCandidateArray[:, 0])
        self.Ymin, self.Ymax = min(self.inCandidateArray[:, 1]), max(self.inCandidateArray[:, 1])
        self.Zmin, self.Zmax = min(self.inCandidateArray[:, 2]), max(self.inCandidateArray[:, 2])

        self.Granges = [[self.Xmin, self.Xmax, self.resolutionGrid],
                        [self.Ymin, self.Ymax, self.resolutionGrid],
                        [self.Zmin, self.Zmax, self.resolutionGrid]]

        #nnInter = naturalneighbor.griddata(self.givenPointsLocation, self.givenPointsValue, self.Granges)

        #return nnInter


class LAH_calculator(object):

    def __init__(self, inGrid = None, fieldName = 'SVF_flat'):

        _workspace = os.path.abspath(os.path.dirname(__file__))
        self.tempSFL = str(_workspace + '/tem./.temFile.vtk')

        if inGrid is None:
            self._inGrid = pv.read(self.tempSFL)
        else:
            self._inGrid = inGrid._DataContainer



        self._value = np.array(self._inGrid.cell_data[fieldName])
        self.allGridPoints = np.array(self._inGrid.field_data['OBS_SFL'])

        self.obsIdxWithin = np.where(self._inGrid.cell_data['Classification'] == 1)[0]
        self._value = self._value[self.obsIdxWithin]
        self.allGridPoints = self.allGridPoints[self.obsIdxWithin]

        self._x_bar = np.sum(self._value) / len(self._value)
        self._s_Star = np.sqrt((np.sum(self._value ** 2) / len(self._value)) - (self._x_bar ** 2))

        self.kdtree = KDTree(self.allGridPoints)
        self.gridSpacing = self._inGrid.spacing[0]
        self.voxelArea = self.gridSpacing ** 2
        self.voxelVolume = self.gridSpacing ** 3


    def voxel_SummarySta(self):
        self._inGrid.LAH_Vox_average, self._inGrid.LAH_Vox_std, self._inGrid.LAH_Vox_CV, self._inGrid.LAH_Vox_Range = self.summarySta(self._value)

    def voxel_SAC(self):
        coords = self.allGridPoints
        values = self._value
        self._inGrid.LAH_Vox_SAC_local, self._inGrid.LAH_Vox_SAC = self.cal_Moran(coords, values)

    def voxel_Diversity(self):
        self._inGrid.LAH_Vox_Diversity = self.cal_Diversity(self._value)

    def cal_Diversity(self, values):
        proportions = np.array(values) / np.sum(values)
        sdi = entropy(proportions, base=2)
        return sdi

    def voxel_Gini(self):
        self._inGrid.LAH_Vox_Gini = self.cal_Gini(self._value)

    def cal_Gini(self, values):
        sorted_light_availability = sorted(values)
        n = len(values)
        _gini = (np.sum([(i + 1) * sorted_light_availability[i] for i in range(n)]) / (n * np.sum(sorted_light_availability))) - ((n + 1) / (n * 2))
        return _gini

    def summarySta(self, values, per95 = True):
        values = np.array(values)
        _average = values.mean()
        _std = values.std()
        _CV = (_std / _average) * 100

        if per95:
            _range = np.quantile(values, 0.95) - np.quantile(values, 0.05)
        else:
            _range = np.max(values) - np.min(values)

        return _average, _std, _CV, _range
    def calculate_spatial_weights_matrix_idw(self, coords):
        n_points = len(coords)
        kdtree = KDTree(coords)
        distances, indices = kdtree.query(coords, k=n_points)

        W = np.zeros((n_points, n_points))

        for i, j in tqdm(itertools.product(range(n_points), repeat=2), nrows=100,
                         desc='Constructing Spatial Weight Matrix'):
            if i != j and distances[i, j] != 0:
                W[i, j] = 1 / distances[i, j]

        row_sums = W.sum(axis=1)
        W_normalized = W / row_sums[:, np.newaxis]

        return W_normalized

    def cal_Moran(self, coords, values):
        W = self.calculate_spatial_weights_matrix_idw(coords)
        n = len(values)
        mean_value = np.mean(values)
        deviation = values - mean_value
        num = np.sum(deviation * (W @ deviation))
        denom = np.sum(deviation ** 2)
        moran_i = n * num / (np.sum(W) * denom)
        l_moran_i = W @ deviation
        return l_moran_i, moran_i



    def normalize_array(self, arr):
        arr = np.array(arr)
        min_val = np.min(arr)
        max_val = np.max(arr)
        normalized_arr = (arr - min_val) / (max_val - min_val) * 100
        return normalized_arr


    def vertical_Summary(self):

        relativeHeight = np.array(self._inGrid.cell_data['Z_normed'])
        relativeHeight = relativeHeight[self.obsIdxWithin]
        relativeHeight[relativeHeight < 0] = 0
        relativeHeight = self.normalize_array(relativeHeight)
        _SVF = self.normalize_array(self._value)
        __points = np.vstack((relativeHeight, _SVF)).transpose()

        _p0 = [np.max(_SVF), np.median(relativeHeight), 1, np.min(_SVF)]
        #_params, _params_covariance = curve_fit(sigmoid_func, relativeHeight, _SVF, _p0, maxfev=99999)
        _params, _params_covariance = curve_fit(sigmoid_func, relativeHeight, _SVF, maxfev=99999)

        #Light attenuation rate
        self._inGrid.LAH_Ver_LAR = _params[0]
        #Height of the inflection point
        self._inGrid.LAH_Ver_HIP = _params[1]
        self._inGrid.LAH_Ver_HIPr = self._inGrid.LAH_Ver_HIP / np.max(relativeHeight)

        _hull = ConvexHull(__points)
        self._inGrid.LAH_Ver_ACH = _hull.volume

    def vertical_ACH(self):

        pass

    def horizontal_Summary(self, givenHeight = 1.5):
        relativeHeight = np.array(self._inGrid.cell_data['Z_normed'])
        relativeHeight = relativeHeight[self.obsIdxWithin]
        relativeHeight[relativeHeight < 0] = 0

        _SVF = self._value
        _OBS_SFL = self.allGridPoints
        tolerance = self.gridSpacing
        _SVF_filterSet = _SVF[np.abs(relativeHeight - givenHeight) <= tolerance]
        _OBS_SFL_filterSet = _OBS_SFL[np.abs(relativeHeight - givenHeight) <= tolerance]

        self._inGrid.LAH_Hor_average, self._inGrid.LAH_Hor_std, self._inGrid.LAH_Hor_CV, self._inGrid.LAH_Hor_Range = self.summarySta(_SVF_filterSet)
        self._inGrid.LAH_Hor_SAC_local, self._inGrid.LAH_Hor_SAC = self.cal_Moran(_OBS_SFL_filterSet, _SVF_filterSet)
        self._inGrid.LAH_Hor_Diversity = self.cal_Diversity(_SVF_filterSet)
        self._inGrid.LAH_Hor_Gini = self.cal_Gini(_SVF_filterSet)


    def cluster3D_Summary(self):
        self._inGrid.set_active_scalars('Gi_Value')
        self._inGrid.compute_cell_sizes()

        self.NumLandscape = len(self._value)

        _threshed_hotspot = self._inGrid.threshold(value=2.576, invert = False)
        _threshed_coldspot = self._inGrid.threshold(value=[-99999, -2.576])

        _bodiesHot = _threshed_hotspot.split_bodies()
        _bodiesCold = _threshed_coldspot.split_bodies()

        sumStaHot = []
        for hot_key in _bodiesHot.keys():
            oneBody_h = _bodiesHot[hot_key]
            oneBody_h_volume = oneBody_h.n_cells * self.voxelVolume
            oneBody_h_Surface = oneBody_h.extract_geometry()
            oneBody_h_area = oneBody_h_Surface.n_cells * self.voxelArea
            Chot, r2hot = miniball.get_bounding_ball(np.array(oneBody_h.points))
            sumStaHot.append([oneBody_h_volume, oneBody_h_area, r2hot])

        sumStaCold = []
        for cold_key in _bodiesCold.keys():
            oneBody_c = _bodiesCold[cold_key]
            oneBody_c_volume = oneBody_c.n_cells * self.voxelVolume
            oneBody_c_Surface = oneBody_c.extract_geometry()
            oneBody_c_area = oneBody_c_Surface.n_cells * self.voxelArea
            Ccold, r2cold = miniball.get_bounding_ball(np.array(oneBody_c.points))

            sumStaCold.append([oneBody_c_volume, oneBody_c_area, r2cold])

        sumStaHot = np.array(sumStaHot)
        sumStaCold = np.array(sumStaCold)

        self._inGrid.LAH_3Dcluster_Hot_Volume = np.sum(sumStaHot[:, 0])
        self._inGrid.LAH_3Dcluster_Cold_Volume = np.sum(sumStaCold[:, 0])

        self._inGrid.LAH_3Dcluster_Hot_Volume_relative = self._inGrid.LAH_3Dcluster_Hot_Volume / (self.NumLandscape * self.voxelVolume)
        self._inGrid.LAH_3Dcluster_Cold_Volume_relative = self._inGrid.LAH_3Dcluster_Cold_Volume / (self.NumLandscape * self.voxelVolume)

        self._inGrid.LAH_3Dcluster_VolumeRatio_Hot2Cold = self._inGrid.LAH_3Dcluster_Hot_Volume / self._inGrid.LAH_3Dcluster_Cold_Volume

        self._inGrid.LAH_3Dcluster_Hot_Largest_Volume = np.max(sumStaHot[:, 0])
        self._inGrid.LAH_3Dcluster_Cold_Largest_Volume = np.max(sumStaCold[:, 0])


        self._inGrid.LAH_3Dcluster_Hot_Abundance = len(_bodiesHot)
        self._inGrid.LAH_3Dcluster_Cold_Abundance = len(_bodiesCold)

        self._inGrid.LAH_3Dcluster_Hot_Volume_Numweight = self._inGrid.LAH_3Dcluster_Hot_Volume / self._inGrid.LAH_3Dcluster_Hot_Abundance
        self._inGrid.LAH_3Dcluster_Cold_Volume_Numweight = self._inGrid.LAH_3Dcluster_Cold_Volume / self._inGrid.LAH_3Dcluster_Cold_Abundance

        self._inGrid.LAH_3Dcluster_Hot_Cohesion = np.mean(self.cal_Cohesion(N = self.NumLandscape, P = sumStaHot[:, 1], A = sumStaHot[:, 0]))
        self._inGrid.LAH_3Dcluster_Cold_Cohesion = np.mean(self.cal_Cohesion(N = self.NumLandscape, P = sumStaCold[:, 1], A = sumStaCold[:, 0]))

        self._inGrid.LAH_3Dcluster_Hot_ShapeFactor = self.cal_shape_factor(sumStaHot[:, 0], sumStaHot[:, 1])
        self._inGrid.LAH_3Dcluster_Cold_ShapeFactor = self.cal_shape_factor(sumStaCold[:, 0], sumStaCold[:, 1])

        miniballHotVolume = self.cal_ShphericalVolume(sumStaHot[:, 2])
        miniballColdVolume = self.cal_ShphericalVolume(sumStaCold[:, 2])
        self._inGrid.LAH_3Dcluster_Hot_ShapeIndex = np.mean(sumStaHot[:, 0] / miniballHotVolume)
        self._inGrid.LAH_3Dcluster_Cold_ShapeIndex = np.mean(sumStaCold[:, 0] / miniballColdVolume)



    def cal_Cohesion(self,N, P, A):
        p = P / self.voxelArea
        a = A / self.voxelVolume

        sum_p = np.sum(p)
        sum_pa = np.sum(p * np.sqrt(a))
        pc = (1 - sum_p / sum_pa) * (1 - (1 / np.sqrt(N - 1))) ** -1
        return pc
    def cal_ShphericalVolume(self, r2):
        r = np.sqrt(r2)
        return (4/3) * np.pi * r**3
    def cal_shape_index(self, V):

        return

    def cal_shape_factor(self, V, A):
        return np.mean((36 * np.pi * V) / (A ** 2))

    def cluster3D_Connectivity(self):

        return

    def hotspotAnalysis(self):

        _x_bar = np.sum(self._value) / len(self._value)
        _s_Star = np.sqrt((np.sum(self._value ** 2) / len(self._value)) - (_x_bar ** 2))

        _gi_star_list = np.ones(self._inGrid.n_cells)
        _gi_star_list = _gi_star_list * -99999
        obsIDX = np.arange(len(self.obsIdxWithin))

        gi_star_valuesSet = p_map(self.cal_Gix, obsIDX, num_cpus = (os.cpu_count() - 2), desc='Hot(cold) spot identifying', ncols=100)

        gi_star_valuesSet = np.array(gi_star_valuesSet)
        _gi_star_list[self.obsIdxWithin] = gi_star_valuesSet

        self._inGrid.cell_data['Gi_Value'] = _gi_star_list
        self._inGrid.save(self.tempSFL)

    def cal_Gix(self, obsIdx):
        onepLocation = self.allGridPoints[obsIdx]

        distances, indices = self.kdtree.query(onepLocation, k=27)

        distances = np.where(distances == 0, 1, distances)
        _omega = 1. / distances

        ind_v = self._value[indices]

        _A = np.sum(ind_v * _omega)
        _B = self._x_bar * np.sum(_omega)
        _C = (len(self._value) - 1) * (np.sum(_omega ** 2))
        _D = (np.sum(_omega)) ** 2
        _E = ((_C - _D) / (len(self._value) - 1)) ** 0.5

        _Gi_x = (_A - _B) / (self._s_Star * _E)

        return _Gi_x



    def computeLAH(self, Voxel = True, Vertical = True, Horizontal = True, Cluster3D = True, save = True):

        if Voxel is True:
            self.voxel_SummarySta()
            self.voxel_SAC()
            self.voxel_Gini()
            self.voxel_Diversity()

        if Vertical is True:
            self.vertical_Summary()

        if Horizontal is True:
            self.horizontal_Summary()

        if Cluster3D is True:
            if 'Gi_Value' not in self._inGrid.cell_data:
                self.hotspotAnalysis()

            self.cluster3D_Summary()

        dataSet = {'Indicators': ['Average', 'Standard_deviation', 'Coefficient_of_variation', 'Range',
                               'Spatial_autocorrelation', 'Diversity', 'Gini_coefficient', 'Light_attenuation_rate',
                               'Height_of_inflection_point', 'Relative_height_of_inflection_point', 'Convex_hull_area',
                               'Average', 'Standard_deviation', 'Coefficient_of_variation', 'Range',
                               'Spatial_autocorrelation', 'Diversity', 'Gini_coefficient', 'Hot_volume', 'Cold_volume',
                               'Relative_hot_volume', 'Relative_cold_volume', 'Volume_ratio_of_hot_to_cold',
                               'Largest_hot_volume', 'Largest_cold_volume', 'Hot_abundance', 'Cold_abundance',
                               'Hot_volume_average', 'Cold_volume_average', 'Hot_cohesion', 'Cold_cohesion',
                               'Hot_shape_factor', 'Cold_shape_factor', 'Hot_shape_index', 'Cold_shape_index'],
                'Scale': ['Voxel', 'Voxel', 'Voxel', 'Voxel', 'Voxel', 'Voxel', 'Voxel', 'Vertical', 'Vertical',
                          'Vertical', 'Vertical', 'Horizontal', 'Horizontal', 'Horizontal', 'Horizontal', 'Horizontal',
                          'Horizontal', 'Horizontal', '3D_Cluster', '3D_Cluster', '3D_Cluster', '3D_Cluster',
                          '3D_Cluster', '3D_Cluster', '3D_Cluster', '3D_Cluster', '3D_Cluster', '3D_Cluster',
                          '3D_Cluster', '3D_Cluster', '3D_Cluster', '3D_Cluster', '3D_Cluster', '3D_Cluster',
                          '3D_Cluster'],
                'Value': [self._inGrid.LAH_Vox_average,
                          self._inGrid.LAH_Vox_std,
                          self._inGrid.LAH_Vox_CV,
                          self._inGrid.LAH_Vox_Range,
                          self._inGrid.LAH_Vox_SAC,
                          self._inGrid.LAH_Vox_Diversity,
                          self._inGrid.LAH_Vox_Gini,
                          self._inGrid.LAH_Ver_LAR,
                          self._inGrid.LAH_Ver_HIP,
                          self._inGrid.LAH_Ver_HIPr,
                          self._inGrid.LAH_Ver_ACH,
                          self._inGrid.LAH_Hor_average,
                          self._inGrid.LAH_Hor_std,
                          self._inGrid.LAH_Hor_CV,
                          self._inGrid.LAH_Hor_Range,
                          self._inGrid.LAH_Hor_SAC,
                          self._inGrid.LAH_Hor_Diversity,
                          self._inGrid.LAH_Hor_Gini,
                          self._inGrid.LAH_3Dcluster_Hot_Volume,
                          self._inGrid.LAH_3Dcluster_Cold_Volume,
                          self._inGrid.LAH_3Dcluster_Hot_Volume_relative,
                          self._inGrid.LAH_3Dcluster_Cold_Volume_relative,
                          self._inGrid.LAH_3Dcluster_VolumeRatio_Hot2Cold,
                          self._inGrid.LAH_3Dcluster_Hot_Largest_Volume,
                          self._inGrid.LAH_3Dcluster_Cold_Largest_Volume,
                          self._inGrid.LAH_3Dcluster_Hot_Abundance,
                          self._inGrid.LAH_3Dcluster_Cold_Abundance,
                          self._inGrid.LAH_3Dcluster_Hot_Volume_Numweight,
                          self._inGrid.LAH_3Dcluster_Cold_Volume_Numweight,
                          self._inGrid.LAH_3Dcluster_Hot_Cohesion,
                          self._inGrid.LAH_3Dcluster_Cold_Cohesion,
                          self._inGrid.LAH_3Dcluster_Hot_ShapeFactor,
                          self._inGrid.LAH_3Dcluster_Cold_ShapeFactor,
                          self._inGrid.LAH_3Dcluster_Hot_ShapeIndex,
                          self._inGrid.LAH_3Dcluster_Cold_ShapeIndex
                          ],
                'Abbreviation': ['AVE_Vox', 'STD_Vox', 'CV_Vox', 'RAN_Vox', 'SAC_Vox', 'DIV_Vox', 'GINI_Vox', 'LAR_Ver',
                                 'HIP_Ver', 'HIPr_Ver', 'ACH_Ver', 'AVE_Hor', 'STD_Hor', 'CV_Hor', 'RAN_Hor', 'SAC_Hor',
                                 'DIV_Hor', 'GINI_Hor', 'HVOL_3D', 'CVOL_3D', 'HVOLr_3D', 'CVOLr_3D', 'VRH2C_3D',
                                 'LHV_3D', 'LCV_3D', 'HAB_3D', 'CAB_3D', 'HVA_3D', 'CVA_3D', 'HCO_3D', 'CCO_3D',
                                 'HSF_3D', 'CSF_3D', 'HSI_3D', 'CSI_3D']
                }

        indicatorCatalog = pd.DataFrame(dataSet)





        if save is not True:
            return indicatorCatalog

        if save is True:

            self._inGrid.save(self.tempSFL)




def sigmoid_func(x, a, b):
    #
    return 100 / (1 + np.exp(-a * (x - b)))

def sigmoid_func2(x, L ,x0, k, b):
    y = L / (1 + np.exp(-k*(x-x0))) + b
    return y











