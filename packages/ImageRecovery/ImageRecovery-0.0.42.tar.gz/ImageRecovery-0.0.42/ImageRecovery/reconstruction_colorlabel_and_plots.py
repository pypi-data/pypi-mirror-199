import numpy as np
from scipy import signal

class PlotParameters:

    def __init__(self, L, partition, mode_3D, mode_anim, color_grid, neighbor_dataframe,dim_reduction_vis,
                 current_dir, embedding_mode, graph_weighting, node2vec_parameters, proximity_mode, plot_mode, args):
        self.L = L
        self.partition = partition
        self.mode_3D = mode_3D
        self.mode_anim = mode_anim
        self.color_grid = color_grid
        self.neighbor_dataframe = neighbor_dataframe
        self.dim_reduction_vis = dim_reduction_vis
        self.current_dir = current_dir
        self.embedding_mode = embedding_mode
        self.graph_weighting = graph_weighting
        self.node2vec_parameters = node2vec_parameters
        self.proximity_mode = proximity_mode
        self.plot_mode = plot_mode
        self.args = args


    def get_color_list(self, n, positions):
        """""
        Gets labels for our nodes based on their position, corresponding to a n x n grid.
        """""

        if self.color_grid == "hue":
            #n = 7
            n = self.partition
            hue_matrix = np.zeros((n,n))
            for i,row in enumerate(hue_matrix):
                hue_matrix[i] = np.arange(n)


        if self.color_grid == "gaussian":
            n = self.partition

            def gkern(kernlen=21, std=3):
                """Returns a 2D Gaussian kernel array."""
                gkern1d = signal.gaussian(kernlen, std=std).reshape(kernlen, 1)
                gkern2d = np.outer(gkern1d, gkern1d)
                return gkern2d
            gauss_matrix = gkern(kernlen=n, std=5)*100

        if self.color_grid == "gaussian_3D":
            if self.mode_3D == False:
                raise ValueError("mode should be 3D")
            else:
                gauss_matrix = np.random.normal(5,4, size=(n,n,n))*100


        if self.color_grid == "concentric":
            n = self.partition
            x = np.linspace(-1, 1, n)
            y = x.copy()
            z = x.copy()
            X, Y = np.meshgrid(x, y)
            z =  np.sin((X ** 2 + Y ** 2) ** (8 / 9))
            color_map_concentric = z * 1000

            color_map_concentric = z*10
        if self.color_grid == "concentric_faces":
            n = self.partition
            n_waves = 5
            x = np.linspace(-n_waves, n_waves, n)   # This controls the amount of waves
            y = x.copy()

            X, Y = np.meshgrid(x, y)
            z = np.sin((X ** 2 + Y ** 2) ** (8 / 9))
            color_map_concentric = z*1000


        if self.color_grid == "distortion":
            # DISTORTION MATRIX
            partitions = self.partition  # number of times array divides
            n = 2 ** partitions
            # n = partitions ** 2
            # Rectangular color matrix
            distortion_matrix_rec = np.zeros((partitions, n))
            for i in range(partitions):
                t = 2 ** (i)
                partition = int(n / t)  # partition length
                for j in range(n):
                    if j % 2 == 0:
                        # print(t, j, partition)
                        distortion_matrix_rec[i][j * partition:(j + 1) * partition] = 1
            # Square color matrix
            distortion_matrix = np.zeros((n, n))
            for (i, row) in enumerate(distortion_matrix_rec):
                n_rows = np.shape(distortion_matrix_rec)[0]  # partitions  (There is 2** partitions rows)
                repetition = int(n / n_rows)
                distortion_matrix[i*repetition:(i+1)*repetition] = row
                # for j in range(n_rows):
                #     index = i * n_rows + j
                #     distortion_matrix[index] = row

        mushroom_matrix = np.rot90(np.transpose(np.array(np.mat("3 3 3 3 3 2 2 2 2 2 2 3 3 3 3 3;"
                                                    "3 3 3 2 2 0 0 0 0 1 1 2 2 3 3 3;"
                                                    "3 3 2 1 1 0 0 0 0 1 1 1 1 2 3 3;"
                                                    "3 2 1 1 0 0 0 0 0 0 1 1 1 1 2 3;"
                                                    "3 2 1 0 0 1 1 1 1 0 0 1 1 1 2 3;"
                                                    "2 0 0 0 1 1 1 1 1 1 0 0 0 0 0 2;"
                                                    "2 0 0 0 1 1 1 1 1 1 0 0 1 1 0 2;"
                                                    "2 1 0 0 1 1 1 1 1 1 0 1 1 1 1 2;"
                                                    "2 1 1 0 0 1 1 1 1 0 0 1 1 1 1 2;"
                                                    "2 1 1 0 0 0 0 0 0 0 0 0 1 1 0 2;"
                                                    "2 1 0 0 2 2 2 2 2 2 2 2 0 0 0 2;"
                                                    "3 2 2 2 1 1 2 1 1 2 1 1 2 2 2 3;"
                                                    "3 3 2 1 1 1 2 1 1 2 1 1 1 2 3 3;"
                                                    "3 3 2 1 1 1 1 1 1 1 1 1 1 2 3 3;"
                                                    "3 3 3 2 1 1 1 1 1 1 1 1 2 3 3 3;"
                                                    "3 3 3 3 2 2 2 2 2 2 2 2 3 3 3 3"))),2)
        mario_matrix = np.array(np.mat(

            "3 3 3 3 0 0 0 0 0 0 3 3 3 3 3 3 ;"
            "3 3 3 0 0 0 0 0 0 0 0 0 0 3 3 3 ;"
            "3 3 3 4 4 4 5 5 5 2 5 3 3 3 3 3 ;"
            "3 3 4 5 4 5 5 5 5 2 5 5 5 3 3 3 ;"
            "3 3 4 5 4 4 5 5 5 5 2 5 5 5 3 3 ;"
            "3 3 4 4 5 5 5 5 5 2 2 2 2 3 3 3 ;"
            "3 3 3 3 5 5 5 5 5 5 5 5 3 3 3 3 ;"
            "3 3 3 0 0 6 0 0 0 0 3 3 3 3 3 3 ;"
            "3 3 0 0 0 6 0 0 6 0 0 0 0 3 3 3 ;"
            "3 0 0 0 0 6 6 6 6 0 0 0 0 3 3 3 ;"
            "3 5 5 0 6 7 6 6 7 6 0 5 5 3 3 3 ;"
            "3 5 5 5 6 6 6 6 6 6 5 5 5 3 3 3 ;"
            "3 5 5 6 6 6 6 6 6 6 6 5 5 3 3 3 ;"
            "3 3 3 6 6 6 3 3 6 6 6 3 3 3 3 3 ;"
            "3 3 4 4 4 3 3 3 3 4 4 4 3 3 3 3 ;"
            "3 4 4 4 4 3 3 3 3 4 4 4 4 3 3 3 "
        ))
        mario_matrix = np.rot90(mario_matrix, 3)  # rotate 180 so it is not upside-down.

        star_matrix = np.transpose(np.array(np.mat("3 3 3 3 3 3 3 2 2 3 3 3 3 3 3 3;"
                                                    "3 3 3 3 3 3 2 7 7 2 3 3 3 3 3 3;"
                                                    "3 3 3 3 3 3 2 7 7 2 3 3 3 3 3 3;"
                                                    "3 3 3 3 3 2 7 7 7 7 2 3 3 3 3 3;"
                                                    "2 2 2 2 2 2 7 7 7 7 2 2 2 2 2 2;"
                                                    "2 7 7 7 7 7 7 7 7 7 7 7 7 7 7 2;"
                                                    "3 2 7 7 7 7 2 7 7 2 7 7 7 7 2 3;"
                                                    "3 3 2 7 7 7 2 7 7 2 7 7 7 2 3 3;"
                                                    "3 3 3 2 7 7 2 7 7 2 7 7 2 3 3 3;"
                                                    "3 3 3 2 7 7 7 7 7 7 7 7 2 3 3 3;"
                                                    "3 3 2 7 7 7 7 7 7 7 7 7 7 2 3 3;"
                                                    "3 3 2 7 7 7 7 7 7 7 7 7 7 2 3 3;"
                                                    "3 2 7 7 7 7 7 2 2 7 7 7 7 7 2 3;"
                                                    "3 2 7 7 7 2 2 3 3 2 2 7 7 7 2 3;"
                                                    "2 7 7 2 2 3 3 3 3 3 3 2 2 7 7 2;"
                                                    "2 2 2 3 3 3 3 3 3 3 3 3 3 2 2 2")))
        star_matrix = np.rot90(star_matrix, 2)  # rotate 180 so it is not upside-down.

        flower_matrix = np.transpose(np.array(np.mat("3 3 3 2 2 2 2 2 2 2 2 2 2 3 3 3;"
                                                    "3 2 2 2 8 8 8 8 8 8 8 8 2 2 2 3;"
                                                    "2 2 8 8 8 7 7 7 7 7 7 8 8 8 2 2;"
                                                    "2 8 8 7 7 7 2 1 1 2 7 7 7 8 8 2;"
                                                    "2 8 8 7 7 7 2 7 7 2 7 7 7 8 8 2;"
                                                    "2 8 8 8 8 7 7 7 7 7 7 8 8 8 8 2;"
                                                    "2 2 8 8 8 8 8 8 8 8 8 8 8 8 2 2;"
                                                    "3 2 2 2 8 8 8 8 8 8 8 8 2 2 2 3;"
                                                    "3 3 3 2 2 2 2 2 2 2 2 2 2 3 3 3;"
                                                    "3 2 2 3 3 3 2 9 9 2 3 3 3 2 2 3;"
                                                    "2 9 9 2 2 3 2 9 9 2 3 2 2 9 9 2;"
                                                    "2 9 9 9 9 2 2 9 9 2 2 9 9 9 9 2;"
                                                    "2 9 9 9 9 9 2 9 9 2 9 9 9 9 9 2;"
                                                    "3 2 9 9 9 9 2 9 9 2 9 9 9 9 2 3;"
                                                    "3 3 2 2 9 9 9 9 9 9 9 9 2 2 3 3;"
                                                    "3 3 3 3 2 2 2 2 2 2 2 2 3 3 3 3")))

        flower_matrix = np.rot90(flower_matrix, 2)  # rotate 180 so it is not upside-down.

        chance_matrix = np.transpose(np.array(np.mat("3 4 4 4 4 4 4 4 4 4 4 4 4 4 4 3;"
                                                    "4 5 5 5 5 5 5 5 5 5 5 5 5 5 5 2;"
                                                    "4 5 2 5 5 5 5 5 5 5 5 5 5 2 5 2;"
                                                    "4 5 5 5 5 4 4 4 4 4 5 5 5 5 5 2;"
                                                    "4 5 5 5 4 4 2 2 2 4 4 5 5 5 5 2;"
                                                    "4 5 5 5 4 4 2 5 5 4 4 2 5 5 5 2;"
                                                    "4 5 5 5 4 4 2 5 5 4 4 2 5 5 5 2;"
                                                    "4 5 5 5 5 2 2 5 4 4 4 2 5 5 5 2;"
                                                    "4 5 5 5 5 5 5 4 4 2 2 2 5 5 5 2;"
                                                    "4 5 5 5 5 5 5 4 4 2 5 5 5 5 5 2;"
                                                    "4 5 5 5 5 5 5 5 2 2 5 5 5 5 5 2;"
                                                    "4 5 5 5 5 5 5 4 4 5 5 5 5 5 5 2;"
                                                    "4 5 5 5 5 5 5 4 4 2 5 5 5 5 5 2;"
                                                    "4 5 2 5 5 5 5 5 2 2 5 5 5 2 5 2;"
                                                    "4 5 5 5 5 5 5 5 5 5 5 5 5 5 5 2;"
                                                    "2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2")))
        chance_matrix = np.rot90(chance_matrix, 2)  # rotate 180 so it is not upside-down.

        boo_matrix = np.transpose(np.array(np.mat("3 3 3 3 3 2 2 2 2 2 3 3 3 3 3 3;"
                                                    "3 3 3 2 2 1 1 1 1 1 2 2 3 3 3 3;"
                                                    "3 3 2 1 1 1 1 1 1 1 1 1 2 3 3 3;"
                                                    "3 2 1 1 1 1 1 1 1 1 1 1 1 2 3 3;"
                                                    "3 2 1 2 1 2 1 1 1 1 1 1 1 1 2 3;"
                                                    "2 1 1 2 1 2 1 1 1 1 2 2 2 1 1 2;"
                                                    "2 1 1 2 1 2 1 1 1 2 1 1 2 1 1 2;"
                                                    "2 1 1 1 1 1 1 1 1 1 1 1 2 1 2 3;"
                                                    "2 1 0 1 0 1 0 1 1 1 1 2 1 1 1 2;"
                                                    "2 1 0 0 0 0 0 1 1 1 1 1 1 1 1 2;"
                                                    "2 1 0 0 0 0 0 1 1 1 1 1 1 1 1 2;"
                                                    "3 2 1 0 0 0 0 0 1 1 1 1 1 1 1 2;"
                                                    "3 2 1 0 1 0 1 0 1 1 1 1 1 1 2 3;"
                                                    "3 3 2 1 1 1 1 1 1 1 1 1 1 2 3 3;"
                                                    "3 3 3 2 2 1 1 1 1 1 1 2 2 3 3 3;"
                                                    "3 3 3 3 3 2 2 2 2 2 2 3 3 3 3 3")))
        boo_matrix = np.rot90(boo_matrix, 2)  # rotate 180 so it is not upside-down.


        if self.mode_3D:
            x, y, z = positions[0], positions[1], positions[2]
            # Delete the following lines if they don't cause errors:
            # color_matrix = np.arange(0, n ** 3)
            # np.random.shuffle(color_matrix)  # shuffle
            # color_matrix = color_matrix.reshape((n, n, n))  # reshape to cube matrix

            # checkERBOARD TRI-COLORED

            if self.color_grid == "tri_checkers":
                color_matrix = np.zeros((n, n, n))
                for indices, element in np.ndenumerate(color_matrix):
                    sum_indices = sum(indices)
                    if (sum_indices+1) % 3 == 0:
                        color_matrix[indices[0]][indices[1]][indices[2]] = 1
                    elif (sum_indices+2) % 3 == 0:
                        color_matrix[indices[0]][indices[1]][indices[2]] = 2

            if self.color_grid == "mario_faces":
                n = 16
                color_matrix = np.full((n, n, n), 10)   # Initialize matrix with value 10 (which is transparent color)

                # Fill the faces in with images
                # X faces
                for i in range(1):
                    color_matrix[i,:,:] = mario_matrix
                    color_matrix[n-1-i,:,:] = mushroom_matrix
                    # Y faces
                    color_matrix[:,i,:] = flower_matrix
                    color_matrix[:,n-1-i,:] = chance_matrix
                    # Z faces
                    color_matrix[:,:,i] = boo_matrix
                    color_matrix[:,:,n-1-i] = star_matrix

            if self.color_grid == "distortion":
                n = 2**(self.partition)
                color_matrix = np.empty((n,n,n))
                color_matrix.fill(2)   # Fill with transparent color which will be in index 2 (index 0 = background, index 1 = distortion)

                # color_matrix = np.zeros((n,n,n))
                for i in range(1):
                    color_matrix[i, :, :] = distortion_matrix
                    color_matrix[n - 1 - i, :, :] = distortion_matrix
                    # Y faces
                    color_matrix[:, i, :] = distortion_matrix
                    color_matrix[:, n - 1 - i, :] = distortion_matrix
                    # Z faces
                    color_matrix[:, :, i] = distortion_matrix
                    color_matrix[:, :, n - 1 - i] = distortion_matrix


            if self.color_grid == "hue":
                n = self.partition
                #n = 7
                # print(n)
                color_matrix = np.full((n, n, n), n)   # Initialize matrix with value n (which is transparent color)

                # Fill the faces in with images
                # X faces
                for i in range(1):
                    color_matrix[i,:,:] = hue_matrix
                    color_matrix[n-1-i,:,:] = hue_matrix
                    # Y faces
                    color_matrix[:,i,:] = hue_matrix
                    color_matrix[:,n-1-i,:] = hue_matrix
                    # Z faces
                    color_matrix[:,:,i] = hue_matrix
                    color_matrix[:,:,n-1-i] = hue_matrix

            if self.color_grid == "gaussian":
                n = self.partition
                # n = 7
                # print(n)
                color_matrix = np.full((n, n, n), -1)  # Initialize matrix with value n (which is transparent color)

                # Fill the faces in with images
                # X faces
                for i in range(1):
                    color_matrix[i, :, :] = gauss_matrix
                    color_matrix[n - 1 - i, :, :] = gauss_matrix
                    # Y faces
                    color_matrix[:, i, :] = gauss_matrix
                    color_matrix[:, n - 1 - i, :] = gauss_matrix
                    # Z faces
                    color_matrix[:, :, i] = gauss_matrix
                    color_matrix[:, :, n - 1 - i] = gauss_matrix
            if self.color_grid == "gaussian_3D":
                color_matrix = gauss_matrix

            if self.color_grid == "concentric":
                n=self.partition
                color_matrix = np.full((n, n, n), -1)
                color_matrix = color_map_concentric

            if self.color_grid == "concentric_faces":
                n=self.partition
                color_matrix = np.full((n, n, n), -1)
                # Guarantee that 20% of layers are here:
                thick_layers = int(n*0.2)
                #for i in range(thick_layers):
                    # color_matrix[i, :, :] = color_map_concentric
                    # color_matrix[n - 1 - i, :, :] = color_map_concentric
                    # # Y faces
                    # color_matrix[:, i, :] = color_map_concentric
                    # color_matrix[:, n - 1 - i, :] =color_map_concentric
                    # # Z faces
                    # color_matrix[:, :, i] = color_map_concentric
                    # color_matrix[:, :, n - 1 - i] = color_map_concentric
                color_matrix[0] = color_map_concentric
                color_matrix[1] = color_map_concentric
                color_matrix[2] = color_map_concentric

                color_matrix[-1] = color_map_concentric
                color_matrix[-2] = color_map_concentric
                color_matrix[-3] = color_map_concentric

                color_matrix[:, 1, :] = color_map_concentric
                color_matrix[:, -1, :] = color_map_concentric
                color_matrix[:, 2, :] = color_map_concentric
                color_matrix[:, -2, :] = color_map_concentric
                color_matrix[:, 0, :] = color_map_concentric
                color_matrix[:, 0, :] = color_map_concentric

                color_matrix[:, :, 1] = color_map_concentric
                color_matrix[:, :, -1] = color_map_concentric
                color_matrix[:, :, 2] = color_map_concentric
                color_matrix[:, :, -2] = color_map_concentric
                color_matrix[:, :, 0] = color_map_concentric
                color_matrix[:, :, 0] = color_map_concentric

                #print("whole matrix", color_matrix)
                # print("2d", color_map_concentric)



        # If it is a 2D image
        else:
            x, y = positions[0], positions[1]
            color_matrix = np.arange(0, n ** 2)
            np.random.shuffle(color_matrix)  # shuffle
            color_matrix = color_matrix.reshape(n, n)  # reshape to square matrix

            if self.color_grid == "concentric_faces":
                color_matrix = color_map_concentric
            elif self.color_grid == "tri_checkers":
                color_matrix = np.zeros((n, n))
                for indices, element in np.ndenumerate(color_matrix):
                    sum_indices = sum(indices)
                    if (sum_indices + 1) % 3 == 0:
                        color_matrix[indices[0]][indices[1]] = 1
                    elif (sum_indices + 2) % 3 == 0:
                        color_matrix[indices[0]][indices[1]]= 2
            elif self.color_grid == "swedish_flag":
                n = 8
                # SWEDISH FLAG COLORS
                color_matrix = np.zeros((n,n))
                color_matrix[[2,3],:] = 1   # blue row
                color_matrix[:,[3,4]] = 2   # blue column

            elif self.color_grid == "pixel_monster":
                n = 13
                color_matrix = np.array([
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
                [0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0],
                [0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0],
                [0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                ])
                color_matrix = np.rot90(color_matrix, 3)  # rotate 180 so it is not upside-down.

            elif self.color_grid == "triangle":
                n = 3
                color_matrix = np.array([
                [1, 0, 0],
                [0, 1, 0],
                [0, 0, 1]
                ])
            elif self.color_grid == "mushroom":
                n = 16
                color_matrix = mushroom_matrix


            elif self.color_grid == "mario":
                n = 16
                color_matrix = mario_matrix

            elif self.color_grid == "star":
                n = 16
                color_matrix = star_matrix
            elif self.color_grid == "flower":
                n=16
                color_matrix = flower_matrix
            elif self.color_grid == "chance":
                n=16
                color_matrix = chance_matrix
            elif self.color_grid == "boo":
                n = 16
                color_matrix = boo_matrix
            elif self.color_grid == "distortion":
                color_matrix = distortion_matrix
            elif self.color_grid == "concentric":
                color_matrix = color_map_concentric




        # Color_list is a linearized version of the color matrix for all elements
        # Initialize color_list:
        color_list = np.empty(len(x))

        # ---------------

        # Find the corresponding index in the color_matrix and fill a "linear" color list (equivalent to hcat)
        def get_index_color_list():
            for i in range(len(positions[0])):
                color_matrix_indices = [-1, -1, -1]  # initialize with dummies negative value
                for color_int in range(n):
                    for position_index in range(len(positions)):
                        if (self.L / n) * color_int < positions[position_index][i] < (self.L / n) * (color_int + 1):
                            color_matrix_indices[position_index] = color_int
                if self.mode_3D == True:
                    color_list[i] = color_matrix[color_matrix_indices[0]][color_matrix_indices[1]][
                        color_matrix_indices[2]]
                else:
                    color_list[i] = color_matrix[color_matrix_indices[0]][color_matrix_indices[1]]
            return color_list

        color_list = get_index_color_list()
        return color_list

    def get_labels_by_position(self, file_title):
        positions = self.neighbor_dataframe['POS']

        x = [positions[i][0] for i in range(len(positions))]
        y = [positions[i][1] for i in range(len(positions))]

        if self.mode_3D:
            z = [positions[i][2] for i in range(len(positions))]
            positions_list = [x, y, z]
        else:
            positions_list = [x, y]

        n = self.partition
        # n--> number of partitions
        # Initialize color matrix
        color_list = self.get_color_list(n, positions_list)  # Labels for our nodes

        # Write label_list
        f = open(file_title, 'w')
        for (i, label) in enumerate(color_list):
            node = i + 1
            f.write(str(node) + " " + str(int(label)) + "\n")

        return color_list

    def get_edge_list(self, file_title, weighting="unweight"):

        every_neighbor_list = self.neighbor_dataframe['NN']
        every_weight_list = self.neighbor_dataframe['Nweight']
        every_dist_list = self.neighbor_dataframe['Ndist']

        f = open(file_title, 'w')
        for (i, neighbor_list) in enumerate(every_neighbor_list):
            node = i + 1  # start counting at 1
            if not neighbor_list:       # check if node has edges
                f.write(str(node))
                raise "Disconnected graph. Suggestion: change parameters so the average degree is higher"
            else:
                for (j, nn) in enumerate(neighbor_list):  # If it has edges, write them
                    if weighting =="unweight":
                        f.write(str(node) + " " + str(nn) + "\n")

                    else:
                        #weight = every_weight_list[i][j]
                        if weighting == "distance":
                            weight = every_dist_list[i][j]
                        elif weighting == "softmax_inverse_distance":
                            weight = every_weight_list[i][j]
                            f.write(str(node) + " " + str(nn) + " " + str(weight) + "\n")

    def plot_umap_control_embedded(self, vectors, param, args, n_neighbors, min_dist, densmap, data_from_graph,
                                   embedding_mode, embedded_dim, shape_str):
        pass
















