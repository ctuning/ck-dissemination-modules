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

# ============================================================================
def init(i):
    return {'return':0}

##############################################################################
# view entry as html

def html_viewer(i):
    """
    Input:  {
              data_uoa
              url_base
              url_pull
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    h=''
    raw='no'
    top='no'

    duoa=i['data_uoa']
    burl=i['url_base']
    purl=i['url_pull']

    if duoa!='':
       # Load entry
       rx=ck.access({'action':'load',
                     'module_uoa':work['self_module_uid'],
                     'data_uoa':duoa})
       if rx['return']>0: return rx

       dd=rx['dict']
       duid=rx['data_uid']

       name=dd.get('name','')

       email=dd.get('email','')

       personal_web=dd.get('personal_web_page','')
       prof_web=dd.get('professional_web_page','')

       l_image=dd.get('large_image','')
       s_image=dd.get('small_image','')

       cjobs=dd.get('current_jobs',[])


       h+='<table border="0" cellpadding="3">\n'
       h+=' <tr>\n'

       h+='  <td valign="top">\n'
       if l_image!='':
          h+='   <img src="'+purl+s_image+'">'
       h+='  </td>\n'

       h+='  <td valign="top">\n'

       h+='   <span id="ck_entries1a">'+name+'</span><br>\n'
       h+='   <div id="ck_entries_space4"></div>\n'
       h+='   <hr class="ck_hr">\n'

       if len(cjobs)>0:

          h+='<span id="ck_entries1"><i>\n'
          for q in cjobs:
              t=q.get('title','')
              o=q.get('organization','')
              ow=q.get('organization_web','')

              hx=''
              if t!='': hx+=t
              if o!='':
                 if hx!='':hx+=', '
                 if ow=='':
                    hx+=o
                 else:
                    hx+='<a href="'+ow+'">'+o+'</a>'

              h+='<div id="ck_entries_space4"></div>\n'
              h+='&nbsp;&nbsp;&nbsp;&nbsp;'+hx+'<br>\n'

          h+='</span></i>\n'

       h+='   <div id="ck_entries_space4"></div>\n'
       h+='   <hr class="ck_hr">\n'
       h+='     <table border="0" cellpadding="3">\n'


       if email!='':
          h+='      <tr><td valign="top"><b>EMail:</b></td><td valign="top">\n'
          h+='        <a href="mailto:'+email+'">'+email+'</a>\n'
          h+='      </td></tr>\n'

       if prof_web!='':
          h+='      <tr><td valign="top"><b>Professional web:</b></td><td valign="top">\n'
          h+='        <a href="'+prof_web+'">'+prof_web+'</a>\n'
          h+='      </td></tr>\n'

       if personal_web!='':
          h+='      <tr><td valign="top"><b>Personal web:</b></td><td valign="top">\n'
          h+='        <a href="'+personal_web+'">'+personal_web+'</a>\n'
          h+='      </td></tr>\n'

       h+='     </table>\n'


       h+='  </td>\n'

       h+=' </tr>\n'
       h+='</table>\n'

       ####################### List publications
       h+='   <hr class="ck_hr">\n'
       urlx1=burl+'wcid=dissemination.keynote:&search='+duid
       h+='   <span id="ck_text51"><b>Keynotes: </b><a href="'+urlx1+'">[&nbsp;search in CK&nbsp;]</a></span><br>\n'

       urlx1=burl+'wcid=dissemination.publication:&search='+duid
       h+='   <span id="ck_text51"><b>Publications: </b><a href="'+urlx1+'">[&nbsp;search in CK&nbsp;]</a></span><br>\n'

       urlx1=burl+'wcid=dissemination.publication.artifact:&search='+duid
       h+='   <span id="ck_text51"><b>Artifacts for publications: </b><a href="'+urlx1+'">[&nbsp;search in CK&nbsp;]</a></span><br>\n'

       urlx1=burl+'wcid=dissemination.lecture:&search='+duid
       h+='   <span id="ck_text51"><b>Lectures: </b><a href="'+urlx1+'">[&nbsp;search in CK&nbsp;]</a></span><br>\n'

       urlx1=burl+'wcid=dissemination.event:&search='+duid
       h+='   <span id="ck_text51"><b>Events: </b><a href="'+urlx1+'">[&nbsp;search in CK&nbsp;]</a></span><br>\n'

       urlx1=burl+'wcid=dissemination.soft:&search='+duid
       h+='   <span id="ck_text51"><b>Developed software: </b><a href="'+urlx1+'">[&nbsp;search in CK&nbsp;]</a></span><br>\n'

       urlx1=burl+'wcid=dissemination.hardware:&search='+duid
       h+='   <span id="ck_text51"><b>Developed hardware: </b><a href="'+urlx1+'">[&nbsp;search in CK&nbsp;]</a></span><br>\n'

       urlx1=burl+'wcid=dissemination.repo:&search='+duid
       h+='   <span id="ck_text51"><b>Shared repositories: </b><a href="'+urlx1+'">[&nbsp;search in CK&nbsp;]</a></span><br>\n'


    return {'return':0, 'raw':raw, 'show_top':top, 'html':h}

##############################################################################
# extended add

def add(i):
    """
    Input:  {
              (template) - if !='', use this program as template!
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    o=i.get('out','')

    duoa=i.get('data_uoa','')

    d=i.get('dict',{})
    d['name']=duoa

    i['dict']=d

    i['common_func']='yes'
    i['sort_keys']='yes'

    return ck.access(i)
