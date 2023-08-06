s='GeXTeXGeXTeXGeXTeXGeXTeXGeXTeXGeXTeXGeXTeXGeXTeXGeXTeX13_scf.pot'
s='C4H4OC4H4OC2C4H4OC4H4OC2'

import regex
import sortedcontainers

def simplyfy_symbols(symbols):
    """
    Remove all numbers from symbols.

    > >> simplyfy_symbols('CO2')
    COO
    > >> simplyfy_symbols('H2O2')
    HHOO
    """
    return regex.sub("([A-Z][a-z]*)([0-9]+)", lambda m: m.group(1)*int(m.group(2)), symbols)


symbol_regexp=regex.compile(r'([A-Z][a-z]*|\{(?>[^{}]|(?R))*(?>\}))([0-9]*)')

def decompose_symbols(symbols):
    """ Return array of symbols (or {} groups) and its counts
    > >> decompose_symbols('C2C2CHe3ZnC')
    (array(['C','He','Zn','C'], dtype=object), array([5,3,1,1]))
    """
    sym=np.empty(len(symbols), dtype=object)
    lns=np.empty(len(symbols), dtype=int)
    i=0
    ln=0
    ls=len(symbols)

    while i < ls:
      m=symbol_regexp.match(symbols[i:])
      s=m.group(1)
      cnt=n.group(2)
      cnt=int(cnt) if cnt else 1
      if ln > 0 and s == sym[ln-1]:
         lns[ln-1]+=1
      else:
         sym[ln]=s
         lns[ln]=cnt
         ln+=1
      i+=len(m.group(0))
    sym.resize(ln)
    lns.resize(ln)
    return sym, lns

def pretty_symbols(symbols):
    """
    Make a symbols string more pretty. Especially suitable for a long 2D semiinfinite bulks.

    > >> pretty_symbols("GeXTeXGeXTeXGeXTeXGeXTeX9")
    '{GeXTeX}4X8'
    > >> pretty_symbols("C4H4OC4H4OC2C4H4OC4H4OC2")
    '{{C4H4O}2C2}2'
    > >> pretty_symbols("CO2")
    'CO2'
    """

    sym, lns = decompose_symbols(symbols)

    for i in range(0,n):
      for j in range(1, min(n-i,i)):
         if symbols[i-j]!=symbols[i+j+1]:
             j-=1
             break

         if j:
             if not results:
                pass
                #results.append((i-j, 
             if results:
                pass




def ekt(symbols):
    prev=[]
    i = 0
    while i < len(symbols):
        for t in prev:
            lt = len(t)
            j = i+lt
            if t == symbols[i:j]:
               k = j+lt
               while t == symbols[j:k]:
                     j=k
                     k+=lt
               repeat = (j - i) // lt + 1

               t = pretty_symbols(t)
               if re.match('^[A-Z][a-z]*$', t):
                   sub = f'{t}{repeat}'
               else:
                   sub = f'{{{t}}}{repeat}'
               symbols = f'{symbols[:i-lt]}{sub}{symbols[j:]}'
               i = i - lt + len(sub)
               break
        else:
               prev = [ p + symbols[i] for p in prev ]
               prev.append(symbols[i])
               i=i+1
    return symbols

#print(pretty_symbols(s))
#print(s)
