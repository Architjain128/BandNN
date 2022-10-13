"""This file is for generating the feature vector for a molecule"""
import numpy as np


def get_features(conformer,species,bond_connectivity_list):
    """generating all feature vectors"""
    conformer=np.array(conformer)
    nonbondcutoff = 6

    bonds = generate_bondconnectivty_matrix(bond_connectivity_list)

    #Calculate the atomic environment vector for each atom
    atomic_envs = generate_atomic_env(bonds, species)

    #Calculate the sets of bonds and bond values
    bondlist, bonddistances = generate_bond_data(conformer, bonds)

    #Calculate the 3 atom angle sets and angle values
    angles_list, angles = generate_angle_data(conformer, bonds)

    #Calculate  4 atom dihedral sets and dihedral values
    dihedral_list, dihedral_angles = generate_dihedral_data(conformer,bonds)

    # Calculate the list of Non-bonds
    nonbond_list, nonbonddistances = generate_nonbond_data(conformer, bonds, nonbondcutoff)

    # Zipping the data
    features = {}
    features['bonds'] = np.array(generate_bond_features(bonddistances,bondlist,atomic_envs))
    features['angles'] = np.array(generate_angle_features(angles,angles_list,atomic_envs,\
        bondlist,bonddistances))
    features['nonbonds'] = np.array(generate_bond_features(nonbonddistances,nonbond_list,\
        atomic_envs))
    features['dihedrals'] = np.array(generate_dihedralangle_features([dihedral_angles, \
        dihedral_list], atomic_envs, bondlist, bonddistances, [angles_list, angles]))
    return features


def generate_bondconnectivty_matrix(bond_connectivity_list):
    """genrate matrix for bond connectivity"""
    bond_matrix = [[0 for i in range(len(bond_connectivity_list))] for \
        j in range(len(bond_connectivity_list))]
    for i_1, bond_connectivity_list_i_1 in enumerate(bond_connectivity_list):
        for i_2 in bond_connectivity_list_i_1:
            bond_matrix[i_1][i_2] = 1
            bond_matrix[i_2][i_1] = 1
    return bond_matrix


def generate_atomic_env(bonds, species):
    """genrate atomic environment"""
    atomic_envs = []
    for i, bonds_i in enumerate(bonds):
        atom_id = {'H':0, 'C':1, 'O':2, 'N':3 }
        atomtype = [0,0,0,0]
        atomtype[atom_id[species[i]]]  = 1
        immediate_neighbour_count = [0,0,0,0]
        for j, bonds_i_j in enumerate(bonds_i):
            if bonds_i_j > 0:
                immediate_neighbour_count[atom_id[species[j]]] += 1
        atomic_envs.append(atomtype + immediate_neighbour_count)
    return atomic_envs


def generate_bond_data(conformer,bonds):
    """Calculate the paiwise-distances among the atoms"""
    distance = [[0 for i in range(len(conformer))] for j in range(len(conformer))]
    for i, conformer_i in enumerate(conformer):
        for j, conformer_j in enumerate(conformer):
            distance[i][j] = np.linalg.norm(conformer_i-conformer_j)

    bondlist = []
    bonddistances = []
    for i, bonds_i in enumerate(bonds):
        for j in range(i):
            if bonds_i[j] == 1:
                bondlist.append([i,j])
                bonddistances.append(distance[i][j])

    return bondlist, bonddistances


def generate_bond_features(bonddistances, bondlist, atomtype):
    """get bond feature vector"""
    labels = []
    for bond, bondlist_bond in enumerate(bondlist):
        bond_feature = []
        if atomtype[bondlist_bond[0]] > atomtype[bondlist_bond[1]]:
            bond_feature += atomtype[bondlist_bond[0]] + atomtype[bondlist_bond[1]]
        else:
            bond_feature += atomtype[bondlist_bond[1]] + atomtype[bondlist_bond[0]]
        bond_feature.append(bonddistances[bond])
        labels.append(bond_feature)
    return labels


def generate_angle_data(conformer,bonds):
    """genrate data for angles"""
    angles_list = []
    for i in range(len(conformer)):
        for j in range(len(conformer)):
            for k in range(len(conformer)):
                if j!=i and j!=k and i>k and bonds[i][j]!=0 and bonds[j][k]!=0:
                    angles_list.append([i,j,k])

    angles = []
    for angle_triplet in angles_list:
        angle = get_angle(conformer[angle_triplet[0]], conformer[angle_triplet[1]], \
            conformer[angle_triplet[2]])
        angles.append(angle)
    return angles_list, angles


def get_angle(coor1,coor2,coor3):
    """calculate angle"""
    b_a =coor1 - coor2
    b_c = coor3 - coor2
    cosine_angle = np.dot(b_a, b_c) / (np.linalg.norm(b_a) * np.linalg.norm(b_c))
    if cosine_angle > 1.0:
        cosine_angle=1.0
    elif cosine_angle < -1.0:
        cosine_angle=-1.0
    if -1.0 <= cosine_angle <=1.0 :
        angle = np.arccos(cosine_angle)
        if angle > np.pi:
            angle=2*(np.pi)-angle
    return angle


