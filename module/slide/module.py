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
              (crop)               - if 'yes', crop 
              (uid)                - env UID to substitute, if empty use filebase
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

    duoa=i['data_uoa']
    muoa=i['module_uoa']
    f=i['file']

    crop=i.get('crop','')

    # Get path to entry
    r=ck.access({'action':'load',
                 'module_uoa':muoa,
                 'data_uoa':duoa})
    if r['return']>0: return r
    p=r['path']

    # Check file
    pp=os.path.join(p,f)

    uid=i.get('uid','')
    if uid=='':
       uid=os.path.splitext(f)[0]

    # Check crop
    if crop=='yes':
       fn,fe=os.path.splitext(f)
       fc=fn+'-cropped'+fe
       fcpng=fn+'-cropped.png'

       ppc=os.path.join(p,fc)
       ppcpng=os.path.join(p,fcpng)

       if os.path.isfile(ppc):
          os.remove(ppc)

       # Convert to cropped pdf
       os.system('pdfcrop '+pp+' '+ppc)

       # Check
       if not os.path.isfile(ppc):
          return {'return':1, 'error':'cropped file was not created'}

       # Convert to cropped png
       os.system('convert -density 300 -quality 100 -scale 800 '+ppc+' '+ppcpng)

       pp=ppc
       f=fc

    # Check braces
    if i.get('add_braces_to_file','')=='yes':
       px=os.path.dirname(pp)
       fn,fe=os.path.splitext(f)
       pp=os.path.join(px,'{'+fn+'}'+fe)

    # Update env vars
    sub={}
    sub['CK_PATH_'+uid]=pp.replace('\\','/') # convert path to Unix format

    return {'return':0, 'substitute':sub}
