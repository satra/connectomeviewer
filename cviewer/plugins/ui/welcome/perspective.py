#------------------------------------------------------------------------------
# Copyright (C) 2009 Richard W. Lincoln
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to
#  deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
#  IN THE SOFTWARE.
#------------------------------------------------------------------------------

""" Defines the WelcomePerspective for the ConnectomeViewer """

#------------------------------------------------------------------------------
#  Imports:
#------------------------------------------------------------------------------

from enthought.traits.api import Tuple
from enthought.pyface.workbench.api import Perspective, PerspectiveItem

#------------------------------------------------------------------------------
#  "WelcomePerspective" class:
#------------------------------------------------------------------------------

class WelcomePerspective(Perspective):
    """ Defines the ConnectomeViewer WelcomePerspective
    """

    # The perspective's unique identifier (unique within a workbench window).
    id = "cviewer.perspective.welcome_perspective"

    # The perspective's name.
    name = "Welcome"

    # Is the perspective enabled?
    enabled = True

    # Should the editor area be shown in this perspective:
    show_editor_area = False

    # The contents of the perspective:
    contents = [PerspectiveItem(id="cviewer.plugins.cff.ui.cff_view.welcome_view",
                    position="left", width=1.0)]
