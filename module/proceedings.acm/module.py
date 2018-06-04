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
              data_uoa                - proceedings entry
              (skip_paper_generation) - if 'yes', do not generate papers
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    import os
    import shutil
    import zipfile

    curdir=os.getcwd()

    o=i.get('out','')
    oo=''
    if o=='con': oo=o

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

    spg=i.get('skip_paper_generation','')

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
    doi=d.get('doi','')
    
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

        a['repo_uoa']=r['repo_uoa']
        a['repo_uid']=r['repo_uid']

        # Load paper
        ii={'action':'load',
            'module_uoa':cfg['module_deps']['dissemination.publication'],
            'data_uoa':aduoa}

        r=ck.access(ii)
        if r['return']>0: return r

        a['paper_dict']=r['dict']
        a['paper_path']=r['path']

    # Generate table of evaluated artifacts for http://cTuning.org/ae/artifacts.html
    ck.out('')
    ck.out('Generating paper and artifact table ...')

    f=duoa+'--ctuning-ae-artifacts.html'

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
    ck.out('')
    ck.out('Generating proceedings summary for ACM DL ...')

    if doi.startswith('https://doi.org/'):
       doi=doi[16:]
    doi=doi.replace('/','-')

    ps=duoa+'--summary'
    if not os.path.isdir(ps):
       os.mkdir(ps)

    p0=os.path.join(ps,doi)
    if not os.path.isdir(p0):
       os.mkdir(p0)

    fs=os.path.join(p0,'summary.html')

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

    # Prepare packs for ACM DL
    ck.out('')
    ck.out('Preparing artifact packs ...')
    ck.out('')

    os.chdir(curdir)

    pa=os.path.join(curdir,duoa+'--artifacts')
    if not os.path.isdir(pa):
       os.mkdir(pa)

    pp=os.path.join(curdir,duoa+'--papers')
    if not os.path.isdir(pp):
       os.mkdir(pp)

    for a in artifacts:
        aduoa=a['data_uoa']

        ck.out('* '+aduoa)

        da=a['dict']
        dp=a['paper_dict']

        aruoa=a['repo_uoa']

        paper_doi=da.get('paper_doi','')
        artifact_doi=da.get('artifact_doi','')

        if paper_doi.startswith('https://doi.org/'):
           paper_doi=paper_doi[16:]
        paper_doi=paper_doi.replace('/','-')

        if artifact_doi.startswith('https://doi.org/'):
           artifact_doi=artifact_doi[16:]
        artifact_doi=artifact_doi.replace('/','-')

        # Compiling papers
        if spg!='yes':
           ck.out('********************************************')
           ck.out('Cleaning paper sources ...')
           ck.out('')

           p1=os.path.join(pp,paper_doi)
           if not os.path.isdir(p1):
              os.mkdir(p1)

           # Saving artifact dict
           r=ck.save_json_to_file({'json_file':os.path.join(p1, cfg['file_artifact_meta']), 'dict':da})
           if r['return']>0: return r

           # Saving paper dict
           r=ck.save_json_to_file({'json_file':os.path.join(p1, cfg['file_paper_meta']), 'dict':dp})
           if r['return']>0: return r

           cur_dir=os.getcwd()
           ii={'action':'clean',
               'module_uoa':cfg['module_deps']['dissemination.publication'],
               'data_uoa':aduoa}
           r=ck.access(ii)
           if r['return']>0: return r
           os.chdir(cur_dir)

           ck.out('********************************************')
           ck.out('Compiling paper sources ...')
           ck.out('')

           cur_dir=os.getcwd()
           ii={'action':'compile',
               'module_uoa':cfg['module_deps']['dissemination.publication'],
               'data_uoa':aduoa}
           r=ck.access(ii)
           if r['return']>0: return r
           os.chdir(cur_dir)

           ck.out('********************************************')
           ck.out('Copying paper ...')
           ck.out('')

           # Copying
           ii={'action':'find',
               'module_uoa':cfg['module_deps']['dissemination.publication'],
               'data_uoa':aduoa}
           r=ck.access(ii)
           if r['return']>0: return r

           pf1=os.path.join(r['path'],'paper.pdf')
           pf2=os.path.join(p1, 'paper.pdf')

           shutil.copy(pf1,pf2)

        # Preparing artifacts
        ck.out('********************************************')
        ck.out('Preparing CK artifact snapshot ...')
        ck.out('')

        p2=os.path.join(pa,artifact_doi)

        if os.path.isdir(p2):
           shutil.rmtree(p2, onerror=ck.rm_read_only)

        if not os.path.isdir(p2):
           os.mkdir(p2)

        # Saving artifact dict
        r=ck.save_json_to_file({'json_file':os.path.join(p2, cfg['file_artifact_meta']), 'dict':da})
        if r['return']>0: return r

        # Saving paper dict
        r=ck.save_json_to_file({'json_file':os.path.join(p2, cfg['file_paper_meta']), 'dict':dp})
        if r['return']>0: return r

        if True:
           cur_dir=os.getcwd()
           os.chdir(p2)

           ii={'action':'snapshot',
               'module_uoa':cfg['module_deps']['artifact'],
               'repo':aruoa,
               'file_name':os.path.join(p2, 'ck-workflow-'),
               'force_clean':'yes',
               'copy_repos':'yes',
               'out':oo}
           r=ck.access(ii)
           if r['return']>0: return r

           os.chdir(cur_dir)

           repo_results=da.get('ck_repo_results','')
           if repo_results!='':

              os.chdir(p2)

              ii={'action':'snapshot',
                  'module_uoa':cfg['module_deps']['artifact'],
                  'repo':repo_results,
                  'no_deps':'yes',
                  'file_name':os.path.join(p2, 'ck-workflow-results-'),
                  'force_clean':'yes',
                  'copy_repos':'yes',
                  'out':oo}
              r=ck.access(ii)
              if r['return']>0: return r

              os.chdir(cur_dir)

        # Check original repo
        orepo=da.get('original_repo','')
        if orepo!='':
           import tempfile
           ptmp=os.path.join(tempfile.gettempdir(),'tmp-original-repo')

           if o=='con':
              ck.out('Temp directory: '+ptmp)
              ck.out('')

           if os.path.isdir(ptmp):
              shutil.rmtree(ptmp, onerror=ck.rm_read_only)

           orepo='https://github.com/ctuning/ck'
           ck.out('')
           ck.out('Cloning '+orepo+' ...')
           ck.out('')
           os.system('git clone '+orepo+' '+ptmp)

           r=ck.list_all_files({'path':ptmp, 'all':'yes'})
           if r['return']>0: return r

           flx=r['list']

           try:
              f=open(os.path.join(p2,'original-artifact.zip'), 'wb')
              z=zipfile.ZipFile(f, 'w', zipfile.ZIP_DEFLATED)

              print (ptmp)
              for fn in flx:
                  print (fn)
                  z.write(os.path.join(ptmp,fn), fn, zipfile.ZIP_DEFLATED)

              # ck-install.json
              z.close()
              f.close()

           except Exception as e:
              return {'return':1, 'error':'failed to prepare CK artifact collections ('+format(e)+')'}

           shutil.rmtree(ptmp, onerror=ck.rm_read_only)

    return {'return':0}
