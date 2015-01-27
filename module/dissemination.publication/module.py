#
# Collective Knowledge
#
# See CK LICENSE.txt for licensing details.
# See CK Copyright.txt for copyright details.
#
# Developer: Grigori Fursin
#

cfg={}  # Will be updated by CK (meta description of this module)
work={} # Will be updated by CK (temporal data)
ck=None # Will be updated by CK (initialized CK kernel) 

# Local settings
import shutil
import os
import json

# ============================================================================
def init(i):
    return {'return':0}

##############################################################################
# generate title

def generate(i):

    """
    Generating "low-hanging fruit" research topics and papers ;) 

    Input:  {
              data_uoa   - data with topic template
              (repo_uoa) - repository
            }

    Output: {
              return  - return code >0 if error
              string  - generated title
            }
    """

    import random

    md=i.get('out','')

    if md!='json':
       ck.out('This is a beta version of a research topic generator!')
       ck.out('')

       ck.out('Academic promotion is still often based on a total number of publications')
       ck.out('rather than novelty, usefulness, statistical meaningfulness, availability of code and data,')
       ck.out('and reproducibility of experimental results.')
       ck.out('Therefore, we decided to help some of our academic colleagues and created this customizable ')

       x=''
       x+='Collective Mind module'
       ck.out(x+' to automatically generate research topics in computer engineering') 
       ck.out('useful for grant proposals, PhD/MS theses, "low hanging fruit" and incremental articles.')

       ck.out('We hope it will be very appreciated by our community ;) !')
       ck.out('It should also continue making all reviewers and readers very happy')
       ck.out('with numerous and exciting articles!')

    du=i.get('data_uoa','')
    if du=='': 
       return {'return':1,'error':'data_uoa is not defined'}

    dr=i.get('repo_uoa','')

    ii={'module_uoa':work['self_module_uoa'],
        'action':'load',
        'data_uoa':du}
    if dr!='': ii['repo_uoa']=dr
    r=ck.access(ii)
    if r['return']>0: return r

    d=r['dict'].get('template_for_generator',[])

    # Generating topic
    s=''

    for q in d:
        t=q.get('text','')
        c=q.get('choice',[])

        if t!='':
           s+=t
        else:
           ll=len(c)
           l=random.randint(0,ll-1)
           s+=c[l]

    if md!='json':
       ck.out('')
       ck.out('Generated topic:')
       ck.out('')

       ck.out(s)

       ck.out('')
       ck.out('Simply restart this module to generate new exciting topic')
       ck.out('  or alternatively check out our manifesto at http://c-mind.org/reproducibility')
       ck.out('  on reproducibility in computer engineering!')

    return {'return':0, 'string':s}
