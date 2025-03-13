from enum import Enum
from formula import *

class Verdict(Enum):
    TRUE = 0
    UNKNOWN_TRUE = 1
    UNKNOWN_FALSE = 2
    FALSE = 3

# Eval tables for everything except AP
eval_tables = {
   Not: {
       '': {
            Verdict.TRUE: (Verdict.FALSE, ''),
            Verdict.FALSE: (Verdict.TRUE, ''),
            Verdict.UNKNOWN_TRUE: (Verdict.UNKNOWN_FALSE, ''),
            Verdict.UNKNOWN_FALSE: (Verdict.UNKNOWN_TRUE, '')
       }
   },
   And: {
       '': {
           Verdict.TRUE: {
                Verdict.TRUE: (Verdict.TRUE, ''),
                Verdict.UNKNOWN_TRUE: (Verdict.UNKNOWN_TRUE, 'R'),
                Verdict.UNKNOWN_FALSE: (Verdict.UNKNOWN_FALSE, 'R'),
                Verdict.FALSE: (Verdict.FALSE, '')
           },
           Verdict.UNKNOWN_TRUE: {
                Verdict.TRUE: (Verdict.UNKNOWN_TRUE, 'L'),
                Verdict.UNKNOWN_TRUE: (Verdict.UNKNOWN_TRUE, ''),
                Verdict.UNKNOWN_FALSE: (Verdict.UNKNOWN_FALSE, ''),
                Verdict.FALSE: (Verdict.FALSE, '')
           },
              Verdict.UNKNOWN_FALSE: {
                 Verdict.TRUE: (Verdict.UNKNOWN_FALSE, 'L'),
                 Verdict.UNKNOWN_TRUE: (Verdict.UNKNOWN_FALSE, ''),
                 Verdict.UNKNOWN_FALSE: (Verdict.UNKNOWN_FALSE, ''),
                 Verdict.FALSE: (Verdict.FALSE, '')
              },
            Verdict.FALSE: {
                    Verdict.TRUE: (Verdict.FALSE, ''),
                    Verdict.UNKNOWN_TRUE: (Verdict.FALSE, ''),
                    Verdict.UNKNOWN_FALSE: (Verdict.FALSE, ''),
                    Verdict.FALSE: (Verdict.FALSE, '')
            }
       },
       'L': {
           Verdict.TRUE: (Verdict.TRUE, ''),
           Verdict.UNKNOWN_TRUE: (Verdict.UNKNOWN_TRUE, 'L'),
           Verdict.UNKNOWN_FALSE: (Verdict.UNKNOWN_FALSE, 'L'),
            Verdict.FALSE: (Verdict.FALSE, '')
        },
        'R': {
            Verdict.TRUE: (Verdict.TRUE, ''),
            Verdict.UNKNOWN_TRUE: (Verdict.UNKNOWN_TRUE, 'R'),
            Verdict.UNKNOWN_FALSE: (Verdict.UNKNOWN_FALSE, 'R'),
            Verdict.FALSE: (Verdict.FALSE, '')
        }
   },
   Or: {
        '': {
            Verdict.TRUE: {
                Verdict.TRUE: (Verdict.TRUE, ''),
                Verdict.UNKNOWN_TRUE: (Verdict.TRUE, ''),
                Verdict.UNKNOWN_FALSE: (Verdict.TRUE, ''),
                Verdict.FALSE: (Verdict.TRUE, '')
            },
            Verdict.UNKNOWN_TRUE: {
                Verdict.TRUE: (Verdict.TRUE, ''),
                Verdict.UNKNOWN_TRUE: (Verdict.UNKNOWN_TRUE, ''),
                Verdict.UNKNOWN_FALSE: (Verdict.UNKNOWN_TRUE, ''),
                Verdict.FALSE: (Verdict.UNKNOWN_TRUE, 'L')
            },
            Verdict.UNKNOWN_FALSE: {
                Verdict.TRUE: (Verdict.TRUE, ''),
                Verdict.UNKNOWN_TRUE: (Verdict.UNKNOWN_TRUE, ''),
                Verdict.UNKNOWN_FALSE: (Verdict.UNKNOWN_FALSE, ''),
                Verdict.FALSE: (Verdict.UNKNOWN_FALSE, 'L')
            },
            Verdict.FALSE: {
                Verdict.TRUE: (Verdict.TRUE, ''),
                Verdict.UNKNOWN_TRUE: (Verdict.UNKNOWN_TRUE, 'R'),
                Verdict.UNKNOWN_FALSE: (Verdict.UNKNOWN_FALSE, 'R'),
                Verdict.FALSE: (Verdict.FALSE, '')
            }
        },
        'L': {
            Verdict.TRUE: (Verdict.TRUE, ''),
            Verdict.UNKNOWN_TRUE: (Verdict.UNKNOWN_TRUE, 'L'),
            Verdict.UNKNOWN_FALSE: (Verdict.UNKNOWN_FALSE, 'L'),
            Verdict.FALSE: (Verdict.FALSE, '')
        },
        'R': {
            Verdict.TRUE: (Verdict.TRUE, ''),
            Verdict.UNKNOWN_TRUE: (Verdict.UNKNOWN_TRUE, 'R'),
            Verdict.UNKNOWN_FALSE: (Verdict.UNKNOWN_FALSE, 'R'),
            Verdict.FALSE: (Verdict.FALSE, '')
        }
   },
   W: {
        '': {
            Verdict.TRUE: (Verdict.UNKNOWN_TRUE, 'M'),
            Verdict.UNKNOWN_TRUE: (Verdict.UNKNOWN_TRUE, 'M'),
            Verdict.UNKNOWN_FALSE: (Verdict.UNKNOWN_TRUE, 'M'),
            Verdict.FALSE: (Verdict.UNKNOWN_TRUE, 'M')
        },
        'M': {
            Verdict.TRUE: (Verdict.TRUE, ''),
            Verdict.UNKNOWN_TRUE: (Verdict.UNKNOWN_FALSE, ''),
            Verdict.UNKNOWN_FALSE: (Verdict.UNKNOWN_FALSE, ''),
            Verdict.FALSE: (Verdict.FALSE, '')
        }
    },
    X: {
        '': {
            Verdict.TRUE: (Verdict.UNKNOWN_FALSE, 'M'),
            Verdict.UNKNOWN_TRUE: (Verdict.UNKNOWN_FALSE, 'M'),
            Verdict.UNKNOWN_FALSE: (Verdict.UNKNOWN_FALSE, 'M'),
            Verdict.FALSE: (Verdict.UNKNOWN_FALSE, 'M')
        },
        'M': {
            Verdict.TRUE: (Verdict.TRUE, ''),
            Verdict.UNKNOWN_TRUE: (Verdict.UNKNOWN_FALSE, ''),
            Verdict.UNKNOWN_FALSE: (Verdict.UNKNOWN_FALSE, ''),
            Verdict.FALSE: (Verdict.FALSE, '')
        }
    },
    G: {
        '': {
            Verdict.TRUE: (Verdict.UNKNOWN_TRUE, ''),
            Verdict.UNKNOWN_TRUE: (Verdict.UNKNOWN_FALSE, ''),
            Verdict.UNKNOWN_FALSE: (Verdict.UNKNOWN_FALSE, ''),
            Verdict.FALSE: (Verdict.FALSE, '')
        }
    },
    F: {
        '': {
            Verdict.TRUE: (Verdict.TRUE, ''),
            Verdict.UNKNOWN_TRUE: (Verdict.UNKNOWN_FALSE, ''),
            Verdict.UNKNOWN_FALSE: (Verdict.UNKNOWN_FALSE, ''),
            Verdict.FALSE: (Verdict.UNKNOWN_FALSE, '')
        }
    },
    U: {
        '': {
            Verdict.TRUE: {
                Verdict.TRUE: (Verdict.TRUE, ''),
                Verdict.UNKNOWN_TRUE: (Verdict.UNKNOWN_FALSE, ''),
                Verdict.UNKNOWN_FALSE: (Verdict.UNKNOWN_FALSE, ''),
                Verdict.FALSE: (Verdict.UNKNOWN_FALSE, '')
            },
            Verdict.UNKNOWN_TRUE: {
                Verdict.TRUE: (Verdict.TRUE, ''),
                Verdict.UNKNOWN_TRUE: (Verdict.UNKNOWN_FALSE, ''),
                Verdict.UNKNOWN_FALSE: (Verdict.UNKNOWN_FALSE, ''),
                Verdict.FALSE: (Verdict.UNKNOWN_FALSE, 'B')
            },
            Verdict.UNKNOWN_FALSE: {
                Verdict.TRUE: (Verdict.TRUE, ''),
                Verdict.UNKNOWN_TRUE: (Verdict.UNKNOWN_FALSE, ''),
                Verdict.UNKNOWN_FALSE: (Verdict.UNKNOWN_FALSE, ''),
                Verdict.FALSE: (Verdict.UNKNOWN_FALSE, 'B')
            },
            Verdict.FALSE: {
                Verdict.TRUE: (Verdict.TRUE, ''),
                Verdict.UNKNOWN_TRUE: (Verdict.UNKNOWN_FALSE, 'R'),
                Verdict.UNKNOWN_FALSE: (Verdict.UNKNOWN_FALSE, 'R'),
                Verdict.FALSE: (Verdict.FALSE, '')
            }
        },
        'B': {
            Verdict.TRUE: {
                Verdict.TRUE: (Verdict.TRUE, ''),
                Verdict.UNKNOWN_TRUE: (Verdict.UNKNOWN_FALSE, ''),
                Verdict.UNKNOWN_FALSE: (Verdict.UNKNOWN_FALSE, ''),
                Verdict.FALSE: (Verdict.UNKNOWN_FALSE, '')
            },
            Verdict.UNKNOWN_TRUE: {
                Verdict.TRUE: (Verdict.UNKNOWN_FALSE, 'L'),
                Verdict.UNKNOWN_TRUE: (Verdict.UNKNOWN_FALSE, 'B'),
                Verdict.UNKNOWN_FALSE: (Verdict.UNKNOWN_FALSE, 'B'),
                Verdict.FALSE: (Verdict.UNKNOWN_FALSE, 'B')
            },
            Verdict.UNKNOWN_FALSE: {
                Verdict.TRUE: (Verdict.UNKNOWN_FALSE, 'L'),
                Verdict.UNKNOWN_TRUE: (Verdict.UNKNOWN_FALSE, 'B'),
                Verdict.UNKNOWN_FALSE: (Verdict.UNKNOWN_FALSE, 'B'),
                Verdict.FALSE: (Verdict.UNKNOWN_FALSE, 'B')
            },
            Verdict.FALSE: {
                Verdict.TRUE: (Verdict.FALSE, ''),
                Verdict.UNKNOWN_TRUE: (Verdict.FALSE, ''),
                Verdict.UNKNOWN_FALSE: (Verdict.FALSE, ''),
                Verdict.FALSE: (Verdict.FALSE, '')
            }
        },
        'L': {
            Verdict.TRUE: (Verdict.TRUE, ''),
            Verdict.UNKNOWN_TRUE: (Verdict.UNKNOWN_FALSE, 'L'),
            Verdict.UNKNOWN_FALSE: (Verdict.UNKNOWN_FALSE, 'L'),
            Verdict.FALSE: (Verdict.FALSE, '')
        },
        'R': {
            Verdict.TRUE: (Verdict.TRUE, ''),
            Verdict.UNKNOWN_TRUE: (Verdict.UNKNOWN_FALSE, 'R'),
            Verdict.UNKNOWN_FALSE: (Verdict.UNKNOWN_FALSE, 'R'),
            Verdict.FALSE: (Verdict.FALSE, '')
        }
    }
}