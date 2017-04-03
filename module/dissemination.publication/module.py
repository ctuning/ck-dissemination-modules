#
# Collective Knowledge
#
# See CK LICENSE.txt for licensing details.
# See CK COPYRIGHT.txt for copyright details.
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
    txt+='(useful for grant proposals, PhD/MS theses, "low hanging fruit" and incremental articles).'+'\n'

    txt+=on+'\n'
    txt+='We hope it will be very appreciated by the academic community ;) !\n'
    txt+='It should make all reviewers and readers even more happy\n'
    txt+='when trying to process all those numerous exciting publications!\n'
    txt+='We also found that it is even possible to predict which papers will be published\n'
    txt+='within next few years (our observations for the past decade are surprisingly correct)!\n'

    du=i.get('data_uoa','')
    if du=='': du='template-joke'

#    if du=='': 
#       return {'return':1,'error':'data_uoa is not defined'}

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

    selected=False
    swn=False

    for q in d:
        t=q.get('text','')

        p=q.get('probability','')
        if p=='': p=1.0
        p=float(p)

        c=q.get('choice',[])

        # Check if select with next and previous was not selected:
        if swn:
           swn=False

           if not selected:
              continue

        xswn=q.get('select_with_next','')
        if xswn=='yes': swn=True

        # Check to select
        selected=False
        x=float(random.randint(0,1000))/1000
        if x<p:
           selected=True

        if selected:
           if t!='':
              s+=t

           ll=len(c)
           if ll>0:
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
    txt+='  '+x+'\n'
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

    if html:
       txt+=on+'\n'
       txt+='Simply restart this module to generate next exciting topic\n'
       txt+='or alternatively check out our '+x1+', '+x2+', and '+x3+' to enable systematic, collaborative and reproducible R&D.\n\n'

       txt+='<hr>\n'
       txt+='You can even automate generation of these topics from CMD using our <a href="http://github.com/ctuning/ck">CK</a> framework:<br>\n'
       txt+='&nbsp;&nbsp;>&nbsp;ck pull repo:ck-dissemination --url=https://github.com/gfursin/ck-dissemination.git<br>\n'
       txt+='&nbsp;&nbsp;>&nbsp;ck generate dissemination.publication:template-joke<br>\n'

       txt+='<br><br><small><i>\n'

       txt+='Powered by Collective Knowledge, (C)opyright '

       txt+='<a href="http://fursin.net/research">'
       txt+='Grigori Fursin'
       txt+='</a>'
       txt+=', 2012-2015\n'

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

              html         - generated HTML

              raw          - if 'yes', output in CK raw format
              show_top     - if 'yes', include CK top header with QR-code
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

          when=dd.get('when','')
          where=dd.get('where','')
          where_url=dd.get('where_url','')
          if where!='' and where_url!='':
             where='<a href="'+where_url+'">'+where+'</a>'

          appeared=where
          if when!='':
             if appeared!='': appeared+=', '
             appeared+=when

          h+='<div id="ck_entries">\n'
       
          h+='<center><span id="ck_article_title">'+title+'</span><br>'

          if appeared!='':
             h+='<div id="ck_entries_space4"></div>\n'
             h+='<span id="ck_article_authors" style="font-style: normal;">\n'
             h+=appeared+'\n'
             h+='</span>\n'

          if len(authors)!='':
             h+='<div id="ck_entries_space8"></div>\n'
             h+='<div id="ck_entries_space8"></div>\n'
             h+='<span id="ck_article_authors">\n'

             x=''
             for a in authors:
                 name=a.get('name','')
                 aff=a.get('affiliation','')
                 url=a.get('url','')

                 if ck.is_uid(name):
                    # Name is UID, load entry
                    r=ck.access({'action':'load',
                                 'module_uoa':cfg['module_deps']['person'],
                                 'data_uoa':name})
                    if r['return']>0: return r
                    ad=r['dict']

                    name=ad.get('name','')

                 name=name.replace(' ','&nbsp;')
                 if url!='': name='<a href="'+url+'">'+name+'</a>'

                 if x!='': x+=', '
                 x+=name+'&nbsp;<sup>'+aff+'</sup>'

             h+=x+'<br>\n'
             h+='</span>\n'

          if len(affs)>0:
             h+='<div id="ck_entries_space8"></div>\n'
             h+='<span id="ck_article_affiliations">\n'

             x=''
             for a in sorted(affs, key=int):
                 af=affs[str(a)]
                 name=af.get('name','').replace(' ','&nbsp;')

                 if x!='': x+=', '
                 x+='<sup>'+str(a)+'</sup>&nbsp;'+name

             h+=x+'<br>\n'
             h+='</span>\n'

          h+='</center>\n'

          if len(cauthor)>0:
             h+='<div id="ck_entries_space8"></div>\n'
             h+='<span id="ck_article_cauthor">\n'
             h+='<i>Corresponding author: <a href="mailto:'+cauthor+'">'+cauthor+'</a></i>\n'
             h+='</span>\n'

          if hshare!='':
             h+='<div id="ck_entries_space8"></div>\n'
             h+=hshare
             h+=' <div id="ck_entries_space8"></div>\n'

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

