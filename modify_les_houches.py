#!/usr/bin/env python
import os
import shlex

def main(options,args) :
    base_file = open(options.file)
    fs = dict()
    weights = dict()
    variations = ['_1_1','_0.5_0.5','_1_0.5','_0.5_1','_1_2','_2_1','_2_2']
    for v in variations :
        if '%s%s'%(options.outdir,v) not in os.listdir('.') :
            os.mkdir('%s%s'%(options.outdir,v))
        fs[v] = open('%s%s/%s'%(options.outdir,v,options.file.split('/')[-1]),'w')
        weights[v] = ''
    #
    #
    #
    next_line_is_weight = False
    weight_line = ''
    weight_nom = ''
    everything_else = ''
    nline = 0
    for line in base_file :
        nline += 1
        if not nline%1000 :
            print 'processing line %10d'%(nline)
        #
        # Treatment of weight lines
        #
        if next_line_is_weight :
            weight_line = line
            weight_nom = shlex.split(weight_line)[2]
            #print weight_nom
            next_line_is_weight = False
            continue
        #elif '#rwgt' in line :
        #    continue
        elif '#new weight' in line :
            #
            # distribute weights
            #
            the_line = shlex.split(line)
            the_var =  '_%2.1f_%2.1f'%(float(the_line[3]),float(the_line[4]))
            the_var = the_var.replace('1.0','1')
            the_var = the_var.replace('2.0','2')
            #if the_var == '_1_1' : continue
            weights[the_var] += weight_line.replace(weight_nom,the_line[2])

        else :
            tmpline = line
            if tmpline.replace(' ','')[0] == '#' :
                tmpline = '#'+tmpline.lstrip(' #')
            everything_else += tmpline
        #
        # write out
        #
        if '<event>' in line :
            next_line_is_weight = True
            for v in variations :
                fs[v].write(weights[v]+everything_else)
                weights[v] = ''
            everything_else = ''
            weight_line = ''

    # write last event
    for v in variations :
        fs[v].write(weights[v]+everything_else)
        
    for v in variations :
        fs[v].close()
    base_file.close()

if __name__ == "__main__":
    from optparse import OptionParser
    p = OptionParser()

    p.add_option('--file' ,type='string' ,default='pwgevents-0001.lhe',dest='file' ,help='file')
    p.add_option('--outdir' ,type='string' ,default='OutDir',dest='outdir' ,help='file')
    options,args = p.parse_args()
    
    main(options,args)