def generate_angle_features(angles, angletype, atomtype,bondlist,bonddistances):
    """get angle feature vector"""
    labels = []
    for angle, angletype_angle in enumerate(angletype):
        anglefeature = []
        if atomtype[angletype_angle[0]] > atomtype[angletype_angle[2]]:
            anglefeature += atomtype[angletype_angle[0]] + atomtype[angletype_angle[2]]
            bondlen1 = get_bondlen(angletype_angle[0],angletype_angle[1],bondlist,bonddistances)
            bondlen2 = get_bondlen(angletype_angle[1],angletype_angle[2],bondlist,bonddistances)
        else:
            anglefeature += atomtype[angletype_angle[2]] + atomtype[angletype_angle[0]]
            bondlen1 = get_bondlen(angletype_angle[1],angletype_angle[2],bondlist,bonddistances)
            bondlen2 = get_bondlen(angletype_angle[0],angletype_angle[1],bondlist,bonddistances)

        anglefeature += atomtype[angletype_angle[1]]
        anglefeature += ([angles[angle],bondlen1,bondlen2])
        labels.append(anglefeature)
    return labels


def get_bondlen(i_1,i_2,bondtypelist,bondlenlist):
    """calculate bond length"""
    try:
        index = bondtypelist.index([i_1,i_2])
    except: # pylint: disable=bare-except
        index = bondtypelist.index([i_2,i_1])
    return bondlenlist[index]

def generate_nonbond_data(conformer,bonds,nonbondcutoff):
    """Calculate the paiwise-distances among the atoms"""
    distance = [[0 for i in range(len(conformer))] for j in range(len(conformer))]
    for i, conformer_i in enumerate(conformer):
        for j, conformer_j in enumerate(conformer):
            distance[i][j] = np.linalg.norm(conformer_i-conformer_j)
    nonbond_distances = []
    nonbond_list = []
    for i in range(len(conformer)):
        for j in range(len(conformer)):
            if i > j and distance[i][j] <  nonbondcutoff and (bonds[i][j] == 0 ) :
                nonbond_list.append([i,j])
                nonbond_distances.append(distance[i][j])
    return nonbond_list, nonbond_distances

def generate_dihedral_data(conformer,bonds):
    """genrate data for dihedral"""
    dihedral_list= []
    for i in range(len(conformer)):
        for j in range(len(conformer)):
            for k in range(len(conformer)):
                for l_ind in range(i):
                    if (i!=j and i!=k and j!=k and j!=l_ind):
                        if(bonds[i][j] == 1 and bonds[j][k]==1 and bonds[k][l_ind]==1):
                            dihedral_list.append([i,j,k,l_ind])

    dihedrals = []
    for dihed in dihedral_list:
        dihedral_angle = get_dihedral(conformer[dihed[0]],conformer[dihed[1]],\
            conformer[dihed[2]],conformer[dihed[3]])
        dihedrals.append(dihedral_angle)
    return dihedral_list,dihedrals


def get_dihedral(p_0, p_1, p_2, p_3):
    """calculate dihedral"""
    b_0=p_0-p_1
    b_1=p_2-p_1
    b_2=p_3-p_2

    b_0xb_1 = np.cross(b_0,b_1)
    b_1xb_2 = np.cross(b_2,b_1)

    b_0xb_1_x_b_1xb_2 = np.cross(b_0xb_1,b_1xb_2)
    y_y = np.dot(b_0xb_1_x_b_1xb_2, b_1)*(1.0/np.linalg.norm(b_1))
    x_x = np.dot(b_0xb_1, b_1xb_2)
    return np.arctan2(y_y, x_x)


def get_angleval(i_1,i_2,i_3,angletypelist,anglevallist):
    """calculate angle value"""
    try:
        index = angletypelist.index([i_1,i_2,i_3])
    except: # pylint: disable=bare-except
        index = angletypelist.index([i_3,i_2,i_1])

    return anglevallist[index]


def generate_dihedralangle_features(dihedrals, \
    atomtype,bondtypelist,bondlenlist,angles):

    """get dihedral feature vector"""
    # dihedral_angles = dihedrals[0]
    dihedral_list = dihedrals[1]
    # angletypelist =
    anglevallist = angles[1]
    labels = []
    for dihedral, dihedral_angle in enumerate(dihedrals[0]):
        dihedral_feature = []
        if atomtype[dihedral_list[dihedral][0]] > atomtype[dihedral_list[dihedral][3]]:
            index1 = 0
            index2 = 1
            index3 = 2
            index4 = 3
        else:
            index1 = 3
            index2 = 2
            index3 = 1
            index4 = 0

        dihedral_feature += atomtype[dihedral_list[dihedral][index1]] + \
            atomtype[dihedral_list[dihedral][index2]]
        dihedral_feature += atomtype[dihedral_list[dihedral][index3]] + \
            atomtype[dihedral_list[dihedral][index4]]

        dihedral_feature += (dihedral_angle, get_angleval(dihedral_list[dihedral][index1],\
            dihedral_list[dihedral][index2],dihedral_list[dihedral][index3], angles[0],\
            anglevallist), get_angleval(dihedral_list[dihedral][index2],\
            dihedral_list[dihedral][index3],dihedral_list[dihedral][index4],angles[0],\
            anglevallist), get_bondlen(dihedral_list[dihedral][index1],\
            dihedral_list[dihedral][index2], bondtypelist,bondlenlist),\
            get_bondlen(dihedral_list[dihedral][index2],\
            dihedral_list[dihedral][index3],bondtypelist,bondlenlist),\
            get_bondlen(dihedral_list[dihedral][index3],dihedral_list[dihedral][index4],\
            bondtypelist,bondlenlist))
        labels.append(dihedral_feature)
    return labels
