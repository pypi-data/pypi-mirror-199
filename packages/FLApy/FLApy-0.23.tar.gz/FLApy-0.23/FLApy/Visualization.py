# -*- coding: utf-8 -*-

#---------------------------------------------------------------------#
#   FLApy:A Calculator of Illumination factor within Understory       #
#   IA:Illumination factors calculator/interpolation/change analysis  #
#   Virsion: 1.0                                                      #
#   Developer: Wang Bin (Yunnan University, Kunming, China)           #
#   Latest modification time: 2022-4-1                                #
#---------------------------------------------------------------------#


import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt
import pyvista as pv

def visXYZ_points(point, method = 'pv'):    #xyz
    '''''
    if method == 'maya':
        lasin = np.array(point)

        x, y, z = lasin[:, 0], lasin[:, 1], lasin[:, 2]
        mlab.points3d(x, y, z, z, colormap="spectral", mode="point")
        return mlab.show()
    '''''

    if method == 'o3d':
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(point)

        return o3d.visualization.draw_geometries([pcd])

    elif method == 'pv':

        pc = pv.PolyData(point)

        value = point[:, -1]

        pc['Elevation'] = value

        return pc.plot(render_points_as_spheres=False, show_grid=True)

def visSphereMap(inMap, method = 'Orthographic'):
    if method == 'Mollweide':
        return hp.mollview(inMap)
    elif method == 'Gnomonic':
        return hp.gnomview(inMap)
    elif method == 'Orthographic':
        return hp.orthview(inMap, rot=(0, 90 , 180), half_sky= True)
    elif method == 'Cartesian':
        return hp.cartview(inMap)

def visIlluminationScalar(inScalar, inArray = None, resolution = 10, contours = 10, normalization = False, method = 'maya'):
    if normalization == True:
        inScalar = (inScalar - np.min(inScalar)) / (np.max(inScalar) - np.min(inScalar))
    else:
        inScalar = inScalar
    '''''
    if method == 'maya':
        mlab.contour3d(inScalar, contours = contours, transparent = True)
        return mlab.show()
    '''''
    if method == 'plotly':
        if len(inArray) == 0:
            raise OSError('The results obsevered is required.')
        else:
            Xmin, Xmax = min(inArray[:, 0]), max(inArray[:, 0])
            Ymin, Ymax = min(inArray[:, 1]), max(inArray[:, 1])
            Zmin, Zmax = min(inArray[:, 2]), max(inArray[:, 2])

            X, Y, Z = np.mgrid[Xmin:Xmax:resolution,Ymin:Ymax:resolution, Zmin:Zmax:resolution]

            fig = go.Figure(data=go.Volume(
                x=X.flatten(),
                y=Y.flatten(),
                z=Z.flatten(),
                value=inScalar.flatten(),
                isomin=300,
                isomax=np.max(inScalar),
                opacity=0.1,
                opacityscale=[[-0.5, 1], [-0.2, 0], [0.2, 0], [0.5, 1]],
                surface_count = 21,
                colorscale='RdBu'

            ))

            return fig.show()

def vis3D_LightRegime(inData, field):
#The results produced by Interpolation is required, and need to be mapped to 3D grid
    p = pv.Plotter()

    p.add_mesh(inData, scalars = field, cmap='jet')
    p.show_grid()
    return p.show()

def vis3D_LightRegime_filtered(inData):
    #inData.cell_data['values'] = inData.cell_data['classification'] * inData.cell_data['values']
    p = pv.Plotter()

    p.add_mesh(inData, scalars='SVF', cmap='jet')
    p.show_grid()
    return p.show()

def vis3D_LightRegime_plane(inData):

    return



def vis3D_LightRegime_time(indata_T1, indata_T2, method = 'T1 - T2'):

    return

def vis2D_raster(inData):

    return

def themeConfig():
    mytheme = pv.themes.DefaultTheme()
    mytheme.background = 'white'
    mytheme.font.family = 'times'
    mytheme.font.color = 'black'
    mytheme.cmap = 'jet'
    mytheme.axes.x_color = 'black'
    mytheme.axes.y_color = 'black'
    mytheme.axes.z_color = 'black'
    mytheme.colorbar_orientation = 'vertical'

    return pv.global_theme.load_theme(mytheme)

