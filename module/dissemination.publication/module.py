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

# LaTex tokens
tokens=[
        {"key":'%CK_TEX={', "end":"}", "id":250, "html1":'',"html2":"", "remove":"no"},
        {"key":'%CK_ABSTRACT={', "end":"}", "id":250, "html1":'<i>',"html2":"</i>", "remove":"no"},
        {"key":'%CK={', "end":"}", "id":100, "html1":'',"html2":"", "remove":"yes"},
        {"key":'%CK_HTML={', "end":"}", "id":150, "html1":'',"html2":"", "remove":"no"},
        {"key":'%CK_URL={', "end":"}", "id":198, "html1":'',"html2":"", "remove":"no"},
        {"key":'%CK_IMG={', "end":"}", "id":199, "html1":'',"html2":"", "remove":"no"},
        {"key":'%CK_INTERACTIVE_GRAPH_PASSIVE={', "end":"}", "id":298, "html1":'',"html2":"", "remove":"no"},
        {"key":'%CK_INTERACTIVE_GRAPH={', "end":"}", "id":299, "html1":'',"html2":"", "remove":"no"},
        {"key":'\\%', "id":500, "html1":'&#37;'},
        {"key":'\n\n', "id":60, "html1":'\n<p>'},
        {"key":'\\&', "id":105, "html1":"&"},
        {"key":'\\_', "id":105, "html1":"_"},
        {"key":'\\label{', "end":"}", "id":10, "html1":'',"html2":"", "remove":"no"},
        {"key":'\\section{', "end":"}", "id":80, "html1":"\n\n<h2>","html2":"</h2>\n"},
        {"key":'\\subsection{', "end":"}", "id":81, "html1":"\n\n<h3>","html2":"</h3>\n"},
        {"key":'\\subsubsection{', "end":"}", "id":82, "html1":"\n\n<h4>","html2":"</h4>\n"},
        {"key":'\\emph{', "end":"}", "id":3, "html1":"<i>","html2":"</i>"},
        {"key":'\\textbf{', "end":"}", "id":3, "html1":"<b>","html2":"</b>"},
        {"key":'\\textit{', "end":"}", "id":3, "html1":"<i>","html2":"</i>"},
        {"key":'\\texttt{', "end":"}", "id":3, "html1":"<pre>","html2":"</pre>"},
        {"key":'\\url{', "end":"}", "id":333, "html1":"","html2":""},
        {"key":'{\\bf', "end":"}", "id":3, "html1":"<b>","html2":"</b>"},
        {"key":'{\\it', "end":"}", "id":3, "html1":"<i>","html2":"</i>"},
        {"key":'~', "end":"", "id":4, "html1":"&nbsp;","html2":""},
        {"key":'\\item', "id":49, "html1":'\n<li>\n'},
        {"key":'\\begin{itemize}', "id":43, "html1":'\n<ul>\n'},
        {"key":'\\end{itemize}', "id":44, "html1":'</ul>\n'},
        {"key":'\\begin{verbatim}', "id":43, "html1":'\n<pre>'},
        {"key":'\\end{verbatim}', "id":44, "html1":'</pre>\n'},
        {"key":'\\begin{lstlisting', "end":"]", "id":43, "html1":'\n<pre>', "remove":"yes"},
        {"key":'\\end{lstlisting}', "id":44, "html1":'</pre>\n'},
        {"key":'\\caption{', "end":"}", "id":20, "html1":'<br><i>',"html2":"</i><br><br>\n"},
        {"key":'\\centering', "id":90, "html1":""},
        {"key":'\\includegraphics', "end":"}", "id":30, "html1":'',"html2":"", "remove":"yes"},
        {"key":'\\begin{table', "end":"]", "id":555, "html1":'<center><div style="background-color:#f0f1f2;">\n',"html2":"", "remove":"no"},
        {"key":'\\end{table}', "id":49, "html1":'</div></center>\n'},
        {"key":'\\end{table*}', "id":49, "html1":'</div></center>\n'},
        {"key":'\\begin{figure', "end":"]", "id":554, "html1":'\n<center><div style="background-color:#f0f1f2;">\n',"html2":"", "remove":"no"},
        {"key":'\\end{figure}', "id":49, "html1":'</div></center>\n'},
        {"key":'\\end{figure*}', "id":50, "html1":'</div></center>\n'},
        {"key":'\\input{', "end":"}", "id":44, "html1":'',"html2":"", "remove":"yes"},
        {"key":'{\\center', "end":"}", "id":44, "html1":'<center>\n',"html2":"</center>\n", "remove":"no"},
        {"key":'\\begin{center}', "end":"\\end{center}", "id":44, "html1":'<center>\n',"html2":"</center><br>\n", "remove":"no"},
        {"key":'\\cite{', "end":"}", "id":300, "html1":"[","html2":"]"},
        {"key":'\\ref{', "end":"}", "id":600, "html1":"","html2":""},
        {"key":'{\\small', "end":"}", "id":3, "html1":"","html2":""},
        {"key":'\\vspace{', "end":"}", "id":950, "html1":"<br>","html2":"","remove":"yes"},
        {"key":'%', "end":"\n", "id":1000, "html1":"","html2":"", "remove":"yes"}
       ]

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

