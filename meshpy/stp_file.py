"""
Contains class that allows reading and writing stable pose data.
Run this file with the following command: python stp_file.py MIN_PROB DIR_PATH

MIN_PROB -- Minimum Probability of a given pose being realized.
DIR_PATH -- Path to directory containing .obj files to be converted to .stp files (e.g. ~/obj_folder/)

Authors: Nikhil Sharma and Matt Matl
"""

import os
import numpy as np

import mesh
import stable_pose as sp

class StablePoseFile:
    """
    A Stable Pose .stp file reader and writer.

    Attributes
    ----------
    filepath : :obj:`str`
        The full path to the .stp file associated with this reader/writer.
    """

    def __init__(self, filepath):
        """Construct and initialize a .stp file reader and writer.

        Parameters
        ----------
        filepath : :obj:`str`
            The full path to the desired .stp file

        Raises
        ------
        ValueError
            If the file extension is not .stp.
        """
        self.filepath_ = filepath
        file_root, file_ext = os.path.splitext(self.filepath_)
        if file_ext != '.stp':
            raise ValueError('Extension %s invalid for STPs' %(file_ext))

    @property
    def filepath(self):
        """Returns the full path to the .stp file associated with this reader/writer.

        Returns
        -------
        :obj:`str`
            The full path to the .stp file associated with this reader/writer.
        """
        return self.filepath_

    def read(self):
        """Reads in the .stp file and returns a list of StablePose objects.

        Returns
        -------
        :obj:`list` of :obj`StablePose`
            A list of StablePose objects read from the .stp file.
        """
        stable_poses = []
        f = open(self.filepath_, "r")
        data = [line.split() for line in f]
        for i in range(len(data)):
            if len(data[i]) > 0 and data[i][0] == "p":
                p = float(data[i][1])
                r = [[data[i+1][1], data[i+1][2], data[i+1][3]], [data[i+2][0], data[i+2][1],
                      data[i+2][2]], [data[i+3][0], data[i+3][1], data[i+3][2]]]
                r = np.array(r).astype(np.float64)
                x0 = np.array([data[i+4][1], data[i+4][2], data[i+4][3]]).astype(np.float64)
                try:
                        identifier = data[i+5][1]
                except:
                        Warning("No identifier in data. Setting to 0")
                        stp_id=0
                stable_poses.append(sp.StablePose(p, r, x0,stp_id=identifier))
        return stable_poses

    def write(self, stable_poses, min_prob=0):
        """Writes out the stable poses for a mesh with a minimum probability filter.

        Parameters
        ----------
        stable_poses: :obj:`list` of :obj:`StablePose`
            List of stable poses that should be written to the file.

        min_prob : float
            The minimum probability for a pose to actually be written to the
            file.
        """
        R_list = []
        for pose in stable_poses:
            if pose.p >= min_prob:
                R_list.append([pose.p, pose.r, pose.x0,pose.id])

        f = open(self.filepath_[:-4] + ".stp", "w")
        f.write("#############################################################\n")
        f.write("# STP file generated by UC Berkeley Automation Sciences Lab #\n")
        f.write("#                                                           #\n")
        f.write("# Num Poses: %d" %len(R_list))
        for _ in range(46 - len(str(len(R_list)))):
            f.write(" ")
        f.write(" #\n")
        f.write("# Min Probability: %s" %str(min_prob))
        for _ in range(40 - len(str(min_prob))):
            f.write(" ")
        f.write(" #\n")
        f.write("#                                                           #\n")
        f.write("#############################################################\n")
        f.write("\n")

        # adding R matrices to .stp file
        pose_index = 1
        for i in range(len(R_list)):
            f.write("p %f\n" %R_list[i][0])
            f.write("r %f %f %f\n" %(R_list[i][1][0][0], R_list[i][1][0][1], R_list[i][1][0][2]))
            f.write("  %f %f %f\n" %(R_list[i][1][1][0], R_list[i][1][1][1], R_list[i][1][1][2]))
            f.write("  %f %f %f\n" %(R_list[i][1][2][0], R_list[i][1][2][1], R_list[i][1][2][2]))
            f.write("x0 %f %f %f\n" %(R_list[i][2][0], R_list[i][2][1], R_list[i][2][2]))
            f.write("id %s\n" %R_list[i][3])
        f.write("\n\n")
        f.close()

if __name__ == '__main__':
    pass
