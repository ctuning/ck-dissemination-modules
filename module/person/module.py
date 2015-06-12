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


    return {'return':0, 'raw':raw, 'show_top':top, 'html':h}
