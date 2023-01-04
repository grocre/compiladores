
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'BAIXO CIMA DIREITA ESQUERDA INICIAR MOVER PEGAR SAIR\n        expressao : comando acao\n                | comando\n                    \n    \n        comando : INICIAR \n                | MOVER\n                | PEGAR\n                | SAIR\n    \n        acao : BAIXO  \n            | CIMA\n            | DIREITA\n            | ESQUERDA\n    '
    
_lr_action_items = {'INICIAR':([0,],[3,]),'MOVER':([0,],[4,]),'PEGAR':([0,],[5,]),'SAIR':([0,],[6,]),'$end':([1,2,3,4,5,6,7,8,9,10,11,],[0,-2,-3,-4,-5,-6,-1,-7,-8,-9,-10,]),'BAIXO':([2,3,4,5,6,],[8,-3,-4,-5,-6,]),'CIMA':([2,3,4,5,6,],[9,-3,-4,-5,-6,]),'DIREITA':([2,3,4,5,6,],[10,-3,-4,-5,-6,]),'ESQUERDA':([2,3,4,5,6,],[11,-3,-4,-5,-6,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'expressao':([0,],[1,]),'comando':([0,],[2,]),'acao':([2,],[7,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> expressao","S'",1,None,None,None),
  ('expressao -> comando acao','expressao',2,'p_expressao','calculator.py',47),
  ('expressao -> comando','expressao',1,'p_expressao','calculator.py',48),
  ('comando -> INICIAR','comando',1,'p_comando','calculator.py',183),
  ('comando -> MOVER','comando',1,'p_comando','calculator.py',184),
  ('comando -> PEGAR','comando',1,'p_comando','calculator.py',185),
  ('comando -> SAIR','comando',1,'p_comando','calculator.py',186),
  ('acao -> BAIXO','acao',1,'p_acao','calculator.py',192),
  ('acao -> CIMA','acao',1,'p_acao','calculator.py',193),
  ('acao -> DIREITA','acao',1,'p_acao','calculator.py',194),
  ('acao -> ESQUERDA','acao',1,'p_acao','calculator.py',195),
]