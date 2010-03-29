# -*- coding: utf-8 -*-

# (note this doesn't actually work correctly in windows...)

print chr(10).join("".join((" ","▲")[c] for c in l)for l in reduce(lambda s,n,w=90:s+[[w>>(s[-1][i-1]*4+s[-1][i]*2+s[-1][(i+1)%len(s[0])])&1 for i in range(len(s[-1]))]],range(31),[[0]*31+[1]+[0]*31]))
