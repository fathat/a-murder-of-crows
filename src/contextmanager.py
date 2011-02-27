import code

class ContextManager(object):
    def __init__(self, contexts):
        self._contexts = {}
        self.current_context = contexts[0]
        
        for context in contexts:
            self._contexts[context.name] = context
            
            context.switch_requested += self._switch_to_context

    def _switch_to_context(self, context_name):
        print "in switch to context", context_name
        self.current_context = self._contexts[context_name]
        self.current_context.on_activate()