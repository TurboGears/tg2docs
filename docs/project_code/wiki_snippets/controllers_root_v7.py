# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import expose, flash, require, url, request, redirect
from tg.i18n import ugettext as _, lazy_ugettext as l_

from wiki20.lib.base import BaseController
from wiki20.model import DBSession, metadata
from wiki20.controllers.error import ErrorController
from wiki20.model import Page
import re
from docutils.core import publish_parts
from sqlalchemy.exceptions import InvalidRequestError

wikiwords = re.compile(r"\b([A-Z]\w+[A-Z]+\w+)")



__all__ = ['RootController']


class RootController(BaseController):
    """
    The root controller for the Wiki-20 application.
    
    All the other controllers and WSGI applications should be mounted on this
    controller. For example::
    
        panel = ControlPanelController()
        another_app = AnotherWSGIApplication()
    
    Keep in mind that WSGI applications shouldn't be mounted directly: They
    must be wrapped around with :class:`tg.controllers.WSGIAppController`.
    
    """
    
    error = ErrorController()

    @expose('wiki20.templates.page')
    def _default(self, pagename="FrontPage"):
        try:
            page = DBSession.query(Page).filter_by(pagename=pagename).one()
        except InvalidRequestError:
            raise redirect("notfound", pagename = pagename)
        content = publish_parts(page.data, writer_name="html")["html_body"]
        root = url('/')
        content = wikiwords.sub(r'<a href="%s\1">\1</a>' % root, content)
        return dict(content=content, wikipage=page)

    @expose(template="wiki20.templates.edit")
    def edit(self, pagename):
        page = DBSession.query(Page).filter_by(pagename=pagename).one()
        return dict(wikipage=page)

    @expose('wiki20.templates.about')
    def about(self):
        """Handle the 'about' page."""
        return dict(page='about')

    @expose()
    def save(self, pagename, data, submit):
        page = DBSession.query(Page).filter_by(pagename=pagename).one()
        page.data = data
        redirect("/" + pagename)
        
    @expose("wiki20.templates.edit")
    def notfound(self, pagename):
        page = Page(pagename=pagename, data="")
        DBSession.add(page)
        return dict(wikipage=page)
