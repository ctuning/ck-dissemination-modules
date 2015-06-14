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

##############################################################################
# viewing entry as html

def html_viewer(i):
    """
    Input:  {
              data_uoa

              url_base
              url_pull

              url_pull_tmp
              tmp_data_uoa

              url_wiki

              html_share

              form_name     - current form name

              (all_params)
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """
    import os

    h=''
    raw='no'
    top='yes'

    duoa=i['data_uoa']
    burl=i['url_base']
    purl=i['url_pull']
    wurl=i.get('url_wiki','')

    tpurl=i['url_pull_tmp']
    tpuoa=i['tmp_data_uoa']

    ap=i.get('all_params',{})

    ruoa=ap.get('ck_top_repo','')
    muoa=ap.get('ck_top_module','')

    cparams=ap.get('graph_params','') # current graph params

    hshare=i.get('html_share','')

    form_name=i['form_name']
    form_submit='document.'+form_name+'.submit();'

    if duoa!='':
       # Load entry
       rx=ck.access({'action':'load',
                     'module_uoa':work['self_module_uid'],
                     'data_uoa':duoa})
       if rx['return']>0: return rx

       pp=rx['path']

       dd=rx['dict']
       duid=rx['data_uid']

       if dd.get('live','')!='yes':
          raw='yes'
       else:
          title=dd.get('title','')
          authors=dd.get('authors',[])
          affs=dd.get('affiliations',{})
          cauthor=dd.get('cor_author_email','')

          h+='<div id="ck_entries">\n'
       
          h+='<center><span id="ck_article_title">'+title+'</span><br>'

          if len(authors)!='':
             h+='<div id="ck_entries_space4"></div>\n'
             h+='<span id="ck_article_authors">\n'

             x=''
             for a in authors:
                 name=a.get('name','')
                 aff=a.get('affiliation','')
                 url=a.get('url','')

                 if url!='': name='<a href="'+url+'">'+name+'</a>'

                 if x!='': x+=', '
                 x+=name+'&nbsp;<sup>'+aff+'</sup>'

             h+=x+'<br>\n'
             h+='</span>\n'

          if len(affs)>0:
             h+='<div id="ck_entries_space4"></div>\n'
             h+='<span id="ck_article_affiliations">\n'

             x=''
             for a in sorted(affs, key=int):
                 af=affs[str(a)]
                 name=af.get('name','')

                 if x!='': x+=',&nbsp;&nbsp;&nbsp;'
                 x+='<sup>'+str(a)+'</sup>&nbsp;'+name

             h+=x+'<br>\n'
             h+='</span>\n'

          h+='</center>\n'

          if len(cauthor)>0:
             h+='<div id="ck_entries_space4"></div>\n'
             h+='<span id="ck_article_cauthor">\n'
             h+='<i>Corresponding author: <a href="mailto:'+cauthor+'">'+cauthor+'</a></i>\n'
             h+='</span>\n'

          h+='<div id="ck_entries_space4"></div>\n'
          h+='<div id="ck_entries_space4"></div>\n'
          h+='<div id="ck_entries_space4"></div>\n'
          h+='<div id="ck_entries_space4"></div>\n'

          # Checking template
          t=dd.get('template','')
          if t!='':
             h+='<span id="ck_article_text">\n'

             px=os.path.join(pp,t)
             if os.path.isfile(px):
                rx=ck.load_text_file({'text_file':px})
                if rx['return']>0: return rx
                th=rx['string']



             h+=th

             h+='</span\n'

          h+='</div>\n'

    return {'return':0, 'raw':raw, 'show_top':top, 'html':h}
