#------------------------------------------------------------------------------
#  Copyright (c) 2011, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
from traits.api import Unicode, Bool

from enaml.core.trait_types import EnamlEvent

from .container import Container


class Page(Container):
    """ A component which is used as a page in a Notebook control.

    """
    #: The title to use for the page in the notebook.
    title = Unicode

    #: The icon to user for the page in the notebook.
    # icon = 

    #: The tool tip to use for a page when the user hovers a tab.
    tool_tip = Unicode

    #: Whether or not the tab for the page should be enabled. Note
    #: that this is different from 'enabled' which applies to the 
    #: page itself as opposed to the tab for the page.
    tab_enabled = Bool(True)

    #: An event fired when the user closes the page by clicking on 
    #: the tab's close button. This event is fired by the parent 
    #: Notebook with no payload.
    closed = EnamlEvent

    #--------------------------------------------------------------------------
    # Initialization
    #--------------------------------------------------------------------------
    def creation_attributes(self):
        """ Return the dict of creation attributes for the control.

        """
        super_attrs = super(Page, self).creation_attributes()
        super_attrs['title'] = self.title
        super_attrs['tool_tip'] = self.tool_tip
        super_attrs['tab_enabled'] = self.tab_enabled
        return super_attrs

    def bind(self):
        """ Bind the change handlers for the control.

        """
        super(Page, self).bind()
        self.publish_attributes('title', 'tool_tip', 'tab_enabled')

    #--------------------------------------------------------------------------
    # Public API
    #--------------------------------------------------------------------------
    def open(self):
        """ A convenience method for calling 'open_tab' on the parent
        Notebook, passing this page as an argument.

        """
        parent = self.parent
        if parent is not None:
            parent.open_tab(self)

    def close(self):
        """ A convenience method for calling 'close_tab' on the parent
        Notebook, passing this page as an argument.

        """ 
        parent = self.parent
        if parent is not None:
            parent.close_tab(self)

