import numpy as np
import itasca as it
it.command("python-reset-state false")

def define_reference_load_pos(h_high):
    #it.command("model restore 'StruProp.sav'")
    command = '''
    structure node group 'loading_ref' slot 'reference' range position-z {} group 'guoduduan' slot 'GuoDuDuan'
    structure node history displacement-x position 0 0 {}
    structure node history displacement-y position 0 0 {}
    structure node history displacement-z position 0 0 {}
    structure node history velocity-x position 0 0 {}
    structure node history velocity-y position 0 0 {}
    structure node history velocity-z position 0 0 {}
    '''.format(h_high,h_high,h_high,h_high,h_high,h_high,h_high)
    it.command(command)

#0 for Fx, 1 for Fy, 2 for Fz, 3 for Mx, 4 for My, 5 for Mz

def loading_sw(group,load,Type):
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
            sn_ref.set_apply(Type-1,load_n)
        elif Type == 4:
            load_n = -load*sn_ref.pos()[0]/Jy
            sn_ref.set_apply(Type-2,load_n)
        elif Type == 5:
            r = np.sqrt(sn_ref.pos()[0]**2+sn_ref.pos()[1]**2)
            theta = np.arcsin(sn_ref.pos()[1]/r)
            load_n = load*r/Jy
            if sn_ref.pos()[0] < 0:
                sn_ref.set_apply(Type-5,-load_n*np.sin(theta))
                sn_ref.set_apply(Type-4,-load_n*np.cos(theta))
            else:
                sn_ref.set_apply(Type-5,-load_n*np.sin(theta))
                sn_ref.set_apply(Type-4, load_n*np.cos(theta))

# loading('loading_ref', 1000, 0)
# loading('loading_ref', 1000, 1)
# loading('loading_ref', 1000, 2)
# loading('loading_ref', 1000, 5)


# Horizontal for horizontal direction, Diagonal for diagnoal direction

def loading_ice(load,pos_z,direction):
    load_n = load / 4.
    command = '''
    structure node group 'loading_ref_ice' slot 'reference' range position-z {} group 'zhutui' slot 'jacket'
    '''.format(pos_z)
    it.command(command)
    
    if direction == 'Horizontal':
        command = '''
        structure node apply force {} 0 0 range group 'loading_ref_ice' slot 'reference'
        '''.format(load_n)
        it.command(command)
    elif direction == 'Diagonal':
        command = '''
        structure node apply force {} {} 0 range group 'loading_ref_ice' slot 'reference'
        '''.format(load_n*np.sqrt(2),load_n*np.sqrt(2))
        it.command(command)

#Loading_ice(1000,4.0,2)

def state_load_factor(case_id,load_s,load_w,load_i,load_patern):
    # 0 for SLS with dominat load_s
    # 1 for SLS with dominat load_w, load_i
    # 2 for ULS with dominat load_s
    # 3 for ULS with dominat load_w, load_i
    
    global fac_s
    global fac_w
    global fac_i
    
    if case_id == 0:
        fac_s = [1.0,1.0,1.0,1.0,1.0,1.0]
        fac_w = [0.7,0.7,0.7,0.7,0.7,0.7]
        fac_i = [0.7,0.7,0.7,0.7,0.7,0.7]
    elif case_id == 1:
        fac_s = [0.7,0.7,0.7,0.7,0.7,0.7]
        fac_w = [1.0,1.0,1.0,1.0,1.0,1.0]
        fac_i = [1.0,1.0,1.0,1.0,1.0,1.0]
    elif case_id == 2:
        fac_s = [1.35*1.1*1.0, 1.35*1.1*1.0, 1.1, 1.35*1.1*1.0, 1.35*1.1*1.0, 1.35*1.1*1.0]
        fac_w = [1.35*1.1*0.7, 1.35*1.1*0.7, 1.35*1.1*0.7, 1.35*1.1*0.7, 1.35*1.1*0.7, 1.35*1.1*0.7]
        fac_i = [1.35*1.1*0.7, 1.35*1.1*0.7, 1.35*1.1*0.7, 1.35*1.1*0.7, 1.35*1.1*0.7, 1.35*1.1*0.7]
    elif case_id == 3:
        fac_s = [1.35*1.1*0.7, 1.35*1.1*0.7, 1.1, 1.35*1.1*0.7, 1.35*1.1*0.7, 1.35*1.1*0.7]
        fac_w = [1.35*1.1*1.0, 1.35*1.1*1.0, 1.35*1.1*1.0, 1.35*1.1*1.0, 1.35*1.1*1.0, 1.35*1.1*1.0]
        fac_i = [1.35*1.1*1.0, 1.35*1.1*1.0, 1.35*1.1*1.0, 1.35*1.1*1.0, 1.35*1.1*1.0, 1.35*1.1*1.0]
    
    for i in range(len(load_s)):
        load_s[i] = load_s[i] * fac_s[i]
        load_w[i] = load_w[i] * fac_w[i]
        load_i[i] = load_i[i] * fac_i[i]
        # if i < len(load_i):
            # load_i[i] = load_i[i] * fac_i[i]
    
    if load_patern == 'Horizontal':
        pass
    elif load_patern == 'Diagonal':
        load_s[0] = load_s[1] = load_s[0]/np.sqrt(2)
        load_s[3] = load_s[4] = load_s[4]/np.sqrt(2)
        load_w[0] = load_w[1] = load_w[0]/np.sqrt(2)
        load_w[3] = load_w[4] = load_w[4]/np.sqrt(2)
        load_i[0] = load_i[1] = load_i[0]/np.sqrt(2)
        load_i[3] = load_i[4] = load_i[4]/np.sqrt(2)
    
    return load_s,load_w,load_i

#Load_s,Load_w,Load_i = state_load_factor(case_id,Load_s,Load_w,Load_i)


def apply_loading(load):
    for i in range(0,6):
        loading_sw('loading_ref', load[i], i)


def apply_combined_loadings(combine_load_s,combine_load_w,combine_load_i,Load_s,Load_w,Load_i,pos_load_i,load_patern):
    if combine_load_s == 'YES':
        apply_loading(Load_s)
        if combine_load_w == 'YES':
            apply_loading(Load_w)
            if combine_load_i == 'YES':
                for i in range(0,6):
                    loading_ice(Load_i[i],pos_load_i,load_patern)

#apply_loadings(combine_load_s,combine_load_w,combine_load_i,pos_load_i,load_patern)










