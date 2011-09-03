import wx
import wx.html

from traits.api import implements, Str

from .wx_element import WXElement

from ..i_html import IHtml


class WXHtml(WXElement):
    """ A wxPython implementation of IHtml.
    
    The WXHtml widget renders html source using a wx.html.HtmlWindow.

    See Also
    --------
    IHtml
    
    """
    implements(IHtml)

    #===========================================================================
    # IHtml interface
    #===========================================================================
    source = Str

    #===========================================================================
    # Implementation
    #===========================================================================

    #---------------------------------------------------------------------------
    # Initialization
    #---------------------------------------------------------------------------
    def create_widget(self):
        """ Creates the underlying html control.

        This is called by the 'layout' method and is not meant for public
        consumption.

        """
        # GetBestSize on the HtmlWindow returns (0, 0) (wtf?)
        # So for now, we just set the min size to something sensible.
        self.widget = wx.html.HtmlWindow(self.parent_widget(), size=(300, 200))

    def init_attributes(self):
        """ Initializes the attributes of the control.

        This is called by the 'layout' method and is not meant for public
        consumption.

        """
        self.set_page_source(self.source)

    def init_meta_handlers(self):
        """ Initializes the meta handlers for the control.

        This is called by the 'layout' method and is not meant for public
        consumption.

        """
        pass

    #---------------------------------------------------------------------------
    # Notification
    #---------------------------------------------------------------------------
    def _source_changed(self, source):
        """ The change handler for the 'source' attribute. Not meant for
        public consumption.

        """
        self.set_page_source(source)

    #---------------------------------------------------------------------------
    # Widget update
    #---------------------------------------------------------------------------
    def set_page_source(self, source):
        """ Sets the page source for the underlying control. Not meant 
        for public consumption.

        """
        self.widget.SetPage(source)

    #---------------------------------------------------------------------------
    # Layout helpers
    #---------------------------------------------------------------------------
    def default_sizer_flags(self):
        """ Updates the default sizer flags to have a proportion of 2.

        """
        return super(WXHtml, self).default_sizer_flags().Proportion(2)
