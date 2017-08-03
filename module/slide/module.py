#
# Collective Knowledge (individual slides)
#
# See CK LICENSE.txt for licensing details
# See CK COPYRIGHT.txt for copyright details
#
# Developer: Grigori Fursin, Grigori.Fursin@cTuning.org, http://fursin.net
#

cfg={}  # Will be updated by CK (meta description of this module)
work={} # Will be updated by CK (temporal data)
ck=None # Will be updated by CK (initialized CK kernel) 

# Local settings

##############################################################################
# Initialize module

def init(i):
    """

    Input:  {}

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """
    return {'return':0}

##############################################################################
# prepare slide for latex

def prepare_for_latex(i):
    """
    Input:  {
              data_uoa             - slide entry
              file                 - slide file to process (in pdf)
              (uid)                - env UID to substitute, if empty use filebase
              (extra_uid)          - append to the beginning of the output file
              (add_braces_to_file) - if 'yes', add {} to filename before extension (to allow . in filename)
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              sub          - dict with substitutes for LaTeX
            }

    """

    import os
    import filecmp
    import shutil

    duoa=i['data_uoa']
    muoa=i['module_uoa']
    f=i['file']

    path=i.get('path','')

    # Get path to entry
    r=ck.access({'action':'load',
                 'module_uoa':muoa,
                 'data_uoa':duoa})
    if r['return']>0: return r
    p=r['path']

    # Check file
    pp=os.path.join(p,f)

    if not os.path.isfile(pp):
       return {'return':1, 'error':'file "'+pp+'" not found'}

    uid=i.get('uid','')
    if uid=='':
       uid=os.path.splitext(f)[0]

    # New path
    ppn=os.getcwd()

    if path!='':
       ppn=os.path.join(ppn,path)

    ppd=ppn

    euid=i.get('extra_uid','')
    if euid!='':
       # also replace dots to avoid problems in LaTex
       f0,f1=os.path.splitext(f)

       f=euid+'-'+f0.replace('.','-')+f1

    ppn=os.path.join(ppn,f)

    # Check if files are not the same
    if not os.path.isfile(ppn) or not filecmp.cmp(pp,ppn):
       if not os.path.isdir(ppd):
          os.makedirs(ppd)

       ck.out('Copying file '+f+' to '+path+' ...')
       shutil.copyfile(pp,ppn)

    # Check braces
    if i.get('add_braces_to_file','')=='yes':
       px=os.path.dirname(pp)
       fn,fe=os.path.splitext(f)
       pp=os.path.join(px,'{'+fn+'}'+fe)

    # Update env vars
    sub={}
    sub['CK_PATH_'+uid]=pp.replace('\\','/') # convert path to Unix format

    return {'return':0, 'substitute':sub}

##############################################################################
# convert to various format

def convert(i):
    """
    Input:  {
               data_uoa             - slide entry
               (file)               - file to convert

               (density)            - png density
               (quality)            - png quality
               (scale)              - png scale
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    import os

    duoa=i['data_uoa']
    muoa=i['module_uoa']
 
    # Get path to an entry
    r=ck.access({'action':'load',
                 'module_uoa':muoa,
                 'data_uoa':duoa})
    if r['return']>0: return r
    d=r['dict']
    p=r['path']

    pd=i.get('density','')
    if pd=='': 
       pd=d.get('density','')
       if pd=='':
          pd='300'

    pq=i.get('quality','')
    if pq=='': 
       pq=d.get('quality','')
       if pq=='': 
          pq='100'

    ps=i.get('scale','')
    if ps=='':
       ps=d.get('scale','')
       if ps=='':
          ps='800'

    slides=d.get('slides',[])

    f=i.get('file','')
    if f!='':
       f=os.path.splitext(f)[0]
       slides=[f]

    # Processing slides
    for fn in slides:
        ck.out('==================================================================================')
        ck.out('* '+fn)
        ck.out('')

        f=fn+'.pdf'
        pp=os.path.join(p,f)

        fc=fn+'-cropped.pdf'
        fcpng=fn+'-cropped.png'

        ppc=os.path.join(p,fc)
        ppcpng=os.path.join(p,fcpng)

        if os.path.isfile(ppc):
           os.remove(ppc)

        # Convert to cropped pdf
        s='pdfcrop '+pp+' '+ppc
        ck.out(s)
        os.system(s)

        # Check
        if not os.path.isfile(ppc):
           return {'return':1, 'error':'cropped file was not created'}

        # Convert to cropped png
        s='convert -density '+str(pd)+' -quality '+str(pq)+' -scale '+str(ps)+' '+ppc+' '+ppcpng
        ck.out('')
        ck.out(s)
        os.system(s)

        # Check
        if not os.path.isfile(ppcpng):
           return {'return':1, 'error':'PNG file was not created'}

    return {'return':0}
