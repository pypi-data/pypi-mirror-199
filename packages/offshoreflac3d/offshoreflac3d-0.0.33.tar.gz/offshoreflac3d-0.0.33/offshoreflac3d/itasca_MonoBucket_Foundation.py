import numpy as np
import itasca as it
it.command("python-reset-state false")

def foundation(mudline,L,scour_depth,factor,thickness_skirt,thickness_cap):
    it.command("model restore 'Initial'")
    
    for z in it.zone.list():
        groups = ['Volume1','Volume2','Volume3']
        for group in groups:
            if z.in_group(group):
                z.set_group('suction caisson','SC')
    
        groups = ['Volume4','Volume5','Volume6','Volume7','Volume8','Volume9','Volume10','Volume11']
        for group in groups:
            if z.in_group(group):
                z.set_group('NoSC','SC')
    
    
    command = '''
    structure liner create by-zone-face id 11 group 'Cap' slot 'SC' element-type=dkt-cst range position-z {} group 'suction caisson' slot 'SC'
    zone face group 'InterFace' slot '1' internal range group 'NoSC' slot 'SC' group 'suction caisson' slot 'SC' position-z {} {}
    zone separate by-face new-side group 'InterFace2' range group 'InterFace' slot '1'
    structure liner create by-face id 11 group 'Skirt' slot 'SC' element-type=dkt-cst embedded range group 'InterFace2'
    
    structure liner group 'bucket' range group 'Skirt' slot 'SC'
    structure liner group 'bucket' range group 'Cap' slot 'SC'
    '''.format(mudline,mudline-L,mudline)
    it.command(command)
    
    command = '''
    structure liner property isotropic 2.1e8 0.3
    structure liner property density 7.85 thickness {} range group 'Skirt' slot 'SC'
    structure liner property density 0.08 thickness {} range group 'Cap' slot 'SC'
    structure node join
    '''.format(thickness_skirt,thickness_cap)
    it.command(command)
    
    command = '''
    fish define Interaction
        loop foreach local _se struct.list(struct.group(::struct.list)=='bucket')
            struct.liner.normal.stiffness(_se,1)=(zone.prop(zone.near(struct.pos(_se)),'bulk')+4*zone.prop(zone.near(struct.pos(_se)),'shear')/3)/0.5*20.0
            struct.liner.normal.stiffness(_se,2)=(zone.prop(zone.near(struct.pos(_se)),'bulk')+4*zone.prop(zone.near(struct.pos(_se)),'shear')/3)/0.5*20.0
            struct.liner.shear.stiffness(_se,1)=(zone.prop(zone.near(struct.pos(_se)),'bulk')+4*zone.prop(zone.near(struct.pos(_se)),'shear')/3)/0.5*20.0
            struct.liner.shear.stiffness(_se,2)=(zone.prop(zone.near(struct.pos(_se)),'bulk')+4*zone.prop(zone.near(struct.pos(_se)),'shear')/3)/0.5*20.0
            local angle = zone.prop(zone.near(struct.pos(_se)),'friction')
            struct.liner.shear.friction(_se,1)=math.atan(math.tan(angle*math.pi/180)*{})/math.pi*180
            struct.liner.shear.friction(_se,2)=math.atan(math.tan(angle*math.pi/180)*{})/math.pi*180
            struct.liner.shear.cohesion(_se,1)=zone.prop(zone.near(struct.pos(_se)),'cohesion')*{}
            struct.liner.shear.cohesion(_se,2)=zone.prop(zone.near(struct.pos(_se)),'cohesion')*{}
        endloop
    end
    '''.format(factor,factor,factor,factor)
    it.command(command)
    it.fish.call_function('Interaction')
    
    command ='''
    structure liner property slide off
    structure link tolerance-slide 1.5
    '''
    it.command(command)
    
    command ='''
    zone delete range position-z {} {} group 'suction caisson' slot 'SC' not
    model solve ratio 1e-6
    model save 'Foundation.sav'
    '''.format(mudline,mudline-scour_depth)
    it.command(command)

