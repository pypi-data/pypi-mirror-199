# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import pyvista as pv
import itertools
import os

from tqdm import tqdm
from scipy.spatial import KDTree
from p_tqdm import p_map

class LAcalculator():
    def __init__(self, inDataContainer = None, lensMapRadius = 500, pointSizeRange = (0.5, 7)):
        _workspace = os.path.abspath(os.path.dirname(__file__))
        self.tempSFL = str(_workspace + '/tem./.temFile.vtk')
        if inDataContainer is None:
            self._DataContainer = pv.read(self.tempSFL)
        else:
            self._DataContainer = inDataContainer._SFL




        self._mapRadius = lensMapRadius
        self.pointSizeRange = pointSizeRange

        self.pointsBuffered = self._DataContainer.field_data['PTS']
        self.mergeTerrain = np.concatenate((self._DataContainer.field_data['DEM'], self._DataContainer.field_data['DTM']), axis=0)
        self._obsSet = self._DataContainer.field_data['OBS_SFL']


    def mergeTer(self, DEM, DTM):
        mergeTerrainPoints = np.concatenate((DEM.points, DTM.points), axis=0)
        return mergeTerrainPoints
    def pol2cart(self, rho, phi):
        x = rho * np.cos(phi)
        y = rho * np.sin(phi)
        return x, y

    def sph2cart(self, theta, phi, r):
        x = r * np.sin(theta) * np.cos(phi)
        y = r * np.sin(theta) * np.sin(phi)
        z = r * np.cos(theta)
        return x, y, z

    def sph2pol(self, theta, phi):
        r = self._mapRadius*np.ones(len(phi))
        rho = r * np.sin(theta) / (1 + np.cos(theta))
        phi = phi
        return rho, phi

    def cart2sph(self, x, y, z):
        coords = np.vstack((x, y, z)).transpose()
        r = np.sqrt(np.sum((coords) ** 2, axis=1))
        theta = np.arccos(z / (r))
        phi = np.arctan2(y, x)
        #r = self._mapRadius*np.ones(len(phi))
        return r, theta, phi

    def cart2pol(self, x, y):
        """
        Convert Cartesian coordinates (x, y) to polar coordinates (r, theta).
        """
        r = np.sqrt(x ** 2 + y ** 2)
        theta = np.arctan2(y, x)
        return r, theta

    def plotReferenceMap(self, inMap = None):
        if inMap is None:
            inMap = self.cMapAll
        else:
            inMap = inMap
        plt.imshow(inMap, interpolation='nearest')
        plt.colorbar()
        return plt.show()


    def referenceGrid(self):
        radius = self._mapRadius
        xgrid, ygrid = np.meshgrid(np.arange(1, radius * 2 + 1), np.arange(1, radius * 2 + 1))
        xgrid = (xgrid - radius - 0.5)
        ygrid = (ygrid - radius - 0.5)
        gridCoord = np.column_stack((xgrid.ravel(), ygrid.ravel()))
        grid_rad, grid_theta = self.cart2pol(xgrid.ravel(), ygrid.ravel())
        grid_rad[grid_rad > radius] = np.nan

        grid_image = np.ones((radius * 2, radius * 2))
        imdx = np.reshape(np.isnan(grid_rad), grid_image.shape)
        grid_image[imdx] = 0
        return grid_image, gridCoord
    def drawIn_vegPoints(self, inPoints, inObs, pointSizeRangeSet):
        # inPoints:XYZ(x, 3)
        # inPoints:XYZ(1, 3)
        image2ev, gridCoord = self.referenceGrid()
        pointSizeRangeMin = min(pointSizeRangeSet)
        pointSizeRangeMax = max(pointSizeRangeSet)
        vegCBOed = inPoints - inObs
        vegCBOed = vegCBOed[vegCBOed[:, 2] > 0]
        veg2sph_r, veg2sph_theta, veg2sph_phi = self.cart2sph(vegCBOed[:, 0], vegCBOed[:, 1], vegCBOed[:, 2])
        veg2pol_rho, veg2pol_phi = self.sph2pol(veg2sph_theta, veg2sph_phi)
        tx, ty = self.pol2cart(veg2pol_rho, veg2pol_phi)
        datcart = np.column_stack((tx, ty))
        gridCoordCellSize = np.abs(gridCoord[1][0]-gridCoord[0][0])
        Dmin, Dmax = np.min(veg2sph_r), np.max(veg2sph_r)
        position = (veg2sph_r - Dmin) / (Dmax - Dmin)
        rmax = (pointSizeRangeMax / 2) * gridCoordCellSize
        rmin = (pointSizeRangeMin / 2) * gridCoordCellSize
        told = (((1 - position) * (rmax - rmin)) + rmin)
        tree = KDTree(gridCoord)
        pointsWithin = tree.query_ball_point(x=datcart, r=told)
        indx = np.array(list(itertools.chain.from_iterable(pointsWithin)))
        indx = np.unique(indx)
        ndx = np.zeros(gridCoord[:, 0].size, dtype=bool)
        ndx[indx] = True
        imdx = np.reshape(ndx, image2ev.shape)
        image2ev[imdx] = 0
        self.vegCoverMap = image2ev
        return image2ev

    def drawIn_terrain(self, inTerrain, inObs):
        image2ev, gridCoord = self.referenceGrid()
        ndx = np.zeros(gridCoord[:, 0].size, dtype=bool)
        terCBOed = inTerrain - inObs
        terCBOed = terCBOed[terCBOed[:, 2] > 0]
        ter2sph_r, ter2sph_theta, ter2sph_phi = self.cart2sph(terCBOed[:, 0], terCBOed[:, 1], terCBOed[:, 2])
        ter2pol_rho, ter2pol_phi = self.sph2pol(ter2sph_theta, ter2sph_phi)
        bins = 360
        gridCoordRho, gridCoordPhi = self.cart2pol(gridCoord[:, 0], gridCoord[:, 1])
        ndx = update_terrain_indices(gridCoordPhi, ter2sph_phi, ter2pol_rho, bins, gridCoordRho, ndx)
        imdx = np.reshape(ndx, image2ev.shape)
        image2ev[imdx] = 0
        self.terCoverMap = image2ev
        return self.terCoverMap



    def cal_LA(self, image2ev):
        # Prepare image for evaluation
        _, gridCoord = self.referenceGrid()
        radius = self._mapRadius
        ygrid = gridCoord[:, 1]
        gridCoordRho, gridCoordPhi = self.cart2pol(gridCoord[:, 0], gridCoord[:, 1])

        #image2ev[image2ev > 0] = 1
        image2ev = image2ev.ravel()

        # Create zenith rings
        n = 9
        lens_profile_tht = np.arange(0, 91, 10)
        lens_profile_rpix = np.linspace(0, 1, n + 1)  # Linear profile per 10deg zenith angle
        ring_tht = np.linspace(0, 90, n + 1)  # Zenith angle in degree, i.e., zenith is tht = 0; horizon is tht = 90
        ring_radius = np.interp(ring_tht, lens_profile_tht, lens_profile_rpix * radius)

        # Initialize variables
        num_rings = len(ring_radius) - 1
        white_to_all_ratio = np.empty(num_rings) * np.nan
        surface_area_ratio_hemi = np.empty(num_rings) * np.nan
        surface_area_ratio_flat = np.empty(num_rings) * np.nan

        # Loop through zenith angle rings
        for rix in range(num_rings):
            inner_radius = ring_radius[rix]
            outer_radius = ring_radius[rix + 1]
            relevant_pix = np.where((gridCoordRho > inner_radius) & (gridCoordRho <= outer_radius))[0]

            white_to_all_ratio[rix] = np.sum(image2ev[relevant_pix] == 1) / len(relevant_pix)
            surface_area_ratio_hemi[rix] = np.cos(np.radians(ring_tht[rix])) - np.cos(np.radians(ring_tht[rix + 1]))
            surface_area_ratio_flat[rix] = np.sin(np.radians(ring_tht[rix + 1])) ** 2 - np.sin(np.radians(ring_tht[rix])) ** 2

        # Calculate SVF
        flat_SVF = np.sum(white_to_all_ratio * surface_area_ratio_flat)
        hemi_SVF = np.sum(white_to_all_ratio * surface_area_ratio_hemi)

        return (flat_SVF, hemi_SVF)

    def computeSingle(self, index):
        obsIn = self._obsSet[index]

        result4oneObs = self.drawIn_vegPoints(self.pointsBuffered, obsIn, self.pointSizeRange)
        result4oneObsTer = self.drawIn_terrain(self.mergeTerrain, obsIn)
        mergeResult = result4oneObsTer * result4oneObs

        self.cMap4veg = result4oneObs
        self.cMap4ter = result4oneObsTer
        self.cMapAll = mergeResult
        SVF = self.cal_LA(self.cMapAll)
        self._SVF_ = SVF
        return (SVF[0], SVF[1])


    def computeBatch(self, save = True, multiPro = False):

        #obsIdx = np.arange(len(self._obsSet))
        obsIdx = np.where(self._DataContainer.cell_data['Classification'] == 1)[0]
        SVFcellData = np.zeros((len(self._obsSet), 2))

        if multiPro is False:
            SVFset = []
            for runidx in tqdm(obsIdx, ncols=100, desc='Batch processing'):
                svfOne = self.computeSingle(runidx)
                SVFset.append(svfOne)

        else:
            SVFset = p_map(self.computeSingle, obsIdx, num_cpus = (os.cpu_count() - 1), desc='Batch processing', ncols=100)


        SVFset = np.array(SVFset)

        SVFcellData[obsIdx] = SVFset


        self.multi_SVF_ = SVFcellData

        if save is not True:
            return SVFcellData
        elif save is True:
            self._DataContainer.cell_data['SVF_flat'] = SVFcellData[:, 0]
            self._DataContainer.cell_data['SVF_hemi'] = SVFcellData[:, 1]

            self._DataContainer.save(self.tempSFL)