# TBD: should redirect to module:report ?

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
#          if wurl!='' and dd.get('skip_wiki_discussion','')!='yes':
#             h+='[&nbsp;<a href="'+wurl+'">Discussion wiki (comments, reproducibility, etc.)</a>&nbsp;]'
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

##############################################################################
# convert tex article to live ck report

def convert_to_live_ck_report(i):
    """
    Input:  {
              module_uoa
              data_uoa    - LaTex publication to process
              (input)     - input file (paper.tex by default)
              (input_bbl) - BBL input file for references (paper.bbl by default)
              (output)    - output file in CK live report format
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    # Init
    anchors={}
    refs={}
    cites={}
    xcites=[]
    figures={}
    tables={}
    sections={}
    appendices={}

    ifigures=0
    itables=0
    isections=0
    iappendices='A'

    muoa=i['module_uoa']
    duoa=i['data_uoa']

    fi=i.get('input','')
    if fi=='': fi='paper.tex'

    fib=i.get('input_bbl','')
    if fib=='': fib='paper.bbl'

    fo=i.get('output','')
    if fo=='': fo='ck-interactive-paper.html'

    # Check entry in current path (for URL)
    r=ck.cid({})
    if r['return']>0: return r

    self_cid=r['module_uid']+':'+r['data_uid']
    self_url='$#ck_root_url#$action=pull&common_func=yes&cid='+self_cid+'&filename='

    # Get path to entry
    r=ck.access({'action':'load',
                 'module_uoa':muoa,
                 'data_uoa':duoa})
    if r['return']>0: return r

    p=r['path']

    pfi=os.path.join(p,fi)
    pfib=os.path.join(p,fib)
    
    # Read paper
    ck.out('')
    ck.out('Loading paper: '+pfi+' ...')

    r=ck.load_text_file({'text_file':pfi})
    if r['return']>0: return r
    paper=r['string'].replace('\r','')

    # Read references
    ck.out('')
    ck.out('Loading references: '+pfib+' ...')

    r=ck.load_text_file({'text_file':pfib})
    if r['return']>0: return r
    bbl=r['string'].replace('\r','')

    # Parse references
    ck.out('')
    ck.out('Parsing references: '+pfib+' ...')

    j=bbl.find('\\bibitem{')
    while j>=0:
       j1=bbl.find('}',j+1)
       if j1>=0:
          ref=bbl[j+9:j1]
          j2=bbl.find('\n\n', j1+1)
          if j2>0:
             ck.out('  * '+ref)
             s=bbl[j1+1:j2].strip()

             # Processing special tokens
             s=s.replace('~','&nbsp;').replace('\\newblock','<br>').replace('\\&','&')

             # https://www.w3schools.com/charsets/ref_utf_latin_extended_a.asp
             s=s.replace('\\c{T}','&Tcedil;').replace('\\u{a}','&abreve;').replace('\\c{s}','&scedil;')

             j5=s.find('\\url{')
             if j5>=0:
                j6=s.find('}',j5+1)
                if j6>=0:
                   s=s[:j5]+'<a href="'+s[j5+4:j6]+'">Link</a>'+s[j6+1:]

             s=s.replace('{\\em','').replace('{','').replace('}','')

             cites[ref]={'html':s}

       j=bbl.find('\\bibitem{',j+1)

    r=ck.load_text_file({'text_file':pfib})
    if r['return']>0: return r
    bbl=r['string']

    hpaper=''

    # Searching first section (ignore all above - will be prepared by CK via meta.json)
    nref=1
    j=paper.find('%CK_INTERACTIVE_START')
    if j>=0:
       # Searching for the bibliography
       j1=paper.find('\\bibliographystyle')
       if j1>=0:
          hpaper=paper[j:j1-1]+'\n\n'

          # Start processing special commands
          for tt in tokens:
              t=tt['key']
              tend=tt.get('end','')
              thtml1=tt.get('html1','')
              thtml2=tt.get('html2','')
              idx=tt['id']

              if tend!='':
                 j=hpaper.find(t)
                 while j>=0:
                    j1=hpaper.find(tend,j+len(t))
                    if j1>=0:
                       sx=hpaper[j+len(t):j1]

                       xthtml1=thtml1

                       sx_right=''

                       if idx==80:
                          # Check if appendices
                          l=hpaper.rfind('%CK_APPENDIX={', 0, j+1)
                          if l>=0:
                             l1=hpaper.find('}',l+1)
                             app=hpaper[l+14:l1]
                          else:
                             isections+=1
                             app=str(isections)

                          sx=app+'&nbsp;&nbsp;'+sx
                          sx_right='\n\n<!-- CK_CUR_SECTION={'+app+'} -->\n\n'

                          l=hpaper.find('CK_LABEL={', j)
                          if l>=0:
                             l1=hpaper.find('}',l+1)
                             lbl=hpaper[l+10:l1]

                             sx_right='\n\n<a name="'+lbl+'">'+sx_right

                             refs[lbl]=app

                       elif idx==81:
                          # Check current session
                          l=hpaper.rfind('CK_CUR_SECTION={',0, j+1)
                          if l>=0:
                             l1=hpaper.find('}',l+1)
                             section=hpaper[l+16:l1]

                             subsection=''
                             l2=hpaper.rfind('CK_CUR_SUBSECTION={',l,j+1)
                             if l2>=0:
                                l3=hpaper.find('}',l2)
                                if l3>=0:
                                   subsection=hpaper[l2+19:l3]

                             if subsection=='':
                                subsection='1'
                             else:
                                subsection=str(int(subsection)+1)   

                             app=section+'.'+subsection

                             sx=app+'&nbsp;&nbsp;'+sx
                             sx_right='\n\n<!-- CK_CUR_SUBSECTION={'+subsection+'} -->\n\n'

                             l=hpaper.find('CK_LABEL={', j)
                             if l>=0:
                                l1=hpaper.find('}',l+1)
                                lbl=hpaper[l+10:l1]

                                sx_right='\n\n<a name="'+lbl+'">'+sx_right

                                refs[lbl]=app

                       elif idx==82:
                          # Check current session
                          l=hpaper.rfind('CK_CUR_SECTION={',0, j+1)
                          if l>=0:
                             l1=hpaper.find('}',l+1)
                             section=hpaper[l+16:l1]

                             subsection=''
                             l2=hpaper.rfind('CK_CUR_SUBSECTION={',l,j+1)
                             if l2>=0:
                                l3=hpaper.find('}',l2)
                                if l3>=0:
                                   subsection=hpaper[l2+19:l3]

                                   subsubsection=''
                                   l4=hpaper.rfind('CK_CUR_SUBSUBSECTION={',l2,j+1)
                                   if l4>=0:
                                      l5=hpaper.find('}',l4)
                                      if l5>=0:
                                         subsubsection=hpaper[l4+22:l5]

                                   if subsubsection=='':
                                      subsubsection='1'
                                   else:
                                      subsubsection=str(int(subsubsection)+1)   

                                   app=section+'.'+subsection+'.'+subsubsection

                                   sx=app+'&nbsp;&nbsp;'+sx
                                   sx_right='\n\n<!-- CK_CUR_SUBSUBSECTION={'+subsubsection+'} -->\n\n'

                                   l=hpaper.find('CK_LABEL={', j)
                                   if l>=0:
                                      l1=hpaper.find('}',l+1)
                                      lbl=hpaper[l+10:l1]

                                      sx_right='\n\n<a name="'+lbl+'">'+sx_right

                                      refs[lbl]=app

                       if idx==554:
                          # Check if appendices
                          ifigures+=1

                          anc=''
                          xlbl=''

                          l=hpaper.find('CK_LABEL={', j)
                          if l>=0:
                             l1=hpaper.find('}',l+1)
                             lbl=hpaper[l+10:l1]

                             figures[lbl]={'id':ifigures}

                             refs[lbl]=str(ifigures)

                             xlbl='<a name="'+lbl+'">'
 
                          sx='\n<br>'+xlbl+'<b>Figure '+str(ifigures)+'</b>\n'

                       elif idx==555:
                          # Check if appendices
                          itables+=1

                          anc=''
                          xlbl=''

                          l=hpaper.find('CK_LABEL={', j)
                          if l>=0:
                             l1=hpaper.find('}',l+1)
                             lbl=hpaper[l+10:l1]

                             tables[lbl]={'id':itables}

                             refs[lbl]=str(itables)

                             xlbl='<a name="'+lbl+'">'
 
                          sx='\n<br>'+xlbl+'<b>Table '+str(itables)+'</b><br><br>\n'

                       elif idx==10:
                          sx=sx.replace(':','_').replace('-','_')

                          sx='<!-- CK_LABEL={'+sx+'} -->\n\n'

#                          xthtml1=thtml1.replace('$#aname#$',sx)

                       elif idx==600:
                          sx=sx.replace(':','_').replace('-','_')

                          sx='<a href="#'+sx+'">'+str(refs[sx])+'</a>'

#                          xthtml1=thtml1.replace('$#aname#$',sx)

                       elif idx==150:
                          rx=ck.load_text_file({'text_file':sx})
                          if rx['return']>0: return rx
                          sx=rx['string']

                       elif idx==333:
                          sx='<a href="'+sx+'">'+sx+'</a>'

                       elif idx==198:
                          r=ck.convert_json_str_to_dict({'str':'{'+sx+'}', 'skip_quote_replacement':'yes'})
                          if r['return']>0: return r
                          ii=r['dict']

                          url=ii['url']
                          text=ii['text']

                          sx='<a href="'+url+'">'+text+'</a><br>'

                       elif idx==199:
                          b9=sx.find(';')
                          if b9<0:
                             sx='<img src="'+sx+'">'
                          else:
                             sy=sx[b9+1:].strip()
                             sx=sx[:b9].strip()

                             sx='<a href="'+sy+'"><img src="'+sx+'"></a>'

                       elif idx==298: # Passive graph (include)
                          sx='\n$#ck_include_start#$\n{'+sx+'}\n$#ck_include_stop#$\n'

                       elif idx==299: # Active graph (generate)
                          sx='\n$#ck_access_start#$\n{'+sx+'}\n$#ck_access_stop#$\n'

                       elif idx==250:
                          psx=os.path.join(p,sx)
                          rx=ck.load_text_file({'text_file':psx})
                          if rx['return']>0: return rx
                          sx=rx['string']

                       elif idx==300:
                          ycites=sx.replace('\n','').strip().split(',')
                          xc=''
                          for cx in ycites:
                              c=cx.strip()
                              if c in cites:
                                 x=cites[c]
                                 n=x.get('number','')
                                 if n=='':
                                    n=nref
                                    x['number']=n
                                    xcites.append(c)
                                    nref+=1
                                 if xc!='': xc+=', '
                                 xc+='<a href="#ref_'+str(n)+'">'+str(n)+'</a>'
                              else:
                                 return {'return':1, 'error':'citation "'+c+'" was not found in bbl'}   
                          sx=xc
    
                       elif idx==100:
                          # Convert from JSON to dict
                          r=ck.convert_json_str_to_dict({'str':'{'+sx+'}', 'skip_quote_replacement':'yes'})
                          if r['return']>0: return r
                          ii=r['dict']

                          tp=ii.get('ck_url','')
                          fx=ii.get('file','')
                          px=ii.get('path','')

                          euid=ii.get('extra_uid','')
                          if euid!='': euid+='-'

                          ckimg=ii.get('ck_image','')
                          ckimgw=ii.get('ck_image_width','')

                          ckey='%CK_URL={'+fx+'}'

                          if fx.endswith('.pdf'):
                             fx=fx[:-4]+'.png'
                             ii['file']=fx

                          if euid!='':
                             f0,f1=os.path.splitext(fx)
                             fx=f0.replace('.','-')+f1

                          fxx=px+'/'+euid+fx
                          url=self_url+fxx
 
                          ck.out('')
                          ck.out('* Processing CK command '+sx+' ...')

                          r=ck.access(ii)
                          if r['return']>0: return r

                          x=''
                          if ckimg=='yes':
                             x='<br><br><img src="'+url+'" width="'+str(ckimgw)+'"><br>'

                          hpaper1=hpaper.replace(ckey,x)
                          if hpaper1!=hpaper:
                             ck.out('  CHANGED!')
                             hpaper=hpaper1

                       if tt.get('remove','')=='yes': 
                          sx=''

                       hpaper=hpaper[:j]+xthtml1+sx+thtml2+hpaper[j1+len(tend):]

                       # Add extra to the right of the line (CK remarks)
                       if sx_right!='':
                          k=hpaper.find('\n',j+1)
                          if k>=0:
                             hpaper=hpaper[:k]+sx_right+hpaper[k+1:]

                    else:
                       return {'return':1, 'error':'inconsistent token "'+t+'" in tex file ('+hpaper[j:j+16]+' ...)'}

                    j=hpaper.find(t, j)

              else:
                 hpaper=hpaper.replace(t, thtml1)

    # Check references
    if len(xcites)>0:
       hpaper+='<br><br>\n'
       hpaper+='<h2>References</h2>\n'

       hpaper+='<table border="0" cellpadding="5" cellspacing="0">\n'

       nref=0
       for c in xcites:
           nref+=1

           hpaper+=' <tr>\n'
           hpaper+='  <td valign="top"><a name="ref_'+str(nref)+'"><b>['+str(nref)+']</b></td>'

           hpaper+='  <td valign="top">'+cites[c]['html']

           hpaper+='  <br></td>\n'

           hpaper+=' </tr>\n'

       hpaper+='</table>\n'

       for q in range(0,50):
           hpaper+='<br>'

    # Saving to report
    ck.out('')
    ck.out('Saving interactive CK report: '+fo+' ...')
    r=ck.save_text_file({'text_file':fo, 'string':hpaper})
    if r['return']>0: return r

    return {'return':0}
