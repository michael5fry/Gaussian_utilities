#!/usr/bin/env
import numpy as np
import pandas as pd
import math

#-----------------------------------------------------------------------------------------------------
# -----------------TRAJECTORY AND MINIMA CREATOR -------------------------------------------------
#-----------------------------------------------------------------------------------------------------

def create_xyz_coord(lines_xyz):
    confinment = ' ---------------------------------------------------------------------\n'
    xyz_starter = []
    for i in lines_xyz:
        if i != confinment:
            xyz_starter.append(i)
        else:
            break
            
    xyz_coord = []
    atoms = []
    for i in range(len(xyz_starter)):
        data = xyz_starter[i].split()
        xyz_coord.append(data[1])
        xyz_coord.append('\t')
        xyz_coord.append(data[3])
        xyz_coord.append('\t')
        xyz_coord.append(data[4])
        xyz_coord.append('\t')
        xyz_coord.append(data[5])
        xyz_coord.append('\n')
        atoms.append(data[1])
        
    return np.array(xyz_coord), np.array(atoms)

#-----------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------

def TRJ_creator(file_name):
    starter = []
    with open(file_name, 'r') as fp:
        for i in fp:
            starter.append(i)
        
    # do a strong for loop to Obtain: 
    #the position of Rough xyz and SCF-Energy correlated to that configuration
    index_xyz, index_scf = [], []
    for i in range(len(starter)):
        if starter[i].find('Standard orientation: ')!=-1: # Rough xyz starting position
            index_xyz.append(i)
        if starter[i].find('SCF Done')!=-1: # Rough SCF-Energy correlated to that configuration
            index_scf.append(i)
    
    # Create the effective xyz coordinate of the optimized configurazion
    all_xyz_coord = []
    for i in range(len(index_xyz)):
        lines_xyz = starter[index_xyz[i]+5:index_xyz[i]+50000] #+5 first while +50000 is just a very big number 
                # use the defined function for to create each xyz      for which you encounter the confinment
        xyz_coord_n, atoms = create_xyz_coord(lines_xyz)
    
        # and append them on the list
        all_xyz_coord.append(xyz_coord_n)
    all_xyz_coord = np.array(all_xyz_coord)
    
    scf_energies=[float(starter[index_scf[i]].split()[4]) for i in range(len(index_scf))]
    
    #####################
    # writing Full TRJ:
    #####################
    
    file_name_no_extension=file_name.split('.')[0]

    intro =   ' ' + str(len(atoms)) + '\n'
    title = 'All Trajectories of '+file_name+' file from an Optimization cicle\n'
    subtitle = ', SCF energy: ' 
    with open( file_name_no_extension +'_trj.xyz', 'w') as fp:
        fp.write(intro)
        fp.write(title)
        for i in range(len(all_xyz_coord)):
            for j in range(len(all_xyz_coord[i])):
                fp.write(all_xyz_coord[i][j])
            if i != len(all_xyz_coord)-1:
                fp.write('\n')
                fp.write(intro)
                last_i=i
                fp.write('Configuration N° ' + str(i+1) + subtitle + str(scf_energies[i]) + ' hartree\n')
            else:
                pass
    #########################      
    # writing Local Minimum:
    #########################
    intro =   ' ' + str(len(atoms)) + '\n'
    title = 'Local Minimum Configuration N°'+ str(last_i+1)+':\t'+str(scf_energies[last_i])+' hartree\n'
    with open( file_name_no_extension +'_local-minima.xyz', 'w') as fp:
        fp.write(intro)
        fp.write(title)
        for k in range(len(all_xyz_coord[-1])):
            #for j in range(len(all_xyz_coord[i])):
            fp.write(all_xyz_coord[-1][k])
        fp.write('\n')
    
    print('TRJ File created\nThe name of the trajectory file is:',file_name_no_extension +'_trj.xyz')
    print('Local Minima configuration File created\nThe name of Local Minima configuration file is:',file_name_no_extension +'_local-minima.xyz')
    return print('Files produced correctly')

