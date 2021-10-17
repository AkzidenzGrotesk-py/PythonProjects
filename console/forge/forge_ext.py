import forge_highlighter, forge_find_replace

#
# This is what a Forge extension class should look like
#
# class ForgeExtensionClass:
#     def __init__(self):
#         self.Forge = None
#
#     def initiate(self):
#         pass
#
#     def open_loop(self):
#         pass
#
#     def close_loop(self):
#         pass
#
#     def commands(self, cmds, l_cmds):
#         pass
#
#     def reload(self):
#         pass
#
#     def extend_errors(self):
#         return {}
#

installed_extensions = [forge_highlighter.ForgeHighlighter(), forge_find_replace.ForgeFindReplace()] # insert class initatiated

class ForgeExtensionHandler:
    def __init__(self, forge):
        self.Forge = forge
        self.ie = installed_extensions

        for e in self.ie:
            e.Forge = forge

    def initiate(self):
        for e in self.ie:
            e.initiate()

    def open_loop(self):
        for e in self.ie:
            e.open_loop()

    def close_loop(self):
        for e in self.ie:
            e.close_loop()

    def commands(self, cmds, l_cmds):
        t_f = False
        for e in self.ie:
            o = e.commands(cmds, l_cmds)
            t_f = o if o else False

        return t_f

    def reload(self):
        for e in self.ie:
            e.reload()

    def extend_errors(self):
        ers = {}
        for e in self.ie:
            ers = ers | e.extend_errors()
        return ers
