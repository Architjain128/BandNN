"""This file con_verts xyz coordinates to zmat"""
import numpy as np

def get_zmat_from_coordinates(xyzarr):
    """generate z_mat from coordinates"""
    xyzarr = np.array(xyzarr)
    distmat = distance_matrix(xyzarr)
    zmat = []
    npart = xyzarr.shape[0]
    rlist = []
    alist = []
    dlist = []
    rconnect = []
    aconnect = []
    dconnect = []

    if npart > 0:

        if npart > 1:
            # and the second, with distance from first
            rlist.append(distmat[0][1])
            zmat.append([1,rlist[0]])
            rconnect.append(1)

            if npart > 2:
                rconnect.append(1)
                rlist.append(distmat[0][2])
                alist.append(angle(xyzarr, 2, 0, 1))
                aconnect.append(2)
                zmat.append([1, rlist[1], 2, alist[0]])


                if npart > 3:
                    for i in range(3, npart):
                        rconnect.append(i-2)
                        aconnect.append(i-1)
                        dconnect.append(i)
                        rlist.append(distmat[i-3][i])
                        alist.append(angle(xyzarr, i, i-3, i-2))
                        dlist.append(dihedral(xyzarr, i, i-3, i-2, i-1))
                        zmat.append([i-2, rlist[i-1], i-1, alist[i-2], i, dlist[i-3]])
    zparams = rlist+alist+dlist
    zconnect  = [rconnect,aconnect,dconnect]
    return (zparams, zconnect)

def get_coordinates_from_zmat(zparams, zconnect):
    """generate coordinates from z_mat"""

    rlist=[]
    alist=[]
    dlist=[]
    zparams = zparams.tolist()
    for _ in range(len(zconnect[0])):
        rlist.append(zparams.pop(0))
    for _ in range(len(zconnect[1])):
        alist.append(zparams.pop(0))
    for _ in range(len(zconnect[2])):
        dlist.append(zparams.pop(0))

    npart = len(zconnect[0]) + 1

    xyzarr = np.zeros([npart, 3])
    if npart > 1:
        xyzarr[1] = [rlist[0], 0.0, 0.0]

    if npart > 2:
        x_val = rlist[1] * np.cos(alist[0])
        y_val = rlist[1] * np.sin(alist[0])
        b_ij = xyzarr[zconnect[1][0] - 1] - xyzarr[zconnect[0][1] - 1]
        if b_ij[0] < 0:
            x_val = xyzarr[zconnect[0][1] - 1][0] - x_val
            y_val = xyzarr[zconnect[0][1] - 1][1] - y_val
        else:
            x_val = xyzarr[zconnect[0][1] - 1][0] + x_val
            y_val = xyzarr[zconnect[0][1] - 1][1] + y_val
        xyzarr[2] = [x_val, y_val, 0.0]

    for n_ind in range(3, npart):

        x_val = rlist[n_ind-1] * np.cos(alist[n_ind-2])
        y_val = rlist[n_ind-1] * np.cos(dlist[n_ind-3] - np.pi) * np.sin(alist[n_ind-2])
        z_val = rlist[n_ind-1] * np.sin(dlist[n_ind-3] - np.pi) * np.sin(alist[n_ind-2])

        b_c = xyzarr[zconnect[0][n_ind-1] - 1] - xyzarr[zconnect[1][n_ind-2] - 1]
        b_c = b_c / np.linalg.norm(b_c)
        n_v = np.cross(xyzarr[zconnect[1][n_ind-2] - 1] - xyzarr[zconnect[2][n_ind-3] - 1], b_c)
        n_v = n_v / np.linalg.norm(n_v)
        ncb_c = np.cross(n_v, b_c)

        xyzarr[n_ind] = [xyzarr[zconnect[0][n_ind-1] - 1][0] - b_c[0] * x_val + ncb_c[0] * y_val\
            + n_v[0] * z_val, xyzarr[zconnect[0][n_ind-1] - 1][1] - b_c[1] * x_val + ncb_c[1] *\
            y_val + n_v[1] * z_val, xyzarr[zconnect[0][n_ind-1] - 1][2] - b_c[2] * x_val + \
            ncb_c[2] * y_val + n_v[2] * z_val]

    return xyzarr


def angle(xyzarr, i, j, k):
    """calculate angle"""
    rij = xyzarr[i] - xyzarr[j]
    rkj = xyzarr[k] - xyzarr[j]
    cos_theta = np.dot(rij, rkj)
    sin_theta = np.linalg.norm(np.cross(rij, rkj))
    theta = np.arctan2(sin_theta, cos_theta)
    return theta

def dihedral(xyzarr, i, j, k, l_val):
    """calculate dihedral"""
    rji = xyzarr[j] - xyzarr[i]
    rkj = xyzarr[k] - xyzarr[j]
    rlk = xyzarr[l_val] - xyzarr[k]
    v_1 = np.cross(rji, rkj)
    v_1 = v_1 / np.linalg.norm(v_1)
    v_2 = np.cross(rlk, rkj)
    v_2 = v_2 / np.linalg.norm(v_2)
    m_1 = np.cross(v_1, rkj) / np.linalg.norm(rkj)
    x_val = np.dot(v_1, v_2)
    y_val = np.dot(m_1, v_2)
    chi = np.arctan2(y_val, x_val)
    return chi



def distance_matrix(xyzarr):
    """calculate distance matrix"""
    npart = xyzarr.shape[0]
    dist_mat = np.zeros([npart, npart])
    for i in range(npart):
        for j in range(0, i):
            rvec = xyzarr[i] - xyzarr[j]
            dist_mat[i][j] = dist_mat[j][i] = np.sqrt(np.dot(rvec, rvec))
    return dist_mat
