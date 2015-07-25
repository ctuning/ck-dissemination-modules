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
              (html)     - if 'yes', force html
            }

    Output: {
              return  - return code >0 if error
              string  - generated title
            }
    """

    import random

    o=i.get('out','')

    html=False
    if i.get('html','')=='yes': html=True

    on=''
    if html: on='<br><br>'

    txt=''

    x='This is a beta version of a research topic generator!'
    if html: x='<b>'+x+'</b>'
    txt+=x+'\n'
    txt+=on+'\n'

    txt+='Academic promotion is still often based on a total number of publications'+'\n'
    txt+='rather than novelty, usefulness, statistical meaningfulness, availability of code and data,'+'\n'
    txt+='and reproducibility of experimental results.'+'\n'

    txt+=on+'\n'
    txt+='Therefore, some years ago, we decided to help some of our academic colleagues and created this customizable '+'\n'

    x=''
    x+='Collective Knowledge module'
    txt+=x+' to automatically generate research topics in computer engineering'+'\n' 
    txt+='useful for grant proposals, PhD/MS theses, "low hanging fruit" and incremental articles.'+'\n'

    txt+=on+'\n'
    txt+='We hope it will be very appreciated by our community ;) !\n'
    txt+='It should also continue making all reviewers and readers very happy\n'
    txt+='with all those numerous and exciting articles!\n'
    txt+='We also found that it is even possible to predict which papers will be published\n'
    txt+='within next few years (our observations started from 2012 are surprisingly correct)!\n'

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

    txt+=on+'\n'
    x='Generated topic:'
    if html: x='<b>'+x+'</b>'
    txt+=x+'\n'
    txt+=on+'\n'

    if html: txt+='<i><span style="color:#7f0000;">'
    x=s
    if html: x='<b>'+s+'</b>'
    txt+=x+'\n'
    if html: txt+='</span></i>'

    x1='wiki'
    if html: x1='<a href="http://cknowledge.org/reproducibility">'+x1+'</a>'
    else: x1+=' (cknowledge.org/reproducibility)'

    x2='open-source framework and repository'
    if html: x2='<a href="http://github.com/ctuning/ck">'+x2+'</a>'
    else: x2+=' (github.com/ctuning/ck)'

    x3='new publication model'
    if html: x3='<a href="https://hal.inria.fr/hal-01006563">'+x3+'</a>'
    else: x3+=' (hal.inria.fr/hal-01006563)'

    txt+=on+'\n'
    txt+='Simply restart this module to generate next exciting topic\n'
    txt+='  or alternatively check out our '+x1+', '+x2+', and '+x3+' to enable systematic, collaborative and reproducible R&D.\n'

    if html:
       txt+='<hr>\n'
       txt+='You can even automate generation of these topics from CMD using our <a href="http://github.com/ctuning/ck">CK</a> framework:<br>\n'
       txt+='&nbsp;&nbsp;>&nbsp;ck pull repo:ck-dissemination --url=https://github.com/gfursin/ck-dissemination.git<br>\n'
       txt+='&nbsp;&nbsp;>&nbsp;ck generate dissemination.publication:template-joke<br>\n'

    if html:
       txt+='<br><br><small><i>\n'

    txt+='Powered by Collective Knowledge, (C)opyright '

    if html='<a href="http://fursin.net/research">'
    txt+='Grigori Fursin'
    if html='</a>'

    txt+=', 2012-2015\n'

    if html:
       txt+='</i></small>\n'
       
    # Output if not JSON
    if o!='json' and o!='json_file':
       ck.out(txt)

    r={'return':0}
    if html: r['html']=txt
    else: r['string']=s

    return r

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
    top='no'

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

          if hshare!='':
             h+='<div id="ck_entries_space4"></div>\n'
             h+=hshare
             h+=' <div id="ck_entries_space4"></div>\n'

          h+='<div style="text-align: right;">'
          if wurl!='':
             h+='[&nbsp;<a href="'+wurl+'">Discussion wiki (comments, reproducibility, etc.)</a>&nbsp;]'
          h+='</div>\n'

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

                th=th.replace('$#ck_root_url#$', burl)

             h+=th

             h+='</span\n'

          h+='</div>\n'

    return {'return':0, 'raw':raw, 'show_top':top, 'html':h}