##############################################################################
# preprocess LaTex papers

def preprocess(i):
    """
    Input:  {
              doc - paper to preprocess (LaTex file)
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    doc=i['doc']

    ck.out('')
    ck.out('Loading document '+doc+' ...')

    r=ck.load_text_file({'text_file':doc})
    if r['return']>0: return r

    s_orig=r['string']

    l=s_orig.split('\n')
    ll=len(l)

    ck.out('')
    ck.out('Processing document ...')

    changed=False

    cur_ck=''
    detected=False

    j=0
    while j<ll:
       s=l[j]
       j+=1

       sx=s.strip()
       if detected:
          if not cur_ck.endswith('}') and sx.startswith('%'):
             cur_ck+=sx[1:].strip()
          else:
             detected=False

             ck.out('')
             ck.out('* Detected CK instruction:')
             ck.out('')
             ck.out('    '+cur_ck)

             # Convert from JSON to dict
             r=ck.convert_json_str_to_dict({'str':cur_ck, 'skip_quote_replacement':'yes'})
             if r['return']>0: return r
             ii=r['dict']

             action=ii['action']
             cid=ii.get('cid','')
             tp=ii.get('type','path')

             ck.out('')
             r=ck.access(ii)
             if r['return']>0: return r

             sub=r.get('substitute',{})

             # Substituting
             for k in sub:
                 v='%'+k
                 j1=j
                 while j1<ll:
                     ss=l[j1]
                     js=ss.find(v)
                     if js>0:
                        if tp=='path':
                           k1=ss.find('{')
                           if k1>0 and ss.rfind('}')>0:
                              k2=ss.rfind('}')
                              s1=ss[:k1+1]
                              s2=ss[k2:]
                           else:
                              s1=''
                              s2=ss[js:]
                           l[j1]=s1+sub[k]+s2
                        elif tp=='textlet':
                           j1+=1
                           l[j1]=sub[k]
                           j1+=1
                           while j1<len(l):
                              if l[j1].find(v+'_END')>=0:
                                 break
                              del(l[j1]) 

                        ll=len(l)

                        changed=True

                     j1+=1

       if sx.startswith('%CK={'):
          cur_ck=sx[4:]
          detected=True

    if changed:
       fbak=doc+'.bak'

       ck.out('')
       ck.out('Document changed, backing up to '+fbak+' ...')

       r=ck.save_text_file({'text_file':fbak, 'string':s_orig})
       if r['return']>0: return r

       ck.out('')
       ck.out('Updating document '+doc+' ...')

       s=''
       for x in l:
           s+=x+'\n'

       r=ck.save_text_file({'text_file':doc, 'string':s})
       if r['return']>0: return r
       

    return {'return':0}
