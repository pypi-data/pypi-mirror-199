import numpy as np 
from shapely import geometry as geo
import itasca as it
it.command("python-reset-state false")


    
def definition_pos_ref(h_high,h_mudline):
    it.command("model restore 'Foundation'")
    
    command ='''
    zone gridpoint initialize displacement 0.0 0.0 0.0
    zone gridpoint initialize velocity 0.0 0.0 0.0
    structure node initialize displacement 0.0 0.0 0.0
    structure node initialize displacement-rotational 0.0 0.0 0.0
    structure node initialize velocity 0.0 0.0 0.0
    structure node initialize velocity-rotational 0.0 0.0 0.0
    '''
    it.command(command)

    command = '''
    structure node group 'loading_ref' slot 'reference' range position-z [mudline] group 'Skirt' slot 'SC'
    structure node history displacement-x position 0 0 [mudline]
    structure node history displacement-y position 0 0 [mudline]
    structure node history displacement-z position 0 0 [mudline]
    structure node history velocity-x position 0 0 [mudline]
    structure node history velocity-y position 0 0 [mudline]
    structure node history velocity-z position 0 0 [mudline]
    '''
    it.command(command)

#0 for Fx, 1 for Fy, 2 for Fz, 3 for Mx, 4 for My, 5 for Mz

def loading(group,load,Type):
    Jx = Jy = Jp = 0
    Node_ref = []
    N = 0
    for sn in it.structure.node.list():
        if sn.group('reference') == group:
            Jx = Jx + sn.pos()[0]**2
            Jy = Jx
            Jp = Jx + Jy
            Node_ref.append(sn)
            N = N + 1

    load_n = load / N

    for sn_ref in Node_ref:
        if Type == 0:
            sn_ref.set_apply(Type,load_n)
        elif Type == 1:
            sn_ref.set_apply(Type,load_n)
        elif Type == 2:
            sn_ref.set_apply(Type,load_n)
        elif Type == 3:
            load_n = load*sn_ref.pos()[1]/Jx
            load_n_final = sn_ref.apply()[0][2] + load_n
            sn_ref.set_apply(Type-1,load_n_final)
        elif Type == 4:
            load_n = -load*sn_ref.pos()[0]/Jy
            load_n_final = sn_ref.apply()[0][2] + load_n
            sn_ref.set_apply(Type-2,load_n_final)
        elif Type == 5:
            r = np.sqrt(sn_ref.pos()[0]**2+sn_ref.pos()[1]**2)
            theta = np.arcsin(sn_ref.pos()[1]/r)
            load_n = load*r/Jy
            if sn_ref.pos()[0] < 0:
                load_n_final_x = sn_ref.apply()[0][0] + -load_n*np.sin(theta)
                load_n_final_y = sn_ref.apply()[0][1] + -load_n*np.cos(theta)
                sn_ref.set_apply(Type-5,load_n_final_x)
                sn_ref.set_apply(Type-4,load_n_final_y)
            else:
                load_n_final_x = sn_ref.apply()[0][0] + -load_n*np.sin(theta)
                load_n_final_y = sn_ref.apply()[0][1] +  load_n*np.cos(theta)
                sn_ref.set_apply(Type-5,load_n_final_x)
                sn_ref.set_apply(Type-4,load_n_final_y)

# loading('loading_ref', 1000, 0)
# loading('loading_ref', 1000, 1)
# loading('loading_ref', 1000, 2)
# loading('loading_ref', 1000, 5)
