"""
This module contains ...
"""

# TODO - automatic update when visualization class is already created

### Internal dependencies
import sys
import importlib

### External dependencies
import yaml
import numpy as np

### Internal dependencies
from ._pyplot import PyplotVisualizer

### Module variables
this = sys.modules[__name__]

GEOLOGICAL_FEATURES = [
    'grid',
    'domain',
    'geology',
    # 'beddings'
    'faults',
    'fractures',
]

SURFACES_FEATURES = [
    'topography',
    'bedrock',
    'water_level',
]

DOMAIN_FEATURES = [
    'delimitation',
    'topography',
    'bedrock',
    'water_level',
]

ANISOTROPIC_FEATURES = [
    'cost',
    'alpha',
    'beta',
    'time',
    'karst',
]

features = [
    GEOLOGICAL_FEATURES,
    DOMAIN_FEATURES,
    ANISOTROPIC_FEATURES
]
AUTHORIZED_FEATURES = [f for list_ in features for f in list_]

# Tests if pyvista is installed
find_pyvista = importlib.util.find_spec("pyvista")
test = find_pyvista is not None
if test:
    from ._pyvista import PyvistaVisualizer
    subclass = PyvistaVisualizer
else:
    subclass = PyplotVisualizer


class Visualizer(subclass):
    """
    TODO
    """
    # ajouter __method__ pour dire qu'elle existe pas
    # si yapa pyvista d'installé
    
    def __init__(self, project_directory: str, notebook: bool = True,
                 *args, **kwargs) -> None:
        """"""
        super().__init__(project_directory, *args, **kwargs)
        
    def _is_feature_name_valid(self, feature) -> bool:
        """
        TODO
        """
        if feature not in AUTHORIZED_FEATURES:
            msg = ("ERROR : selected feature has been not recognized "
                   "(authorized features : {})".format(AUTHORIZED_FEATURES))
            raise ValueError(msg)
        else:
            return True
        
    def _is_feature_data_valid(self, simulation, feature) -> bool:
        """
        TODO
        """
        if feature in GEOLOGICAL_FEATURES:
            if getattr(simulation, feature) is None:
                msg = "ERROR : '{}' attribute is None type.".format(feature)
                raise ValueError(msg)
        
        elif feature in DOMAIN_FEATURES:
            if getattr(simulation, 'domain') is None:
                msg = "ERROR : '{}' attribute is None type.".format(feature)
                raise ValueError(msg)
            if getattr(simulation.domain, feature) is None:
                msg = ("ERROR : '{}' domain's attribute"
                       "is of None type.".format(feature))
                raise ValueError(msg)
    
        elif feature in ANISOTROPIC_FEATURES:
            if not hasattr(simulation, 'maps'):  # TODO - à supprimer ?
                msg = "ERROR : environment has no 'maps' attribute."
                raise ValueError(msg)
            
        if feature in ['alpha', 'beta']:
            if simulation.fmm['algorithm'] != 'Riemann3':
                msg = "ERROR : environment has no '{}' data.".format(feature)
                raise ValueError(msg)
            
        return True

# def show(environment, feature, settings={}):
#     """
#     TODO
#     """

#     ### Controls validity of settings
#     attributes = ['domain', 'inlets', 'outlets', 'tracers']
#     for attribute in attributes:
#         if attribute in settings:
#             if not hasattr(environment, attribute):
#                 print('WARNING : No {} available'.format(attribute))
#                 del settings[attribute]
#             else:
#                 if getattr(environment, attribute) is None:
#                     print('WARNING : No {} available'.format(attribute))
#                     del settings[attribute]

#     ### Plot feature
#     if _is_feature_valid(environment, feature):
#         _show_data(environment, feature, settings)

#     return None

# def show_array(array: np.ndarray, engine: str = 'pyplot',
#                ghost=False) -> None:
#     """
#     TODO
#     """
#     if engine == 'pyplot':
#         from ._pyplot import show_array
#     elif engine == 'pyvista':
#         from ._pyvista import show_array
        
#     show_array(array, ghost)
    
        
#     return None
    
# ###################
# ### DEBUG PLOTS ###
# ###################

# def debug(environment, step, engine='matplotlib', settings={}):
#     """
#     TODO
#     """
#     if engine == 'pyvista':
#         from pykasso.visualization import _pyvista

