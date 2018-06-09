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
              (save_docker_images)    - if 'yes', save Docker images (on user host)

              (dtd_data_uoa)
              (dtd_module_uoa)
              (dtd_file)
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

    ocon=(i.get('out','')=='con')
    oo=''
    if ocon: oo='con'

    # Check entry name
    duoa=i.get('data_uoa','')
    if duoa=='':
       return {'return':1, 'error':'proceedings entry is not specified. Use "ck generate proceedings.acm:{proceedings name such as request.asplos18}"'}

    xduoa=duoa.replace('.','-')

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

    f=xduoa+'-ctuning-ae-artifacts.html'

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

    ps=xduoa+'-summary'
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

    pa=os.path.join(curdir,xduoa+'--artifacts')
    if not os.path.isdir(pa):
       os.mkdir(pa)

    pp=os.path.join(curdir,xduoa+'--papers')
    if not os.path.isdir(pp):
       os.mkdir(pp)

    # Summary for ACM DL XML
    pxml=os.path.join(curdir, xduoa+'.xml')
    sum_papers=[]

    # Preparing info about a conference
    sum_papers.append({'comment':'Submitted by: '+d.get('proceedings_submitted_by','')})

    r=ck.get_current_date_time({})
    if r['return']>0: return r

    sum_papers.append({'comment':'Created: automatically by the CK framework ('+r['iso_datetime']+')'})

    # Conference record
    sum_papers.append({'conference_rec':[
       {'conference_date':[
         {'start_date':d.get('event_start_date','')},
         {'end_date':d.get('event_end_date','')}]},
       {'conference_loc':[
         {'city':d.get('event_city','')},
         {'state':d.get('event_state','')},
         {'country':d.get('event_country','')}]},
       {'conference_url':d.get('event_url','')}]})

    # Series record
    sum_papers.append({'series_rec':[
     {'series_name':[
       {'series_id':d.get('series_id','')},
       {'series_title':d.get('series_title','')},
       {'series_vol':d.get('series_vol','')}]}]})

    # Organizers
    organizers=[]
    iq=0

    dorg=d.get('organizers',[])
    dadv=d.get('advisory_board',[])
    dorg+=dadv
    for org in dorg:
        xorg=[]
        iq+=1

        first_name=org.get('first_name','')
        last_name=org.get('last_name','')

        aff=org.get('affiliation','')

        role=org.get('role','')

        extra=org.get('extra','')
        if extra!='':
           role+=' ('+extra+')'

        xorg.append({'seq_no':str(iq)})
        xorg.append({'first_name':first_name})
        xorg.append({'last_name':last_name})
        xorg.append({'affiliation':aff})
        xorg.append({'role':role})

        organizers.append({"ch_ed":xorg})

    # Front matter
    fm=d.get('front_matter',{})

    xfm=[]
    fm_file=''
    if len(fm)>0:
       fm_file=fm.get('fm_file','')
       fm_text=fm.get('fm_text','')

       if fm_file!='':
          fm_file=xduoa+'-'+fm_file

       xfm.append({'fm_file':fm_file})
       xfm.append({'fm_text':fm_text})

    # Abstract
    fa=d.get('abstract_file','')

    pabs=os.path.join(p, fa)
    r=ck.load_text_file({'text_file':pabs})
    if r['return']>0: return r

    abstract=[]
    for a in r['string'].split('<par>'):
        abstract.append({'par':a.strip().replace('\n',' ')})

    # Proceedings info
    sum_papers.append({'proceeding_rec':[
     {'proc_id':d.get('proc_id','')},
     {'acronym':d.get('proc_acronym','')},
     {'proc_desc':d.get('proc_desc','')},
     {'conference_number':d.get('proc_conference_number','')},
     {'proc_class':d.get('proc_class','')},
     {'proc_title':d.get('proc_title','')},
     {'proc_subtitle':d.get('proc_subtitle','')},
     {'proc_volume_no':d.get('proc_volume_no','')},
     {'doi_number':d.get('proc_doi_number','')},
     {'isbn':d.get('proc_isbn','')},
     {'isbn13':d.get('proc_isbn13','')},
     {'copyright_year':d.get('proc_copyright_year','')},
     {'publication_date':d.get('proc_publication_date','')},
     {'pages':d.get('proc_pages','')},
     {'abstract':abstract},
     {'publisher':d.get('proc_publisher',[])},
     {'sponsor_rec':d.get('proc_sponsor_rec',[])},
     {'ccs2012':d.get('proc_ccs2012',[])},
     {"chair_editor":organizers},
     {"front_matter":xfm},
     {"cms_conf_id":d.get('proc_cms_conf_id','')}
     ]})

    # Start content 
    content=d.get('proc_content',[])
    sum_papers.append({'content':content})

    # Compiling front matter if exists
    fm_uoa=fm.get('data_uoa','')
    if spg!='yes' and fm_uoa!='':
       ck.out('')
       ck.out('* Preparing front-matter ...')
       ck.out('')

       ck.out('********************************************')
       ck.out('Cleaning front matter sources ...')
       ck.out('')

       cur_dir=os.getcwd()
       ii={'action':'clean',
           'module_uoa':cfg['module_deps']['dissemination.publication'],
           'data_uoa':fm_uoa}
       r=ck.access(ii)
       if r['return']>0: return r
       os.chdir(cur_dir)

       ck.out('********************************************')
       ck.out('Compiling front-matter sources ...')
       ck.out('')

       cur_dir=os.getcwd()
       ii={'action':'compile',
           'module_uoa':cfg['module_deps']['dissemination.publication'],
           'data_uoa':fm_uoa}
       r=ck.access(ii)
       if r['return']>0: return r
       os.chdir(cur_dir)

       ck.out('********************************************')
       ck.out('Copying paper ...')
       ck.out('')

       # Copying
       ii={'action':'find',
           'module_uoa':cfg['module_deps']['dissemination.publication'],
           'data_uoa':fm_uoa}
       r=ck.access(ii)
       if r['return']>0: return r

       pf1=os.path.join(r['path'],'paper.pdf')

       if not os.path.isfile(pf1):
          return {'return':1, 'error':'seems that paper PDF was not generated ('+pf1+')'}

       # Copying paper in ACM DL format
       pf3=os.path.join(curdir, fm_file)

       shutil.copy(pf1,pf3)

    # Preparing papers and artifact packs
    seq_no=1
    a_id=0
    sort_key=30

    paper_section=[
      {"sort_key":str(sort_key)},
      {"section_seq_no":str(2)},
      {"section_type":"SESSION"},
      {"section_title":"Artifact presentations"},
      {"section_page_from":""}
    ]
    content.append({"section":paper_section})

    for a in artifacts:
        aduoa=a['data_uoa']

        a_id+=1
        s_a_id=str(a_id)

        ck.out(s_a_id+') '+aduoa)

        # Summary per artifact
        sum_artifact=[]

        sort_key+=10
        seq_no+=1 # can start in a previous section (keynote)

        da=a['dict']
        dp=a['paper_dict']
        paper_path=a['paper_path']

        aruoa=a['repo_uoa']

        paper_doi=da.get('paper_doi','')
        artifact_doi=da.get('artifact_doi','')

        if paper_doi.startswith('https://doi.org/'):
           paper_doi=paper_doi[16:]
        paper_doi=paper_doi.replace('/','-')

        if artifact_doi.startswith('https://doi.org/'):
           artifact_doi=artifact_doi[16:]
        artifact_doi=artifact_doi.replace('/','-')

        # Check if has abstract
        fa=da.get('abstract_file','')
        if fa=='': fa='paper_abstract.txt'

        pabs=os.path.join(paper_path, fa)
        abstract=[]

        xa=['']
        r=ck.load_text_file({'text_file':pabs})
        if r['return']==0:
           xa=r['string'].split('<par>')

        for a in xa:
            abstract.append({'par':a.strip().replace('\n',' ')})

        # Article XML
        article_id=''
        j=paper_doi.find('/')
        if j>0:
           article_id=paper_doi[j+1:].strip()

        paper_file_name=xduoa+'-paper-'+s_a_id+'.pdf'

        ccc=[{'copyright_holder':[
                {'copyright_holder_name':'ACM'},
                {'copyright_holder_year':'2018'}]}]

        keywords=[]
        for k in da.get('keywords',[]):
            keywords.append({'kw':k})
        if len(keywords)==0:
           keywords=[{'kw':''}]

        authors=[]
        author_seq_no=0
        affiliations=dp.get('affiliations',{})
        for au in dp.get('authors',[]):
            author_seq_no+=1

            name=au.get('name','')
            aff=au.get('affiliation','').split(',')
            email_address=au.get('email_address','')

            affiliation=''
            for x in aff:
                if x!='':
                   if affiliation!='': affiliation+='; '
                   affiliation+=affiliations[x]['name']

            r=ck.access({'action':'load',
                         'module_uoa':cfg['module_deps']['person'],
                         'data_uoa':name})
            if r['return']>0: return r
            dperson=r['dict']

            first_name=dperson.get('first_name','')
            last_name=dperson.get('last_name','')

            y=[
                {'seq_no':str(author_seq_no)},
                {'first_name':first_name},
                {'last_name':last_name},
                {'affiliation':affiliation},
                {'role':'AUTHOR'},
                {'email_address':email_address}
              ]

            authors.append({'au':y})

        article_record=[
          {"article_id":article_id},
          {"sort_key":str(sort_key)},
          {"display_label":"p"},
          {"article_publication_date":d.get('proc_publication_date','')},
          {"seq_no":str(seq_no)},
          {"title":dp.get('title','')},
          {"doi_number":paper_doi},
          {"url":""},
          {"abstract":abstract},
          {"keywords":keywords},
          {"ccs2012":d.get('proc_ccs2012','')},
          {"authors":authors},
          {"fulltext": [
            {"file":[
              {"seq_no":str(seq_no)},
              {"fname":paper_file_name}]}]},
          {"ccc":ccc}
        ]

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

           if not os.path.isfile(pf1):
              return {'return':1, 'error':'seems that paper PDF was not generated ('+pf1+')'}

           shutil.copy(pf1,pf2)

           # Copying paper in ACM DL format
           pf3=os.path.join(curdir, paper_file_name)

           shutil.copy(pf1,pf3)

        paper_section.append({"article_rec":article_record})

        # Preparing artifacts
        if i.get('skip_artifacts','')=='yes':
           continue

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
           if ocon:
              ck.out('')
              ck.out('Packing original repository ...')
              ck.out('')

           import tempfile
           ptmp=os.path.join(tempfile.gettempdir(),'tmp-original-repo')

           if ocon:
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

              for fn in flx:
                  z.write(os.path.join(ptmp,fn), fn, zipfile.ZIP_DEFLATED)

              # ck-install.json
              z.close()
              f.close()

           except Exception as e:
              return {'return':1, 'error':'failed to prepare CK artifact collections ('+format(e)+')'}

           shutil.rmtree(ptmp, onerror=ck.rm_read_only)

        # Check original repo
        docker_images=da.get('docker_images',[])
        if len(docker_images)>0 and i.get('save_docker_images','')=='yes':
           if ocon:
              ck.out('')
              ck.out('Preparing Docker images ...')

           for dk in docker_images:
               dduoa=dk['data_uoa']

               if ocon:
                  ck.out('')
                  ck.out('Saving Docker image "'+dduoa+'" with sudo (we expect that you already prepared this image) ...')
                  ck.out('')

               fn='docker-image-'+dduoa+'.tar'
               xfn=os.path.join(p2, fn)

               r=ck.access({'action':'save',
                            'module_uoa':cfg['module_deps']['docker'],
                            'data_uoa':dduoa,
                            'filename':xfn,
                            'sudo':'yes',
                            'out':oo})
               if r['return']>0: return r

    # Check proc content 2 (panels, etc)
    content2=d.get('proc_content2',[])
    if len(content2)>0:
       section=[
         {'sort_key':str(sort_key+10)},
         {'section_seq_no':'3'},
       ]

       section+=content2

       content.append({'section':section})

    # Record proceedings summary XML
    if ocon:
       ck.out('')
       ck.out('Recording proceedings summary to XML (and validating if supported) ...')
       ck.out('')

    ii={'action':'generate',
        'module_uoa':cfg['module_deps']['xml'],
        'dict':sum_papers,
        'root_key':'proceeding',
        'root_attributes':{'ts':'05/09/2017', 'ver':'10.1'},
        'xml_file':pxml}

    dduoa=i.get('dtd_data_uoa','')
    dmuoa=i.get('dtd_module_uoa','')
    dfile=i.get('dtd_file','')

    if dduoa!='': ii['data_uoa']=dduoa
    if dmuoa!='': ii['dtd_module_uoa']=dmuoa
    if dfile!='': ii['dtd_file']=dfile

    r=ck.access(ii)
    if r['return']>0: return r

    return {'return':0}
