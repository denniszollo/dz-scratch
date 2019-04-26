#! /usr/bin/env python

import traits.api as traits
import traitsui.api as ui
import progress_editor as pe
class Example(traits.HasTraits):
    basic_value_1 = traits.Int
    basic_value_2 = traits.Int
    basic_value_3 = traits.Int
    mybutton = traits.Button
    mygroup = ui.Group
    mytabbed = ui.Tabbed
    
    def on_apply(self):
      print "on apply"

    def default_traits_view(self):
        self.mygroup = \
            ui.Group(
            ui.Item('basic_value_1', editor=pe.SimpleEditor()),
            ui.Item('mybutton'),),
        self.mytabbed = \
            ui.Tabbed(
            self.mygroup,
            ui.Item('basic_value_2'),
            ui.Item('basic_value_3'),
            ),
        self.view = ui.View(
            self.mytabbed,
            resizable=True,
        )
        self.view.on_apply = self.on_apply
        return self.view
    def _mybutton_fired(self):
       print type(self.mytabbed[0])
       for each in self.mytabbed[0].all_trait_names():
         print "trait : {0} : {1}".format(each, self.view.get(each))
       print self.mytabbed[0].selected

if __name__ == '__main__':
    example = Example()
    example.configure_traits()