def update_terrain_indices(gridCoordPhi, ter2sph_phi, ter2pol_rho, bins, gridCoordRho, ndx):
    for idx in range(bins):
        tbinMin = np.deg2rad(-180) + np.deg2rad(idx)
        tbinMax = np.deg2rad(-180) + np.deg2rad(idx + 1)
        keptPointsRho = ter2pol_rho[(ter2sph_phi >= tbinMin) & (ter2sph_phi < tbinMax)]

        if len(keptPointsRho) != 0:
            keptPointsRhoMin = np.min(keptPointsRho)
        else:
            Aloop = 2
            while len(keptPointsRho) == 0:
                tbinMax = np.deg2rad(-180) + np.deg2rad(idx + Aloop)
                keptPointsRho = ter2pol_rho[(ter2sph_phi >= tbinMin) & (ter2sph_phi < tbinMax)]
                Aloop = Aloop + 1
            keptPointsRhoMin = np.min(keptPointsRho)

        keptGridRhoIdx = np.where((gridCoordPhi >= tbinMin) & (gridCoordPhi < tbinMax))[0]
        keptGridRho = gridCoordRho[(gridCoordPhi >= tbinMin) & (gridCoordPhi < tbinMax)]
        keptGridRhoIdx = keptGridRhoIdx[keptGridRho >= keptPointsRhoMin]
        ndx[keptGridRhoIdx] = True
    return ndx


