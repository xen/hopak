# -*- coding: utf-8 -*-

import models

def _load(name):
    o = models.MetaModel(name, (models.Model,),
            {'__yaml__': name}
    )

    return o

def load(name):
    ret = models.ModelRegistry.resolve(name, default=False)
    if ret:
        return ret

    return _load(name)
