#
# Collective Knowledge (automating ACM proceedings with papers and artifacts)
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
# generate ACM proceedings

def generate(i):
    """
    Input:  {
              data_uoa - proceedings entry
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    import os

    o=i.get('out','')

    # Check entry name
    duoa=i.get('data_uoa','')
    if duoa=='':
       return {'return':1, 'error':'proceedings entry is not specified. Use "ck generate proceedings.acm:{proceedings name such as request.asplos18}"'}

    # Load entry
    r=ck.access({'action':'load',
                 'module_uoa':work['self_module_uid'],
                 'data_uoa':duoa})
    if r['return']>0: return r

    d=r['dict']
    p=r['path']

    # Check abstract
    fa=os.path.join(p,'abstract.html')
    abstract=''
    if os.path.isfile(fa):
       r=ck.load_text_file({'text_file':fa})
       if r['return']>0: return r
       abstract=r['string']

    # Get various meta
    url=d['url']
    short_name=d['short_name']
    
    # Get list of artifacts (papers, etc)
    artifacts=d.get('ck_artifacts',[])

    # Load artifacts
    ck.out('Reading CK artifacts (papers, code, data, etc) ...')
    ck.out('')

    for a in artifacts:
        aduoa=a['data_uoa']

        ck.out('* '+aduoa)

        # Load artifact
        ii={'action':'load',
            'module_uoa':cfg['module_deps']['artifact'],
            'data_uoa':aduoa}

        r=ck.access(ii)
        if r['return']>0: return r

        a['dict']=r['dict']
        a['path']=r['path']

        # Load paper
        ii={'action':'load',
            'module_uoa':cfg['module_deps']['dissemination.publication'],
            'data_uoa':aduoa}

        r=ck.access(ii)
        if r['return']>0: return r

        a['paper_dict']=r['dict']
        a['paper_path']=r['path']

    # Generate table of evaluated artifacts for http://cTuning.org/ae/artifacts.html
    f='ctuning-ae-artifacts-'+duoa+'.html'

    anchor=short_name.lower().replace("'","")

    h=' <li><a href="#'+anchor+'">'+short_name+'</a></li>\n'
    h+='\n'

    h+='<!------------------------------------------------>\n'
    h+='<a name="'+anchor+'"><h2>Accepted artifacts for '+short_name+'</h2>\n'
    h+='\n'
    h+='<i>[ <a href="'+url+'">'+short_name+' AE website</a> ]</i>\n'
    h+='\n'

    h+='<p>\n'
    h+='<!-- <i> Notes\n'
    h+='</i> !-->\n'
    h+='\n'

    hartifacts=''

    hartifacts+='<table border="1" style="border-width: 1px;border-spacing:0px;" cellpadding="5">\n'

    hartifacts+=' <tr>\n'
    hartifacts+='  <td valign="top"><b>Paper</b></td>\n'
    hartifacts+='  <td valign="top"><b>Artifact available</b></td>\n'
    hartifacts+='  <td valign="top"><b>Artifact functional</b></td>\n'
    hartifacts+='  <td valign="top"><b>Artifact reusable</b></td>\n'
    hartifacts+='  <td valign="top"><b>Results reproduced</b></td>\n'
    hartifacts+='  <td valign="top"><b>Results replicated</b></td>\n'
    hartifacts+=' </tr>\n'

    for a in artifacts:
        aduoa=a['data_uoa']

        da=a['dict']
        dp=a['paper_dict']

        paper_doi=da.get('paper_doi','')
        artifact_doi=da.get('artifact_doi','')

        title=dp.get('title','')

        ck_results=da.get('ck_results','')
        ck_workflow=da.get('ck_workflow','')
        original_repo=da.get('original_repo','')

        authors=dp.get('authors',[])
        xauthors=''
        for q in authors:
            name=q.get('name','')
            if name!='':
               # Check if has entry or just a name
               r=ck.access({'action':'load',
                            'module_uoa':cfg['module_deps']['person'],
                            'data_uoa':name})
               if r['return']==0:
                  x=r['dict'].get('name','')
                  if x!='': name=x

            if xauthors!='':
               xauthors+=', '

            xauthors+=name

        badges=da.get('acm_badges',{})

        b_available=badges.get('available','').lower()=='yes'
        b_functional=badges.get('functional','').lower()=='yes'
        b_reusable=badges.get('reusable','').lower()=='yes'
        b_reproduced=badges.get('reproduced','').lower()=='yes'
        b_replicated=badges.get('replicated','').lower()=='yes'

        hartifacts+=' <tr>\n'

        x='<b>'+title+'</b><br><i>'+xauthors+'</i><p>\n'
        if paper_doi!='':
           x+=' [ <a href="'+paper_doi+'">Paper DOI</a> ]'
        if artifact_doi!='':
           x+=' [ <a href="'+artifact_doi+'">Artifact DOI</a> ]\n'
        if original_repo!='':
           x+=' [ <a href="'+original_repo+'">Original artifact</a> ]\n'
        if ck_workflow!='':
           x+=' [ <a href="'+ck_workflow+'">CK workflow</a> ]\n'
        if ck_results!='':
           x+=' [ <a href="'+ck_results+'">CK results</a> ]\n'

        hartifacts+='  <td valign="top">\n'
        hartifacts+='   '+x+'\n'
        hartifacts+='  </td>\n'

        x=''
        if b_available:
           x='<img src="https://www.acm.org/binaries/content/gallery/acm/publications/replication-badges/artifacts_available_dl.jpg" width="64"><br>'
        hartifacts+='  <td valign="top" align="center">'+x+'</td>\n'

        x=''
        if b_functional and not b_reusable:
           x='<img src="https://www.acm.org/binaries/content/gallery/acm/publications/replication-badges/artifacts_evaluated_functional_dl.jpg" width="64"><br>'
        hartifacts+='  <td valign="top" align="center">\n'
        hartifacts+='   '+x+'\n'
        hartifacts+='  </td>\n'

        x=''
        if b_reusable:
           x='<img src="https://www.acm.org/binaries/content/gallery/acm/publications/replication-badges/artifacts_evaluated_reusable_dl.jpg" width="64"><br>'
        hartifacts+='  <td valign="top" align="center">\n'
        hartifacts+='   '+x+'\n'
        hartifacts+='  </td>\n'

        x=''
        if b_reproduced:
           x='<img src="https://www.acm.org/binaries/content/gallery/acm/publications/replication-badges/results_reproduced_dl.jpg" width="64"><br>'
        hartifacts+='  <td valign="top" align="center">\n'
        hartifacts+='   '+x+'\n'
        hartifacts+='  </td>\n'

        x=''
        if b_replicated:
           x='<img src="https://www.acm.org/binaries/content/gallery/acm/publications/replication-badges/results_replicated_dl.jpg" width="64"><br>'
        hartifacts+='  <td valign="top" align="center">\n'
        hartifacts+='   '+x+'\n'
        hartifacts+='  </td>\n'

        hartifacts+=' </tr>\n'

    hartifacts+='</table>\n'
    h+=hartifacts

    r=ck.save_text_file({'text_file':f, 'string':h})
    if r['return']>0: return r

    # Generating summary for ACM DL
    fs='acm-proceedings-summary-'+duoa+'.html'

    hsummary=''

    name=d.get('name','')
    if name!='':
       hsummary+='<h3>Proceedings of the '+name+'</h3>\n'
       hsummary+='\n'

    if abstract!='':
       hsummary+='<p>\n'
       hsummary+='<b>Abstract</b>\n'
       hsummary+='<p>\n'
       hsummary+=abstract+'\n'

    organizers=d.get('organizers',[])
    if len(organizers)>0:
       hsummary+='<p>\n'
       hsummary+='<b>Organizers</b>\n'
       hsummary+='<ul>\n'
       for q in organizers:
           oname=q.get('name','')
           oaff=q.get('affiliation','')
           oextra=q.get('extra','')

           if oname!='':
              # Read name
              r=ck.access({'action':'load',
                           'module_uoa':cfg['module_deps']['person'],
                           'data_uoa':oname})
              if r['return']==0:
                 x=r['dict'].get('name','')
                 if x!='': oname=x

              hsummary+=' <li><b>'+oname+'</b>'
              if oaff!='':
                 hsummary+=', '+oaff
              if oextra!='':
                 hsummary+=' (<i>'+oextra+'</i>)'
              hsummary+='\n'

       hsummary+='</ul>\n'

    host_conference=d.get('host_conference','')
    host_conference_url=d.get('host_conference_url','')
    if host_conference!='':
       hsummary+='<p>\n'
       hsummary+='<b>Publication of</b>\n'
       hsummary+='<ul>\n'
       hsummary+=' <li>\n'
       hsummary+='  '+host_conference.replace('\n','<br>\n')
       if host_conference_url!='':
          hsummary+='  <p>\n'
          hsummary+='  [ <a href="'+host_conference_url+'">ACM DL</a> ]\n'
       hsummary+='</ul>\n'

    source_materials=d.get('source_materials',[])
    if len(source_materials)>0:
       hsummary+='<p>\n'
       hsummary+='<b>Source materials:</b>\n'
       hsummary+='<ul>\n'
       for q in source_materials:
           hsummary+=' <li>'+q+'\n'
           hsummary+='  [ <a href="'+host_conference_url+'">ACM DL</a> ]\n'
       hsummary+='</ul>\n'

    hsummary+='<p>\n'
    hsummary+='<b>Evaluated artifacts and accepted papers:</b>\n'
    hsummary+='<p>\n'
    hsummary+=hartifacts

    aa=d.get('acm_appears_in',[])
    if len(aa)>0:
       hsummary+='<p>\n'
       hsummary+='<b>APPEARS IN</b>\n'
       hsummary+='<ul>\n'
       for q in aa:
           name=q['name']
           url=q['url']
           hsummary+=' <li><a href="'+url+'">'+name+'</a>\n'
       hsummary+='</ul>\n'

    r=ck.save_text_file({'text_file':fs, 'string':hsummary})
    if r['return']>0: return r



    return {'return':0}