#         if step == 'model':
#             _pyvista._debug_plot_model(environment, settings)
#         elif step == 'fmm':
#             _pyvista._debug_plot_fmm(environment, settings)

#     return None







# #     #############################
# #     ### Visualization methods ###
# #     #############################
# #
# #     def show_catchment(self, label='geology', title=None, cmap='binary'):
# #         """
# #         Show the entire study domain.
# #
# #         Parameters
# #         ----------
# #         label : str, optional
# #             Data to show : 'geology', 'topography', 'orientationx', 'orientationy' 'faults' or 'fractures'.
# #             By default : 'geology'.
# #         title : str, optional
# #             Title of the plot. If 'None', 'data' becomes the label.
# #         cmap : str, optional
# #             Color map, 'binary' by default.
# #         """
# #         import matplotlib.patches as mp
# #         fig, ax1 = plt.subplots()
# #         #if title is None:
# #         #    title = label
# #         #fig.suptitle(title, fontsize=16)
# #
# #         # Load data to show
# #         try:
# #             data = [data.data[:,:,0] for data in self.geology.data if data.label==label][-1]
# #         except:
# #             print('no data for indicated label parameter')
# #
# #         im1 = ax1.imshow(data.T, origin="lower", extent=self.grid.extent, cmap=cmap)
# #
# #         fig.colorbar(im1, ax=ax1)
# #         if self.settings['data_has_mask']:
# #             import matplotlib.patches as mp
# #             p1 = mp.PathPatch(self.mask.polygon, lw=2, fill=0, edgecolor='red', label='mask')
# #             ax1.add_patch(p1)
# #
# #         # Points
# #         for pts in self.points.points:
# #             x, y = zip(*pts.points)
# #             ax1.plot(x, y, 'o', label=pts.points_key)
# #
# #         ax1.set_aspect('equal', 'box')
# #         plt.legend(loc='upper right')
# #         plt.show()
# #         return fig
# #
# #     def _show_maps(self, sim=-1, iteration=-1, cmap='binary'):
# #         """
# #         Show the simulated karst network as an image.
# #         """
# #         karst_network = self.karst_simulations[sim]
# #
# #         fig, ([ax1,ax2],[ax3,ax4]) = plt.subplots(2, 2, sharex=True, sharey=True)
# #         fig.suptitle('Karst Network', fontsize=16)
# #
# #         ax1.imshow(karst_network.maps['outlets'], extent=self.grid.extent, origin='lower', cmap=cmap)
# #         ax1.set_title('Outlets')
# #
# #         ax2.imshow(karst_network.maps['cost'][iteration], extent=self.grid.extent, origin='lower', cmap=cmap)
# #         ax2.set_title('Cost')
# #
# #         ax3.imshow(karst_network.maps['time'][iteration], extent=self.grid.extent, origin='lower', cmap=cmap)
# #         ax3.set_title('Time')
# #
# #         ax4.imshow(karst_network.maps['karst'][iteration], extent=self.grid.extent, origin='lower', cmap=cmap)
# #         ax4.set_title('Karst')
# #
# #         fig.subplots_adjust(hspace=0.5)
# #         plt.show()
# #         return None
# #
# #
# #     def show(self, data=None, title=None):
# #         """
# #         Show the entire study domain (defaults to showing most recent simulation).
# #         """
# #         if data is None:
# #             data = self.karst_simulations[-1]
# #
# #         fig = plt.figure(figsize=(20,10))
# #
# #         # Cost map
# #         fig.add_subplot(131, aspect='equal')
# #         d = data.maps['cost'][-1]
# #         plt.xlabel('Cost array'+str(d.shape))
# #         d = np.transpose(d, (1,0)) # imshow read MxN and we have NxM
# #         plt.imshow(d, extent=self.grid.extent, origin='lower', cmap='gray') #darker=slower
# #         plt.colorbar(fraction=0.046, pad=0.04)
# #
# #         # Travel time map
# #         fig.add_subplot(132, aspect='equal')
# #         d = data.maps['time'][-1]
# #         plt.xlabel('Travel time array'+str(d.shape))
# #         d = np.transpose(d, (1,0)) # imshow read MxN and we have NxM
# #         plt.imshow(d, extent=self.grid.extent, origin='lower', cmap='cividis') #darker=faster
# #         plt.colorbar(fraction=0.046, pad=0.04)
# #
# #         # Karst map
# #         fig.add_subplot(133, aspect='equal')
# #         d = data.maps['karst'][-1]
# #         plt.xlabel('Karst array'+str(d.shape))
# #         d = np.transpose(d, (1,0)) # imshow read MxN and we have NxM
# #         plt.imshow(d, extent=self.grid.extent, origin='lower', cmap='gray_r') #darker=conduits
# #         plt.colorbar(fraction=0.046, pad=0.04)
# #         i = plt.scatter(data.points['inlets'].x,  data.points['inlets'].y,  c='orange')
# #         o = plt.scatter(data.points['outlets'].x, data.points['outlets'].y, c='steelblue')
# #         p = matplotlib.patches.Rectangle((0,0),0,0, ec='r', fc='none')
# #         if self.settings['data_has_mask']:
# #             closed_polygon = self.mask.vertices[:]
# #             closed_polygon.append(closed_polygon[0])
# #             x,y = zip(*closed_polygon)
# #             plt.plot(x,y, color='red', label='mask')
# #         #plt.legend([i,o,p], ['inlets', 'outlets', 'catchment'], loc='upper right')
# #         plt.legend([i,o], ['inlets', 'outlets'], loc='upper right')
# #
# #         if title is not None:
# #             fig.suptitle(title, fontsize=16)
# #         plt.show()
# #         return fig
# #
# #     def show_network(self, data=None, simplify=False, ax=None, plot_nodes=True, mask=True, labels=['inlets', 'outlets'], title=None, cmap=None, color='k', alpha=1, legend=True):
# #         """
# #         #Chloe: This is a new function that I use to create all the figures for the paper.
# #         Show the karst network as a graph with nodes and edges. Defaults to showing latest iteration.
# #
# #         Parameters
# #         ----------
# #         data:
# #             karst simulation object containing nodes, edges, points, etc. Can be obtained from self.karst_simulations[i]
# #         ax :
# #             axis to plot on
# #         label :
# #             None or list of strings ['nodes','edges','inlets','outlets'], indicating which components to label
# #         title : str
# #             title of plot
# #         cmap : str
# #             colormap to use when plotting
# #         color : str
# #             single color to use when plotting (cannot have both cmap and color)
# #         alpha : float
# #             opacity to plot with (1=opaque, 0=transparent)
# #         legend : bool
# #             whether to display legend
# #         plot_nodes : bool
# #             whether to display nodes
# #         polygon : bool
# #             whether to display the bounding polygon
# #         """
# #
# #         if ax == None:
# #             fig,ax = plt.subplots(figsize=(10,10))
# #             ax.set_aspect('equal')
# #
# #         if data == None:
# #             data = self.karst_simulations[-1]
# #
# #         if mask == True:
# #             if self.settings['data_has_mask']:
# #                 closed_polygon = self.mask.vertices[:]
# #                 closed_polygon.append(closed_polygon[0])
# #                 x,y = zip(*closed_polygon)
# #                 ax.plot(x,y, color='maroon')
# #                 p = matplotlib.lines.Line2D([0],[0], color='k')
# #
# #         if simplify == True:
# #             nodes = data.network['nodes']   #get all nodes
# #             nodes_simple = data.network['karstnet'].graph_simpl.nodes  #get indices of only the nodes in the simplified graph
# #             nodes_simple = {key: nodes[key] for key in nodes_simple}   #make df of only the nodes in the simplified graph, for plotting
# #             edges = data.network['edges']   #get all edges
# #             edges_simple = data.network['karstnet'].graph_simpl.edges  #get only the edges in the simplified graph
# #             edges_simple = {i: edge for i,edge in enumerate(edges_simple)}   #make df of only the edges in the simplified graph, for p
# #             nodes = pd.DataFrame.from_dict(nodes_simple, orient='index', columns=['x','y','type']) #convert to pandas for easier plotting
# #             edges = pd.DataFrame.from_dict(edges_simple, orient='index', columns=['inNode','outNode'])
# #         else:
# #             nodes = pd.DataFrame.from_dict(data.network['nodes'], orient='index', columns=['x','y','type']) #convert to pandas for easier plotting
# #             edges = pd.DataFrame.from_dict(data.network['edges'], orient='index', columns=['inNode','outNode'])
# #
# #         #Set up data for plotting:
# #         fromX = nodes.x.loc[edges.inNode]      #calculate coordinates for link start and end points
# #         fromY = nodes.y.loc[edges.inNode]
# #         toX   = nodes.x.loc[edges.outNode]
# #         toY   = nodes.y.loc[edges.outNode]
# #
# #         #Plot nodes and edges:
# #         if plot_nodes:
# #             n = ax.scatter(nodes.x,              nodes.y,                  c='k',         alpha=alpha, s=5)  #scatterplot nodes
# #         i = ax.scatter(data.points['inlets'].x,  data.points['inlets'].y,  c='orange',    s=30) #scatterplot inlets
# #         o = ax.scatter(data.points['outlets'].x, data.points['outlets'].y, c='steelblue', s=30) #scatterplot outlets
# #         e = matplotlib.lines.Line2D([0],[0])                                                  #line artist for legend
# #         for ind in edges.index:                                                               #loop over edge indices
# #             if cmap is not None:
# #                 ax.plot((fromX.iloc[ind], toX.iloc[ind]), (fromY.iloc[ind], toY.iloc[ind]), c=plt.cm.get_cmap(cmap)(ind/len(edges)), alpha=alpha)  #plot each edge, moving along color gradient to show order
# #             elif color is not None:
# #                 ax.plot((fromX.iloc[ind], toX.iloc[ind]), (fromY.iloc[ind], toY.iloc[ind]), c=color, alpha=alpha)  #plot each edge in same color
# #
# #         #Add labels:
# #         if labels == None:
# #             pass
# #         else:
# #             if 'nodes' in labels:                                         #label node indices
# #                 for ind in nodes.index:                                   #loop over node indices
# #                     ax.annotate(str(ind), xy=(nodes.y[ind]-10, nodes.x[ind]))  #annotate slightly to left of each node
# #             if 'edges' in labels:
# #                 for ind in edges.index:
# #                     ax.annotate(str(ind), xy=(edges.y[ind]-10, edges.x[ind]))  #annotate slightly to left of each edge
# #             if 'inlets' in labels:
# #                 for index,inlet in data.points['inlets'].iterrows():
# #                     ax.annotate(str(int(inlet.outlet))+'-'+str(int(inlet.inlet_iteration)),  xy=(inlet.x-(6*self.grid.dx),  inlet.y))
# #             if 'outlets' in labels:
# #                 for index,outlet in data.points['outlets'].iterrows():
# #                     ax.annotate(str(int(outlet.name)), xy=(outlet.x-(4*self.grid.dx), outlet.y))
# #
# #         #Add legend & title:
# #         if legend:
# #             if plot_nodes:
# #                 if plot_polygon:
# #                     ax.legend([i,o,n,e,p],['inlets','outlets','nodes','edges','mask'])
# #                 else:
# #                     ax.legend([i,o,n,e],['inlets','outlets','nodes','edges'])
# #             else:
# #                 if plot_polygon:
# #                     ax.legend([i,o,e,p],['inlets','outlets','edges','mask'])
# #                 else:
# #                     ax.legend([i,o,e],['inlets','outlets','edges','mask'])
# #         if title is not None:
# #             ax.set_title(title, fontsize=16)
# #
# #         return None












# # def show_average_paths(self):
# #     """
# #     todo
# #     """
# #     ### Call the plotter
# #     p = pv.Plotter(notebook=False)

# #     ### Construct the grid
# #     vtk = pv.UniformGrid()
# #     vtk.dimensions = np.array((self.GRID.nx, self.GRID.ny, self.GRID.nz)) + 1
# #     vtk.origin     = (self.GRID.x0 - self.GRID.dx/2, self.GRID.y0 - self.GRID.dy/2, self.GRID.z0 - self.GRID.dz/2)
# #     vtk.spacing    = (self.GRID.dx, self.GRID.dy, self.GRID.dz)

# #     vtk['values'] = self.karst_prob.flatten(order="F")

# #     mesh = vtk.cast_to_unstructured_grid()
# #     ghosts = np.argwhere(vtk['values'] < 1.0)
# #     mesh.remove_cells(ghosts)
# #     p.add_mesh(mesh, show_edges=False)

# #     ### Plotting
# #     # p.add_title(feature)
# #     p.add_axes()
# #     bounds = p.show_bounds(mesh=vtk)
# #     p.add_actor(bounds)
# #     p.show(cpos='xy')

# #     return None