#------------------------------------------------------------------------------
#  Copyright (c) 2011, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
from traits.api import Property, Either, Tuple, Instance, List, cached_property

from enaml.core.trait_types import CoercingInstance
from enaml.layout.geometry import Box
from enaml.layout.box_model import PaddingBoxModel

from .constraints_widget import (
    ConstraintsWidget, PolicyEnum, get_from_box_model
)


class Container(ConstraintsWidget):
    """ A ConstraintsWidget subclass that provides functionality for 
    laying out constrainable children according to their system of 
    constraints.

    The Container is the canonical component used to arrange child
    widgets using constraints-based layout. Given a heierarchy of
    components, the top-most Container will be charged with the actual
    layout of the decendents. This allows constraints to cross the 
    boundaries of Containers, enabling powerful and flexible layouts.

    There are widgets whose boundaries constraints may not cross. Some
    examples of these would be a ScrollArea or a TabGroup. See the 
    documentation of a given container component as to whether or not
    constraints may cross its boundaries.

    """
    #: A read-only symbolic object that represents the internal left 
    #: padding of the container.
    padding_left = Property(fget=get_from_box_model)

    #: A read-only symbolic object that represents the internal right 
    #: padding of the container.
    padding_right = Property(fget=get_from_box_model)

    #: A read-only symbolic object that represents the internal top 
    #: padding of the container.
    padding_top = Property(fget=get_from_box_model)

    #: A read-only symbolic object that represents the internal bottom 
    #: padding of the container.
    padding_bottom = Property(fget=get_from_box_model)

    #: A read-only symbolic object that represents the internal left 
    #: boundary of the content area of the container.
    contents_left = Property(fget=get_from_box_model)

    #: A read-only symbolic object that represents the internal right 
    #: boundary of the content area of the container.
    contents_right = Property(fget=get_from_box_model)

    #: A read-only symbolic object that represents the internal top 
    #: boundary of the content area of the container.
    contents_top = Property(fget=get_from_box_model)

    #: A read-only symbolic object that represents the internal bottom 
    #: boundary of the content area of the container.
    contents_bottom = Property(fget=get_from_box_model)

    #: A read-only symbolic object that represents the internal width of
    #: the content area of the container.
    contents_width = Property(fget=get_from_box_model)

    #: A read-only symbolic object that represents the internal height of
    #: the content area of the container.
    contents_height = Property(fget=get_from_box_model)

    #: A read-only symbolic object that represents the internal center 
    #: along the vertical direction the content area of the container.
    contents_v_center = Property(fget=get_from_box_model)

    #: A read-only symbolic object that represents the internal center 
    #: along the horizontal direction of the content area of the container.
    contents_h_center = Property(fget=get_from_box_model)

    #: A box object which holds the padding for this component. The 
    #: default padding is Box(10, 10, 10, 10).
    padding = CoercingInstance(Box, (10, 10, 10, 10))

    #: The PolicyEnum for the strength with which to enforce the padding.
    #: This can be a single policy value to apply to everything, or a 
    #: 4-tuple of policies to apply to the individual padding.           
    padding_strength = Either(
        PolicyEnum, Tuple(PolicyEnum, PolicyEnum, PolicyEnum, PolicyEnum),
        default='required'
    )

    #: The list of children that can participate in constraints based
    #: layout. This list is composed of components in the list of 
    #: children that are instances of Constrainable.
    constraints_children = Property(
        List(Instance(ConstraintsWidget)), depends_on='children',
    )

    #: The private storage the box model instance for this component. 
    _box_model = Instance(PaddingBoxModel)
    def __box_model_default(self):
        return PaddingBoxModel(self.constraints_id)

    #--------------------------------------------------------------------------
    # Constraints Generation
    #--------------------------------------------------------------------------
    def _collect_constraints(self):
        """ Collect the list of symbolic constraints for the component.

        This method is overridden from the parent class to add the 
        constraints for the container padding to the list of collected
        constraints.

        """
        cns = super(Container, self)._collect_constraints()
        cns.extend(self._padding_constraints())
        return cns

    def _padding_constraints(self):
        """ Creates the symbolic constraints for the container padding.

        These constraints apply to the internal layout calculations of 
        a container. The default implementation constrains the padding 
        according the 'padding' values and 'padding_strength' policies. 
        It also places a required constraint >= 0 on every padding 
        constraint variable.

        """
        cns = []
        padding = self.padding
        tags = ('top', 'right', 'bottom', 'left')
        strengths = self.padding_strength
        if isinstance(strengths, basestring):
            strengths = (strengths,) * 4
        for tag, strength, padding in zip(tags, strengths, padding):
            tag = 'padding_' + tag
            sym = getattr(self, tag)
            cns.append(sym >= 0)
            if strength != 'ignore':
                cns.append((sym == padding) | strength)
        return cns

    #--------------------------------------------------------------------------
    # Property Getters
    #--------------------------------------------------------------------------
    @cached_property
    def _get_constraints_children(self):
        """ Cached property getter for 'constraints_children'. 

        This getter returns the sublist of children that are instances 
        of ConstraintsWidget.

        """
        flt = lambda child: isinstance(child, ConstraintsWidget)
        return filter(flt, self.children)

